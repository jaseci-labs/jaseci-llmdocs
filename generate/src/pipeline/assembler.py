"""
Single-pass LLM assembler for Jac documentation.

Stage 2 of the lossless pipeline: assembles final reference from extracted content.
Uses ONE LLM call with template-driven structure.
Supports optional RAG integration for smarter content/rule retrieval.
"""

import re
from pathlib import Path
from .llm import LLM
from .deterministic_extractor import DeterministicExtractor, ExtractedContent


class Assembler:
    """Assembles final reference document from extracted content."""

    def __init__(self, llm: LLM, config: dict, on_progress=None, on_token=None, rag_retriever=None):
        self.llm = llm
        self.config = config
        self.on_progress = on_progress or (lambda *a: None)
        self.on_token = on_token
        self.rag_retriever = rag_retriever

        root = Path(__file__).parents[2]
        prompt_path = root / "config" / "assembly_prompt.txt"
        with open(prompt_path) as f:
            self.prompt_template = f.read()

    def assemble(self, extracted: ExtractedContent, extractor: DeterministicExtractor) -> str:
        """Assemble final document from extracted content in single LLM call."""
        if self.rag_retriever is not None:
            return self._assemble_with_rag(extracted, extractor)
        return self._assemble_monolithic(extracted, extractor)

    def _assemble_monolithic(self, extracted: ExtractedContent, extractor: DeterministicExtractor) -> str:
        """Original monolithic assembly path (unchanged)."""
        self.on_progress(0, 2, "Formatting extracted content...")

        formatted_content = extractor.format_for_assembly(extracted)

        self.on_progress(1, 2, "Assembling with LLM...")

        prompt = self.prompt_template.replace("{content}", formatted_content)
        if self.on_token:
            result = self.llm.query_stream(prompt, on_token=self.on_token)
        else:
            result = self.llm.query(prompt)

        if not result:
            raise RuntimeError("LLM assembly failed - no output")

        self.on_progress(2, 2, "Assembly complete")

        return result

    def _assemble_with_rag(self, extracted: ExtractedContent, extractor: DeterministicExtractor) -> str:
        """RAG-enhanced assembly: retrieves relevant rules + MMR examples."""
        self.on_progress(0, 3, "Retrieving relevant rules and examples via RAG...")

        retrieval = self.rag_retriever.retrieve_for_assembly(extracted)
        stats = retrieval.get("stats", {})
        self.on_progress(
            1, 3,
            f"RAG retrieved {stats.get('rules_retrieved', 0)} rules, "
            f"{stats.get('example_types', 0)} example types"
        )

        prompt = self._build_rag_prompt(extracted, extractor, retrieval)

        self.on_progress(2, 3, "Assembling with LLM (RAG-enhanced)...")

        if self.on_token:
            result = self.llm.query_stream(prompt, on_token=self.on_token)
        else:
            result = self.llm.query(prompt)

        if not result:
            raise RuntimeError("LLM assembly failed - no output")

        self.on_progress(3, 3, "Assembly complete (RAG)")

        return result

    def _build_rag_prompt(self, extracted: ExtractedContent, extractor: DeterministicExtractor, retrieval: dict) -> str:
        """Build a focused prompt using RAG-retrieved rules and examples."""
        template = self.prompt_template

        # Extract sections from template:
        # 1. Global directives (everything before HIGH-FAILURE SYNTAX)
        # 2. HIGH-FAILURE SYNTAX rules (replaced by RAG-selected rules)
        # 3. TOPICS section (kept as-is)
        # 4. PATTERNS section (kept as-is)
        # 5. {content} placeholder (replaced by RAG-curated content)
        # 6. VERIFIED SYNTAX EXAMPLES (replaced by RAG-selected verified examples)
        # 7. Golden style (kept as-is)

        # Separate RAG-retrieved rules by category
        syntax_rules = []
        topic_defs = []
        verified_examples = []
        pattern_defs = []
        other_rules = []

        for rule_text in retrieval.get("rules", []):
            if "WRONG:" in rule_text or "Wrong:" in rule_text or rule_text.startswith("- "):
                syntax_rules.append(rule_text)
            elif rule_text.strip().startswith("PATTERN"):
                pattern_defs.append(rule_text)
            elif re.match(r'^\d+\.', rule_text.strip()):
                topic_defs.append(rule_text)
            elif rule_text.startswith("#") or "with entry" in rule_text[:50]:
                verified_examples.append(rule_text)
            else:
                other_rules.append(rule_text)

        # Build the RAG-curated content to replace {content}
        rag_content_parts = []

        # Add extracted signatures (same as monolithic)
        rag_content_parts.append("# EXTRACTED SIGNATURES (from source docs)")
        for construct_type in ['node', 'edge', 'walker', 'obj', 'enum', 'function', 'glob']:
            if construct_type in extracted.signatures and extracted.signatures[construct_type]:
                rag_content_parts.append(f"\n## {construct_type.upper()}")
                seen = set()
                for sig in extracted.signatures[construct_type][:10]:
                    normalized = re.sub(r'\s+', ' ', sig.strip())
                    if normalized not in seen and len(normalized) > 10:
                        seen.add(normalized)
                        rag_content_parts.append(sig)

        # Add RAG-selected examples (MMR-diverse)
        rag_content_parts.append("\n\n# RAG-SELECTED EXAMPLES (MMR-diverse)")
        for construct_type, example_texts in retrieval.get("examples", {}).items():
            if example_texts:
                rag_content_parts.append(f"\n## {construct_type.upper()} EXAMPLES")
                for ex_text in example_texts:
                    rag_content_parts.append(f"```jac\n{ex_text}\n```")

        # Add keywords found
        rag_content_parts.append(
            f"\n\n# KEYWORDS FOUND: {', '.join(sorted(extracted.keywords_found))}"
        )

        # Also include extractor's syntax verification
        syntax_verification = extractor._verify_syntax_patterns()
        if syntax_verification:
            rag_content_parts.append("\n# SYNTAX VERIFICATION (from official docs)")
            for name, verified in syntax_verification.items():
                status = "OK" if verified else "NOT FOUND"
                rag_content_parts.append(f"# - {name}: {status}")

        formatted_content = "\n".join(rag_content_parts)

        # Replace {content} in template
        prompt = template.replace("{content}", formatted_content)

        return prompt


