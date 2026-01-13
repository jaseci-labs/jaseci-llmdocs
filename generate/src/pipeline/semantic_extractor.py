"""
Semantic AST Extractor for Jac Language

Extracts structural signatures from Jac code while discarding implementation bodies.
This enables high compression ratios while preserving the API surface area.

Key principle: Extract WHAT things are (signatures, types) not HOW they work (bodies).
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class DefinitionKind(Enum):
    NODE = "node"
    EDGE = "edge"
    WALKER = "walker"
    OBJECT = "obj"
    ENUM = "enum"
    ABILITY = "can"
    FUNCTION = "def"
    GLOBAL = "glob"
    TEST = "test"


@dataclass
class Attribute:
    name: str
    type_hint: Optional[str] = None
    default: Optional[str] = None

    def to_signature(self) -> str:
        parts = [f"has {self.name}"]
        if self.type_hint:
            parts[0] += f": {self.type_hint}"
        if self.default:
            parts[0] += f" = {self.default}"
        return parts[0] + ";"


@dataclass
class AbilitySignature:
    name: str
    params: Optional[str] = None
    return_type: Optional[str] = None
    trigger: Optional[str] = None  # e.g., "with Person entry"
    is_async: bool = False

    def to_signature(self) -> str:
        prefix = "async can" if self.is_async else "can"
        sig = f"{prefix} {self.name}"
        if self.params:
            sig += f"({self.params})"
        if self.return_type:
            sig += f" -> {self.return_type}"
        if self.trigger:
            sig += f" {self.trigger}"
        return sig + ";"


@dataclass
class FunctionSignature:
    name: str
    params: Optional[str] = None
    return_type: Optional[str] = None
    is_async: bool = False

    def to_signature(self) -> str:
        prefix = "async def" if self.is_async else "def"
        sig = f"{prefix} {self.name}"
        if self.params:
            sig += f"({self.params})"
        elif self.params == "":
            sig += "()"
        if self.return_type:
            sig += f" -> {self.return_type}"
        return sig + ";"


@dataclass
class Definition:
    kind: DefinitionKind
    name: str
    parent: Optional[str] = None  # For inheritance
    attributes: list[Attribute] = field(default_factory=list)
    abilities: list[AbilitySignature] = field(default_factory=list)
    functions: list[FunctionSignature] = field(default_factory=list)
    docstring: Optional[str] = None
    file_source: Optional[str] = None
    line_number: int = 0

    def to_skeleton(self) -> str:
        lines = []

        if self.docstring:
            lines.append(f"# {self.docstring}")

        if self.kind == DefinitionKind.FUNCTION:
            for func in self.functions:
                lines.append(func.to_signature())
            return "\n".join(lines)

        if self.kind == DefinitionKind.GLOBAL:
            for attr in self.attributes:
                lines.append(f"glob {attr.name}")
                if attr.type_hint:
                    lines[-1] = f"glob {attr.name}: {attr.type_hint}"
                if attr.default:
                    lines[-1] += f" = {attr.default}"
                lines[-1] += ";"
            return "\n".join(lines)

        header = f"{self.kind.value} {self.name}"
        if self.parent:
            header += f"({self.parent})"
        header += " {"

        lines.append(header)

        for attr in self.attributes:
            lines.append(f"    {attr.to_signature()}")

        for ability in self.abilities:
            lines.append(f"    {ability.to_signature()}")

        for func in self.functions:
            lines.append(f"    {func.to_signature()}")

        lines.append("}")

        return "\n".join(lines)


class JacTokenizer:
    """Simple tokenizer for Jac code that handles strings and comments."""

    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.length = len(code)

    def skip_whitespace(self):
        while self.pos < self.length and self.code[self.pos] in ' \t\n\r':
            self.pos += 1

    def skip_line_comment(self):
        if self.pos < self.length - 1 and self.code[self.pos:self.pos+2] == '#*':
            end = self.code.find('*#', self.pos + 2)
            if end != -1:
                self.pos = end + 2
            else:
                self.pos = self.length
        elif self.pos < self.length and self.code[self.pos] == '#':
            while self.pos < self.length and self.code[self.pos] != '\n':
                self.pos += 1

    def read_string(self) -> str:
        quote = self.code[self.pos]
        result = quote
        self.pos += 1

        while self.pos < self.length:
            ch = self.code[self.pos]
            result += ch
            self.pos += 1

            if ch == '\\' and self.pos < self.length:
                result += self.code[self.pos]
                self.pos += 1
            elif ch == quote:
                break

        return result

    def find_matching_brace(self, start_pos: int) -> int:
        """Find the position of the closing brace that matches the opening brace at start_pos."""
        self.pos = start_pos
        if self.pos >= self.length or self.code[self.pos] != '{':
            return -1

        depth = 0
        while self.pos < self.length:
            ch = self.code[self.pos]

            if ch == '#':
                self.skip_line_comment()
                continue
            elif ch in '"\'':
                self.read_string()
                continue
            elif ch == '{':
                depth += 1
                self.pos += 1
            elif ch == '}':
                depth -= 1
                self.pos += 1
                if depth == 0:
                    return self.pos - 1
            else:
                self.pos += 1

        return -1


class SemanticExtractor:
    """
    Extracts semantic structure from Jac source code.

    Focuses on extracting signatures (the API surface) while discarding
    implementation bodies. This enables high compression while preserving
    the information needed for code generation.
    """

    ARCHETYPE_KEYWORDS = {'node', 'edge', 'walker', 'obj', 'object', 'enum', 'test'}

    ARCHETYPE_PATTERN = re.compile(
        r'((?:#[^\n]*\n)*)?'  # Optional docstring comments
        r'(node|edge|walker|obj(?:ect)?|enum|test)\s+'  # Keyword
        r'(\w+)'  # Name
        r'(?:\s*<[^>]*>)?'  # Optional generics
        r'(?:\s*\(\s*(\w+)\s*\))?'  # Optional parent
        r'\s*\{'  # Opening brace
    )

    HAS_PATTERN = re.compile(
        r'has\s+(\w+)\s*'  # has name
        r'(?::\s*([^=;]+?))?'  # Optional type
        r'(?:\s*=\s*([^;]+?))?'  # Optional default
        r'\s*;'
    )

    CAN_PATTERN = re.compile(
        r'(async\s+)?can\s+(\w+)'  # can name
        r'(?:\s*\(([^)]*)\))?'  # Optional params
        r'(?:\s*->\s*([^\s{]+))?'  # Optional return type
        r'(?:\s+(with\s+[^{]+))?'  # Optional trigger
        r'\s*(?:\{|;)'  # Body or declaration
    )

    DEF_PATTERN = re.compile(
        r'(async\s+)?def\s+(\w+)'  # def name
        r'(?:\s*\(([^)]*)\))?'  # Optional params
        r'(?:\s*->\s*([^\s{]+))?'  # Optional return type
        r'\s*(?:\{|;)'  # Body or declaration
    )

    GLOB_PATTERN = re.compile(
        r'glob\s+(\w+)\s*'  # glob name
        r'(?::\s*([^=;]+?))?'  # Optional type
        r'(?:\s*=\s*([^;]+?))?'  # Optional value
        r'\s*;'
    )

    def __init__(self, config: dict = None):
        self.config = config or {}

    def extract_from_code(self, code: str, file_path: str = None) -> list[Definition]:
        """Extract all definitions from Jac source code."""
        definitions = []
        tokenizer = JacTokenizer(code)

        for match in self.ARCHETYPE_PATTERN.finditer(code):
            docstring_block = match.group(1)
            keyword = match.group(2)
            name = match.group(3)
            parent = match.group(4)

            brace_start = match.end() - 1
            brace_end = tokenizer.find_matching_brace(brace_start)

            if brace_end == -1:
                continue

            body = code[brace_start + 1:brace_end]
            line_number = code[:match.start()].count('\n') + 1

            kind = self._keyword_to_kind(keyword)
            docstring = self._parse_docstring(docstring_block)

            definition = Definition(
                kind=kind,
                name=name,
                parent=parent,
                docstring=docstring,
                file_source=file_path,
                line_number=line_number
            )

            definition.attributes = self._extract_attributes(body)
            definition.abilities = self._extract_abilities(body)
            definition.functions = self._extract_functions(body)

            definitions.append(definition)

        top_level_functions = self._extract_top_level_functions(code, definitions)
        definitions.extend(top_level_functions)

        globals = self._extract_globals(code)
        definitions.extend(globals)

        return definitions

    def _keyword_to_kind(self, keyword: str) -> DefinitionKind:
        mapping = {
            'node': DefinitionKind.NODE,
            'edge': DefinitionKind.EDGE,
            'walker': DefinitionKind.WALKER,
            'obj': DefinitionKind.OBJECT,
            'object': DefinitionKind.OBJECT,
            'enum': DefinitionKind.ENUM,
            'test': DefinitionKind.TEST,
        }
        return mapping.get(keyword, DefinitionKind.OBJECT)

    def _parse_docstring(self, comment_block: str) -> Optional[str]:
        if not comment_block:
            return None

        lines = []
        for line in comment_block.strip().split('\n'):
            line = line.strip()
            if line.startswith('#'):
                line = line[1:].strip()
                if line and not line.startswith('#'):
                    lines.append(line)

        return ' '.join(lines) if lines else None

    def _extract_attributes(self, body: str) -> list[Attribute]:
        """Extract has declarations from body."""
        attributes = []
        for match in self.HAS_PATTERN.finditer(body):
            attr = Attribute(
                name=match.group(1),
                type_hint=match.group(2).strip() if match.group(2) else None,
                default=match.group(3).strip() if match.group(3) else None
            )
            attributes.append(attr)
        return attributes

    def _extract_abilities(self, body: str) -> list[AbilitySignature]:
        """Extract can ability signatures from body."""
        abilities = []
        for match in self.CAN_PATTERN.finditer(body):
            ability = AbilitySignature(
                name=match.group(2),
                params=match.group(3).strip() if match.group(3) else None,
                return_type=match.group(4).strip() if match.group(4) else None,
                trigger=match.group(5).strip() if match.group(5) else None,
                is_async=bool(match.group(1))
            )
            abilities.append(ability)
        return abilities

    def _extract_functions(self, body: str) -> list[FunctionSignature]:
        """Extract def function signatures from body."""
        functions = []
        for match in self.DEF_PATTERN.finditer(body):
            func = FunctionSignature(
                name=match.group(2),
                params=match.group(3).strip() if match.group(3) else None,
                return_type=match.group(4).strip() if match.group(4) else None,
                is_async=bool(match.group(1))
            )
            functions.append(func)
        return functions

    def _extract_top_level_functions(self, code: str, existing_defs: list[Definition]) -> list[Definition]:
        """Extract top-level function definitions not inside archetypes."""
        definitions = []
        covered_ranges = []

        for match in self.ARCHETYPE_PATTERN.finditer(code):
            tokenizer = JacTokenizer(code)
            brace_start = match.end() - 1
            brace_end = tokenizer.find_matching_brace(brace_start)
            if brace_end != -1:
                covered_ranges.append((match.start(), brace_end + 1))

        def is_covered(pos: int) -> bool:
            for start, end in covered_ranges:
                if start <= pos < end:
                    return True
            return False

        for match in self.DEF_PATTERN.finditer(code):
            if is_covered(match.start()):
                continue

            func = FunctionSignature(
                name=match.group(2),
                params=match.group(3).strip() if match.group(3) else None,
                return_type=match.group(4).strip() if match.group(4) else None,
                is_async=bool(match.group(1))
            )

            definition = Definition(
                kind=DefinitionKind.FUNCTION,
                name=func.name,
                line_number=code[:match.start()].count('\n') + 1
            )
            definition.functions = [func]
            definitions.append(definition)

        return definitions

    def _extract_globals(self, code: str) -> list[Definition]:
        """Extract global variable declarations."""
        definitions = []
        for match in self.GLOB_PATTERN.finditer(code):
            definition = Definition(
                kind=DefinitionKind.GLOBAL,
                name=match.group(1),
                line_number=code[:match.start()].count('\n') + 1
            )
            attr = Attribute(
                name=match.group(1),
                type_hint=match.group(2).strip() if match.group(2) else None,
                default=match.group(3).strip() if match.group(3) else None
            )
            definition.attributes = [attr]
            definitions.append(definition)
        return definitions

    def analyze_file(self, file_path: Path) -> dict:
        """Analyze a single .jac file and return structured results."""
        try:
            code = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {"error": str(e), "file": str(file_path)}

        definitions = self.extract_from_code(code, file_path.name)

        stats = {
            'nodes': 0,
            'edges': 0,
            'walkers': 0,
            'objects': 0,
            'abilities': 0,
            'functions': 0,
            'globals': 0,
        }

        for defn in definitions:
            if defn.kind == DefinitionKind.NODE:
                stats['nodes'] += 1
            elif defn.kind == DefinitionKind.EDGE:
                stats['edges'] += 1
            elif defn.kind == DefinitionKind.WALKER:
                stats['walkers'] += 1
            elif defn.kind == DefinitionKind.OBJECT:
                stats['objects'] += 1
            elif defn.kind == DefinitionKind.FUNCTION:
                stats['functions'] += 1
            elif defn.kind == DefinitionKind.GLOBAL:
                stats['globals'] += 1

            stats['abilities'] += len(defn.abilities)

        return {
            "file": file_path.name,
            "definitions": definitions,
            "stats": stats
        }

    def process_directory(self, dir_path: Path) -> dict:
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
                "globals": 0,
            }
        }

        jac_files = list(dir_path.rglob("*.jac"))
        results["totals"]["files"] = len(jac_files)

        for jac_file in jac_files:
            analysis = self.analyze_file(jac_file)
            if "error" not in analysis:
                results["files"].append(analysis)
                results["all_definitions"].extend(analysis["definitions"])

                for key, count in analysis["stats"].items():
                    results["totals"][key] = results["totals"].get(key, 0) + count

        return results

    def _deduplicate_definitions(self, definitions: list[Definition]) -> list[Definition]:
        """Deduplicate definitions by (kind, name), keeping the most complete one."""
        seen = {}
        for defn in definitions:
            key = (defn.kind.value, defn.name)
            if key not in seen:
                seen[key] = defn
            else:
                existing = seen[key]
                existing_score = len(existing.attributes) + len(existing.abilities) + len(existing.functions)
                new_score = len(defn.attributes) + len(defn.abilities) + len(defn.functions)
                if new_score > existing_score:
                    seen[key] = defn
        return list(seen.values())

    def generate_skeleton(self, results: dict) -> str:
        """Generate a skeleton documentation from extracted definitions."""
        sections = []

        deduped = self._deduplicate_definitions(results["all_definitions"])

        sections.append("# Jac API Reference (Skeleton)")
        sections.append(f"# Extracted from {results['totals']['files']} source files")
        sections.append(f"# {len(deduped)} unique definitions (from {len(results['all_definitions'])} total)")
        sections.append("")

        by_kind = {}
        for defn in deduped:
            kind_name = defn.kind.value
            if kind_name not in by_kind:
                by_kind[kind_name] = []
            by_kind[kind_name].append(defn)

        kind_order = ['node', 'edge', 'walker', 'obj', 'def', 'glob', 'enum', 'test']

        for kind in kind_order:
            if kind in by_kind and by_kind[kind]:
                kind_title = {
                    'node': 'Nodes',
                    'edge': 'Edges',
                    'walker': 'Walkers',
                    'obj': 'Objects',
                    'def': 'Functions',
                    'glob': 'Globals',
                    'enum': 'Enums',
                    'test': 'Tests',
                }.get(kind, kind.title())

                sections.append(f"## {kind_title}")
                sections.append("")

                for defn in by_kind[kind]:
                    sections.append(defn.to_skeleton())
                    sections.append("")

        return '\n'.join(sections)

    def extract_from_markdown(self, markdown: str) -> list[Definition]:
        """Extract Jac definitions from code blocks in markdown."""
        all_definitions = []

        code_block_pattern = re.compile(r'```jac\s*\n(.*?)```', re.DOTALL)

        for match in code_block_pattern.finditer(markdown):
            code = match.group(1)
            definitions = self.extract_from_code(code)
            all_definitions.extend(definitions)

        return all_definitions
