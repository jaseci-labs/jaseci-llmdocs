# Jac LLM Benchmark - Quick Start Guide

This guide will walk you through running the Jac Language LLM Benchmark in 5 minutes.

## What This Does

Tests how well an LLM can write Jac code by:
- 40 coding tasks across 8 difficulty levels
- Automatic evaluation of syntax and required elements
- Detailed scoring report by category and level
- **Total possible: 900 points**

## Prerequisites

- Python 3.7+
- The benchmark script: `jac_llm_benchmark.py`
- Jac documentation: `jaseci-complete.txt`

## Quick Start (3 Steps)

### Step 1: Export Test Cases (5 seconds)

```bash
python jac_llm_benchmark.py export test_prompts.json
```

**Output:** Creates `test_prompts.json` with 40 test cases

You'll see:
```
Test prompts exported to test_prompts.json
Total tests: 40
Total possible points: 900
```

### Step 2: Get LLM to Write Code (manual)

**Prompt Template for LLM:**

```
I need you to write Jac code for a benchmark test.

DOCUMENTATION:
[Paste contents of jaseci-complete.txt here]

TEST CASES:
[Paste contents of test_prompts.json here]

INSTRUCTIONS:
- For each test in the "tests" array, write valid Jac code that solves the task
- Return ONLY a JSON object where keys are test IDs and values are code strings
- Follow all Jac syntax rules: semicolons, braces, type annotations
- Pay attention to hints for required elements
- Do NOT include explanations, ONLY the JSON response

RESPONSE FORMAT:
{
    "basic_01": "with entry {\n    print(\"Hello, Jac!\");\n}",
    "basic_02": "glob counter: int = 0;\n\nwith entry {\n    print(:g:counter);\n}",
    ...
}
```

**Save the LLM's JSON response** to a file like `gpt4_responses.json`

### Step 3: Evaluate & Get Report (5 seconds)

```bash
python jac_llm_benchmark.py evaluate gpt4_responses.json gpt4_report.txt
```

**Output:**
- `gpt4_report.txt` - Human-readable detailed report
- `gpt4_responses_results.json` - Machine-readable results

## Understanding the Report

### Summary Section
```
OVERALL SUMMARY
--------------------------------------------------------------------------------
Total Score:      750.5/900 (83.39%)
Tests Completed:  40/40
```

**Grading Scale:**
- 90-100% = Excellent
- 80-89% = Good
- 70-79% = Fair
- 60-69% = Passing
- <60% = Needs Work

### Category Breakdown
```
CATEGORY BREAKDOWN
--------------------------------------------------------------------------------
Basic Syntax          25.00/25  (100.0%) [5 tests]
Objects               48.50/50  (97.0%)  [5 tests]
Graph Basics          67.50/75  (90.0%)  [5 tests]
Walkers               85.00/100 (85.0%)  [5 tests]
...
```

Shows performance in each topic area.

### Difficulty Level Breakdown
```
DIFFICULTY LEVEL BREAKDOWN
--------------------------------------------------------------------------------
Level 1          25.00/25  (100.0%) [5 tests]
Level 2          48.50/50  (97.0%)  [5 tests]
Level 3          67.50/75  (90.0%)  [5 tests]
...
Level 8         140.00/200 (70.0%)  [5 tests]
```

Shows how the LLM handles increasing complexity.

### Detailed Results
Each test shows:
- Score and percentage
- Which required elements were found/missing
- Syntax feedback and warnings
- The actual code generated

## Test an Example (Try It Now!)

I've included `example_responses.json` with sample answers. Test it:

```bash
python jac_llm_benchmark.py evaluate example_responses.json example_report.txt
cat example_report.txt
```

This shows you what a complete evaluation looks like.

## Comparing Multiple LLMs

Test different models and compare:

```bash
# GPT-4
python jac_llm_benchmark.py evaluate gpt4_responses.json gpt4_report.txt

# Claude
python jac_llm_benchmark.py evaluate claude_responses.json claude_report.txt

# Llama
python jac_llm_benchmark.py evaluate llama_responses.json llama_report.txt

# Compare scores
grep "overall_percentage" *_results.json
```

## Test Categories & Point Values

