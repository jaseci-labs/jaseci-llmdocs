# Jac Documentation Pipeline - Agent Guide

## Quick Start

Activate environment first:
```bash
source ~/anaconda3/etc/profile.d/conda.sh && conda activate jac
```

### Validate existing output (no API key needed)
```bash
python generate/run_pipeline.py --validate-only
```

### Run pipeline (requires OPENROUTER_API_KEY in .env)
```bash
python generate/run_pipeline.py --skip-fetch   # reuse fetched docs
python generate/run_pipeline.py                 # full run including fetch
```

### JSON-only mode (suppress progress lines)
```bash
python generate/run_pipeline.py --validate-only --json
```

## Output Format

Progress lines print to stdout during execution. A structured JSON summary is always printed at the end between delimiters:

```
---JSON_SUMMARY---
{ ... }
---END_SUMMARY---
```

### Key fields in JSON summary

- `success` (bool): overall pass/fail
- `validation.recommendation`: `"PASS"` or `"REVIEW"`
- `validation.strict.failed`: number of code blocks that failed `jac check`
- `validation.strict.errors`: list of error details (up to 10)
- `validation.syntax.incorrect`: list of syntax patterns that don't match canonical Jac
- `validation.patterns.missing`: required patterns not found in output
- `output_path`: path to the generated candidate file

### Exit codes

- `0` = validation passed
- `1` = validation failed (check `validation` in JSON)
- `2` = pipeline error (check `error` in JSON)

## Pipeline Stages

1. **Fetch** - pulls source docs, sanitizes markdown (`--skip-fetch` to skip)
2. **Extract** - deterministic signature/example extraction (no LLM)
3. **Assemble** - single LLM call to produce final reference doc
4. **Validate** - strict `jac check` on all code blocks + syntax verification

## Files

| File | Purpose |
|------|---------|
| `run_pipeline.py` | CLI entry point |
| `config/config.yaml` | Pipeline config (model, source dirs) |
| `config/assembly_prompt.txt` | LLM prompt template |
| `src/pipeline/validator.py` | Code block validation via `jac check` |
| `src/pipeline/docs_validator.py` | Canonical syntax pattern checks |
| `release/jac-llmdocs.md` | Generated output |
| `release/jac-llmdocs.validation.json` | Validation results |

## Decision Flow

```
run --validate-only
  |
  v
recommendation == "PASS"? --> read release/jac-llmdocs.md, done
  |
  no
  v
check validation.strict.errors --> fix assembly_prompt.txt or validator
  |
  v
check validation.syntax.incorrect --> fix assembly_prompt.txt rules
  |
  v
re-run pipeline (--skip-fetch) and validate again
```
