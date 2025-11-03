# Jac Language Coding Test

## Task
Write valid Jac code for each test case below. Return responses as JSON.

## Documentation
Refer only to the documentation file that you were provided. 

## Response Format
Return JSON object mapping test IDs to code strings:

```json
{
    "basic_01": "with entry {\n    print(\"Hello, Jac!\");\n}",
    "basic_02": "glob counter: int = 0;\n\nwith entry {\n    print(:g:counter);\n}",
    "obj_01": "obj Person {\n    has name: str;\n    has age: int;\n}"
}
```
Output to "tests/test-<documentation name>.txt", documentation name being the name of the txt file that you were instructed to read. 

## Test Cases
See `test_prompts.json` for all 40 test cases with:
- `id`: Test identifier (use as JSON key)
- `task`: What to implement
- `hints`: Required elements to include
- `points`: Point value

## Important
- Write ONLY valid Jac code, no explanations
- When unsure of certain syntax, refer back to the documentation file you were provided
- Include all required elements from hints
- Use proper Jac syntax (not Python syntax)
- Escape strings properly in JSON (`\n` for newlines, `\"` for quotes)
- **NO trailing commas** - the last entry must NOT have a comma before the closing brace
- Ensure valid JSON syntax (test with a JSON validator)
- **Double-check all closing brackets/parentheses** - ensure every opening `{`, `(`, `[` has a matching closing `}`, `)`, `]`
- Output all 40 tests
