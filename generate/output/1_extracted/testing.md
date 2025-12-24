# testing


## From: contrib.md

Run tests locally using the test script above

This is how we run our tests.

```bash
--8<-- "scripts/tests.sh"
```


## From: keywords.md

| Keyword | Description |
| --- | --- |
|[`test`](https://www.jac-lang.org/learn/jac_ref/#test-implementations)|Defines test cases for code validation and unit testing. |


## From: library_mode.md

| Function | Description | Parameters |
|----------|-------------|------------|
| `jac_test(func)` | Mark function as test | `func`: Test function |
| `run_test(filepath, ...)` | Run test suite | `filepath`: Test file<br>`func_name`, `filter`, `xit`, `maxfail`, `directory`, `verbose`: test options |
| `report(expr, custom)` | Report value from walker | `expr`: Value to report<br>`custom`: custom report flag |
| `printgraph(node, depth, traverse, edge_type, bfs, edge_limit, node_limit, file, format)` | Generate graph visualization | `node`: Start node<br>`depth`: Max depth<br>`traverse`: traversal flag<br>`edge_type`: filter edges<br>`bfs`: breadth-first flag<br>`edge_limit`, `node_limit`: limits<br>`file`: output path<br>`format`: 'dot' or 'mermaid' |


## From: jac_import_patterns.md

## Testing

All patterns tested and verified in:
- `test_js_generation.py::test_category1_named_imports_generate_correct_js`
- `test_js_generation.py::test_category2_default_imports_generate_correct_js`
- `test_category4_namespace_imports_generate_correct_js`
- `test_js_generation.py::test_hyphenated_package_imports_generate_correct_js`
- `test_pyast_gen_pass.py::test_string_literal_import_requires_cl`
- `test_pyast_gen_pass.py::test_string_literal_import_works_with_cl`


## From: jsx_client_serv_design.md

Test Suite | Location | Coverage
|------------|----------|----------|
| **Client codegen tests** | [test_client_codegen.py](../jaclang/compiler/tests/test_client_codegen.py) | `cl` keyword detection, manifest generation |
| **ESTree generation tests** | [test_esast_gen_pass.py](../jaclang/compiler/passes/ecmascript/tests/test_esast_gen_pass.py) | JavaScript AST generation |
| **JavaScript generation tests** | [test_js_generation.py](../jaclang/compiler/passes/ecmascript/tests/test_js_generation.py) | JS code output from ESTree |
| **Client bundle tests** | [test_client_bundle.py](../jaclang/runtimelib/tests/test_client_bundle.py) | Bundle building, caching, import resolution |
| **Server endpoint tests** | [test_serve.py](../jaclang/runtimelib/tests/test_serve.py) | HTTP endpoints, page rendering |
| **JSX rendering tests** | [test_jsx_render.py](../jaclang/runtimelib/tests/test_jsx_render.py) | JSX parsing and rendering |
| **Reactive signals tests** | [test_reactive_signals.py](../jaclang/runtimelib/tests/test_reactive_signals.py) | Signal creation, effects, dependency tracking |
| **Router tests** | [test_router.py](../jaclang/runtimelib/tests/test_router.py) | Routing, navigation, route guards |
| **Closures tests** | [test_closures.py](../jaclang/runtimelib/tests/test_closures.py) | Nested functions, closure semantics in JavaScript |

### Example Test Fixtures

- [client_jsx.jac](../jaclang/compiler/passes/ecmascript/tests/fixtures/client_jsx.jac) - Comprehensive client syntax examples
- [jsx_elements.jac](../examples/reference/jsx_elements.jac) - JSX feature demonstrations
- [test_reactive_signals.jac](../jaclang/runtimelib/tests/fixtures/test_


## From: chapter_18.md

```bash
# Test as service locally
jac serve weather_api.jac --port 8000

# Test the endpoints
curl -X POST http://localhost:8000/walker/get_weather \
  -H "Content-Type: application/json" \
  -d '{"city": "New York"}'
```
```bash
# Test locally
docker run -p 8000:8000 \
  -e WEATHER_API_KEY=your-key \
  -e DEBUG=true \
  weather-api:latest

# Test with docker-compose
echo "WEATHER_API_KEY=your-key" > .env
docker-compose up -d

# View logs
docker-compose logs -f weather-api

# Test the containerized API
curl -X POST http://localhost:8000/walker/get_weather \
  -H "Content-Type: application/json" \
  -d '{"city": "London"}'

# Check health
curl -X POST http://localhost:8000/walker/health_check \
  -H "Content-Type: application/json" \
  -d '{}'
```
```bash
# Test the service
kubectl port-forward service/weather-api-service 8080:80 -n weather-app

# Test from another terminal
curl -X POST http://localhost:8080/walker/get_weather \
  -H "Content-Type: application/json" \
  -d '{"city": "Tokyo"}'
```
```bash
# Load testing (using hey or similar)
hey -n 1000 -c 10 -m POST \
  -H "Content-Type: application/json" \
  -d '{"city":"London"}' \
  http://your-service-url/walker/get_weather
```
- Test locally first: Verify your JAC application works before deploying to the cloud


## From: chapter_20.md

### Testing the Migration

!!! example "Migration Testing"
    === "Python Usage"
        ```python
        # test_book.py
        book = Book("The Great Gatsby", "F. Scott Fitzgerald", "123456789")
        print(book.get_info())  # The Great Gatsby by F. Scott Fitzgerald - Available

        success = book.borrow()
        print(f"Borrowed: {success}")  # Borrowed: True
        print(book.get_info())  # The Great Gatsby by F. Scott Fitzgerald - Borrowed
        ```

    === "Jac Usage"
        ```jac
        # test_book.jac
        with entry {
            book = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="123456789");
            print(book.get_info());  # The Great Gatsby by F. Scott Fitzgerald - Available

            success = book.borrow();
            print(f"Borrowed: {success}");  # Borrowed: True
            print(book.get_info());  # The Great Gatsby by F. Scott Fitzgerald - Borrowed
        }
        ```

!!! tip "Successful Migration Steps"
    1. **Start Small**: Begin with utility functions and simple classes
    2. **Embrace Types**: Use Jac's type system for better code quality
    3. **Think Spatially**: Convert relationships to nodes and edges
    4. **Test Incrementally**: Validate each migration step
    5. **Leverage Python**: Keep using Python libraries where beneficial
    6. **Document Changes**: Track migration decisions and patterns

## Best Practices

!!! summary "Migration Best Practices"
    - **Start small**: Begin with isolated components rather than entire applications
    - **Maintain compatibility**: Keep existing Python code running during migration
    - **Test thoroughly**: Validate each migration step with comprehensive tests
    - **Document changes**: Track migration decisions and patterns for team consistency
    - **Train the team**: Ensure all developers understand Object-Spatial Programming concepts
    - **Plan rollback**: Have strategies for reverting changes if issues arise

## Key Takeaways

!!! summary "What We've Learned"
    **Common Challenges:**

    - **Paradigm shift**: Moving from object-oriented to spatial thinking
    - **Team adoption**: Training developers on new concepts and patterns
    - **Integration complexity**: Managing hybrid Python-Jac applications
    - **Testing changes**: Ensuring equivalent behavior after migration

    **Success Factors:**

    - **Clear planning**: Structured approach to migration with defined milestones
    - **Comprehensive testing**: Validation at every step of the migration process
    - **Team alignment**: Consistent understanding of goals and benefits
    - **Iterative improvement**: Continuous refinement of migration patterns

!!! tip "Try It Yourself"
    Practice migration by:
    - Converting a simple Python class to a Jac object
    - Transforming list-based relationships into graph structures
    - Creating hybrid applications that use both Python libraries and Jac features
    - Building comprehensive test suites to validate migration correctness

    Remember: Successful migration is about embracing spatial thinking, not just syntax conversion!


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


## From: chapter_19.md

### Creating Test Data

!!! example "Performance Test Setup"
    ```jac
    # test_data_generator.jac
    import from random { randint, choice }

    walker generate_test_network {
        has person_count: int = 100;
        has avg_friends: int = 5;

        can create_test_network with `root entry {
            # Clear existing test data
            existing_persons = [-->](`?LightPerson);
            existing_friends = [-->](`?Friend);

            for person in existing_persons {
                del person;
            }
            for friendship in existing_friends {
                del friendship;
            }

            # Create people
            people = [];
            for i in range(self.person_count) {
                person = LightPerson(
                    name=f"Person{i}",
                    age=randint(18, 65)
                );
                here ++> person;
                people.append(person);
            }

            # Create friendships
            total_friendships = 0;
            for person in people {
                friends_to_add = randint(1, self.avg_friends * 2);

                for _ in range(friends_to_add) {
                    potential_friend = choice(people);
                    if potential_friend != person {
                        # Check if friendship already exists
                        existing = [person --> Friend --> LightPerson](?name == potential_friend.name);
                        if not existing {
                            friendship = Friend(since="2024-01-15");
                            person ++> friendship ++> potential_friend;
                            total_friendships += 1;
                        }
                    }
                }
            }

            report {
                "people_created": len(people),
                "friendships_created": total_friendships,
                "avg_friends_per_person": round(total_friendships * 2 / len(people), 2)
            };
        }
    }
    ```

### Testing Performance

```bash
# Deploy the optimized version
jac serve distributed_friends.jac

# Generate test data
curl -X POST http://localhost:8000/walker/generate_test_network \
  -H "Content-Type: application/json" \
  -d '{"person_count": 1000, "avg_friends": 10}'

# Run performance benchmarks
curl -X POST http://localhost:8000/walker/run_performance_suite \
  -H "Content-Type: application/json" \
  -d '{"test_count": 5, "test_persons": ["Person1", "Person50", "Person100"]}'

# Check system health
curl -X POST http://localhost:8000/walker/performance_health_check \
  -H "Content-Type: application/json" \
  -d '{}'
```


## From: chapter_15.md

```bash
# Join a room first
curl -X POST http://localhost:8000/walker/join_room \
  -H "Content-Type: application/json" \
  -d '{"room_name": "general", "username": "alice"}'

# Send a message
curl -X POST http://localhost:8000/walker/send_message \
  -H "Content-Type: application/json" \
  -d '{"room_name": "general", "username": "alice", "message": "Hello everyone!"}'

# Get chat history
curl -X POST http://localhost:8000/walker/get_chat_history \
  -H "Content-Type: application/json" \
  -d '{"room_name": "general", "limit": 10}'
```

```bash
curl -X POST http://localhost:8000/walker/receive_webhook \
  -H "Content-Type: application/json" \
  -d '{
    "source": "github",
    "event_type": "push",
    "data": {
      "repository": {"name": "my-repo"},
      "commits": [{"message": "Fix critical bug"}]
    }
  }'
