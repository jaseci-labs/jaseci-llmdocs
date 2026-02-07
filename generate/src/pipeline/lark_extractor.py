"""
Lark-based AST Extractor for Jac Language

Uses the official Jac grammar to properly parse code and extract
structural signatures while discarding implementation bodies.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

try:
    from lark import Lark, Token, Tree
    from lark.exceptions import LarkError
    LARK_AVAILABLE = True
except ImportError:
    LARK_AVAILABLE = False


class DefinitionKind(Enum):
    NODE = "node"
    EDGE = "edge"
    WALKER = "walker"
    OBJECT = "obj"
    CLASS = "class"
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
    is_static: bool = False

    def to_signature(self) -> str:
        prefix = "static " if self.is_static else ""
        parts = [f"{prefix}has {self.name}"]
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
    trigger: Optional[str] = None
    is_async: bool = False
    is_static: bool = False
    is_override: bool = False

    def to_signature(self) -> str:
        parts = []
        if self.is_override:
            parts.append("override")
        if self.is_static:
            parts.append("static")
        if self.is_async:
            parts.append("async")
        parts.append("can")
        if self.name:
            parts.append(self.name)

        sig = " ".join(parts)
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
    is_static: bool = False
    is_override: bool = False

    def to_signature(self) -> str:
        parts = []
        if self.is_override:
            parts.append("override")
        if self.is_static:
            parts.append("static")
        if self.is_async:
            parts.append("async")
        parts.append("def")
        parts.append(self.name)

        sig = " ".join(parts)
        if self.params is not None:
            sig += f"({self.params})"
        if self.return_type:
            sig += f" -> {self.return_type}"
        return sig + ";"


@dataclass
class Definition:
    kind: DefinitionKind
    name: str
    parent: Optional[str] = None
    attributes: list[Attribute] = field(default_factory=list)
    abilities: list[AbilitySignature] = field(default_factory=list)
    functions: list[FunctionSignature] = field(default_factory=list)
    docstring: Optional[str] = None
    file_source: Optional[str] = None
    is_async: bool = False

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
                line = f"glob {attr.name}"
                if attr.type_hint:
                    line = f"glob {attr.name}: {attr.type_hint}"
                if attr.default:
                    line += f" = {attr.default}"
                lines.append(line + ";")
            return "\n".join(lines)

        prefix = "async " if self.is_async else ""
        header = f"{prefix}{self.kind.value} {self.name}"
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

    def merge(self, other: "Definition") -> None:
        """Merge another definition into this one, keeping the union of contents."""
        if self.kind != other.kind or self.name != other.name:
            return

        # Merge docstrings (keep longest or concatenate if different)
        if other.docstring:
            if not self.docstring:
                self.docstring = other.docstring
            elif len(other.docstring) > len(self.docstring):
                self.docstring = other.docstring

        # Merge parent (prefer existing if set, else other)
        if not self.parent and other.parent:
            self.parent = other.parent

        # Merge attributes (deduplicate by name)
        existing_attrs = {a.name: a for a in self.attributes}
        for attr in other.attributes:
            if attr.name not in existing_attrs:
                self.attributes.append(attr)
            else:
                # Update existing if new one has more info (e.g., type hint)
                existing = existing_attrs[attr.name]
                if not existing.type_hint and attr.type_hint:
                    existing.type_hint = attr.type_hint
                if not existing.default and attr.default:
                    existing.default = attr.default

        # Merge abilities (deduplicate by name/signature)
        existing_abilities = {a.name: a for a in self.abilities}
        for ab in other.abilities:
            if ab.name not in existing_abilities:
                self.abilities.append(ab)

        # Merge functions (deduplicate by name)
        existing_funcs = {f.name: f for f in self.functions}
        for func in other.functions:
            if func.name not in existing_funcs:
                self.functions.append(func)


class JacASTExtractor:
    """Walk Jac AST to extract structural signatures."""

    def __init__(self):
        self.definitions = []

    def _get_text(self, item) -> str:
        if isinstance(item, Token):
            return str(item)
        elif isinstance(item, Tree):
            return " ".join(self._get_text(c) for c in item.children)
        elif isinstance(item, str):
            return item
        return ""

    def _find_tree(self, items, tree_type: str):
        for item in items:
            if isinstance(item, Tree) and item.data == tree_type:
                return item
        return None

    def extract(self, tree) -> list[Definition]:
        self.definitions = []
        self._walk(tree)
        return self.definitions

    def _walk(self, tree):
        if not isinstance(tree, Tree):
            return

        if tree.data == "archetype":
            self._process_archetype(tree)
        elif tree.data == "enum":
            self._process_enum(tree)
        elif tree.data == "ability":
            self._process_top_level_ability(tree)
        elif tree.data == "global_var":
            self._process_global_var(tree)
        else:
            for child in tree.children:
                self._walk(child)

    def _process_archetype(self, tree):
        is_async = any(isinstance(c, Token) and c.type == "KW_ASYNC" for c in tree.children)
        decl = self._find_tree(tree.children, "archetype_decl")
        if decl:
            defn = self._extract_archetype_decl(decl)
            if defn:
                defn.is_async = is_async
                self.definitions.append(defn)

    def _extract_archetype_decl(self, tree) -> Optional[Definition]:
        arch_type = None
        name = None
        parent = None
        attrs = []
        abilities = []
        functions = []

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "arch_type":
                    arch_type = self._get_text(child).strip()
                elif child.data == "inherited_archs":
                    parent = self._get_text(child).strip("() ")
                elif child.data == "member_block":
                    attrs, abilities, functions = self._extract_member_block(child)
            elif isinstance(child, Token) and child.type == "NAME":
                name = str(child)

        if arch_type and name:
            kind_map = {
                "node": DefinitionKind.NODE,
                "edge": DefinitionKind.EDGE,
                "walker": DefinitionKind.WALKER,
                "obj": DefinitionKind.OBJECT,
                "class": DefinitionKind.CLASS,
            }
            kind = kind_map.get(arch_type, DefinitionKind.OBJECT)
            return Definition(
                kind=kind,
                name=name,
                parent=parent,
                attributes=attrs,
                abilities=abilities,
                functions=functions,
            )
        return None

    def _extract_member_block(self, tree):
        attrs = []
        abilities = []
        functions = []

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "member_stmt":
                    a, ab, fn = self._extract_member_stmt(child)
                    attrs.extend(a)
                    abilities.extend(ab)
                    functions.extend(fn)
                elif child.data == "has_stmt":
                    attrs.extend(self._extract_has_stmt(child))
                elif child.data == "ability":
                    ab, fn = self._extract_ability(child)
                    if ab:
                        abilities.append(ab)
                    if fn:
                        functions.append(fn)

        return attrs, abilities, functions

    def _extract_member_stmt(self, tree):
        attrs = []
        abilities = []
        functions = []

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "has_stmt":
                    attrs.extend(self._extract_has_stmt(child))
                elif child.data == "ability":
                    ab, fn = self._extract_ability(child)
                    if ab:
                        abilities.append(ab)
                    if fn:
                        functions.append(fn)

        return attrs, abilities, functions

    def _extract_has_stmt(self, tree) -> list[Attribute]:
        attrs = []
        is_static = any(isinstance(c, Token) and c.type == "KW_STATIC" for c in tree.children)

        for child in tree.children:
            if isinstance(child, Tree) and child.data == "has_assign_list":
                attrs.extend(self._extract_has_assign_list(child, is_static))

        return attrs

    def _extract_has_assign_list(self, tree, is_static: bool) -> list[Attribute]:
        attrs = []

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "typed_has_clause":
                    attr = self._extract_typed_has_clause(child, is_static)
                    if attr:
                        attrs.append(attr)
                elif child.data == "has_assign_list":
                    attrs.extend(self._extract_has_assign_list(child, is_static))

        return attrs

    def _extract_typed_has_clause(self, tree, is_static: bool) -> Optional[Attribute]:
        name = None
        type_hint = None
        default = None

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "named_ref":
                    name = self._get_text(child)
                elif child.data == "type_tag":
                    type_hint = self._extract_type_tag(child)
                elif child.data == "expression":
                    default = self._get_text(child)
            elif isinstance(child, Token) and child.type == "NAME":
                name = str(child)

        if name:
            return Attribute(name=name, type_hint=type_hint, default=default, is_static=is_static)
        return None

    def _extract_type_tag(self, tree) -> str:
        for child in tree.children:
            if isinstance(child, Tree) and child.data == "pipe":
                return self._get_text(child)
        return ""

    def _extract_ability(self, tree):
        is_async = any(isinstance(c, Token) and c.type == "KW_ASYNC" for c in tree.children)

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "ability_decl":
                    return self._extract_ability_decl(child, is_async), None
                elif child.data == "function_decl":
                    return None, self._extract_function_decl(child, is_async)

        return None, None

    def _extract_ability_decl(self, tree, is_async: bool) -> Optional[AbilitySignature]:
        name = ""
        trigger = None
        is_override = False
        is_static = False

        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "KW_OVERRIDE":
                    is_override = True
                elif child.type == "KW_STATIC":
                    is_static = True
            elif isinstance(child, Tree):
                if child.data == "named_ref":
                    name = self._get_text(child)
                elif child.data == "event_clause":
                    trigger = self._extract_event_clause(child)

        return AbilitySignature(
            name=name,
            trigger=trigger,
            is_async=is_async,
            is_static=is_static,
            is_override=is_override,
        )

    def _extract_event_clause(self, tree) -> str:
        parts = []
        for child in tree.children:
            if isinstance(child, Token):
                if child.type in ("KW_WITH", "KW_ENTRY", "KW_EXIT"):
                    parts.append(str(child))
            elif isinstance(child, Tree) and child.data == "expression":
                expr = self._get_text(child)
                if parts and parts[-1] == "with":
                    parts.append(expr)
                else:
                    parts.insert(-1 if parts else 0, expr)

        return " ".join(parts)

    def _extract_function_decl(self, tree, is_async: bool) -> Optional[FunctionSignature]:
        name = None
        params = None
        return_type = None
        is_override = False
        is_static = False

        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "KW_OVERRIDE":
                    is_override = True
                elif child.type == "KW_STATIC":
                    is_static = True
            elif isinstance(child, Tree):
                if child.data == "named_ref":
                    name = self._get_text(child)
                elif child.data == "func_decl":
                    params, return_type = self._extract_func_decl(child)

        if name:
            return FunctionSignature(
                name=name,
                params=params,
                return_type=return_type,
                is_async=is_async,
                is_static=is_static,
                is_override=is_override,
            )
        return None

    def _extract_func_decl(self, tree):
        params = ""
        return_type = None

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "func_decl_params":
                    params = self._get_text(child)
                elif child.data == "pipe":
                    return_type = self._get_text(child)

        return params, return_type

    def _process_enum(self, tree):
        decl = self._find_tree(tree.children, "enum_decl")
        if decl:
            defn = self._extract_enum_decl(decl)
            if defn:
                self.definitions.append(defn)

    def _extract_enum_decl(self, tree) -> Optional[Definition]:
        name = None
        parent = None

        for child in tree.children:
            if isinstance(child, Token) and child.type == "NAME":
                name = str(child)
            elif isinstance(child, Tree) and child.data == "inherited_archs":
                parent = self._get_text(child).strip("()")

        if name:
            return Definition(kind=DefinitionKind.ENUM, name=name, parent=parent)
        return None

    def _process_top_level_ability(self, tree):
        ab, fn = self._extract_ability(tree)
        if ab:
            self.definitions.append(Definition(
                kind=DefinitionKind.ABILITY,
                name=ab.name,
                abilities=[ab],
            ))
        if fn:
            self.definitions.append(Definition(
                kind=DefinitionKind.FUNCTION,
                name=fn.name,
                functions=[fn],
            ))

    def _process_global_var(self, tree):
        for child in tree.children:
            if isinstance(child, Tree) and child.data == "assignment_list":
                attrs = self._extract_assignment_list(child)
                for attr in attrs:
                    self.definitions.append(Definition(
                        kind=DefinitionKind.GLOBAL,
                        name=attr.name,
                        attributes=[attr],
                    ))

    def _extract_assignment_list(self, tree) -> list[Attribute]:
        attrs = []
        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "assignment":
                    attr = self._extract_assignment(child)
                    if attr:
                        attrs.append(attr)
                elif child.data == "named_ref":
                    attrs.append(Attribute(name=self._get_text(child)))
        return attrs

    def _extract_assignment(self, tree) -> Optional[Attribute]:
        name = None
        type_hint = None
        default = None

        for child in tree.children:
            if isinstance(child, Tree):
                if child.data == "atomic_chain":
                    name = self._get_text(child)
                elif child.data == "type_tag":
                    type_hint = self._extract_type_tag(child)
                elif child.data == "expression":
                    default = self._get_text(child)

        if name:
            return Attribute(name=name, type_hint=type_hint, default=default)
        return None


class LarkExtractor:
    """AST-based extractor using the official Jac Lark grammar."""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self._parser = None
        self._init_parser()

    def _init_parser(self):
        if not LARK_AVAILABLE:
            return

        grammar_path = Path(__file__).parents[2] / "config" / "grammar" / "jac.lark"
        if not grammar_path.exists():
            return

        try:
            self._parser = Lark(
                grammar_path.read_text(),
                start='start',
                parser='lalr',
                propagate_positions=True,
            )
        except Exception:
            self._parser = None

    @property
    def available(self) -> bool:
        return self._parser is not None

    def extract_from_code(self, code: str, file_path: str = None) -> list[Definition]:
        if not self.available:
            return []

        try:
            tree = self._parser.parse(code)
            extractor = JacASTExtractor()
            definitions = extractor.extract(tree)

            for defn in definitions:
                defn.file_source = file_path

            return definitions
        except LarkError:
            return []
        except Exception:
            return []

    def analyze_file(self, file_path: Path) -> dict:
        try:
            code = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {"error": str(e), "file": str(file_path)}

        definitions = self.extract_from_code(code, file_path.name)

        stats = {
            'nodes': 0, 'edges': 0, 'walkers': 0, 'objects': 0,
            'abilities': 0, 'functions': 0, 'globals': 0, 'enums': 0,
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
            elif defn.kind == DefinitionKind.ENUM:
                stats['enums'] += 1
            stats['abilities'] += len(defn.abilities)

        return {"file": file_path.name, "definitions": definitions, "stats": stats}

    def process_directory(self, dir_path: Path) -> dict:
        results = {
            "files": [],
            "all_definitions": [],
            "totals": {
                "files": 0, "nodes": 0, "edges": 0, "walkers": 0,
                "objects": 0, "abilities": 0, "functions": 0, "globals": 0, "enums": 0,
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

    def extract_from_markdown(self, markdown: str) -> list[Definition]:
        """Extract Jac definitions from code blocks in markdown using AST."""
        if not self.available:
            return []

        import re
        all_definitions = []
        code_block_pattern = re.compile(r'```jac\s*\n(.*?)```', re.DOTALL)

        for match in code_block_pattern.finditer(markdown):
            code = match.group(1)
            # Basic cleanup to ensure parseability if snippet is partial
            if "{" in code and "}" not in code:
                code += "\n}"
            
            definitions = self.extract_from_code(code)
            all_definitions.extend(definitions)

        return all_definitions

    def _deduplicate_definitions(self, definitions: list[Definition]) -> list[Definition]:
        """Deduplicate definitions by (kind, name), merging contents."""
        seen = {}
        for defn in definitions:
            key = (defn.kind.value, defn.name)
            if key not in seen:
                seen[key] = defn
            else:
                seen[key].merge(defn)
        return list(seen.values())

    def generate_skeleton(self, results: dict) -> str:
        deduped = self._deduplicate_definitions(results["all_definitions"])

        sections = []
        sections.append("# Jac API Reference (AST-Extracted)")
        sections.append(f"# Extracted from {results['totals']['files']} source files")
        sections.append(f"# {len(deduped)} unique definitions (from {len(results['all_definitions'])} total)")
        sections.append("")

        by_kind = {}
        for defn in deduped:
            kind_name = defn.kind.value
            if kind_name not in by_kind:
                by_kind[kind_name] = []
            by_kind[kind_name].append(defn)

        kind_order = ['node', 'edge', 'walker', 'obj', 'class', 'def', 'glob', 'enum']
        kind_titles = {
            'node': 'Nodes', 'edge': 'Edges', 'walker': 'Walkers',
            'obj': 'Objects', 'class': 'Classes', 'def': 'Functions',
            'glob': 'Globals', 'enum': 'Enums',
        }

        for kind in kind_order:
            if kind in by_kind and by_kind[kind]:
                sections.append(f"## {kind_titles.get(kind, kind.title())}")
                sections.append("")
                for defn in by_kind[kind]:
                    sections.append(defn.to_skeleton())
                    sections.append("")

        return '\n'.join(sections)
