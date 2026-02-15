"""
Jaclang AST Extractor for Jac Language

Uses jaclang's JacCompiler.parse_str() to parse code and extract
structural signatures while discarding implementation bodies.
Replaces the deprecated lark-based extractor.
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

from jaclang.pycore.compiler import JacCompiler
from jaclang.pycore.program import JacProgram


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
        if self.kind != other.kind or self.name != other.name:
            return

        if other.docstring:
            if not self.docstring:
                self.docstring = other.docstring
            elif len(other.docstring) > len(self.docstring):
                self.docstring = other.docstring

        if not self.parent and other.parent:
            self.parent = other.parent

        existing_attrs = {a.name: a for a in self.attributes}
        for attr in other.attributes:
            if attr.name not in existing_attrs:
                self.attributes.append(attr)
            else:
                existing = existing_attrs[attr.name]
                if not existing.type_hint and attr.type_hint:
                    existing.type_hint = attr.type_hint
                if not existing.default and attr.default:
                    existing.default = attr.default

        existing_abilities = {a.name: a for a in self.abilities}
        for ab in other.abilities:
            if ab.name not in existing_abilities:
                self.abilities.append(ab)

        existing_funcs = {f.name: f for f in self.functions}
        for func in other.functions:
            if func.name not in existing_funcs:
                self.functions.append(func)


def _tok_val(token) -> str:
    """Extract the string value from a jaclang Token or Name node."""
    if token is None:
        return ""
    if hasattr(token, 'value'):
        return str(token.value)
    return str(token)


def _extract_type_tag(node) -> Optional[str]:
    """Extract type string from a SubTag (type_tag) node."""
    if node is None:
        return None
    if hasattr(node, 'tag') and node.tag is not None:
        return _tok_val(node.tag)
    if hasattr(node, 'unparse'):
        unparsed = node.unparse().strip()
        if unparsed.startswith(':'):
            return unparsed[1:].strip()
        return unparsed if unparsed else None
    return None


def _extract_default(node) -> Optional[str]:
    """Extract default value string from a value node."""
    if node is None:
        return None
    if hasattr(node, 'unparse'):
        return node.unparse().strip() or None
    return _tok_val(node) or None


def _extract_params_str(sig) -> Optional[str]:
    """Build a parameter string from a FuncSignature's params list."""
    if not hasattr(sig, 'params') or not sig.params:
        return None
    parts = []
    for pv in sig.params:
        name = _tok_val(pv.name)
        type_str = _extract_type_tag(pv.type_tag) if hasattr(pv, 'type_tag') else None
        default = _extract_default(pv.value) if hasattr(pv, 'value') else None
        p = name
        if type_str:
            p += f": {type_str}"
        if default:
            p += f" = {default}"
        parts.append(p)
    return ", ".join(parts) if parts else None


