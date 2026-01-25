"""Content validator for pipeline stages."""

include:jac utils.patterns;

import:py re;

obj ValidationResult {
    has is_valid: bool;
    has issues: list[str];
    has missing_patterns: list[str];
    has size_ratio: float;
}

obj Validator {
    has min_size_ratio: float = 0.1;
    has required_pattern_ratio: float = 0.5;

    has CRITICAL_PATTERNS: list[tuple] = [
        (r"\+\+>", "edge: ++>"),
        (r"<\+\+>", "edge: <++>"),
        (r"-->", "edge: -->"),
        (r"<-->", "edge: <-->"),
        (r"by\s+llm\s*\(", "by llm()"),
        (r"with\s+entry", "with entry"),
        (r"with\s+exit", "with exit"),
        (r"`root\s+entry", "root entry"),
        (r"\bspawn\b", "spawn"),
        (r"import:py", "import:py"),
        (r"\bhas\s+\w+\s*:", "has x: type"),
        (r"\bnode\s+\w+", "node definition"),
        (r"\bwalker\s+\w+", "walker definition"),
        (r"\bedge\s+\w+", "edge definition"),
        (r"\bobj\s+\w+", "obj definition"),
        (r"\bcan\s+\w+", "ability definition"),
        (r"file\.open", "file.open"),
        (r"json\.dumps", "json.dumps"),
        (r"json\.loads", "json.loads"),
        (r"\basync\b", "async"),
        (r"\bawait\b", "await"),
        (r"\breport\b", "report"),
        (r"\bvisit\b", "visit"),
        (r"\bhere\b", "here keyword"),
        (r"\bself\b", "self keyword")
    ];

    can find_patterns(text: str) -> set[str] {
        """Find all critical patterns in text."""
        found: set[str] = set();
        for (pattern, name) in self.CRITICAL_PATTERNS {
            if re.search(pattern, text, re.IGNORECASE) {
                found.add(name);
            }
        }
        return found;
    }

    can validate(input_text: str, output_text: str) -> dict {
        """Validate output against input content."""
        issues: list[str] = [];
        missing_patterns_list: list[str] = [];

        if not output_text or not output_text.strip() {
            return {
                "is_valid": False,
                "issues": ["Output is empty"],
                "missing_patterns": [],
                "size_ratio": 0.0
            };
        }

        size_ratio = len(output_text) / max(len(input_text), 1);

        if size_ratio < self.min_size_ratio {
            issues.append(
                f"Output too small: {size_ratio:.1%} of input (min: {self.min_size_ratio:.0%})"
            );
        }

        (valid_blocks, block_issue) = validate_code_blocks(output_text);
        if not valid_blocks {
            issues.append(block_issue);
        }

        input_patterns = self.find_patterns(input_text);
        output_patterns = self.find_patterns(output_text);

        if input_patterns {
            missing = input_patterns - output_patterns;
            preserved_ratio = len(output_patterns) / len(input_patterns);

            if preserved_ratio < self.required_pattern_ratio {
                issues.append(
                    f"Too many patterns lost: {preserved_ratio:.0%} preserved "
                    f"(need {self.required_pattern_ratio:.0%})"
                );
            }
            missing_patterns_list = list(missing);
        }

        is_valid = len(issues) == 0;
        return {
            "is_valid": is_valid,
            "issues": issues,
            "missing_patterns": missing_patterns_list,
            "size_ratio": size_ratio
        };
    }

    can validate_final(
        text: str,
        required_patterns: list[str] | None = None
    ) -> dict {
        """Validate final output has minimum required patterns."""
        issues: list[str] = [];

        if required_patterns is None {
            required_patterns = [
                "edge: ++>", "by llm()", "with entry", "spawn",
                "node definition", "walker definition", "has x: type"
            ];
        }

        found = self.find_patterns(text);
        missing = [p for p in required_patterns if p not in found];

        if missing {
            issues.append(f"Missing required patterns: {missing}");
        }

        (valid_blocks, block_issue) = validate_code_blocks(text);
        if not valid_blocks {
            issues.append(block_issue);
        }

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "missing_patterns": missing,
            "size_ratio": 1.0
        };
    }
}
