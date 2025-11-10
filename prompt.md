# Jac Language Coding Test

## Instructions
Write valid Jac code for each test case in `test_prompts.json`. Refer only to the provided documentation file.

Return a single JSON object mapping test IDs to code strings. Output the JSON to a file named "tests/test-<documentation_name>.txt", where `<documentation_name>` is the name of the documentation file you read.

**Example JSON Format:**
```json
{
    "basic_01": "with entry {\n    print(\"Hello, Jac!\");\n}",
    "obj_01": "obj Person {\n    has name: str;\n    has age: int;\n}"
}
```

**Requirements:**
- Your response must be a single, valid JSON object containing all 40 test cases.
- The code must be valid Jac syntax, not Python. Use hints provided in `test_prompts.json`.
- Do not include explanations or comments in the code.
- Ensure all strings are properly escaped (e.g., `\n`, `\"`).
- The JSON must be well-formed: no trailing commas, and all brackets/parentheses must be correctly matched.

