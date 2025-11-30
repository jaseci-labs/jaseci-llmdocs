# JAC LLM Documentation Pipeline

An automated pipeline to condense Jac language documentation into ultra-dense, token-efficient formats optimized for LLM consumption during coding tasks.

## Overview

This pipeline transforms verbose, beginner-friendly documentation into concise reference material that:
- Maximizes information density
- Reduces token usage by 60-80%
- Preserves technical accuracy and code examples
- Removes pedagogical fluff and redundant explanations
- Outputs plain-text or minimal markdown

Inspired by the concept of specialized LLM-optimized documentation for popular libraries and languages.

## Features

- **Intelligent Parsing**: Extracts sections from markdown files with proper hierarchy
- **LLM-Powered Condensation**: Uses Claude to distill content while preserving technical accuracy
- **Configurable Processing**: YAML-based configuration for customization
- **Parallel Processing**: Multi-threaded execution for faster processing
- **Metrics & Validation**: Tracks compression ratios and generates detailed reports
- **Chunking Support**: Handles large files by intelligent chunking

## Installation

```bash
cd jac-llmdocs-pipeline
pip install -r requirements.txt
```

The pipeline will automatically load API keys from the project root `.env` file.

## Configuration

1. Ensure your API key is set in the project root `.env` file:
```bash
OPENROUTER_API_KEY=sk-or-v1-...
```

2. Edit `config/config.yaml` to customize:
   - Source documentation directory
   - Output directory
   - LLM model and parameters
   - Processing options (parallel, chunk size)
   - Condensation settings
   - Validation thresholds

## Usage

### Run Complete Pipeline (Recommended)

Condense all docs AND merge into single file:

```bash
cd scripts
python3 pipeline.py
```

This runs both stages:
1. **Condensation**: 295K tokens → ~90K tokens (condensed docs)
2. **Multi-stage merge**: ~90K → ~3K tokens (single final doc)

Output:
- `output/1_condensed/` - Individual condensed files
- `output/2_merged/jac_docs_final.txt` - Final ultra-condensed doc

### Stage-Specific Options

**Condensation only** (skip merge):
```bash
python3 pipeline.py --condense-only
```

**Merge only** (skip condensation, use existing condensed docs):
```bash
python3 pipeline.py --merge-only
```

### Advanced Options

```bash
# Custom config
python3 pipeline.py --config ../config/config_test.yaml

# Sequential processing (slower, lower memory)
python3 pipeline.py --sequential

# More workers (faster)
python3 pipeline.py --workers 32
```

## Pipeline Architecture

```
Input Docs → Parser → Chunker → LLM Condenser → Post-Process → Output
                                      ↓
                                  Validator
                                      ↓
                                  Metrics
```

### Components

1. **Parser** (`parser.py`): Extracts sections from markdown files
2. **Condenser** (`condenser.py`): LLM-based condensation with Claude
3. **Pipeline** (`pipeline.py`): Orchestrates the entire process

### Condensation Strategy

The pipeline uses a specialized prompt that:
- Removes analogies, motivations, and beginner hand-holding
- Strips HTML tags and excessive formatting
- Converts paragraphs to bullet points
- Consolidates redundant examples
- Preserves all code examples and technical specifications
- Uses reference manual style instead of tutorial style

## Output Structure

Condensed documentation mirrors the input structure:

```
output/
  condensed/
    learn/
      beginners_guide_to_jac.md    (condensed)
      syntax_quick_reference.md     (condensed)
    jac_book/
      chapter_1.md                  (condensed)
      ...
  metrics/
    report_20241129_194530.json     (processing metrics)
```

## Metrics

Each run generates a detailed report including:
- Total sections processed
- Original vs condensed token counts
- Compression ratio achieved
- Processing time
- Error log

Example metrics:
```json
{
  "compression": {
    "original_tokens": 250000,
    "condensed_tokens": 75000,
    "compression_ratio": 0.30,
    "reduction_percentage": 70.0
  }
}
```

## Customization

### Adjusting Condensation Prompt

Edit `config/condensation_prompt.txt` to modify the condensation instructions.

### Processing Specific Categories

In `config/config.yaml`:
```yaml
processing:
  categories: ["learn", "jac_book"]  # Only process these categories
```

### Compression Ratio Validation

Adjust validation thresholds:
```yaml
validation:
  min_ratio: 0.15  # Reject if compressed below 15%
  max_ratio: 0.5   # Reject if compressed above 50%
```

## Example Transformation

**Before (207 tokens):**
> Variables are like labeled boxes where you store information. You give it a name, and you can put different things in it. Think of it like labeling containers in your kitchen - one might be labeled 'sugar' and another 'flour'. In programming, we create variables to hold data that our program needs to remember and use later. You can change what's inside the variable anytime you want, just like you can refill those kitchen containers!

**After (8 tokens):**
> Variables store values with assigned names.

**Compression Ratio:** 3.9% (96% reduction)

## Use Cases

- Creating LLM-friendly documentation for coding assistants
- Reducing context window usage in RAG systems
- Building compact knowledge bases for agentic systems
- Generating quick reference materials from verbose docs

## LLM Provider

Uses **OpenRouter** for access to multiple models through a single API:
- Models: `google/gemini-2.5-flash`, `anthropic/claude-3.5-sonnet`, `openai/gpt-4`, etc.
- API Key: `OPENROUTER_API_KEY` in `.env`

Configure in `config/config.yaml`:
```yaml
llm:
  provider: "openrouter"
  model: "google/gemini-2.5-flash"
  api_key_env: "OPENROUTER_API_KEY"
```

## How It Works

The pipeline runs in two stages:

**Stage 1: Condensation**
- Parses all markdown files from `docs-new/`
- Processes sections in parallel with high concurrency
- Condenses each section via LLM (removes fluff, keeps technical content)
- Outputs to `output/1_condensed/`

**Stage 2: Multi-Stage Merge**
- Groups condensed files by merge ratio (default 4:1)
- **Processes groups concurrently** (default 16 workers per stage)
- Progressively merges and condenses: 88 → 22 → 6 → 2 → 1
- Each stage merges files and re-condenses via LLM
- Outputs final doc to `output/2_merged/jac_docs_final.txt`

See [MERGE.md](MERGE.md) for merge stage details.

## Roadmap

- [x] OpenRouter support with multiple models
- [x] Multi-stage hierarchical merge
- [ ] HTML documentation parsing
- [ ] PDF export
- [ ] Web interface for browsing condensed docs
- [ ] Automatic indexing and search
- [ ] MCP server for on-demand doc fetching

## License

MIT

## References

- [LLM Docs concept](https://llm-docs.com/about)
- [Optimizing Technical Documentation for LLMs](https://dev.to/joshtom/optimizing-technical-documentations-for-llms-4bcd)
