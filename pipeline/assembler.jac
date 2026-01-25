"""Single-pass LLM assembler for Jac documentation using by llm()."""

include:jac pipeline.extractor;
include:jac pipeline.validator;
include:jac config;

import:py from pathlib import Path;

glob llm = Anthropic(model_name="claude-opus-4-5");

"""You are assembling a comprehensive Jac language reference document.

Given the extracted signatures and examples, create a well-organized reference that:
1. Preserves ALL critical syntax patterns (++>, -->, by llm(), spawn, etc.)
2. Groups related constructs together (nodes/edges, walkers, abilities)
3. Uses dense prose format - minimize markdown, maximize information density
4. Keeps code examples focused and under 20 lines each
5. Covers ALL 50+ mandatory topics from the Jac language specification

The output should be optimized for LLM context - dense, accurate, complete.
Target output size: 20-25KB.

CRITICAL: Every pattern in the input MUST appear in the output.
Do not summarize or omit any syntax patterns.

Mandatory topics to cover:
1. Basic syntax (variables, types, expressions, control flow)
2. Data types (int, float, str, bool, list, dict, set, tuple)
3. Import systems (import:py, include:jac)
4. Archetype definitions (node, edge, walker, obj, enum)
5. Graph operations (++>, <++>, -->, spawn, visit, report)
6. Abilities (can, with entry, with exit, here, self, visitor)
7. AI integration (by llm(), Model classes, tools)
8. File I/O (file.open, json, yaml)
9. HTTP/Cloud APIs (__specs__, endpoints, async)
10. WebSocket communication
11. Scheduling and cron jobs
12. Async/await patterns
13. Permissions and access control (grant, revoke)
14. Persistence (save, commit, root graph)
15. Testing (test blocks, assertions)
16. Standard library functions"""
can assemble_reference(content: str) -> str
by llm(model=llm, temperature=0.0);

obj Assembler {
    has validator: Validator = Validator();
    has prompt_template: str = "";

    can :init: {
        prompt_path = Path("config/assembly_prompt.txt");
        if prompt_path.exists() {
            with open(prompt_path) as f {
                self.prompt_template = f.read();
            }
        }
    }

    can :async: assemble(
        extracted: ExtractedContent,
        extractor: DeterministicExtractor,
        progress_callback: object | None = None
    ) -> str {
        """Assemble final document from extracted content."""
        if progress_callback is not None {
            await progress_callback(0, 3, "Formatting extracted content...");
        }

        formatted_content = extractor.format_for_assembly(extracted);

        if progress_callback is not None {
            await progress_callback(1, 3, "Assembling with LLM (single pass)...");
        }

        result = assemble_reference(formatted_content);

        if not result {
            raise RuntimeError("LLM assembly failed - no output");
        }

        if progress_callback is not None {
            await progress_callback(2, 3, "Validating output...");
        }

        validation = self.validator.validate_final(result);
        if not validation["is_valid"] {
            print(f"Warning: Validation issues: {validation['issues']}");
            if validation["missing_patterns"] {
                print(f"Missing patterns: {validation['missing_patterns'][:5]}");
            }
        }

        if progress_callback is not None {
            await progress_callback(3, 3, "Assembly complete");
        }

        output_dir = Path("output/2_final");
        output_dir.mkdir(parents=True, exist_ok=True);
        output_path = output_dir / "reference.txt";
        output_path.write_text(result);

        release_dir = Path("release");
        release_dir.mkdir(exist_ok=True);
        (release_dir / "candidate.txt").write_text(result);

        return result;
    }
}

obj LosslessPipeline {
    """Two-stage lossless pipeline:
    1. Deterministic extraction (no LLM)
    2. Single-pass LLM assembly
    """

    has extractor: DeterministicExtractor = DeterministicExtractor();
    has assembler: Assembler = Assembler();
    has validator: Validator = Validator();

    can :async: run(
        source_dir: str | None = None,
        output_path: str | None = None
    ) -> dict {
        """Execute the two-stage pipeline."""
        if source_dir is None {
            source_dir = "output/0_sanitized";
        }
        if output_path is None {
            output_path = "output/reference.txt";
        }

        source_path = Path(source_dir);
        out_path = Path(output_path);
        out_path.parent.mkdir(parents=True, exist_ok=True);

        print("=" * 50);
        print("Lossless Documentation Pipeline");
        print("=" * 50);

        print("\nStage 1: Deterministic Extraction");
        print("-" * 30);

        extracted = self.extractor.extract_from_directory(source_path);

        print(f"  Signatures extracted: {extracted.total_signatures}");
        print(f"  Examples extracted: {extracted.total_examples}");
        print(f"  Keywords found: {len(extracted.keywords_found)}");

        print("\n  By construct type:");
        for (ct, examples) in sorted(extracted.examples.items(), key=|x| -len(x[1])) {
            if examples {
                print(f"    {ct}: {len(examples)} examples");
            }
        }

        print("\nStage 2: LLM Assembly (single pass)");
        print("-" * 30);

        result = await self.assembler.assemble(extracted, self.extractor);

        out_path.write_text(result);

        release_dir = Path("release");
        release_dir.mkdir(exist_ok=True);
        (release_dir / "candidate.txt").write_text(result);

        input_size = sum(f.stat().st_size for f in source_path.glob("*.md"));
        output_size = len(result);

        print(f"\n  Input: {input_size:,} bytes ({len(list(source_path.glob('*.md')))} files)");
        print(f"  Output: {output_size:,} bytes");
        print(f"  Compression: {input_size/output_size:.1f}x");

        validation = self.validator.validate_final(result);
        print(f"\n  Validation: {'PASSED' if validation['is_valid'] else 'FAILED'}");
        if validation["missing_patterns"] {
            print(f"  Missing: {validation['missing_patterns'][:5]}");
        }

        print("\n" + "=" * 50);
        print(f"Output saved to: {out_path}");
        print(f"Release candidate: {release_dir / 'candidate.txt'}");
        print("=" * 50);

        return {
            "success": True,
            "input_size": input_size,
            "output_size": output_size,
            "compression_ratio": input_size / output_size,
            "output_path": str(out_path),
            "validation": validation["is_valid"]
        };
    }
}
