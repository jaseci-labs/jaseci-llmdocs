# Jac Language LLM Benchmark - Instructions

## Overview
This benchmark tests an LLM's ability to write Jac code based on documentation. It consists of 40 test cases across 8 difficulty levels, covering all major aspects of the Jac language.

## For Human Evaluators

### Step 1: Export Test Prompts
Generate the test cases that will be given to the LLM:

```bash
python jac_llm_benchmark.py export test_prompts.json
```

This creates `test_prompts.json` containing all 40 test cases with:
- Task descriptions
- Difficulty levels (1-8)
- Point values (5-40 points per test)
- Hints about required syntax elements

### Step 2: Provide Documentation to LLM
Give the LLM access to the Jac documentation. You can use:
- `jaseci-complete.txt` (condensed reference)
- Original docs in the `/docs` folder
- Or both for comprehensive coverage

### Step 3: Run the Benchmark
Present the test prompts to the LLM with these instructions:

```
You will be tested on your ability to write Jac code.

Here is the Jac language documentation:
[Paste jaseci-complete.txt or provide file]

Here are the test cases:
[Paste test_prompts.json]

For each test case, write ONLY valid Jac code that solves the task.
Return your responses as a JSON object where:
- Keys are test IDs (e.g., "basic_01", "walker_03")
- Values are Jac code as strings

IMPORTANT:
- Write ONLY code, no explanations
- Follow Jac syntax (semicolons, braces, type annotations)
- Make sure code is complete and syntactically correct
- Pay attention to hints for required elements
```

### Step 4: Collect LLM Responses
Save the LLM's JSON response to a file, e.g., `llm_responses.json`

Example format:
```json
{
    "basic_01": "with entry {\n    print(\"Hello, Jac!\");\n}",
    "basic_02": "glob counter: int = 0;\n\nwith entry {\n    print(:g:counter);\n}",
    "obj_01": "obj Person {\n    has name: str;\n    has age: int;\n}"
}
```

### Step 5: Evaluate Results
Run the evaluation script:

```bash
python jac_llm_benchmark.py evaluate llm_responses.json report.txt
```

This will:
- Check each code snippet for required/forbidden elements
- Perform basic syntax validation
- Calculate scores per test, category, and difficulty level
- Generate a detailed report

### Step 6: Review Results
The evaluation produces:
1. **report.txt** - Human-readable detailed report
2. **llm_responses_results.json** - Machine-readable results with full details

## Scoring System

### Point Distribution
- **Level 1** (Basic Syntax): 5 points per test × 5 tests = 25 points
- **Level 2** (Objects): 10 points per test × 5 tests = 50 points
- **Level 3** (Graph Basics): 15 points per test × 5 tests = 75 points
- **Level 4** (Walkers): 20 points per test × 5 tests = 100 points
- **Level 5** (Advanced Graph): 25 points per test × 5 tests = 125 points
- **Level 6** (AI Integration): 30 points per test × 5 tests = 150 points
- **Level 7** (Cloud): 35 points per test × 5 tests = 175 points
- **Level 8** (Integration): 40 points per test × 5 tests = 200 points

**Total Possible: 900 points**

### Evaluation Criteria
Each test is scored based on:

1. **Required Elements** (main score)
   - Each test specifies required syntax elements
   - Score = (elements_found / total_required) × max_points
   - Example: If 4 out of 5 required elements found → 80% of points

2. **Forbidden Elements** (penalty)
   - Some tests prohibit certain approaches
   - Penalty = (forbidden_found / total_forbidden) × 30% of max_points

3. **Syntax Checks** (feedback only)
   - Missing semicolons
   - Missing type annotations
   - Mismatched braces
   - These provide feedback but don't directly affect score

### Performance Grades
- **90-100%** (810-900 pts): Excellent - Strong understanding of Jac
- **80-89%** (720-809 pts): Good - Solid grasp with minor gaps
- **70-79%** (630-719 pts): Fair - Understands basics, struggles with advanced
- **60-69%** (540-629 pts): Passing - Basic competency, needs improvement
- **Below 60%** (<540 pts): Needs Work - Significant gaps in understanding

## Test Categories

### 1. Basic Syntax (25 points)
- Entry points
- Variables and types
- Enums
- Functions
- Loops

### 2. Objects (50 points)
- Class declaration
- Methods and attributes
- Inheritance
- Lifecycle methods
- Lambda functions

### 3. Graph Basics (75 points)
- Node declaration
- Edge connections
- Custom edges
- Node abilities
- Context references

