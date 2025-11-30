# Multi-Stage Document Merge

After condensing all documentation, you can merge them into a single final document using a multi-stage hierarchical merge process.

## How It Works

The merge pipeline combines documents progressively:

```
Stage 0 (Input):  88 condensed docs
     ↓ (4:1 merge ratio)
Stage 1:          22 merged docs
     ↓ (4:1 merge ratio)
Stage 2:          6 merged docs
     ↓ (4:1 merge ratio)
Stage 3:          2 merged docs
     ↓ (4:1 merge ratio)
Stage 4:          1 final doc
```

Each stage:
1. Groups files evenly based on merge ratio
2. **Processes groups in parallel** (up to `max_workers` concurrent)
3. Merges each group into single document
4. Condenses the merged content via LLM
5. Outputs to next stage directory

**High Concurrency**: With `max_workers: 16`, each merge stage processes up to 16 groups simultaneously, maximizing throughput.

## Configuration

Edit `config/config.yaml`:

```yaml
merge:
  enabled: true          # Enable multi-stage merge
  ratio: 4               # Merge ratio (4:1 means 4→1)
  max_workers: 16        # Concurrent group processing per stage
  output_dir: "./output/merged"
  preserve_structure: true  # Preserve document structure
  final_output: "jac_documentation_final.txt"
```

**Merge Ratios:**
- `ratio: 2` - Gentle merging (2→1 per stage)
- `ratio: 4` - Balanced (4→1 per stage) **[Recommended]**
- `ratio: 8` - Aggressive (8→1 per stage)

## Usage

### Step 1: Condense All Documentation

First, run the condensation pipeline:

```bash
cd scripts
python3 pipeline.py
```

This produces condensed docs in `output/condensed/`

### Step 2: Run Multi-Stage Merge

```bash
python3 merge_pipeline.py
```

Output structure:
```
output/
  merged/
    stage_1/
      stage1_group001.txt
      stage1_group002.txt
      ...
    stage_2/
      stage2_group001.txt
      ...
    stage_3/
      ...
    jac_documentation_final.txt  # Final merged doc
    merge_report_YYYYMMDD_HHMMSS.json
```

### Options

**Use custom input directory:**
```bash
python3 merge_pipeline.py --input /path/to/condensed/docs
```

**Override merge ratio:**
```bash
python3 merge_pipeline.py --ratio 8
```

**Use test config:**
```bash
python3 merge_pipeline.py --config ../config/config_test.yaml
```

## Example Output

```
================================================================================
MULTI-STAGE DOCUMENT MERGE
================================================================================

Initial files: 88
Merge ratio: 4:1
Stages planned: 4
  Stage 0 (input): 88 files
  Stage 1: 22 files
  Stage 2: 6 files
  Stage 3: 2 files
  Stage 4: 1 files

--------------------------------------------------------------------------------

Stage 1: 88 files → 22 groups (parallel workers: 16)
[Progress bar: 22/22 groups]
  Group 1/22: 4 files → 12,345 → 3,456 tokens (28.0%)
  Group 2/22: 4 files → 11,234 → 3,123 tokens (27.8%)
  Group 3/22: 4 files → 10,987 → 3,044 tokens (27.7%)
  ... (processing in parallel)

Stage 2: 22 files → 6 groups
  Processing group 1/6: 4 files → stage2_group001.txt
    Success: 13,824 → 4,123 tokens (29.8%)
  ...

Stage 3: 6 files → 2 groups
  ...

Stage 4: 2 files → 1 groups
  Processing group 1/1: 2 files → stage4_group001.txt
    Success: 8,246 → 2,891 tokens (35.1%)

================================================================================
MERGE COMPLETE: Final document at output/merged/jac_documentation_final.txt
================================================================================

Final document stats:
  Characters: 11,564
  Estimated tokens: ~2,891
  Processing time: 234.56s
```

## Complete Workflow

```bash
# 1. Condense all docs (295K → ~90K tokens)
cd scripts
python3 pipeline.py

# 2. Merge into single doc (~90K → ~3K tokens)
python3 merge_pipeline.py

# 3. Final ultra-condensed doc
cat ../output/merged/jac_documentation_final.txt
```

## Token Reduction Example

Starting from ~295K tokens of raw documentation:

1. **Condensation**: 295K → 90K tokens (70% reduction)
2. **Stage 1 merge**: 90K → 25K tokens
3. **Stage 2 merge**: 25K → 7K tokens
4. **Stage 3 merge**: 7K → 3K tokens
5. **Stage 4 merge**: 3K → 1.5K tokens (final)

**Total reduction**: 295K → 1.5K tokens (99.5% reduction)

The final document contains the most essential information from all Jac documentation in an ultra-dense format optimized for LLM context windows.

## Tips

- **Preserve structure**: Keep `preserve_structure: true` to maintain logical organization
- **Merge ratio**: Higher ratios = more aggressive, fewer stages
- **Review intermediate stages**: Check `output/merged/stage_X/` to verify quality
- **Adjust validation**: If merge fails, widen `validation.max_ratio` in config
