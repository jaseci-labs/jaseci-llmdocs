#!/usr/bin/env python3
"""CLI pipeline runner for agent invocation.

Usage:
    python generate/run_pipeline.py                  # full pipeline (fetch + extract + assemble + validate)
    python generate/run_pipeline.py --stage extract   # run single stage
    python generate/run_pipeline.py --validate-only  # validate existing candidate
    python generate/run_pipeline.py --json           # JSON summary only
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from src.sanitizer import Sanitizer
from src.markdown_extractor import MarkdownExtractor
from src.assembler import Assembler
from src.llm import LLM
from src.code_validator import Validator
from src.syntax_validator import SyntaxValidator


def load_config():
    import yaml
    with open(ROOT / "config" / "config.yaml") as f:
        return yaml.safe_load(f)


def log(msg, quiet=False):
    if not quiet:
        print(msg, flush=True)


def run_fetch(config, quiet=False):
    log("[FETCH] Starting...", quiet)
    t0 = time.time()

    src_dir = ROOT / config.get("source_dir", "docs")
    out_dir = ROOT / "output" / "0_sanitized"
    sanitizer = Sanitizer(config)

    def progress(source_id, current, total):
        log(f"[FETCH] Source {current}/{total}: {source_id}", quiet)

    stats = sanitizer.run(src_dir, out_dir, progress)
    duration = time.time() - t0

    kept = stats.get("kept_files", 0)
    excluded = stats.get("excluded_files", 0)
    log(f"[FETCH] Complete: {kept} files kept, {excluded} excluded ({duration:.1f}s)", quiet)

    return {
        "status": "complete",
        "duration": round(duration, 1),
        "files_kept": kept,
        "files_excluded": excluded,
    }


def run_extract(config, quiet=False):
    log("[EXTRACT] Starting...", quiet)
    t0 = time.time()

    sanitized_dir = ROOT / "output" / "0_sanitized"
    extractor = MarkdownExtractor(config)
    extracted = extractor.extract_from_directory(sanitized_dir)

    duration = time.time() - t0
    log(
        f"[EXTRACT] Signatures: {extracted.total_signatures}, "
        f"Examples: {extracted.total_examples}, "
        f"Keywords: {len(extracted.keywords_found)}",
        quiet,
    )
    log(f"[EXTRACT] Complete ({duration:.1f}s)", quiet)

    return extracted, extractor, {
        "status": "complete",
        "duration": round(duration, 1),
        "signatures": extracted.total_signatures,
        "examples": extracted.total_examples,
        "keywords": len(extracted.keywords_found),
    }


def ensure_rules_jsonl(quiet=False):
    """Generate rules.jsonl from rag_rules.txt if missing or stale."""
    rules_path = ROOT / "config" / "rules.jsonl"
    prompt_path = ROOT / "config" / "rag_rules.txt"

    if not prompt_path.exists():
        return rules_path

    needs_rebuild = (
        not rules_path.exists()
        or prompt_path.stat().st_mtime > rules_path.stat().st_mtime
    )

    if needs_rebuild:
        log("[RAG] Generating rules.jsonl from rag_rules.txt...", quiet)
        sys.path.insert(0, str(ROOT / "scripts"))
        from split_rules import main as split_main
        split_main()

    return rules_path


def init_rag(config, extracted, quiet=False):
    """Initialize RAG retriever with graceful fallback."""
    rag_config = config.get("rag", {})
    if not rag_config.get("enabled", True):
        log("[RAG] Disabled in config", quiet)
        return None

    try:
        from src.rag import RAGRetriever

        retriever = RAGRetriever(config)
        if not retriever.available:
            log("[RAG] Dependencies not installed, falling back to monolithic", quiet)
            return None

        rules_path = ensure_rules_jsonl(quiet)
        rules_count = retriever.ensure_rules_indexed(rules_path)
        log(f"[RAG] Rules indexed: {rules_count}", quiet)

        examples_count = retriever.index_extracted_examples(extracted)
        log(f"[RAG] Examples indexed: {examples_count}", quiet)

        return retriever

    except Exception as exc:
        log(f"[RAG] Initialization failed: {exc}, falling back to monolithic", quiet)
        return None


def fetch_jaclang_version():
    """Fetch current jaclang major.minor version from upstream."""
    import urllib.request
    try:
        url = "https://raw.githubusercontent.com/jaseci-labs/jaseci/main/jac/pyproject.toml"
        with urllib.request.urlopen(url, timeout=10) as resp:
            for line in resp.read().decode().splitlines():
                if line.startswith("version"):
                    return ".".join(line.split('"')[1].split(".")[:2])
    except Exception:
        return None


def check_version_and_archive(quiet=False):
    """Check jaclang version; archive old candidate if version changed."""
    release_dir = ROOT / "release"
    version_file = release_dir / "VERSION"
    current = version_file.read_text().strip() if version_file.exists() else ""

    upstream = fetch_jaclang_version()
    if not upstream:
        log("[VERSION] Could not fetch jaclang version, skipping check", quiet)
        return current

    log(f"[VERSION] Current: {current or '<none>'}, Upstream: {upstream}", quiet)

    if current and current != upstream:
        archive_dir = release_dir / current
        archive_dir.mkdir(parents=True, exist_ok=True)
        candidate = release_dir / "jac-llmdocs.md"
        validation = ROOT / "jac-llmdocs.validation.json"
        if candidate.exists():
            (archive_dir / "jac-llmdocs.md").write_text(candidate.read_text())
        if validation.exists():
            (archive_dir / "jac-llmdocs.validation.json").write_text(validation.read_text())
        log(f"[VERSION] Archived release/{current}/", quiet)

    version_file.write_text(upstream + "\n")
    return upstream


def run_assemble(config, extracted, extractor, quiet=False):
    log("[ASSEMBLE] Starting LLM assembly...", quiet)
    t0 = time.time()

    rag_retriever = init_rag(config, extracted, quiet)

    llm = LLM(config, config.get("assembly", {}))
    token_count = [0]

    def on_token(token):
        token_count[0] += 1
        if token_count[0] % 100 == 0 and not quiet:
            print(".", end="", flush=True)

    def on_progress(current, total, msg):
        log(f"[ASSEMBLE] {msg}", quiet)

    assembler = Assembler(llm, config, on_progress=on_progress, on_token=on_token, rag_retriever=rag_retriever)
    result = assembler.assemble(extracted, extractor)

    if token_count[0] >= 100 and not quiet:
        print(flush=True)

    output_dir = ROOT / "output" / "2_final"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "jac_reference.txt").write_text(result)

    release_dir = ROOT / "release"
    release_dir.mkdir(exist_ok=True)
    (release_dir / "jac-llmdocs.md").write_text(result)

    duration = time.time() - t0
    mode = "RAG-enhanced" if rag_retriever else "monolithic"
    log(
        f"[ASSEMBLE] Output: {len(result):,} bytes saved to release/jac-llmdocs.md ({duration:.1f}s, {mode})",
        quiet,
    )

    return result, {
        "status": "complete",
        "duration": round(duration, 1),
        "output_size": len(result),
        "tokens_streamed": token_count[0],
        "mode": mode,
    }


def run_validate(text, quiet=False):
    log("[VALIDATE] Running validation...", quiet)
    t0 = time.time()

    validator = Validator()

    final_result = validator.validate_final(text)
    patterns = validator.find_patterns(text)

    def strict_progress(current, total, msg):
        if current == total:
            log(f"[VALIDATE] Strict check progress: {current}/{total}", quiet)

    strict_result = validator.validate_strict(text, fail_on_error=False, on_progress=strict_progress)

    docs_validator = SyntaxValidator()
    syntax_verification = docs_validator.validate_syntax_in_output(text)
    incorrect_syntax = [v for v in syntax_verification if not v.matches_docs and v.found_in_output]
    all_syntax_correct = len(incorrect_syntax) == 0

    is_valid = final_result.is_valid and strict_result.failed == 0 and all_syntax_correct
    recommendation = "PASS" if (strict_result.failed == 0 and all_syntax_correct) else "REVIEW"

    duration = time.time() - t0
    log(
        f"[VALIDATE] Strict: {strict_result.passed} passed, "
        f"{strict_result.failed} failed, {strict_result.skipped} skipped",
        quiet,
    )
    log(f"[VALIDATE] Syntax: {'all correct' if all_syntax_correct else f'{len(incorrect_syntax)} incorrect'}", quiet)
    log(f"[VALIDATE] Recommendation: {recommendation} ({duration:.1f}s)", quiet)

    validation_data = {
        "is_valid": is_valid,
        "strict": {
            "total": strict_result.total_blocks,
            "passed": strict_result.passed,
            "failed": strict_result.failed,
            "skipped": strict_result.skipped,
            "pass_rate": strict_result.pass_rate,
            "errors": strict_result.errors[:10] if hasattr(strict_result, "errors") else [],
        },
        "syntax": {
            "all_correct": all_syntax_correct,
            "incorrect": [
                {"construct": v.construct, "expected": v.expected}
                for v in incorrect_syntax
            ],
        },
        "patterns": {
            "found": len(patterns),
            "total": len(validator.CRITICAL_PATTERNS),
            "missing": final_result.missing_patterns,
        },
        "recommendation": recommendation,
    }

    (ROOT / "jac-llmdocs.validation.json").write_text(json.dumps(validation_data, indent=2))

    return validation_data


def main():
    parser = argparse.ArgumentParser(description="Run the Jac docs generation pipeline")
    parser.add_argument("--stage", choices=["fetch", "extract", "assemble"], help="Run single stage")
    parser.add_argument("--validate-only", action="store_true", help="Validate existing release/jac-llmdocs.md")
    parser.add_argument("--json", action="store_true", help="Output JSON summary only")
    args = parser.parse_args()

    quiet = args.json
    summary = {"success": False, "stages": {}, "validation": None, "output_path": None}

    try:
        if args.validate_only:
            candidate = ROOT / "release" / "jac-llmdocs.md"
            if not candidate.exists():
                log("[ERROR] release/jac-llmdocs.md not found", quiet)
                summary["error"] = "release/jac-llmdocs.md not found"
                print_summary(summary)
                sys.exit(2)

            text = candidate.read_text()
            log(f"[VALIDATE] Loaded {len(text):,} bytes from release/jac-llmdocs.md", quiet)
            summary["validation"] = run_validate(text, quiet)
            summary["output_path"] = str(candidate)
            summary["success"] = summary["validation"]["recommendation"] == "PASS"
            print_summary(summary)
            sys.exit(0 if summary["success"] else 1)

        config = load_config()

        version = check_version_and_archive(quiet)
        summary["jaclang_version"] = version

        stages_to_run = ["fetch", "extract", "assemble"]
        if args.stage:
            stages_to_run = [args.stage]

        extracted = None
        extractor = None
        result_text = None

        for stage in stages_to_run:
            if stage == "fetch":
                summary["stages"]["fetch"] = run_fetch(config, quiet)

            elif stage == "extract":
                extracted, extractor, stats = run_extract(config, quiet)
                summary["stages"]["extract"] = stats

            elif stage == "assemble":
                if extracted is None:
                    extracted, extractor, stats = run_extract(config, quiet)
                    summary["stages"]["extract"] = stats
                result_text, stats = run_assemble(config, extracted, extractor, quiet)
                summary["stages"]["assemble"] = stats

        if result_text:
            summary["validation"] = run_validate(result_text, quiet)
            summary["output_path"] = "release/jac-llmdocs.md"
            summary["success"] = summary["validation"]["recommendation"] == "PASS"
        else:
            summary["success"] = True

        print_summary(summary)
        sys.exit(0 if summary.get("success") else 1)

    except KeyboardInterrupt:
        log("\n[ABORT] Interrupted by user", quiet)
        summary["error"] = "interrupted"
        print_summary(summary)
        sys.exit(2)
    except Exception as e:
        log(f"[ERROR] {e}", quiet)
        summary["error"] = str(e)
        print_summary(summary)
        sys.exit(2)


def print_summary(summary):
    print("\n---JSON_SUMMARY---")
    print(json.dumps(summary, indent=2, default=str))
    print("---END_SUMMARY---", flush=True)


if __name__ == "__main__":
    main()
