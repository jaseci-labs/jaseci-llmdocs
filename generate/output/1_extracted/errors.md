# errors


## From: jac_playground.md

### Output Panel
The bottom section displays the output of your program, including:

- Print statements and results
- Error messages and debugging information
- Program execution feedback


## From: jac_import_patterns.md

## Unsupported Patterns

| Pattern | Why Not Supported | Workaround |
|---------|-------------------|------------|
| `default` or `*` in non-`cl` imports | No Python equivalent for default/namespace exports | Use `cl import` instead |
| Side-effect only imports | Not yet implemented | Use regular Python import for now |
| Dynamic imports | Runtime feature, not syntax | Use JavaScript directly or add to roadmap |
| Import assertions (JSON, CSS) | Stage 3 proposal, specialized | May add in future |

## Usage Rules

### 2. Syntax Patterns

```jac
# ❌ Incorrect Usage
import from react { default as React }   # Error: default requires cl
import from lodash { * as _ }            # Error: namespace requires cl
cl import from lodash { * as _, map }    # Generates invalid JS
```

```jac
# ❌ Incorrect Usage - Without quotes
cl import from react-dom { render }  # Error: hyphen not allowed in identifier
```

### Validation
- `pyast_gen_pass.py`:
  - Logs error if `default` or `*` used without `cl`
  - Logs error if string literal imports used without `cl` (Python doesn't support string literal module names)


## From: chapter_6.md

```jac
# Read text file safely
def read_file(filepath: str) -> str | None {
    try {
        with open(filepath, 'r') as file {
            return file.read();
        }
    } except FileNotFoundError {
        print(f"File not found: {filepath}");
        return None;
    } except Exception as e {
        print(f"Error reading file: {e}");
        return None;
    }
}

# Write text file safely
def write_file(filepath: str, content: str) -> bool {
    try {
        with open(filepath, 'w') as file {
            file.write(content);
        }
        return True;
    } except Exception as e {
        print(f"Error writing file: {e}");
        return False;
    }
}

# Read JSON file
def read_json(filepath: str) -> dict | None {
    try {
        with open(filepath, 'r') as file {
            return json.load(file);
        }
    } except FileNotFoundError {
        print(f"JSON file not found: {filepath}");
        return None;
    } except json.JSONDecodeError {
        print(f"Invalid JSON in file: {filepath}");
        return None;
    }
}
```
```jac
impl Calculator.divide {
    if b == 0.0 {
        raise ValueError("Division by zero");
    }
    result = a / b;
    return round(result, self.precision);
}
```
Common issues include missing bytecode, syntax errors, and circular dependencies.
```jac
impl ConfigReader.load_config {
    if not os.path.exists(self.config_file) {
        print(f"Config file {self.config_file} not found, creating default");
        self.create_default_config();
        return True;
    }

    try {
        with open(self.config_file, 'r') as file {
            self.config_data = json.load(file);
        }
        print(f"Config loaded from {self.config_file}");
        return True;
    } except json.JSONDecodeError {
        print(f"Invalid JSON in {self.config_file}");
        return False;
    } except Exception as e {
        print(f"Error loading config: {e}");
        return False;
    }
}
```
```jac
impl ConfigReader.save_config {
    try {
        with open(self.config_file, 'w') as file {
            json.dump(self.config_data, file, indent=2);
        }
        print(f"Config saved to {self.config_file}");
        return True;


## From: chapter_5.md

AI applications require robust error handling and testing strategies.

### Robust AI Integration

```jac
# robust_ai.jac
import from byllm.lib { Model, Image }

glob reliable_llm = Model(model_name="gpt-4o", max_tries=3);

obj RobustCaptioner {
    has fallback_enabled: bool = True;

    """Generate caption with error handling."""
    def safe_caption(image_path: str) -> dict {
        try {
            caption = self.generate_caption_ai(image_path);
            return {
                "success": True,
                "caption": caption,
                "source": "ai"
            };
        } except Exception as e {
            if self.fallback_enabled {
                fallback_caption = f"Image analysis unavailable for {image_path}";
                return {
                    "success": False,
                    "caption": fallback_caption,
                    "source": "fallback",
                    "error": str(e)
                };
            } else {
                raise e;
            }
        }
    }

    """AI-powered caption generation."""
    def generate_caption_ai(image_path: str) -> str by reliable_llm();

    """Validate generated content."""
    def validate_caption(caption: str) -> bool {
        # Basic validation rules
        if len(caption) < 10 {
            return False;
        }
        if "error" in caption.lower() {
            return False;
        }
        return True;
    }
}

with entry {
    captioner = RobustCaptioner(fallback_enabled=True);

    # Test with different scenarios
    test_images = [
        Image("valid_photo.jpg"),
        Image("corrupted.jpg"),
        Image("missing.jpg")
    ];

    for image in test_images {
        result = captioner.safe_caption(image);

        if result["success"] {
            is_valid = captioner.validate_caption(result["caption"]);
            print(f"{image}: {result['caption']} (Valid: {is_valid})");
        } else {
            print(f"{image}: Failed - {result['error']}");
        }
    }
}
```


## From: chapter_17.md

```jac
test error_conditions {
    # Test operations without profile
    try {
        root spawn create_tweet(content="No profile tweet");
        check False;  # Should not reach here
    } except Exception {
        check True;  # Expected behavior
    }

    # Create profile for other tests
    root spawn visit_profile();
    root spawn update_profile(new_username="test_user");

    # Test self-follow prevention
    alice_profile = [root --> Profile][0];
    result = alice_profile spawn follow_request();

    # Should not create self-follow
    self_follows = [alice_profile ->:Follow:-> alice_profile];
    check len(self_follows) == 0;
}
```

```jac
walker feed_loader {
    has user_id: str;
    has loaded_tweets: list[dict] = [];
    has users_visited: set[str] = set();
    has errors: list[str] = [];

    can load_user_feed with Profile entry {
        if here.username in self.users_visited {
            self.errors.append(f"Duplicate visit to {here.username}");
            return;
        }
```

- **Error handling**: Graceful handling of edge cases and failures


## From: async_walker.md

| `error`         | Error message if execution failed                              |
```jac
        # Check for errors
        if schedule_info.error{
            print(f"Error: {schedule_info.error}");
        }
```

```jac
async walker safe_process {
    has input_id: str;
    has success: bool = False;
    has error_message: str = "";
    has results: dict = {};

    can enter with `root entry {
        try {
            # Attempt processing
            data = fetch_data(self.input_id);
            if not data{
                self.error_message = "No data found";
                return;
            }

            self.results = process_data(data);
            self.success = True;
        } except e {
            # Capture error details
            self.error_message = str(e);
            log_error(self.input_id, str(e));
        }
    }
}
```


## From: jaclang.md

- **Improvements to Runtime Error reporting**: Made various improvements to runtime error CLI reporting.
- **Parser Infinite Loop Fix**: Fixed a major parser bug that caused infinite recursion when encountering malformed tuple assignments (e.g., `with entry { a, b = 1, 2; }`), preventing the parser from hanging.
- **Better Syntax Error Messages**: Initial improvements to syntax error diagnostics, providing clearer and more descriptive messages that highlight the location and cause of errors (e.g., `Missing semicolon`).
- **TypeChecker Diagnostics**: Introduced type checking capabilities to catch errors early and improve code quality! The new type checker pass provides static analysis including:
  - **Type Annotation Validation**: Checks explicit type annotations in variable assignments for type mismatches
  - **Type Inference**: Simple type inference for assignments with validation against declared types
  - **Member Access Type Checking**: Type checking for member access patterns (e.g., `obj.field.subfield`)
  - **Import Symbol Type Checking**: Type inference for imported symbols (Basic support)
  - **Function Call Return Type Validation**: Return type checking for function calls (parameter validation not yet supported)
  - **Magic Method Support**: Type checking for special methods like `__call__`, `__add__`, `__mul__`
  - **Binary Operation Type Checking**: Operator type validation with simple custom operator support
  - **Class Instantiation**: Type checking for class constructor calls and member access
  - **Cyclic Symbol Detection**: Detection of self-referencing variable assignments
  - **Missing Import Detection**: Detection of imports from non-existent modules

  Type errors now appear in the Jac VS Code extension (VSCE) with error highlighting during editing.
- **Windows LSP Improvements**: Fixed an issue where outdated syntax and type errors persisted on Windows. Now, only current errors are displayed


## From: streamlit.md

```jac
            if num2 != 0 {
                result = num1 / num2;
            } else {
                st.error("Cannot divide by zero!");
                return;
            }
```
```jac
                } else {
                    st.error("Login failed!");
                }
```


## From: creating_byllm_plugins.md

### 1. Handle Errors Gracefully

```python
@hookimpl
def call_llm(model: Model, caller: Callable, args: dict[str | int, object]) -> object:
    try:
        return model.invoke(caller, args)
    except Exception as e:
        # Log error and provide fallback
        print(f"LLM call failed: {e}")
        return "Error: Unable to process request"
```