### 4. Walkers (100 points)
- Walker declaration
- Visit patterns
- Type filtering
- Walker abilities
- Report statements

### 5. Advanced Graph (125 points)
- Attribute filtering
- Edge type filtering
- Multi-hop traversal
- Walker control flow
- Edge abilities

### 6. AI Integration (150 points)
- Module imports
- Model initialization
- AI functions
- Semantic programming
- Type constraints

### 7. Cloud Deployment (175 points)
- Walker specs
- Authentication config
- Custom endpoints
- Query parameters
- Private walkers

### 8. Integration & Patterns (200 points)
- Complete graph applications
- State machines
- Error handling
- Async operations
- CRUD patterns

## Example Workflow

```bash
# 1. Export test cases
python jac_llm_benchmark.py export test_prompts.json

# 2. Present to LLM with documentation
# [Give LLM the jaseci-complete.txt + test_prompts.json]

# 3. Save LLM responses to file
# [Save as llm_responses.json]

# 4. Evaluate
python jac_llm_benchmark.py evaluate llm_responses.json gpt4_report.txt

# 5. Review results
cat gpt4_report.txt
```

## Comparing Multiple LLMs

To compare different LLMs:

1. Run each LLM through the benchmark separately
2. Save responses with descriptive names:
   - `gpt4_responses.json`
   - `claude_responses.json`
   - `llama_responses.json`
3. Generate reports for each:
   ```bash
   python jac_llm_benchmark.py evaluate gpt4_responses.json gpt4_report.txt
   python jac_llm_benchmark.py evaluate claude_responses.json claude_report.txt
   python jac_llm_benchmark.py evaluate llama_responses.json llama_report.txt
   ```
4. Compare overall percentages and category breakdowns

## Tips for Best Results

### For LLM Prompting:
1. **Provide complete documentation** - Use jaseci-complete.txt
2. **Be clear about format** - Emphasize JSON response structure
3. **Remind about syntax** - Mention semicolons, braces, type annotations
4. **One test at a time** (optional) - For better focus, ask LLM to solve tests sequentially
5. **Allow self-correction** - Let LLM review its own code before submitting

### For Evaluation:
1. **Check JSON validity** - Ensure response file is valid JSON
2. **Review edge cases** - Some tests may have multiple valid solutions
3. **Manual review** - For borderline cases, manually check if code would work
4. **Track improvements** - Run benchmark multiple times with different prompts

## Interpreting Results

### High Scores in Basic Categories, Low in Advanced
- LLM understands syntax but struggles with unique Jac concepts (OSP, walkers)
- May need more examples of graph programming patterns

### High Variance Across Categories
- Inconsistent documentation absorption
- May indicate certain topics explained better than others

### Consistent Syntax Errors
- Missing semicolons/braces suggests format confusion
- May need explicit reminders about Jac vs Python syntax differences

### Perfect Scores in AI/Cloud, Low in Graph
- LLM may be interpolating from similar frameworks
- Actual Jac-specific features not well understood

## Customization

### Adding New Tests
Edit `jac_llm_benchmark.py` and add to the `load_test_cases()` method:

```python
{
    "id": "custom_01",
    "level": 5,
    "category": "Custom Category",
    "task": "Your task description",
    "required_elements": ["element1", "element2"],
    "forbidden_elements": ["badpattern"],
    "points": 25,
    "hints": ["Hint 1", "Hint 2"]
}
```

### Adjusting Scoring
Modify the `evaluate_code()` method to change:
- Required element weighting
- Forbidden element penalty
- Syntax check strictness

### Custom Validators
Add specific validation functions for complex tests:

```python
def validate_walker_traversal(code):
    # Custom logic to check walker behavior
    return score, feedback
```

## Troubleshooting

### "Responses file not found"
- Ensure JSON file path is correct
- Check file was saved properly from LLM output

### "Invalid JSON" errors
- Validate JSON format: `python -m json.tool llm_responses.json`
- Check for proper escaping of newlines and quotes in code strings

### Low scores despite correct-looking code
- Check if required elements are exact matches
- Review hints - some tests need specific syntax (e.g., `?Type not just Type`)
- Verify code has proper Jac syntax (semicolons, braces)

### Tests skipped in results
- Ensure test ID in responses matches exactly (case-sensitive)
- Check that all 40 tests have responses in JSON

## License & Attribution
This benchmark is designed for evaluating LLM performance on the Jac programming language.
Feel free to modify and extend for your specific needs.

## Contact & Contributions
For issues, improvements, or questions about the benchmark, please refer to the main Jaseci documentation.
