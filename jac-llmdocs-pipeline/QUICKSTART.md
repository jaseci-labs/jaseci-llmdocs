# Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   cd jac-llmdocs-pipeline
   pip install -r requirements.txt
   ```

2. **Verify API key in project root `.env`:**
   The pipeline automatically loads from `/home/kevinjin/jaseci-llmdocs/.env`

   Check that your OpenRouter key is set:
   ```bash
   grep OPENROUTER_API_KEY ../../.env
   ```

   Should show: `OPENROUTER_API_KEY=sk-or-v1-...`

## Testing

### Test the Parser
Tests that the document parser can correctly read and section the documentation:

```bash
cd scripts
python3 test_parser.py
```

Expected output:
```
Testing DocumentParser...
================================================================================

1. Collecting markdown files...
   Found 92 markdown files

2. Parsing first file...
   ...

3. Getting statistics for all files...
   Total files: 92
   Total sections: 1936
   Total lines: 35,022
   Total chars: 1,179,372
   Estimated tokens: ~294,843
```

### Test Single File Condensation
Tests the full pipeline on one small file to verify LLM condensation works:

```bash
cd scripts
python3 test_single_file.py
```

This will:
- Parse `docs-new/learn/tool_suite.md`
- Send the first section to Claude for condensation
- Display before/after comparison and metrics

Expected output:
```
Testing Single File Condensation
================================================================================

Test file: /home/kevinjin/jaseci-llmdocs/docs-new/learn/tool_suite.md

1. Parsing file...
   Sections found: 5
   Total chars: 2,XXX
   Estimated tokens: ~XXX

2. Initializing condenser...
   Condenser initialized successfully

3. Condensing first section...
   Section: Jac Tool Suite

   SUCCESS!
   Original tokens:  ~XXX
   Condensed tokens: ~XXX
   Compression ratio: XX%
   Processing time: X.XXs

   [Shows before/after content]

   Validation: PASS
```

## Running the Complete Pipeline

### One Command - Full Pipeline

Condense AND merge into single final document:

```bash
cd scripts
python3 pipeline.py
```

This runs:
1. **Condensation**: All docs → `output/1_condensed/`
2. **Multi-stage merge**: Condensed docs → `output/2_merged/jac_docs_final.txt`

Expected output:
```
================================================================================
STAGE 1: CONDENSATION
================================================================================
Config: 16 file workers, 8 section workers per file
Parallel files: True, Parallel sections: True

Parsed 92 files:
  - 1936 sections
  - 35,022 lines
  - ~294,843 tokens

Processing files in parallel (workers=16)...
[Progress bar]

CONDENSATION REPORT
================================================================================
Sections processed: 1920 / 1936
Original tokens:  ~294,843
Condensed tokens: ~88,452
Compression ratio: 30.00%

================================================================================
STAGE 2: MERGE
================================================================================
Initial files: 92
Merge ratio: 4:1
Stages planned: 4

Stage 1: 92 files → 23 groups
Stage 2: 23 files → 6 groups
Stage 3: 6 files → 2 groups
Stage 4: 2 files → 1 groups

MERGE COMPLETE: output/2_merged/jac_docs_final.txt
Final tokens: ~2,891

================================================================================
PIPELINE COMPLETE
================================================================================
```

### Stage-Specific Runs

**Condensation only:**
```bash
python3 pipeline.py --condense-only
```

**Merge only** (requires existing condensed docs):
```bash
python3 pipeline.py --merge-only
```

### Test Run

Test with smaller dataset:
```bash
python3 pipeline.py --config ../config/config_test.yaml
```

## Output

After running the complete pipeline:

**Condensed Docs:**
- `output/1_condensed/` - Individual condensed files

**Merged Output:**
- `output/2_merged/stage_1/` - First merge stage
- `output/2_merged/stage_2/` - Second merge stage
- `output/2_merged/stage_3/` - Third merge stage
- `output/2_merged/jac_docs_final.txt` - **Final ultra-condensed doc**

**Reports:**
- `output/metrics/condensation_report_*.json` - Condensation metrics
- `output/2_merged/merge_report_*.json` - Merge metrics

**Final document** is ready to use:
```bash
cat output/2_merged/jac_docs_final.txt
```

## Customization

Edit `config/config.yaml` to:
- Change source/output directories
- Select specific categories to process
- Adjust LLM parameters (model, temperature)
- Modify compression ratio thresholds
- Enable/disable parallel processing

Edit `config/condensation_prompt.txt` to change how content is condensed.

## Troubleshooting

**"API key not found"**: Verify `OPENROUTER_API_KEY` is set in the project root `.env` file

**"No files found"**: Check that `source_dir` in config points to the correct docs directory

**High failure rate**: Adjust `validation.min_ratio` and `validation.max_ratio` in config

**Rate limits**: Reduce `processing.max_workers` or use `--sequential`

**Want to use different model?**: Edit `config/config.yaml`:
```yaml
llm:
  provider: "openrouter"
  model: "anthropic/claude-3.5-sonnet"  # Or any OpenRouter model
  api_key_env: "OPENROUTER_API_KEY"
```