| Level | Category | Points/Test | Total | Topics |
|-------|----------|-------------|-------|--------|
| 1 | Basic Syntax | 5 | 25 | Entry points, variables, functions |
| 2 | Objects | 10 | 50 | Classes, methods, inheritance |
| 3 | Graph Basics | 15 | 75 | Nodes, edges, connections |
| 4 | Walkers | 20 | 100 | Traversal, abilities, visit patterns |
| 5 | Advanced Graph | 25 | 125 | Filtering, multi-hop, edge abilities |
| 6 | AI Integration | 30 | 150 | ByLLM, semantic programming |
| 7 | Cloud | 35 | 175 | API specs, authentication |
| 8 | Integration | 40 | 200 | Complete apps, patterns |
| **TOTAL** | | | **900** | |

## Common Issues & Solutions

### Issue: "Responses file not found"
**Solution:** Check file path and ensure JSON was saved correctly

### Issue: Invalid JSON error
**Solution:** Validate JSON format:
```bash
python -m json.tool llm_responses.json
```

### Issue: Low scores despite good-looking code
**Solution:**
- Check if all required elements are present (exact matches)
- Verify Jac-specific syntax (not Python): semicolons, `glob`, `has`, etc.
- Review hints in test_prompts.json for specific requirements

### Issue: Test IDs don't match
**Solution:** Ensure test IDs in response JSON exactly match those in test_prompts.json (case-sensitive)

## Interpreting Results

### High basic scores, low advanced scores
→ LLM understands syntax but not Jac-specific concepts (OSP, walkers)

### Missing semicolons/braces consistently
→ LLM treating Jac like Python, needs syntax reminder

### Perfect on AI/Cloud, poor on Graph
→ LLM may be guessing from similar frameworks, not understanding unique Jac features

### Uneven category scores
→ Documentation may explain some topics better than others

## Advanced Usage

### Customize Tests
Edit `jac_llm_benchmark.py` in the `load_test_cases()` method to add your own tests.

### Adjust Scoring
Modify weights in the `evaluate_code()` method.

### Extract Specific Categories
Filter `test_prompts.json` to test only certain categories:
```python
import json
with open('test_prompts.json') as f:
    data = json.load(f)
    walker_tests = [t for t in data['tests'] if t['category'] == 'Walkers']
```

## Files Overview

```
jac_llm_benchmark.py           # Main benchmark script
jaseci-complete.txt            # Condensed Jac documentation
test_prompts.json              # Generated test cases (export)
example_responses.json         # Example LLM responses
LLM_BENCHMARK_INSTRUCTIONS.md  # Detailed instructions
BENCHMARK_QUICKSTART.md        # This file
```

## Example Session

```bash
# Terminal session
$ python jac_llm_benchmark.py export test_prompts.json
Test prompts exported to test_prompts.json
Total tests: 40
Total possible points: 900

# [Manually: Get LLM responses, save to llm_responses.json]

$ python jac_llm_benchmark.py evaluate llm_responses.json report.txt
Running benchmark on llm_responses.json...
Report saved to report.txt
Detailed JSON results saved to llm_responses_results.json

$ head -20 report.txt
================================================================================
JAC LANGUAGE LLM BENCHMARK REPORT
================================================================================

OVERALL SUMMARY
--------------------------------------------------------------------------------
Total Score:      756.25/900 (84.03%)
Tests Completed:  40/40
...
```

## Tips for Best Results

1. **Use complete documentation** - Provide jaseci-complete.txt
2. **Be explicit about format** - Emphasize JSON structure in prompt
3. **Remind about syntax** - Jac uses semicolons and braces unlike Python
4. **Test iteratively** - Run benchmark, review failures, adjust prompt
5. **Multiple attempts** - Try different prompting strategies

## Next Steps

- Review the full instructions: `LLM_BENCHMARK_INSTRUCTIONS.md`
- Customize tests for your specific needs
- Compare different LLMs and prompting strategies
- Share results with the community!

## Help & Support

For detailed documentation on:
- Test case structure
- Scoring methodology
- Customization options
- Troubleshooting

See: `LLM_BENCHMARK_INSTRUCTIONS.md`

---

**Ready to benchmark?** Run the 3 steps above and see how well your LLM knows Jac! 🚀
