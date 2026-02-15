#!/usr/bin/env python3
"""Content validator for pipeline stages.

Validates that critical syntax patterns, code blocks, and content
are preserved between compression stages. Uses jaclang's in-process
parser for fast syntax checking (~8ms per block).
"""
import re
from dataclasses import dataclass, field
from typing import Optional

from jaclang.pycore.compiler import JacCompiler
from jaclang.pycore.program import JacProgram


class ValidationError(Exception):
    """Raised when strict validation fails."""
    pass


@dataclass
class ValidationResult:
    is_valid: bool
    issues: list
    missing_patterns: list
    size_ratio: float


@dataclass
class JacCheckResult:
    total_blocks: int
    passed: int
    failed: int
    skipped: int
    pass_rate: float
    errors: list = field(default_factory=list)


class Validator:
    CRITICAL_PATTERNS = [
        (r'\+\+>', 'edge: ++>'),
        (r'<\+\+>', 'edge: <++>'),
        (r'-->', 'edge: -->'),
        (r'<-->', 'edge: <-->'),
        (r'\+>:', 'typed connect: +>:'),
        (r':\+>', 'typed connect: :+>'),
        (r'->:', 'typed traversal: ->:'),
        (r':->',  'typed traversal: :->'),
        (r'\bdel-->', 'disconnect: del-->'),
        (r'by\s+llm\s*[;(]', 'by llm'),
        (r'with\s+entry', 'with entry'),
        (r'with\s+exit', 'with exit'),
        (r'`root\s+entry', 'root entry'),
        (r'\bspawn\b', 'spawn'),
        (r'import\s+from\s+\w+\s*\{', 'import from module { }'),
        (r'\bhas\s+\w+\s*:', 'has x: type'),
        (r'\bnode\s+\w+', 'node definition'),
        (r'\bwalker\s+\w+', 'walker definition'),
        (r'\bedge\s+\w+', 'edge definition'),
        (r'\bobj\s+\w+', 'obj definition'),
        (r'\bcan\s+\w+', 'ability definition'),
        (r'file\.open', 'file.open'),
        (r'json\.dumps', 'json.dumps'),
        (r'json\.loads', 'json.loads'),
        (r'\basync\b', 'async'),
        (r'\bawait\b', 'await'),
        (r'\breport\b', 'report'),
        (r'\bvisit\b', 'visit'),
        (r'\bhere\b', 'here keyword'),
        (r'\bself\b', 'self keyword'),
        (r'\bprops\b', 'props keyword'),
        (r'\bcl\s*\{', 'client block'),
        (r'\bsv\s*\{', 'server block'),
        (r'<[A-Z]\w*', 'JSX element'),
        (r'/>', 'JSX self-closing'),
        (r'\buseState\b', 'React useState'),
        (r'\buseEffect\b', 'React useEffect'),
        (r'\bcase\s+\w+\s*:', 'match case with colon'),
        (r'lambda\s+\w+\s*:', 'lambda expression'),
    ]

    _TOPLEVEL_RE = re.compile(
        r'^\s*(?:node|walker|edge|obj|enum|class|async\s+walker|'
        r'def|async\s+def|can|import|glob|test|include|with\s+entry)\b'
    )

    _TYPE_REF_PATTERNS = [
        re.compile(r'\+>:\s*(\w+)\s*\('),       # +>: TypeName(
        re.compile(r'\+\+>\s*(\w+)\s*\('),       # ++> TypeName(
        re.compile(r'<\+:\s*(\w+)\s*\('),        # <+: TypeName(
        re.compile(r'\[->\s*:\s*(\w+)\s*:\s*->'), # [->:TypeName:->]
        re.compile(r'\[-->\]\s*\(\?\s*:\s*(\w+)'),# [-->](?:TypeName)
    ]

    def __init__(self, min_size_ratio=0.1, required_pattern_ratio=0.5):
        self.min_size_ratio = min_size_ratio
        self.required_pattern_ratio = required_pattern_ratio
        self.compiler = JacCompiler()

    def _parse_jac(self, code: str) -> tuple[bool, Optional[str]]:
        """Parse Jac code in-process using jaclang's compiler.

        Returns (passed, error_message).
        """
        prog = JacProgram()
        try:
            module = self.compiler.parse_str(code, "check.jac", prog)
        except Exception as exc:
            return False, str(exc)

        if module.has_syntax_errors:
            errors = prog.errors_had
            if errors:
                return False, str(errors[0])
            return False, "syntax error"
        return True, None

    def find_patterns(self, text):
        found = set()
        for pattern, name in self.CRITICAL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                found.add(name)
        return found

    def validate_code_blocks(self, text):
        fence_count = text.count('```')
        if fence_count % 2 != 0:
            return False, "Unbalanced code fences"
        return True, None

    def validate(self, input_text, output_text):
        issues = []
        missing_patterns = []

        if not output_text or not output_text.strip():
            return ValidationResult(
                is_valid=False,
                issues=["Output is empty"],
                missing_patterns=[],
                size_ratio=0.0
            )

        size_ratio = len(output_text) / max(len(input_text), 1)

        if size_ratio < self.min_size_ratio:
            issues.append(f"Output too small: {size_ratio:.1%} of input (min: {self.min_size_ratio:.0%})")

        valid_blocks, block_issue = self.validate_code_blocks(output_text)
        if not valid_blocks:
            issues.append(block_issue)

        input_patterns = self.find_patterns(input_text)
        output_patterns = self.find_patterns(output_text)

        if input_patterns:
            missing = input_patterns - output_patterns
            preserved_ratio = len(output_patterns) / len(input_patterns)

            if preserved_ratio < self.required_pattern_ratio:
                issues.append(
                    f"Too many patterns lost: {preserved_ratio:.0%} preserved "
                    f"(need {self.required_pattern_ratio:.0%})"
                )
            missing_patterns = list(missing)

        is_valid = len(issues) == 0
        return ValidationResult(
            is_valid=is_valid,
            issues=issues,
            missing_patterns=missing_patterns,
            size_ratio=size_ratio
        )

    def validate_final(self, text, required_patterns=None):
        """Validate final output has minimum required patterns."""
        issues = []

        if required_patterns is None:
            required_patterns = [
                'edge: ++>', 'by llm', 'with entry', 'spawn',
                'node definition', 'walker definition', 'has x: type',
                'typed connect: +>:', 'typed traversal: ->:',
            ]

        found = self.find_patterns(text)
        missing = [p for p in required_patterns if p not in found]

        if missing:
            issues.append(f"Missing required patterns: {missing}")

        valid_blocks, block_issue = self.validate_code_blocks(text)
        if not valid_blocks:
            issues.append(block_issue)

        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            missing_patterns=missing,
            size_ratio=1.0
        )

    def extract_jac_blocks(self, text: str) -> list[tuple[int, str]]:
        """Extract Jac code blocks from markdown text.

        Only extracts blocks explicitly tagged as ```jac or ```jaclang.
        Returns list of (block_index, code) tuples.
        """
        blocks = []
        pattern = r'```(?:jac|jaclang)\s*\n(.*?)```'
        matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)

        for i, match in enumerate(matches):
            code = match.group(1).strip()
            if code and not code.startswith('//') and len(code) > 10:
                blocks.append((i, code))

        return blocks

    def _classify_block(self, code: str) -> str:
        """Classify a code block for validation purposes.

        Returns one of: 'complete', 'declarations', 'statements',
        'client_side', 'api_notation', 'fragment'
        """
        lines = code.strip().split('\n')
        non_blank = [
            ln.strip() for ln in lines
            if ln.strip() and not ln.strip().startswith('#') and not ln.strip().startswith('//')
        ]

        if len(non_blank) < 2:
            return 'fragment'

        fragment_markers = ['...', '# ...', '// ...', '/* ... */', '...}', '{...']
        if any(marker in code for marker in fragment_markers):
            return 'fragment'

        if re.search(r'\bcl\s*\{', code) or re.search(r'\bsv\s+import\b', code):
            return 'client_side'
        if re.search(r'<[A-Z]\w+[\s/>]', code) and not re.search(r'\bnode\s+\w+', code):
            return 'client_side'

        if '__jac__.' in code and not re.search(r'\b(node|walker|obj)\s+\w+', code):
            return 'api_notation'

        # Syntax reference blocks: mostly independent one-liner examples
        # (traversal forms, operator demos) not forming a coherent program
        standalone_expr_count = sum(
            1 for ln in non_blank
            if re.match(r'^\s*\[[-<>:!\w\s,()?.]+\]\s*$', ln)
            or (not ln.rstrip().endswith(';') and not ln.rstrip().endswith('{') and not ln.rstrip().endswith('}')
                and not self._TOPLEVEL_RE.match(ln))
        )
        if len(non_blank) >= 5 and standalone_expr_count / len(non_blank) > 0.5:
            return 'fragment'

        has_archetype = bool(re.search(
            r'\b(?:node|walker|edge|obj|enum|class)\s+\w+', code
        ))
        has_entry = bool(re.search(r'with\s+entry', code))
        has_toplevel_def = bool(re.search(r'^\s*(?:def|can)\s+\w+', code, re.MULTILINE))

        if has_archetype or (has_entry and has_toplevel_def):
            return 'complete'

        has_import = bool(re.search(r'^\s*import\s+', code, re.MULTILINE))
        has_glob = bool(re.search(r'^\s*glob\s+', code, re.MULTILINE))
        has_decl = has_toplevel_def or has_import or has_glob

        bare_count = sum(
            1 for ln in non_blank
            if not self._TOPLEVEL_RE.match(ln)
        )

        if bare_count > 0:
            return 'statements'

        if has_decl:
            return 'declarations'

        return 'declarations'

    @staticmethod
    def _strip_inline_comment(line: str) -> str:
        """Strip # comments while preserving # inside strings."""
        in_str = None
        for i, ch in enumerate(line):
            if ch in ('"', "'") and (i == 0 or line[i - 1] != '\\'):
                if in_str is None:
                    in_str = ch
                elif in_str == ch:
                    in_str = None
            elif ch == '#' and in_str is None:
                return line[:i].rstrip()
        return line

    def _prepare_for_check(self, code: str) -> str:
        """Prepare a code block for parsing by stripping inline comments,
        generating type stubs, and wrapping bare statements in `with entry {}`.
        """
        cleaned_lines = [self._strip_inline_comment(ln) for ln in code.split('\n')]
        code = '\n'.join(cleaned_lines)

        defined_names = set()
        for m in re.finditer(r'\b(?:node|edge|walker|obj|enum|class)\s+(\w+)', code):
            defined_names.add(m.group(1))

        stub_lines = []
        for pattern in self._TYPE_REF_PATTERNS:
            for m in pattern.finditer(code):
                name = m.group(1)
                if name not in defined_names and name[0].isupper():
                    stub_lines.append(f'node {name} {{ has val: int = 0; }}')
                    defined_names.add(name)

        declarations = []
        statements = []
        in_declaration = False
        brace_depth = 0

        for line in cleaned_lines:
            stripped = line.strip()

            if in_declaration:
                declarations.append(line)
                brace_depth += stripped.count('{') - stripped.count('}')
                if brace_depth <= 0:
                    in_declaration = False
                    brace_depth = 0
                continue

            if not stripped or stripped.startswith('#'):
                continue

            is_decl = bool(re.match(
                r'^\s*(?:node|walker|edge|obj|enum|class|async\s+walker|def|async\s+def|'
                r'can|import|glob|test|include)\b',
                stripped
            ))

            if is_decl:
                declarations.append(line)
                brace_depth = stripped.count('{') - stripped.count('}')
                if brace_depth > 0:
                    in_declaration = True
            else:
                statements.append(line)

        if not statements:
            return '\n'.join(stub_lines + declarations) if stub_lines else code

        parts = stub_lines + declarations + ['with entry {'] + ['    ' + s for s in statements] + ['}']
        return '\n'.join(parts)

    def _check_block(
        self,
        idx: int,
        code: str,
    ) -> tuple[int, str, Optional[bool], Optional[str]]:
        """Check a single code block.

        Returns (idx, code, success, error).
        success=None means the block was skipped.
        """
        category = self._classify_block(code)

        if category in ('fragment', 'client_side', 'api_notation'):
            return (idx, code, None, None)

        if category == 'statements':
            check_code = self._prepare_for_check(code)
            success, error = self._parse_jac(check_code)
            return (idx, code, success, error)

        success, error = self._parse_jac(code)
        if not success:
            check_code = self._prepare_for_check(code)
            success, error = self._parse_jac(check_code)
        return (idx, code, success, error)

    def validate_all_examples(
        self,
        text: str,
        fail_threshold: float = 90.0,
        on_progress: Optional[callable] = None,
        **kwargs,
    ) -> JacCheckResult:
        """Run syntax check on all fenced code blocks.

        Args:
            text: Documentation text containing code blocks
            fail_threshold: Minimum pass rate percentage (default 90%)
            on_progress: Optional callback(current, total, message)

        Returns:
            JacCheckResult with comprehensive statistics
        """
        blocks = self.extract_jac_blocks(text)
        total = len(blocks)

        if total == 0:
            return JacCheckResult(0, 0, 0, 0, 0.0, [])

        passed = 0
        failed = 0
        skipped = 0
        errors = []

        for i, (block_idx, code) in enumerate(blocks):
            if on_progress:
                on_progress(i + 1, total, f"Validating {i + 1}/{total} blocks")

            _, _, success, error = self._check_block(block_idx, code)

            if success is None:
                skipped += 1
            elif success:
                passed += 1
            else:
                failed += 1
                preview = code[:150].replace('\n', ' ')
                errors.append({
                    "block": block_idx + 1,
                    "error": error,
                    "code_preview": preview + "..." if len(code) > 150 else preview
                })

        total_checked = passed + failed
        pass_rate = (passed / total_checked * 100) if total_checked > 0 else 0.0

        result = JacCheckResult(
            total_blocks=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            pass_rate=pass_rate,
            errors=errors
        )

        if pass_rate < fail_threshold and total_checked > 0:
            print(f"WARNING: Only {pass_rate:.1f}% of examples passed syntax check (threshold: {fail_threshold}%)")
            for err in errors[:5]:
                print(f"  Block {err['block']}: {err['error']}")

        return result

    def validate_strict(
        self,
        text: str,
        fail_on_error: bool = True,
        on_progress: Optional[callable] = None,
        **kwargs,
    ) -> JacCheckResult:
        """Strictly validate all fenced Jac code blocks.

        Uses in-process jaclang parser for fast validation (~8ms per block).

        Args:
            text: Documentation text containing code blocks
            fail_on_error: If True, raise ValidationError on any failure
            on_progress: Optional callback(current, total, message)

        Returns:
            JacCheckResult with comprehensive statistics

        Raises:
            ValidationError: If fail_on_error=True and any block fails
        """
        blocks = self.extract_jac_blocks(text)
        total = len(blocks)

        if total == 0:
            return JacCheckResult(0, 0, 0, 0, 100.0, [])

        passed = 0
        failed = 0
        skipped = 0
        errors = []

        for i, (idx, code) in enumerate(blocks):
            if on_progress:
                on_progress(i + 1, total, f"Checked {i + 1}/{total} blocks")

            _, _, success, error = self._check_block(idx, code)

            if success is None:
                skipped += 1
            elif success:
                passed += 1
            else:
                failed += 1
                preview = code[:200].replace('\n', ' ')
                errors.append({
                    "line": idx,
                    "error": error,
                    "source": "fenced",
                    "code": preview + "..." if len(code) > 200 else preview
                })

        total_checked = passed + failed
        pass_rate = (passed / total_checked * 100) if total_checked > 0 else 100.0

        result = JacCheckResult(
            total_blocks=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            pass_rate=pass_rate,
            errors=errors
        )

        if errors and fail_on_error:
            error_summary = "\n".join(
                f"  [{e['source']}:{e['line']}] {e['error']}"
                for e in errors[:5]
            )
            raise ValidationError(
                f"{len(errors)} code blocks failed syntax check:\n{error_summary}"
            )

        return result
