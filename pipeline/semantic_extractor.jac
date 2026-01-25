"""Semantic AST Extractor for Jac Language.

Extracts structural signatures from Jac code while discarding implementation bodies.
This enables high compression ratios while preserving the API surface area.

Key principle: Extract WHAT things are (signatures, types) not HOW they work (bodies).
"""

import:py re;
import:py from pathlib import Path;

enum DefinitionKind {
    NODE = "node",
    EDGE = "edge",
    WALKER = "walker",
    OBJECT = "obj",
    ENUM = "enum",
    ABILITY = "can",
    FUNCTION = "def",
    GLOBAL = "glob",
    TEST = "test"
}

obj Attribute {
    has name: str;
    has type_hint: str | None = None;
    has default: str | None = None;

    can to_signature() -> str {
        parts = [f"has {self.name}"];
        if self.type_hint {
            parts[0] += f": {self.type_hint}";
        }
        if self.default {
            parts[0] += f" = {self.default}";
        }
        return parts[0] + ";";
    }
}

obj AbilitySignature {
    has name: str;
    has params: str | None = None;
    has return_type: str | None = None;
    has trigger: str | None = None;
    has is_async: bool = False;

    can to_signature() -> str {
        prefix = "async can" if self.is_async else "can";
        sig = f"{prefix} {self.name}";
        if self.params {
            sig += f"({self.params})";
        }
        if self.return_type {
            sig += f" -> {self.return_type}";
        }
        if self.trigger {
            sig += f" {self.trigger}";
        }
        return sig + ";";
    }
}

obj FunctionSignature {
    has name: str;
    has params: str | None = None;
    has return_type: str | None = None;
    has is_async: bool = False;

    can to_signature() -> str {
        prefix = "async def" if self.is_async else "def";
        sig = f"{prefix} {self.name}";
        if self.params is not None {
            sig += f"({self.params})";
        } elif self.params == "" {
            sig += "()";
        }
        if self.return_type {
            sig += f" -> {self.return_type}";
        }
        return sig + ";";
    }
}

obj Definition {
    has kind: DefinitionKind;
    has name: str;
    has parent: str | None = None;
    has attributes: list[Attribute] = [];
    has abilities: list[AbilitySignature] = [];
    has functions: list[FunctionSignature] = [];
    has docstring: str | None = None;
    has file_source: str | None = None;
    has line_number: int = 0;

    can to_skeleton() -> str {
        lines: list[str] = [];

        if self.docstring {
            lines.append(f"# {self.docstring}");
        }

        if self.kind == DefinitionKind.FUNCTION {
            for func in self.functions {
                lines.append(func.to_signature());
            }
            return "\n".join(lines);
        }

        if self.kind == DefinitionKind.GLOBAL {
            for attr in self.attributes {
                line = f"glob {attr.name}";
                if attr.type_hint {
                    line = f"glob {attr.name}: {attr.type_hint}";
                }
                if attr.default {
                    line += f" = {attr.default}";
                }
                line += ";";
                lines.append(line);
            }
            return "\n".join(lines);
        }

        header = f"{self.kind.value} {self.name}";
        if self.parent {
            header += f"({self.parent})";
        }
        header += " {";

        lines.append(header);

        for attr in self.attributes {
            lines.append(f"    {attr.to_signature()}");
        }

        for ability in self.abilities {
            lines.append(f"    {ability.to_signature()}");
        }

        for func in self.functions {
            lines.append(f"    {func.to_signature()}");
        }

        lines.append("}");

        return "\n".join(lines);
    }
}