class JaclangExtractor:
    """AST-based extractor using jaclang's JacCompiler."""

    ARCH_TYPE_MAP = {
        "node": DefinitionKind.NODE,
        "edge": DefinitionKind.EDGE,
        "walker": DefinitionKind.WALKER,
        "obj": DefinitionKind.OBJECT,
        "class": DefinitionKind.CLASS,
    }

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.compiler = JacCompiler()

    @property
    def available(self) -> bool:
        return True

    def extract_from_code(self, code: str, file_path: str = None) -> list[Definition]:
        prog = JacProgram()
        try:
            module = self.compiler.parse_str(code, file_path or "input.jac", prog)
        except Exception:
            return []

        if module.has_syntax_errors:
            return []

        definitions = []
        for item in module.body:
            node_type = type(item).__name__
            if node_type == "Archetype":
                defn = self._extract_archetype(item)
                if defn:
                    if file_path:
                        defn.file_source = file_path
                    definitions.append(defn)
            elif node_type == "Enum":
                defn = self._extract_enum(item)
                if defn:
                    if file_path:
                        defn.file_source = file_path
                    definitions.append(defn)
            elif node_type == "GlobalVars":
                for defn in self._extract_global_vars(item):
                    if file_path:
                        defn.file_source = file_path
                    definitions.append(defn)
            elif node_type == "Ability":
                defn = self._extract_top_level_ability(item)
                if defn:
                    if file_path:
                        defn.file_source = file_path
                    definitions.append(defn)

        return definitions

    def _extract_archetype(self, node) -> Optional[Definition]:
        arch_type_str = _tok_val(node.arch_type)
        kind = self.ARCH_TYPE_MAP.get(arch_type_str, DefinitionKind.OBJECT)
        name = _tok_val(node.name)
        if not name:
            return None

        parent = None
        if node.base_classes:
            parent = ", ".join(_tok_val(bc) for bc in node.base_classes)

        attrs = []
        abilities = []
        functions = []

        if node.body:
            for member in node.body:
                member_type = type(member).__name__
                if member_type == "ArchHas":
                    attrs.extend(self._extract_arch_has(member))
                elif member_type == "Ability":
                    ab, fn = self._extract_ability(member)
                    if ab:
                        abilities.append(ab)
                    if fn:
                        functions.append(fn)

        return Definition(
            kind=kind,
            name=name,
            parent=parent,
            attributes=attrs,
            abilities=abilities,
            functions=functions,
        )

    def _extract_arch_has(self, arch_has) -> list[Attribute]:
        is_static = getattr(arch_has, 'is_static', False)
        attrs = []
        for hv in arch_has.vars:
            name = _tok_val(hv.name)
            if not name:
                continue
            type_hint = _extract_type_tag(hv.type_tag) if hasattr(hv, 'type_tag') else None
            default = _extract_default(hv.value) if hasattr(hv, 'value') else None
            attrs.append(Attribute(
                name=name,
                type_hint=type_hint,
                default=default,
                is_static=is_static,
            ))
        return attrs

    def _extract_ability(self, node) -> tuple[Optional[AbilitySignature], Optional[FunctionSignature]]:
        is_def = getattr(node, 'is_def', False)
        is_async = getattr(node, 'is_async', False)
        is_static = getattr(node, 'is_static', False)
        is_override = getattr(node, 'is_override', False)
        name = _tok_val(node.name_spec) if hasattr(node, 'name_spec') else ""

        sig = getattr(node, 'signature', None)

        if is_def and sig:
            params_str = _extract_params_str(sig)
            return_type = _tok_val(sig.return_type) if hasattr(sig, 'return_type') and sig.return_type else None
            return None, FunctionSignature(
                name=name,
                params=params_str,
                return_type=return_type,
                is_async=is_async,
                is_static=is_static,
                is_override=is_override,
            )

        if sig and type(sig).__name__ == "EventSignature":
            trigger = sig.unparse().strip() if hasattr(sig, 'unparse') else None
            return AbilitySignature(
                name=name,
                trigger=trigger,
                is_async=is_async,
                is_static=is_static,
                is_override=is_override,
            ), None

        if sig and type(sig).__name__ == "FuncSignature":
            params_str = _extract_params_str(sig)
            return_type = _tok_val(sig.return_type) if hasattr(sig, 'return_type') and sig.return_type else None
            return AbilitySignature(
                name=name,
                params=params_str,
                return_type=return_type,
                is_async=is_async,
                is_static=is_static,
                is_override=is_override,
            ), None

        return AbilitySignature(name=name, is_async=is_async), None

    def _extract_enum(self, node) -> Optional[Definition]:
        name = _tok_val(node.name)
        if not name:
            return None
        parent = None
        if hasattr(node, 'base_classes') and node.base_classes:
            parent = ", ".join(_tok_val(bc) for bc in node.base_classes)
        return Definition(kind=DefinitionKind.ENUM, name=name, parent=parent)

    def _extract_global_vars(self, node) -> list[Definition]:
        definitions = []
        if not hasattr(node, 'assignments'):
            return definitions
        for assignment in node.assignments:
            targets = getattr(assignment, 'target', [])
            if not targets:
                continue
            name = _tok_val(targets[0])
            type_hint = _extract_type_tag(assignment.type_tag) if hasattr(assignment, 'type_tag') else None
            default = _extract_default(assignment.value) if hasattr(assignment, 'value') else None
            definitions.append(Definition(
                kind=DefinitionKind.GLOBAL,
                name=name,
                attributes=[Attribute(name=name, type_hint=type_hint, default=default)],
            ))
        return definitions

    def _extract_top_level_ability(self, node) -> Optional[Definition]:
        is_def = getattr(node, 'is_def', False)
        name = _tok_val(node.name_spec) if hasattr(node, 'name_spec') else ""
        if not name:
            return None

        ab, fn = self._extract_ability(node)

        if is_def and fn:
            return Definition(
                kind=DefinitionKind.FUNCTION,
                name=name,
                functions=[fn],
            )

        if ab:
            return Definition(
                kind=DefinitionKind.ABILITY,
                name=name,
                abilities=[ab],
            )

        return None

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
            elif defn.kind in (DefinitionKind.OBJECT, DefinitionKind.CLASS):
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
        all_definitions = []
        code_block_pattern = re.compile(r'```jac\s*\n(.*?)```', re.DOTALL)

        for match in code_block_pattern.finditer(markdown):
            code = match.group(1)
            if "{" in code and "}" not in code:
                code += "\n}"
            definitions = self.extract_from_code(code)
            all_definitions.extend(definitions)

        return all_definitions

    def _deduplicate_definitions(self, definitions: list[Definition]) -> list[Definition]:
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