```

```bash
# Run cleanup manually
curl -X POST http://localhost:8000/walker/cleanup_inactive_rooms \
  -H "Content-Type: application/json" \
  -d '{"max_age_hours": 48}'

# Generate daily stats
curl -X POST http://localhost:8000/walker/generate_daily_stats \
  -H "Content-Type: application/json" \
  -d '{}'
```


## From: env_vars.md

### Testing

```bash
# Configuration for testing
export DATABASE_NAME="test_db"
export LOGGER_LEVEL="debug"
export TOKEN_TIMEOUT="1"  # Short-lived tokens for testing
export REQUIRE_AUTH_BY_DEFAULT="false"  # Disable auth for easier testing
```


## From: chapter_17.md

Jac provides a powerful testing framework that automatically discovers and runs tests. When you run `jac test myfile.jac`, it automatically looks for `myfile.test.jac` and executes all test blocks within it.

- **Automatic Discovery**: `.test.jac` files are automatically found and executed
- **Graph-Aware Testing**: Native support for testing spatial relationships
- **Walker Testing**: Test mobile computation patterns naturally
- **Type-Safe Assertions**: Leverage Jac's type system in test validation
- **Zero Configuration**: No external testing frameworks required

```jac


## From: chapter_13.md

```bash
# First request - Create counter
curl -X POST http://localhost:8000/walker/get_counter \
  -H "Content-Type: application/json" \
  -d '{}'
# Response: {"returns": [{"value": 0, "status": "created"}]}

# Increment the counter
curl -X POST http://localhost:8000/walker/increment_counter \
  -H "Content-Type: application/json" \
  -d '{}'
# Response: {"returns": [{"value": 1, "previous": 0}]}

# Increment again
curl -X POST http://localhost:8000/walker/increment_counter \
  -H "Content-Type: application/json" \
  -d '{}'
# Response: {"returns": [{"value": 2, "previous": 1}]}

# Check counter value
curl -X POST http://localhost:8000/walker/get_counter \
  -H "Content-Type: application/json" \
  -d '{}'
# Response: {"returns": [{"value": 2, "status": "existing"}]}

# Restart the service (Ctrl+C, then jac serve main.jac again)

# Counter value persists after restart
curl -X POST http://localhost:8000/walker/


## From: breaking_changes.md

#### 1. `check` Keyword Removed - Use `assert` in Test Blocks

The `check` keyword has been removed from Jaclang. All testing functionality is now unified under `assert` statements, which behave differently depending on context: raising exceptions in regular code and reporting test failures within `test` blocks.

**Before**

```jac
glob a: int = 5;
glob b: int = 2;