obj JacTokenizer {
    """Simple tokenizer for Jac code that handles strings and comments."""

    has code: str;
    has pos: int = 0;
    has length: int = 0;

    can :postinit: {
        self.length = len(self.code);
    }

    can skip_whitespace() {
        while self.pos < self.length and self.code[self.pos] in " \t\n\r" {
            self.pos += 1;
        }
    }

    can skip_line_comment() {
        if self.pos < self.length - 1 and self.code[self.pos:self.pos+2] == "#*" {
            end = self.code.find("*#", self.pos + 2);
            if end != -1 {
                self.pos = end + 2;
            } else {
                self.pos = self.length;
            }
        } elif self.pos < self.length and self.code[self.pos] == "#" {
            while self.pos < self.length and self.code[self.pos] != "\n" {
                self.pos += 1;
            }
        }
    }

    can read_string() -> str {
        quote = self.code[self.pos];
        result = quote;
        self.pos += 1;

        while self.pos < self.length {
            ch = self.code[self.pos];
            result += ch;
            self.pos += 1;

            if ch == "\\" and self.pos < self.length {
                result += self.code[self.pos];
                self.pos += 1;
            } elif ch == quote {
                break;
            }
        }

        return result;
    }

    can find_matching_brace(start_pos: int) -> int {
        """Find the position of the closing brace that matches the opening brace at start_pos."""
        self.pos = start_pos;
        if self.pos >= self.length or self.code[self.pos] != "{" {
            return -1;
        }

        depth = 0;
        while self.pos < self.length {
            ch = self.code[self.pos];

            if ch == "#" {
                self.skip_line_comment();
                continue;
            } elif ch in "\"'" {
                self.read_string();
                continue;
            } elif ch == "{" {
                depth += 1;
                self.pos += 1;
            } elif ch == "}" {
                depth -= 1;
                self.pos += 1;
                if depth == 0 {
                    return self.pos - 1;
                }
            } else {
                self.pos += 1;
            }
        }

        return -1;
    }
}