class LosslessPipeline:
    """
    Two-stage lossless pipeline:
    1. Deterministic extraction (no LLM)
    2. Single-pass LLM assembly
    """

    def __init__(self, config_path: Path):
        import yaml
        self.root = Path(__file__).parents[2]

        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.extractor = DeterministicExtractor(self.config)
        self.llm = LLM(self.config, self.config.get('assembly', {}))
        self.assembler = Assembler(self.llm, self.config)
        self.validator = Validator()

    def run(self, source_dir: Path = None, output_path: Path = None) -> dict:
        """Execute the two-stage pipeline."""

        if source_dir is None:
            source_dir = self.root / "output" / "0_sanitized"
        if output_path is None:
            output_path = self.root / "output" / "reference.txt"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        print("=" * 50)
        print("Lossless Documentation Pipeline")
        print("=" * 50)

        # Stage 1: Deterministic extraction
        print("\nStage 1: Deterministic Extraction")
        print("-" * 30)

        extracted = self.extractor.extract_from_directory(source_dir)

        print(f"  Signatures extracted: {extracted.total_signatures}")
        print(f"  Examples extracted: {extracted.total_examples}")
        print(f"  Keywords found: {len(extracted.keywords_found)}")

        # Show distribution
        print("\n  By construct type:")
        for ct, examples in sorted(extracted.examples.items(), key=lambda x: -len(x[1])):
            if examples:
                print(f"    {ct}: {len(examples)} examples")

        # Stage 2: Single-pass assembly
        print("\nStage 2: LLM Assembly (single pass)")
        print("-" * 30)

        result = self.assembler.assemble(extracted, self.extractor)

        # Save result
        output_path.write_text(result)

        # Also save to release
        release_dir = self.root.parent / "release"
        release_dir.mkdir(exist_ok=True)
        (release_dir / "jac-llmdocs.md").write_text(result)

        # Stats
        input_size = sum(f.stat().st_size for f in source_dir.glob("*.md"))
        output_size = len(result)

        print(f"\n  Input: {input_size:,} bytes ({len(list(source_dir.glob('*.md')))} files)")
        print(f"  Output: {output_size:,} bytes")
        print(f"  Compression: {input_size/output_size:.1f}x")

        # Validate
        validation = self.validator.validate_final(result)
        print(f"\n  Validation: {'PASSED' if validation.is_valid else 'FAILED'}")
        if validation.missing_patterns:
            print(f"  Missing: {validation.missing_patterns[:5]}")

        print("\n" + "=" * 50)
        print(f"Output saved to: {output_path}")
        print(f"Release candidate: {release_dir / 'jac-llmdocs.md'}")
        print("=" * 50)

        return {
            'success': True,
            'input_size': input_size,
            'output_size': output_size,
            'compression_ratio': input_size / output_size,
            'output_path': str(output_path),
            'validation': validation.is_valid
        }


def run_pipeline(config_path: str = None):
    """Entry point for lossless pipeline."""
    if config_path is None:
        config_path = Path(__file__).parents[2] / "config" / "config.yaml"
    else:
        config_path = Path(config_path)

    pipeline = LosslessPipeline(config_path)
    return pipeline.run()


if __name__ == "__main__":
    import sys
    config = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(config)
