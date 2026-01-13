import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class JacDefinition:
    """Represents an extracted Jac definition."""
    name: str
    kind: str  # walker, node, edge, object, ability, enum, etc.
    code: str
    docstring: Optional[str] = None
    file_source: Optional[str] = None
    line_number: int = 0

    def to_markdown(self) -> str:
        """Convert to markdown documentation format."""
        parts = [f"### {self.kind.title()}: `{self.name}`"]

        if self.docstring:
            parts.append(f"\n{self.docstring}")

        parts.append(f"\n```jac\n{self.code}\n```")

        if self.file_source:
            parts.append(f"\n*Source: {self.file_source}*")

        return '\n'.join(parts)


class JacExtractor:
    """Extracts patterns, definitions, and examples from .jac source files."""

    DEFINITION_PATTERNS = {
        'walker': r'((?:#.*\n)*)?walker\s+(\w+)(?:\s*<[^>]*>)?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}',
        'node': r'((?:#.*\n)*)?node\s+(\w+)(?:\s*<[^>]*>)?\s*(?::\s*\w+)?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}',
        'edge': r'((?:#.*\n)*)?edge\s+(\w+)(?:\s*<[^>]*>)?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}',
        'object': r'((?:#.*\n)*)?obj(?:ect)?\s+(\w+)(?:\s*<[^>]*>)?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}',
        'enum': r'((?:#.*\n)*)?enum\s+(\w+)\s*\{([^}]*)\}',
        'ability': r'((?:#.*\n)*)?can\s+(\w+)(?:\s*\([^)]*\))?\s*(?:->[^{]*)?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}',
        'global': r'((?:#.*\n)*)?glob\s+(\w+)\s*[:=][^;]*;',
        'test': r'((?:#.*\n)*)?test\s+(\w+)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}',
    }

    SYNTAX_PATTERNS = {
        'edge_ops': r'(\+\+>|-->|<\+\+|<--|<\+\+>|<-->)',
        'spawn': r'spawn\s+(\w+)',
        'visit': r'visit\s+([^;{]+)',
        'report': r'report\s+([^;]+);',
        'entry_exit': r'with\s+(entry|exit)\s*\{',
        'llm_ability': r'by\s+(llm|reason)\s*\(',
        'disengage': r'\bdisengage\b',
        'skip': r'\bskip\b',
        'here': r'\bhere\b',
        'self': r'\bself\b',
        'root': r'\broot\b',
    }

    def __init__(self, config: dict = None):
        self.config = config or {}

    def extract_definitions(self, code: str, file_path: str = None) -> list[JacDefinition]:
        """Extract all definitions from Jac code."""
        definitions = []

        for kind, pattern in self.DEFINITION_PATTERNS.items():
            for match in re.finditer(pattern, code, re.MULTILINE | re.DOTALL):
                groups = match.groups()

                if kind == 'global':
                    docstring = groups[0].strip() if groups[0] else None
                    name = groups[1]
                    full_code = match.group(0)
                else:
                    docstring = self._parse_docstring(groups[0]) if groups[0] else None
                    name = groups[1]
                    body = groups[2] if len(groups) > 2 else ""
                    full_code = match.group(0)

                if docstring:
                    full_code = full_code.replace(groups[0], '').strip()

                definitions.append(JacDefinition(
                    name=name,
                    kind=kind,
                    code=self._clean_code(full_code),
                    docstring=docstring,
                    file_source=file_path,
                    line_number=code[:match.start()].count('\n') + 1
                ))

        return definitions

    def _parse_docstring(self, comment_block: str) -> Optional[str]:
        """Parse docstring from comment block."""
        if not comment_block:
            return None

        lines = []
        for line in comment_block.strip().split('\n'):
            line = line.strip()
            if line.startswith('#'):
                line = line[1:].strip()
                if line.startswith('#'):
                    line = line[1:].strip()
                lines.append(line)

        return ' '.join(lines) if lines else None

    def _clean_code(self, code: str) -> str:
        """Clean up code formatting."""
        lines = code.split('\n')
        if not lines:
            return code

        min_indent = float('inf')
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        if min_indent == float('inf'):
            min_indent = 0

        cleaned = []
        for line in lines:
            if line.strip():
                cleaned.append(line[min_indent:] if len(line) > min_indent else line)
            else:
                cleaned.append('')

        return '\n'.join(cleaned).strip()

    def extract_syntax_examples(self, code: str) -> dict[str, list[str]]:
        """Extract examples of Jac syntax patterns."""
        examples = {}

        for name, pattern in self.SYNTAX_PATTERNS.items():
            matches = re.findall(pattern, code)
            if matches:
                examples[name] = list(set(matches))[:5]

        return examples

    def analyze_file(self, file_path: Path) -> dict:
        """Analyze a single .jac file."""
        try:
            code = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {"error": str(e), "file": str(file_path)}

        definitions = self.extract_definitions(code, file_path.name)
        syntax_examples = self.extract_syntax_examples(code)

        return {
            "file": file_path.name,
            "definitions": definitions,
            "syntax_examples": syntax_examples,
            "stats": {
                "walkers": len([d for d in definitions if d.kind == 'walker']),
                "nodes": len([d for d in definitions if d.kind == 'node']),
                "edges": len([d for d in definitions if d.kind == 'edge']),
                "objects": len([d for d in definitions if d.kind == 'object']),
                "abilities": len([d for d in definitions if d.kind == 'ability']),
                "tests": len([d for d in definitions if d.kind == 'test']),
            }
        }

    def process_directory(self, dir_path: Path) -> dict:
        """Process all .jac files in a directory."""
        results = {
            "files": [],
            "all_definitions": [],
            "syntax_summary": {},
            "totals": {
                "files": 0,
                "walkers": 0,
                "nodes": 0,
                "edges": 0,
                "objects": 0,
                "abilities": 0,
                "tests": 0,
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

                for syntax_type, examples in analysis["syntax_examples"].items():
                    if syntax_type not in results["syntax_summary"]:
                        results["syntax_summary"][syntax_type] = []
                    results["syntax_summary"][syntax_type].extend(examples)

        for syntax_type in results["syntax_summary"]:
            results["syntax_summary"][syntax_type] = list(set(
                results["syntax_summary"][syntax_type]
            ))[:10]

        return results

    def generate_markdown(self, results: dict) -> str:
        """Generate markdown documentation from extracted definitions."""
        sections = []

        sections.append("# Jac Code Examples\n")
        sections.append(f"Extracted from {results['totals']['files']} source files.\n")

        by_kind = {}
        for defn in results["all_definitions"]:
            if defn.kind not in by_kind:
                by_kind[defn.kind] = []
            by_kind[defn.kind].append(defn)

        kind_order = ['walker', 'node', 'edge', 'object', 'ability', 'enum', 'test']

        for kind in kind_order:
            if kind in by_kind and by_kind[kind]:
                sections.append(f"\n## {kind.title()}s\n")
                for defn in by_kind[kind][:20]:
                    sections.append(defn.to_markdown())
                    sections.append("")

        if results["syntax_summary"]:
            sections.append("\n## Syntax Patterns\n")
            for syntax_type, examples in results["syntax_summary"].items():
                readable_name = syntax_type.replace('_', ' ').title()
                sections.append(f"### {readable_name}")
                sections.append(f"Examples: `{'`, `'.join(examples[:5])}`\n")

        return '\n'.join(sections)