obj SemanticExtractor {
    """Extracts semantic structure from Jac source code.

    Focuses on extracting signatures (the API surface) while discarding
    implementation bodies. This enables high compression while preserving
    the information needed for code generation.
    """

    has config: dict = {};

    has ARCHETYPE_PATTERN: object = re.compile(
        r"((?:#[^\n]*\n)*)?",
        r"(node|edge|walker|obj(?:ect)?|enum|test)\s+",
        r"(\w+)",
        r"(?:\s*<[^>]*>)?",
        r"(?:\s*\(\s*(\w+)\s*\))?",
        r"\s*\{",
        flags=re.VERBOSE
    );

    has HAS_PATTERN: object = re.compile(
        r"has\s+(\w+)\s*(?::\s*([^=;]+?))?(?:\s*=\s*([^;]+?))?\s*;"
    );

    has CAN_PATTERN: object = re.compile(
        r"(async\s+)?can\s+(\w+)(?:\s*\(([^)]*)\))?(?:\s*->\s*([^\s{]+))?(?:\s+(with\s+[^{]+))?\s*(?:\{|;)"
    );

    has DEF_PATTERN: object = re.compile(
        r"(async\s+)?def\s+(\w+)(?:\s*\(([^)]*)\))?(?:\s*->\s*([^\s{]+))?\s*(?:\{|;)"
    );

    has GLOB_PATTERN: object = re.compile(
        r"glob\s+(\w+)\s*(?::\s*([^=;]+?))?(?:\s*=\s*([^;]+?))?\s*;"
    );

    can :init: {
        self.ARCHETYPE_PATTERN = re.compile(
            r"((?:#[^\n]*\n)*)?"
            r"(node|edge|walker|obj(?:ect)?|enum|test)\s+"
            r"(\w+)"
            r"(?:\s*<[^>]*>)?"
            r"(?:\s*\(\s*(\w+)\s*\))?"
            r"\s*\{"
        );
    }

    can extract_from_code(code: str, file_path: str | None = None) -> list[Definition] {
        """Extract all definitions from Jac source code."""
        definitions: list[Definition] = [];
        tokenizer = JacTokenizer(code=code);

        for match in self.ARCHETYPE_PATTERN.finditer(code) {
            docstring_block = match.group(1);
            keyword = match.group(2);
            name = match.group(3);
            parent = match.group(4);

            brace_start = match.end() - 1;
            brace_end = tokenizer.find_matching_brace(brace_start);

            if brace_end == -1 {
                continue;
            }

            body = code[brace_start + 1:brace_end];
            line_number = code[:match.start()].count("\n") + 1;

            kind = self._keyword_to_kind(keyword);
            docstring = self._parse_docstring(docstring_block);

            definition = Definition(
                kind=kind,
                name=name,
                parent=parent,
                docstring=docstring,
                file_source=file_path,
                line_number=line_number
            );

            definition.attributes = self._extract_attributes(body);
            definition.abilities = self._extract_abilities(body);
            definition.functions = self._extract_functions(body);

            definitions.append(definition);
        }

        top_level_functions = self._extract_top_level_functions(code, definitions);
        definitions.extend(top_level_functions);

        globals = self._extract_globals(code);
        definitions.extend(globals);

        return definitions;
    }

    can _keyword_to_kind(keyword: str) -> DefinitionKind {
        mapping = {
            "node": DefinitionKind.NODE,
            "edge": DefinitionKind.EDGE,
            "walker": DefinitionKind.WALKER,
            "obj": DefinitionKind.OBJECT,
            "object": DefinitionKind.OBJECT,
            "enum": DefinitionKind.ENUM,
            "test": DefinitionKind.TEST
        };
        return mapping.get(keyword, DefinitionKind.OBJECT);
    }

    can _parse_docstring(comment_block: str | None) -> str | None {
        if not comment_block {
            return None;
        }

        lines: list[str] = [];
        for line in comment_block.strip().split("\n") {
            line = line.strip();
            if line.startswith("#") {
                line = line[1:].strip();
                if line and not line.startswith("#") {
                    lines.append(line);
                }
            }
        }

        return " ".join(lines) if lines else None;
    }

    can _extract_attributes(body: str) -> list[Attribute] {
        """Extract has declarations from body."""
        attributes: list[Attribute] = [];
        for match in self.HAS_PATTERN.finditer(body) {
            attr = Attribute(
                name=match.group(1),
                type_hint=match.group(2).strip() if match.group(2) else None,
                default=match.group(3).strip() if match.group(3) else None
            );
            attributes.append(attr);
        }
        return attributes;
    }

    can _extract_abilities(body: str) -> list[AbilitySignature] {
        """Extract can ability signatures from body."""
        abilities: list[AbilitySignature] = [];
        for match in self.CAN_PATTERN.finditer(body) {
            ability = AbilitySignature(
                name=match.group(2),
                params=match.group(3).strip() if match.group(3) else None,
                return_type=match.group(4).strip() if match.group(4) else None,
                trigger=match.group(5).strip() if match.group(5) else None,
                is_async=bool(match.group(1))
            );
            abilities.append(ability);
        }
        return abilities;
    }

    can _extract_functions(body: str) -> list[FunctionSignature] {
        """Extract def function signatures from body."""
        functions: list[FunctionSignature] = [];
        for match in self.DEF_PATTERN.finditer(body) {
            func = FunctionSignature(
                name=match.group(2),
                params=match.group(3).strip() if match.group(3) else None,
                return_type=match.group(4).strip() if match.group(4) else None,
                is_async=bool(match.group(1))
            );
            functions.append(func);
        }
        return functions;
    }

    can _extract_top_level_functions(code: str, existing_defs: list[Definition]) -> list[Definition] {
        """Extract top-level function definitions not inside archetypes."""
        definitions: list[Definition] = [];
        covered_ranges: list[tuple] = [];

        for match in self.ARCHETYPE_PATTERN.finditer(code) {
            tokenizer = JacTokenizer(code=code);
            brace_start = match.end() - 1;
            brace_end = tokenizer.find_matching_brace(brace_start);
            if brace_end != -1 {
                covered_ranges.append((match.start(), brace_end + 1));
            }
        }

        can is_covered(pos: int) -> bool {
            for (start, end) in covered_ranges {
                if start <= pos < end {
                    return True;
                }
            }
            return False;
        }

        for match in self.DEF_PATTERN.finditer(code) {
            if is_covered(match.start()) {
                continue;
            }

            func = FunctionSignature(
                name=match.group(2),
                params=match.group(3).strip() if match.group(3) else None,
                return_type=match.group(4).strip() if match.group(4) else None,
                is_async=bool(match.group(1))
            );

            definition = Definition(
                kind=DefinitionKind.FUNCTION,
                name=func.name,
                line_number=code[:match.start()].count("\n") + 1
            );
            definition.functions = [func];
            definitions.append(definition);
        }

        return definitions;
    }

    can _extract_globals(code: str) -> list[Definition] {
        """Extract global variable declarations."""
        definitions: list[Definition] = [];
        for match in self.GLOB_PATTERN.finditer(code) {
            definition = Definition(
                kind=DefinitionKind.GLOBAL,
                name=match.group(1),
                line_number=code[:match.start()].count("\n") + 1
            );
            attr = Attribute(
                name=match.group(1),
                type_hint=match.group(2).strip() if match.group(2) else None,
                default=match.group(3).strip() if match.group(3) else None
            );
            definition.attributes = [attr];
            definitions.append(definition);
        }
        return definitions;
    }

    can _deduplicate_definitions(definitions: list[Definition]) -> list[Definition] {
        """Deduplicate definitions by (kind, name), keeping the most complete one."""
        seen: dict = {};
        for defn in definitions {
            key = (defn.kind.value, defn.name);
            if key not in seen {
                seen[key] = defn;
            } else {
                existing = seen[key];
                existing_score = len(existing.attributes) + len(existing.abilities) + len(existing.functions);
                new_score = len(defn.attributes) + len(defn.abilities) + len(defn.functions);
                if new_score > existing_score {
                    seen[key] = defn;
                }
            }
        }
        return list(seen.values());
    }

    can generate_skeleton_from_definitions(definitions: list[Definition]) -> str {
        """Generate a skeleton documentation from extracted definitions."""
        sections: list[str] = [];

        deduped = self._deduplicate_definitions(definitions);

        sections.append("# Jac API Reference (Skeleton)");
        sections.append(f"# {len(deduped)} unique definitions");
        sections.append("");

        by_kind: dict = {};
        for defn in deduped {
            kind_name = defn.kind.value;
            if kind_name not in by_kind {
                by_kind[kind_name] = [];
            }
            by_kind[kind_name].append(defn);
        }

        kind_order = ["node", "edge", "walker", "obj", "def", "glob", "enum", "test"];

        for kind in kind_order {
            if kind in by_kind and by_kind[kind] {
                kind_title = {
                    "node": "Nodes",
                    "edge": "Edges",
                    "walker": "Walkers",
                    "obj": "Objects",
                    "def": "Functions",
                    "glob": "Globals",
                    "enum": "Enums",
                    "test": "Tests"
                }.get(kind, kind.title());

                sections.append(f"## {kind_title}");
                sections.append("");

                for defn in by_kind[kind] {
                    sections.append(defn.to_skeleton());
                    sections.append("");
                }
            }
        }

        return "\n".join(sections);
    }

    can extract_from_markdown(markdown: str) -> list[Definition] {
        """Extract Jac definitions from code blocks in markdown."""
        all_definitions: list[Definition] = [];

        code_block_pattern = re.compile(r"```jac\s*\n(.*?)```", re.DOTALL);

        for match in code_block_pattern.finditer(markdown) {
            code = match.group(1);
            definitions = self.extract_from_code(code);
            all_definitions.extend(definitions);
        }

        return all_definitions;
    }

    can analyze_file(file_path: object) -> dict {
        """Analyze a single .jac file and return structured results."""
        try {
            code = file_path.read_text(encoding="utf-8");
        } except Exception as e {
            return {"error": str(e), "file": str(file_path)};
        }

        definitions = self.extract_from_code(code, file_path.name);

        stats = {
            "nodes": 0,
            "edges": 0,
            "walkers": 0,
            "objects": 0,
            "abilities": 0,
            "functions": 0,
            "globals": 0
        };

        for defn in definitions {
            if defn.kind == DefinitionKind.NODE {
                stats["nodes"] += 1;
            } elif defn.kind == DefinitionKind.EDGE {
                stats["edges"] += 1;
            } elif defn.kind == DefinitionKind.WALKER {
                stats["walkers"] += 1;
            } elif defn.kind == DefinitionKind.OBJECT {
                stats["objects"] += 1;
            } elif defn.kind == DefinitionKind.FUNCTION {
                stats["functions"] += 1;
            } elif defn.kind == DefinitionKind.GLOBAL {
                stats["globals"] += 1;
            }
            stats["abilities"] += len(defn.abilities);
        }

        return {
            "file": file_path.name,
            "definitions": definitions,
            "stats": stats
        };
    }

    can process_directory(dir_path: object) -> dict {
        """Process all .jac files in a directory."""
        results = {
            "files": [],
            "all_definitions": [],
            "totals": {
                "files": 0,
                "nodes": 0,
                "edges": 0,
                "walkers": 0,
                "objects": 0,
                "abilities": 0,
                "functions": 0,
                "globals": 0
            }
        };

        jac_files = list(dir_path.rglob("*.jac"));
        results["totals"]["files"] = len(jac_files);

        for jac_file in jac_files {
            analysis = self.analyze_file(jac_file);
            if "error" not in analysis {
                results["files"].append(analysis);
                results["all_definitions"].extend(analysis["definitions"]);

                for (key, count) in analysis["stats"].items() {
                    results["totals"][key] = results["totals"].get(key, 0) + count;
                }
            }
        }

        return results;
    }

    can generate_skeleton(results: dict) -> str {
        """Generate a skeleton documentation from extraction results."""
        return self.generate_skeleton_from_definitions(results["all_definitions"]);
    }
}