test test_equality {
    check a == 5;


## From: chapter_14.md

Deploy your user-aware application:

```bash
jac serve user_notebook.jac
```

### Testing User Authentication

```bash
# Create a note for Alice
curl -X POST http://localhost:8000/walker/create_note \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Alice Private Note",
    "content": "Secret content",
    "owner": "alice@example.com"
  }'

# Create a note for Bob
curl -X POST http://localhost:8000/walker/create_note \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bob Note",
    "content": "Bob content",
    "owner": "bob@example.com"
  }'

# Get Alice's notes only
curl -X POST http://localhost:8000/walker/list_my_notes \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice@example.com"}'
```
### Testing Note Sharing

```bash
# Alice creates a note
curl -X POST http://localhost:8000/walker/create_note \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Project",
    "content": "Project details",
    "owner": "alice@example.com"
  }'

# Alice shares note with Bob
curl -X POST http://localhost:8000/walker/share_note \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": "note_123",
    "current_user": "alice@example.com",
    "target_user": "bob@example.com"
  }'

# Bob views accessible notes
curl -X POST http://localhost:8000/walker/get_accessible_notes \
  -H "Content-Type: application/json" \
  -d '{"user_id": "bob@example.com"}'
```
### Testing Role-Based Access

```bash
# Check user role
curl -X POST http://localhost:8000/walker/check_user_role \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice@example.com"}'

# Create a note requiring editor role
curl -X POST http://localhost:8000/walker/create_role_based_note \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Editor Note",
    "content": "Only editors can see this",
    "owner": "alice@example.com",
    "required_role": "editor",
    "is_sensitive": true
  }'

# Get notes filtered by role
curl -X POST http://localhost:8000/walker/get_role_filtered_notes \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice@example.com"}'
```


## From: jaclang.md

- **Check Statements Removed**: The `check` keyword has been removed from Jaclang. All testing functionality previously provided by `check` statements is now handled by `assert` statements within test blocks. Assert statements now behave differently depending on context: in regular code they raise `AssertionError` exceptions, while within `test` blocks they integrate with Jac's testing framework to report test failures. This unification simplifies the language by using a single construct for both validation and testing purposes.


## From: cli.md

The `test` command is utilized to run the test suite in the specified .jac file.
```bash
jac test <file_path>
```
Parameters to execute the test command:
- `file_path`: The path to the .jac file.


## From: tutorial.md

#### littleX.test.jac - Proving It Works
```jac
# Test functionality
test create_tweet {
    root spawn create_tweet(content = "Hello World");
    tweet = [root --> (?Profile) --> (?Tweet)][0];
    check tweet.content == "Hello World";
}
```
### Running Your Code
Jaseci automatically links these files:

```bash
# Run tests
jac test littleX.jac
```


## From: creating_byllm_plugins.md

### Step 4: Install and Test Your Plugin

1. Install the plugin in development mode:
   ```bash
   pip install -e .
   ```

2. Create a test Jaclang file to verify plugin functionality:
   ```jaclang
   import:py from byllm, Model;

   glob llm = Model(model_name="gpt-3.5-turbo");

   can test_plugin {
       result = get_answer("What is 2+2?") by llm();
       print(result);
   }

   can get_answer(question: str) -> str by llm();

   with entry {
       test_plugin();
   }
   ```

3. Run the test:
   ```bash
   jac run test.jac
   ```

### 4. Testing Your Plugin

Create comprehensive tests:

```python
import pytest
from byllm.llm import Model
from my_byllm_plugin.plugin import MybyllmRuntime

def test_plugin():
    runtime = MybyllmRuntime()
    model = Model("mockllm", outputs=["test response"])

    def test_function(x: str) -> str:
        """Test function."""
        pass

    result = runtime.call_llm(model, test_function, {"x": "test input"})
    assert result == "test response"
```


## From: rpg_game.md

We’ll test the system by generating AI levels and printing their difficulty, enemies, and maps.

Create a new file called `test_generator.jac`:

```jac linenums="1"
import from level_manager { LevelManager }

with entry {
    level_manager = LevelManager();

    print("Generating 3 AI-powered levels...\n");

    for i in range(3) {
        level, map_obj = level_manager.get_next_level();
        visual_map = level_manager.get_map(map_obj);

        print(f"=== LEVEL {i+1} ===");
        print(f"Difficulty: {level.difficulty}");
        print(f"Enemies: {level.num_enemies}");
        print(f"Walls: {level.num_wall}");
        print("Map:");
        for row in visual_map {
            print(row);
        }
        print("\n");
    }
}
```

Run this script:
```bash
jac run test_generator.jac
```

Expected output (AI may vary):
```
=== LEVEL 1 ===
Difficulty: 1
Enemies: 2
Walls: 3
Map:
BBBBBBBBBBBBBBBBBBBBBB
B..................B
B.....B............B
B..................B
B........E.........B
B..................B
B..........P.......B
B..................B
B.E................B
BBBBBBBBBBBBBBBBBBBBBB
```

