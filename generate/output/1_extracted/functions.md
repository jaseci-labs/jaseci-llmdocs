# functions


## From: jac_in_a_flash.md

Methods are declared with `def`.
Methods that take no parameters omit parentheses in their signature, making the object definition concise.
The object lists method signatures (`def init;`, `override def play;`), and the actual bodies are provided later in `impl Class.method` blocks.


## From: debugger.md

Example program with a function we want to debug:

![Example of complex function](assets/debugger/debugger-complex_function.png)


## From: keywords.md

**Function and Method Definition**

| Keyword | Description |
| --- | --- |
| [`can`](https://www.jac-lang.org/learn/jac_ref/#functions-and-abilities) | Defines an "ability" (a method) for an archetype. |
| [`def`](https://www.jac-lang.org/learn/jac_ref/#functions-and-abilities) | Defines a standard function with mandatory type annotations. |
| [`impl`](https://www.jac-lang.org/learn/jac_ref/#implementations) | Separates the implementation of a construct from its declaration. |
| [`yield`](https://www.jac-lang.org/learn/jac_ref/#yield-statements) | Pauses a function, returns a value, and creates a generator. |


## From: library_mode.md

| Function | Description | Parameters |
|----------|-------------|------------|
| `connect(left, right, edge, undir, conn_assign, edges_only)` | Connect nodes with edge | `left`: source node(s)<br>`right`: target node(s)<br>`edge`: edge class (optional)<br>`undir`: undirected flag<br>`conn_assign`: attribute assignments<br>`edges_only`: return edges instead of nodes |
| `disconnect(left, right, dir, filter)` | Remove edges between nodes | `left`: source node(s)<br>`right`: target node(s)<br>`dir`: edge direction<br>`filter`: edge filter function |
| `build_edge(is_undirected, conn_type, conn_assign)` | Create edge builder function | `is_undirected`: bidirectional flag<br>`conn_type`: edge class<br>`conn_assign`: initial attributes |
| `assign_all(target, attr_val)` | Assign attributes to list of objects | `target`: list of objects<br>`attr_val`: tuple of (attrs, values) |
| `spawn(walker, node)` | Start walker at node | `walker`: Walker instance<br>`node`: Starting node |
| `spawn_call(walker, node)` | Internal spawn execution (sync) | `walker`: Walker anchor<br>`node`: Node/edge anchor |
| `async_spawn_call(walker, node)` | Internal spawn execution (async) | Same as spawn_call (async version) |
| `visit(walker, nodes)` | Visit specified nodes | `walker`: Walker instance<br>`nodes`: Node/edge references |
| `disengage(walker)` | Stop walker traversal | `walker`: Walker to stop |
| `refs(path)` | Convert path to node/edge references | `path`: ObjectSpatialPath |
| `arefs(path)` | Async path references (placeholder) | `path`: ObjectSpatialPath |
| `filter_on(items, func)` | Filter archetype list by predicate | `items`: list of archetypes<br>`func`: filter function |
| `get_edges(origin, destination)` | Get edges connected to nodes | `origin`: list of nodes<br>`destination`: ObjectSpatialDestination |
| `get_edges_with_node(origin, destination, from_visit)` | Get edges and connected nodes | `origin`: list of nodes<br>`destination`: destination spec<br>`from_visit`: include nodes flag |
| `edges_to_nodes(origin, destination)` | Get nodes connected via edges | `origin`: list of nodes<br>`destination`: destination spec |
| `remove_edge(node, edge)` | Remove edge reference from node | `node`: NodeAnchor<br>`edge`: EdgeAnchor |
| `detach(edge)` | Detach edge from both nodes | `edge`: EdgeAnchor |
| `root()` | Get current root node | Root node instance |
| `get_all_root()` | Get all root nodes | List of roots |
| `get_object(id)` | Get archetype by ID string | Archetype or None |
| `object_ref(obj)` | Get hex ID string of archetype | String |
| `save(obj)` | Persist archetype to database | None |
| `destroy(objs)` | Delete archetype(s) from memory | None |
| `commit(anchor)` | Commit data to datasource | None |
| `reset_graph(root)` | Purge graph from memory | Count of deleted items |
| `perm_grant(archetype, level)` | Grant public access to archetype | `archetype`: Target archetype<br>`level`: AccessLevel (READ/CONNECT/WRITE) |
| `perm_revoke(archetype)` | Revoke public access | `archetype`: Target archetype |
| `allow_root(archetype, root_id, level)` | Allow specific root access | `archetype`: Target<br>`root_id`: Root UUID<br>`level`: Access level |
| `disallow_root(archetype, root_id, level)` | Disallow specific root access | Same as allow_root |
| `elevate_root()` | Elevate context to system root | No parameters (uses context) |
| `check_read_access(anchor)` | Check read permission | `anchor`: Target anchor |
| `check_write_access(anchor)` | Check write permission | `anchor`: Target anchor |
| `check_connect_access(anchor)` | Check connect permission | `anchor`: Target anchor |
| `check_access_level(anchor, no_custom)` | Get access level for anchor | `anchor`: Target<br>`no_custom`: skip custom check |
| `jac_import(target, base_path, ...)` | Import Jac/Python module | `target`: Module name<br>`base_path`: Search path<br>`absorb`, `mdl_alias`, `override_name`, `items`, `reload_module`, `lng`: import options |
| `load_module(module_name, module, force)` | Load module into machine | `module_name`: Name<br>`module`: Module object<br>`force`: reload flag |
| `attach_program(program)` | Attach JacProgram to runtime | `program`: JacProgram instance |
| `list_modules()` | List all loaded modules | Returns list of names |
| `list_nodes(module_name)` | List nodes in module | `module_name`: Module to inspect |
| `list_walkers(module_name)` | List walkers in module | `module_name`: Module to inspect |
| `list_edges(module_name)` | List edges in module | `module_name`: Module to inspect |
| `get_archetype(module_name, archetype_name)` | Get archetype class from module | `module_name`: Module<br>`archetype_name`: Class name |
| `make_archetype(cls)` | Convert class to archetype | `cls`: Class to convert |
| `spawn_node(node_name, attributes, module_name)` | Create node instance by name | `node_name`: Node class name<br>`attributes`: Init dict<br>`module_name`: Source module |
| `spawn_walker(walker_name, attributes, module_name)` | Create walker instance by name | `walker_name`: Walker class<br>`attributes`: Init dict<br>`module_name`: Source module |
| `update_walker(module_name, items)` | Reload walker from module | `module_name`: Module<br>`items`: Items to update |
| `create_archetype_from_source(source_code, ...)` | Create archetype from Jac source | `source_code`: Jac code string<br>`module_name`, `base_path`, `cachable`, `keep_temporary_files`: options |
| `jac_test(func)` | Mark function as test | `func`: Test function |
| `run_test(filepath, ...)` | Run test suite | `filepath`: Test file<br>`func_name`, `filter`, `xit`, `maxfail`, `directory`, `verbose`: test options |
| `report(expr, custom)` | Report value from walker | `expr`: Value to report<br>`custom`: custom report flag |
| `printgraph(node, depth, traverse, edge_type, bfs, edge_limit, node_limit, file, format)` | Generate graph visualization | `node`: Start node<br>`depth`: Max depth<br>`traverse`: traversal flag<br>`edge_type`: filter edges<br>`bfs`: breadth-first flag<br>`edge_limit`, `node_limit`: limits<br>`file`: output path<br>`format`: 'dot' or 'mermaid' |
| `call_llm(model, mtir)` | Direct LLM invocation | Advanced LLM usage |
| `get_mtir(caller, args, call_params)` | Get method IR for LLM | LLM internal representation |
| `setup()` | Initialize class references | No parameters |
| `get_context()` | Get current execution context | Returns ExecutionContext |
| `field(factory, init)` | Define dataclass field | `factory`: Default factory<br>`init`: Include in init |
| `impl_patch_filename(file_loc)` | Patch function file location | `file_loc`: File path for stack traces |
| `thread_run(func, *args)` | Run function in thread | `func`: Function<br>`args`: Arguments |
| `thread_wait(future)` | Wait for thread completion | `future`: Future object |
| `create_cmd()` | Create CLI commands | No parameters (placeholder) |


## From: example.md

A function body can simply be replaced with a call to an LLM, removing the need for prompt engineering. `by llm()` delegates execution to an LLM without any extra library code.
```jac
def get_personality(name: str) -> Personality by llm();
```
```jac
def calc_distance(x1: float, y1: float, x2: float, y2: float) -> float {
return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}
```
```jac
obj Tweet {
    has content: str, author: str, timestamp: str, likes: int = 0;

    def like() -> None;
    def unlike() -> None;
    def get_preview(max_length: int) -> str;
    def get_like_count() -> int;
}
```
```jac
impl Tweet.like() -> None {
    self.likes += 1;
}

impl Tweet.unlike() -> None {
    if self.likes > 0 {
            self.likes -= 1;
    }
}

impl Tweet.get_preview(max_length: int) -> str {
    return self.content[:max_length] + "..." if len(self.content) > max_length else self.content;
}

impl Tweet.get_like_count() -> int {
    return self.likes;
}
```


## From: syntax_quick_reference.md

```jac
# functions are defined with the def keyword and a control block
def nextFunction {
	x = 3;     # Variable assignment.
	y = 4;
	(add, mult) = learnMultiple(x, y);       # Function returns two values.
	print(f"sum: {add} prod:{mult}"); 		 # values can be formatted with f-strings
	learnFlowControl();
}

# same as Python, Jac supports default paremeters and multiple return values
def learnMultiple(x: int, y: int = 5) -> (int, int) {
	return (x + y, x * y); # Return two values.
}
```
```jac
def learnSpecial(){
    # lambdas create anonymous functions
    add = lambda a: int, b: int -> int : a + b;
    print(add(5, 3));
```


## From: superset_python.md

```jac
"""Functions in Jac."""

def factorial(n: int) -> int {
    if n == 0 { return 1; }
    else { return n * factorial(n-1); }
}
```

```python
"""Functions in Jac."""
from __future__ import annotations
from jaclang.lib import Obj

def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
```

=== "utils.jac"
    ```jac
    """Validation and AI utilities."""

    def validate_title(title: str) -> bool {
        return len(title) > 3;
    }

    def generate_desc(title: str) -> str {
        return f"Task description for: {title}";
    }
    ```

=== "main.jac"
    ```jac
    """Application with inline Python validation."""
    import models;

    def generate_desc(title: str) -> str {
        return f"Task description for: {title}";
    }

    ::py::
    # Legacy Python validation - kept as-is
    def validate_title(title):
        """Complex validation logic from old codebase."""
        return len(title) > 3 and title.strip() != ""

    def get_sample_task():
        """Helper from legacy code."""
        return {"title": "Build API"}
    ::py::
    ```

=== "main.jac"
    ```jac
    """Main application - imports Python module."""
    import models;
    import validators;

    def generate_desc(title: str) -> str {
        return f"Task description for: {title}";
    }
    ```

=== "validators.py"
    ```python
    """Python validation utilities - shared with other projects."""

    def validate_title(title: str) -> bool:
        """Validator used across multiple projects."""
        return len(title) > 3

    def get_sample_title():
        """Helper to load sample data."""
        return "Build API"
    ```

=== "main.py"
    ```python
    """Python application importing Jac modules."""
    import jaclang  # Enable Jac imports

    from validators import validate_title
    from task_graph import Task, TaskCreator, generate_desc
    from jaclang.lib import spawn, root

    def create_task(title: str):
        """Python function using Jac features."""
        if not validate_title(title):
            print("✗ Title too short!")
            return

        # Use Jac walker
        creator = TaskCreator(title=title)
        spawn(creator, root())

        # Use Jac's AI
        desc = generate_desc(title)
        print(f"  AI: {desc}")

    if __name__ == "__main__":
        create_task("Build API")
    ```

=== "validators.py"
    ```python
    """Python validation utilities."""

    def validate_title(title: str) -> bool:
        """Title validator."""
        return len(title) > 3
    ```

=== "task_graph.jac"
    ```jac
    """Jac module with graph and AI features."""

    node Task {
        has title: str;
        has done: bool = False;
    }

    walker TaskCreator {
        has title: str;

        can create with `root entry {
            task = Task(title=self.title);
            here ++> task;
            print(f"✓ Created: {task.title}");
        }
    }

    def generate_desc(title: str) -> str {
        return f"Task description for: {title}";
    }
    ```

=== "main.py"
    ```python
    """Pure Python using Jac runtime."""
    from jaclang.lib import Node, Walker, on_entry, connect, spawn, root
    from validators import validate_title

    # Define Task node using Jac base class
    class Task(Node):
        title: str
        done: bool

        def __init__(self, title: str):
            super().__init__()
            self.title = title
            self.done = False

    # Define walker using Jac decorators
    class TaskCreator(Walker):
        def __init__(self, title: str):
            super().__init__()
            self.title = title

        @on_entry
        def create(self, here) -> None:
            """Entry point - creates task."""
            if validate_title(self.title):
                task = Task(title=self.title)
                connect(here, task)
                print(f"✓ Created: {task.title}")
                # Note: AI features require .jac syntax
            else:
                print("✗ Title too short!")

    if __name__ == "__main__":
        creator = TaskCreator(title="Build API")
        spawn(creator, root())
    ```

=== "validators.py"
    ```python
    """Python validation utilities."""

    def validate_title(title: str) -> bool:
        """Title validator."""
        return len(title) > 3
    ```


## From: jsx_client_serv_design.md

```jac
cl def homepage() -> dict {
    return <div>
        <h1>Welcome</h1>
        <button onclick={load_feed()}>Load Feed</button>
    </div>;
}
```

```jac
cl import from jac:client_runtime {
    jacLogin,
    jacLogout,
    jacIsLoggedIn,
}

cl def LoginForm() {
    async def handleLogin(event: any) {
        event.preventDefault();
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        success = await jacLogin(username, password);
        if success {
            console.log("Login successful!");
            // Redirect or update UI
        } else {
            console.log("Login failed");
        }
    }

    return <form onsubmit={handleLogin}>
        <input id="username" type="text" placeholder="Username" />
        <input id="password" type="password" placeholder="Password" />
        <button type="submit">Login</button>
    </form>;
}
```

```jac
cl def render_example() {
    // Basic elements
    let basic = <div>Hello World</div>;

    // Elements with attributes
    let with_attrs = <button id="submit" class="btn">Click</button>;

    // Expression attributes and children
    let name = "Alice";
    let greeting = <h1 data-user={name}>Welcome, {name}!</h1>;

    // Spread attributes
    let props = {"class": "card", "id": "main"};
    let with_spread = <div {...props}>Content</div>;

    // Fragment syntax
    let fragment = <>
        <div>First</div>
        <div>Second</div>
    </>;

    // Component usage (capitalized names)
    let component = <Button label="Click Me" />;

    return <div>{greeting}{component}</div>;
}
```

```jac
cl import from jac:client_runtime { createSignal }

cl def Counter() {
    [count, setCount] = createSignal(0);

    def increment() {
        setCount(count() + 1);  // Read with (), set by calling setter
    }

    return <div>
        <p>Count: {count()}</p>
        <button onclick={increment}>Increment</button>
    </div>;
}
```

```jac
cl import from jac:client_runtime { createState }

cl def TodoList() {
    [state, setState] = createState({
        "todos": [],
        "filter": "all"
    });

    def addTodo(text: str) {
        todos = state().todos;
        todos.push({"text": text, "done": False});
        setState({"todos": todos});  // Shallow merge with existing state
    }

    return <div>
        <ul>
            {[<li>{todo.text}</li> for todo in state().todos]}
        </ul>
    </div>;
}
```

```jac
cl import from jac:client_runtime { createSignal, createEffect }

cl def DataFetcher() {
    [userId, setUserId] = createSignal(1);
    [userData, setUserData] = createSignal(None);

    createEffect(lambda -> None {
        id = userId();  // Track dependency!
        console.log("Fetching user", id);
        # In real app, would fetch from API
        setUserData({"id": id, "name": "User " + str(id)});
    });

    return <div>
        <button onclick={lambda: setUserId(userId() + 1)}>Next User</button>
        <p>Current: {userData() and userData().name or "Loading..."}</p>
    </div>;
}
```

```jac
cl import from jac:client_runtime { createRouter, Route }

cl def App() {
    routes = [
        Route("/", HomePage),
        Route("/about", AboutPage),
        Route("/profile", ProfilePage, guard=jacIsLoggedIn)
    ];

    router = createRouter(routes, defaultRoute="/");

    return <div>
        <nav>
            <Link href="/">Home</Link>
            <Link href="/about">About</Link>
            <Link href="/profile">Profile</Link>
        </nav>
        <main>{router.render()}</main>
    </div>;
}
```

```jac
cl import from jac:client_runtime { navigate }

cl def LoginForm() {
    def handleSubmit() {
        # After successful login
        navigate("/dashboard");
    }

    return <form onsubmit={handleSubmit}>...</form>;
}
```

```jac
cl import from jac:client_runtime { Route, jacIsLoggedIn, navigate }

cl def AccessDenied() {
    return <div>
        <h1>Access Denied</h1>
        <button onclick={lambda: navigate("/login")}>Login</button>
    </div>;
}

Route("/admin", AdminPanel, guard=jacIsLoggedIn)
```

```jac
// Client page - renders in browser
cl def homepage() {
    return <div class="app">
        <header>
            <h1>Welcome to Jac</h1>
        </header>
        <main>
            <p>Full-stack web development in one language!</p>
            <button onclick={load_users()}>Load Users</button>
        </main>
    </div>;
}
```

```jac
cl import from jac:client_runtime {
    createSignal,
    createState,
    createRouter,
    Route,
    Link,
    navigate,
}

// Counter component with reactive signal
cl def Counter() {
    [count, setCount] = createSignal(0);

    return <div>
        <h2>Counter: {count()}</h2>
        <button onclick={lambda: setCount(count() + 1)}>+</button>
        <button onclick={lambda: setCount(count() - 1)}>-</button>
    </div>;
}

// Todo list with reactive state
cl def TodoApp() {
    [state, setState] = createState({
        "todos": [],
        "input": ""
    });

    def addTodo() {
        todos = state().todos;
        todos.push({"text": state().input, "done": False});
        setState({"todos": todos, "input": ""});
    }

    return <div>
        <h2>Todos</h2>
        <input
            value={state().input}
            oninput={lambda e: setState({"input": e.target.value})}
        />
        <button onclick={addTodo}>Add</button>
        <ul>
            {[<li>{todo.text}</li> for todo in state().todos]}
        </ul>
    </div>;
}

// Main app with routing
cl def littlex_app() {
    routes = [
        Route("/", Counter),
        Route("/todos", TodoApp)
    ];

    router = createRouter(routes, "/");

    return <div>
        <nav>
            <Link href="/">Counter</Link>
            <Link href="/todos">Todos</Link>
        </nav>
        <main>{router.render()}</main>
    </div>;
}
```


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

with entry {
    # Test file operations
    test_content = "Hello from Jac!";
    if write_file("test.txt", test_content) {
        content = read_file("test.txt");
        print(f"File content: {content}");
    }
}
```
```jac
obj Calculator {
    has precision: int = 2;

    def add(a: float, b: float) -> float;
    def subtract(a: float, b: float) -> float;
    def multiply(a: float, b: float) -> float;
    def divide(a: float, b: float) -> float;
}
```
```jac
impl Calculator.add {
    result = a + b;
    return round(result, self.precision);
}

impl Calculator.subtract {
    result = a - b;
    return round(result, self.precision);
}

impl Calculator.multiply {
    result = a * b;
    return round(result, self.precision);
}

impl Calculator.divide {
    if b == 0.0 {
        raise ValueError("Division by zero");
    }
    result = a / b;
    return round(result, self.precision);
}
```
```jac
obj ConfigReader {
    has config_file: str;
    has config_data: dict[str, any] = {};

    def load_config() -> bool;
    def get_value(key: str, default: any = None) -> any;
    def set_value(key: str, value: any) -> None;
    def save_config() -> bool;
    def create_default_config() -> None;
}
```
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

impl ConfigReader.get_value {
    return self.config_data.get(key, default);
}

impl ConfigReader.set_value {
    self.config_data[key] = value;
}

impl ConfigReader.save_config {
    try {
        with open(self.config_file, 'w') as file {
            json.dump(self.config_data, file, indent=2);
        }
        print(f"Config saved to {self.config_file}");
        return True;
    } except Exception as e {
        print(f"Error saving config: {e}");
        return False;
    }
}

impl ConfigReader.create_default_config {
    self.config_data = {
        "app_name": "My Jac App",
        "version": "1.0.0",
        "debug": False,
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp_db"
        },
        "logging": {
            "level": "INFO",
            "file": "app.log"
        }
    };
    self.save_config();
}
```
```jac
obj Application {
    has config: ConfigReader;
    has logger: any;

    def start() -> None;
    def setup_logging() -> None;
    def get_database_config() -> dict[str, any];
    def run_debug_mode() -> None;
    def run_normal_mode() -> None;
}
```
```jac
impl Application.start {
    print("=== Starting Application ===");

    # Load configuration
    if self.config.load_config() {
        self.setup_logging();

        # Display app info
        app_name = self.config.get_value("app_name", "Unknown App");
        version = self.config.get_value("version", "1.0.0");
        debug_mode = self.config.get_value("debug", False);

        print(f"App: {app_name} v{version}");
        print(f"Debug mode: {debug_mode}");

        # Show database config
        db_config = self.get_database_config();
        print(f"Database: {db_config['host']}:{db_config['port']}/{db_config['name']}");

        if debug_mode {
            self.run_debug_mode();
        } else {
            self.run_normal_mode();
        }
    } else {
        print("Failed to load configuration");
    }
}

impl Application.setup_logging {
    log_config = self.config.get_value("logging", {});
    log_level = log_config.get("level", "INFO");
    log_file = log_config.get("file", "app.log");

    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    );

    self.logger = logging.getLogger("app");
    self.logger.info("Logging configured");
}

impl Application.get_database_config {
    default_db = {"host": "localhost", "port": 5432, "name": "default_db"};
    return self.config.get_value("database", default_db);
}

impl Application.run_debug_mode {
    print(">>> Running in DEBUG mode");
    print(f">>> Full config: {self.config.config_data}");
}

impl Application.run_normal_mode {
    print(">>> Running in NORMAL mode");
    print(">>> Application ready");
}
```


## From: chapter_2.md

### Local Variables
```jac
def add_numbers(a: int, b: int) -> int {
    result: int = a + b;  # Local variable
    return result;
}
with entry {
    sum = add_numbers(5, 10);
    print(f"Sum: {sum}");
}
```

```jac
glob school_name: str = "Jac High School";
glob passing_grade: int = 60;
glob honor_threshold: float = 3.5;

def get_school_info() -> str {
    :g: school_name; # Accessing global variable
    return f"Welcome to {school_name}";
}

with entry {
    print(get_school_info());
    print(f"Honor threshold is {honor_threshold}");
}
```


## From: chapter_10.md

```jac
            def get_status() -> str {
                return f"Delivered {self.delivery_count} messages to {len(self.visited_locations)} locations";
            }
```
```jac
            def report_final() -> None {
                print(f" Attendance Report:");
                print(f"   Present: {self.present_students}");
                print(f"   Absent: {self.absent_students}");
                print(f"   Total checked: {self.checks_done}");
            }
```
```jac
            def report_final() -> None {
                print(f" Attendance Report:");
                print(f"   Present: {self.present_students}");
                print(f"   Absent: {self.absent_students}");
                print(f"   Total checked: {self.checks_done}");
            }
```


## From: byllm.md

- **LLM Function Overriding**: Introduced the ability to override any regular function with an LLM-powered implementation at runtime using the `function_call() by llm()` syntax. This allows for dynamic, on-the-fly replacement of function behavior with generative models. (mtllm)


## From: chapter_9.md

```jac
import from byllm.lib { Model }

# Configure the LLM
glob npc_model = Model(model_name="gpt-4.1-mini");

"""Adjusts the tone or personality of the shop keeper npc depending on weather/time."""
def get_ambient_mood(state: dict) -> str by npc_model();
```
This function, `get_ambient_mood`, takes a dictionary (the walker’s state) and sends it to the model. The model interprets the contents like `temperature` and `time`—and returns a textual mood that fits the situation.

```jac
import from byllm.lib { Model }

# Configure different models
glob npc_model = Model(model_name="gpt-4.1-mini");

node Service{}

walker StateAgent{
    has state: dict = {};

    can start with `root entry {
        visit [-->(`?Service)];
    }
}

node Weather(Service) {
    has temp: int = 80;

    can get with StateAgent entry {
        visitor.state["temperature"] = self.temp;
    }
}

node Time(Service) {
    has hour: int = 12;

    can get with StateAgent entry {
        visitor.state["time"] = f"{self.hour}:00 PM";
    }
}

"""Adjusts the tone or personality of the shop keeper npc depending on weather/time."""
def get_ambient_mood(state: dict) -> str by npc_model();

node NPC {
    can get with StateAgent entry {
        visitor.state["npc_mood"] = get_ambient_mood(visitor.state);
    }
}

walker NPCWalker(StateAgent) {
    can visit_npc with `root entry{
        visit [-->(`?NPC)];
    }
}


with entry {
    root ++> Weather();
    root ++> Time();
    root ++> NPC();

    agent = NPCWalker() spawn root;
    print(agent.state['npc_mood']);
}
```


## From: jac-cloud.md

- **Consistent Jac Code Execution**: Fixed an issue allowing Jac code to be executed both as a standalone program and as an application. Running `jac run` now executes the `main()` function, while `jac serve` launches the application without invoking `main()`.
- **Get all Root Builtin Method**: Introduced `allroots` builtin method to get all the roots available in the memory. Developers can get all the roots in the memory/ database by calling `allroots()` method.
- **Permission Update Builtin Methods**: Introduced `grant`, `revoke` builtin methods, `NoPerm`, `ReadPerm`, `ConnectPerm`, `WritePerm` builtin enums, to give the permission to a node or revoke the permission. Developers can use them by calling `grant(node_1, ConnectPerm)` or `revoke(node_1)` method.


## From: chapter_5.md

Up until this point, we've used Jac's functions to define behavior. However, what if we wanted to incorperate AI capabilities directly into our Jac applications? For example, lets say we're writing a poetry application that can generate poems based on a user supplied topic.

Since Jac is a super set of Python, we can create a function `write_poetry` that takes a topic as input and then make a call to an OpenAI model using its python or langchain library to generate the poem.

First, install the OpenAI Python package:
```bash
pip install openai
```
then set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```
Now we can write our Jac code to integrate with OpenAI's API:

```jac
import from openai { OpenAI }

glob client = OpenAI();

""" Write a poem about topic """
def write_poetry(topic: str) -> str {
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Write a poem about {topic}."
    );
    return response.output_text;
}

with entry {
    poem = write_poetry("A serene landscape with mountains.");
    print(poem);
}
```
Finally, lets generate our poetic masterpiece by running the Jac code:
```console
$ jac run poetry.jac
Amidst the quiet, mountains rise,
Their peaks adorned with endless skies.
A tranquil breeze, a gentle stream,
Within this landscape, like a dream.

Soft whispers of the morning light,
Embrace the earth in pure delight.
A serene world, where hearts find peace,
In nature's hold, all worries cease.
```
Very nice! However, this approach requires manual API management (what if we want to switch to a different AI provider?), and we still have to write the prompt ourselves. Wouldn't it be great if we could just define the function signature and let the AI handle the rest? *Imagine a world where the function was the prompt?* Where we could simply declare a function and the AI would understand what to do? That's the power of byLLM.

Let's see how this works.

First we'll need to install the byLLM package:
```bash
pip install byllm
```
Next we replace the OpenAI import with that of the byLLM package

```jac
import from byllm.lib { Model }
glob llm = Model(model_name="gpt-4.1-mini");
```
Instead of writing the function ourselves, we simply declare the function signature and use the `by` keyword to indicate that this function should be handled by the AI model referenced by `llm()`. The byLLM framework will automatically generate the appropriate prompt based on the function signature.
```jac
def write_poetry(topic: str) -> str by llm();
```

Finally, lets put it all together and run the Jac code:
```jac
# mt_poem.jac - Simple AI integration
import from byllm.lib { Model }

glob llm = Model(model_name="gpt-4.1-mini");

""" Write a poem about topic """
def write_poetry(topic: str) -> str by llm();

with entry {
    poem = write_poetry("A serene landscape with mountains.");
    print(poem);
}
```

```console
$ jac run mt_poem.jac
Beneath the sky so vast and grand,
Mountains rise like ancient bands,
Whispers soft in tranquil air,
A serene landscape, calm and fair.

Colors blend in gentle hues,
Nature's brush with peaceful views,
Rivers sing and breezes dance,
In this quiet, soul’s expanse.
```

### Simple Image Captioning Tool
To further illustrate byLLM's capabilities, let's build a simple image captioning tool. This tool will analyze an image and generate a descriptive caption using an AI model.

First lets grab an image from upsplash to work with. You can use any image you like, but for this example, we'll use a photo of a french bulldog. Download the image and save it as `photo.jpg` in the same directory as your Jac code.

Next we'll make use of MLTLLM's `Image` function to handle image inputs. This function allows us to pass images directly to the AI model for analysis. We'll use OpenAI's `gpt-4o-mini` model for this task.

```jac
# image_captioning.jac - Simple Image Captioning Tool
import from byllm.lib { Model, Image }

glob llm = Model(model_name="gpt-4o-mini");

"""Generate a detailed caption for the given image."""
def caption_image(image: Image) -> str by llm();

with entry {
    caption = caption_image(Image("photo.jpg"));
    print(caption);
}
```
Now we can run our Jac code to generate a caption for the image:
```console
$ jac run image_captioning.jac

A stylish French Bulldog poses confidently against a vibrant yellow backdrop,
showcasing its trendy black and yellow hoodie emblazoned with "WOOF." The pup's
playful demeanor is accentuated by a shiny gold chain draped around its neck,
adding a touch of flair to its outfit. With its adorable large ears perked up
and tongue playfully sticking out, this fashion-forward canine is ready to steal
the spotlight and capture hearts with its charm and personality.
```


## From: chapter_17.md

```jac
def calculate_recommendation_score(
    current_user: Profile,
    candidate: Profile,
    followed_users: list[Profile]
) -> float {
    score = 0.0;

    if self.algorithm in ["friend_based", "hybrid"] {
        # Friend of friend scoring
        candidate_followers = [candidate <-:Follow:<- Profile];
        mutual_connections = set([u.username for u in followed_users]) &
                           set([u.username for u in candidate_followers]);
        score += len(mutual_connections) * 2.0;
    }

    if self.algorithm in ["interest_based", "hybrid"] {
        # Interest-based scoring using tweet content
        current_tweets = [current_user ->:Post:-> Tweet];
        candidate_tweets = [candidate ->:Post:-> Tweet];

        # Simple keyword matching (in real system, use embeddings)
        current_words = set();
        for tweet in current_tweets {
            current_words.update(tweet.content.lower().split());
        }

        candidate_words = set();
        for tweet in candidate_tweets {
            candidate_words.update(tweet.content.lower().split());
        }

        common_words = current_words & candidate_words;
        score += len(common_words) * 0.5;
    }

    return score;
}
```

```jac
def get_recommendation_reason(
    current_user: Profile,
    candidate: Profile,
    followed_users: list[Profile]
) -> str {
    # Determine primary reason for recommendation
    candidate_followers = [candidate <-:Follow:<- Profile];
    mutual_connections = set([u.username for u in followed_users]) &
                       set([u.username for u in candidate_followers]);

    if mutual_connections {
        return f"Friends with {list(mutual_connections)[0]}";
    }

    return "Similar interests";
}
```


## From: chapter_13.md

```jac
node Counter {
    has value: int = 0;

    def increment() -> int {
        self.value += 1;
        return self.value;
    }

    def get_value() -> int {
        return self.value;
    }
}
```

```jac
node Counter {
    has value: int = 0;
    has created_at: str;

    can increment() -> int {
        self.value += 1;
        return self.value;
    }

    can reset() -> int {
        self.value = 0;
        return self.value;
    }
}
```

```jac
node Counter {
    has created_at: str;
    has value: int = 0;

    def increment() -> int {
        old_value = self.value;
        self.value += 1;

        # Create history entry
        history = HistoryEntry(
            timestamp=str(datetime.now()),
            old_value=old_value,
            new_value=self.value
        );
        self ++> history;
        return self.value;
    }

    def get_history() -> list[dict] {
        history_nodes = [self --> HistoryEntry];
        return [
            {
                "timestamp": h.timestamp,
                "old_value": h.old_value,
                "new_value": h.new_value
            }
            for h in history_nodes
        ];
    }
}
```

```jac
node CounterManager {
    has created_at: str;

    def create_counter(name: str) -> dict {
        # Check if counter already exists
        existing = [self --> Counter](?name == name);
        if existing {
            return {"status": "exists", "counter": existing[0].name};
        }

        new_counter = Counter(name=name, value=0);
        self ++> new_counter;
        return {"status": "created", "counter": name};
    }

    def list_counters() -> list[dict] {
        counters = [self --> Counter];
        return [
            {"name": c.name, "value": c.value}
            for c in counters
        ];
    }

    def get_total() -> int {
        counters = [self --> Counter];
        return sum([c.value for c in counters]);
    }
}
```

```jac
node Counter {
    has name: str;
    has value: int = 0;

    def increment(amount: int = 1) -> int {
        self.value += amount;
        return self.value;
    }
}
```


## From: breaking_changes.md

#### 1. `dotgen` builtin function is now name `printgraph`

This renaming aims to make the function's purpose clearer, as `printgraph` more accurately reflects its action of outputting graph data, similar to how it can also output in JSON format. Also other formats may be added (like mermaid).

**Before**

```jac
node N {has val: int;}
edge E {has val: int = 0;}

with entry {
    end = root;
    for i in range(0, 2) {
        end +>: E : val=i :+> (end := [ N(val=i) for i in range(0, 2) ]);
    }
    data = dotgen(node=root);
    print(data);
}
```

**After**

```jac
node N {has val: int;}
edge E {has val: int = 0;}

with entry {
    end = root;
    for i in range(0, 2) {
        end +>: E : val=i :+> (end := [ N(val=i) for i in range(0, 2) ]);
    }
    data = printgraph(node=root);
    print(data);
}
```

#### 3. `def` keyword introduced

Instead of using `can` keyword for all functions and abilities, `can` statements are only used for object-spatial abilities and `def` keyword must be used for traditional python like functions and methods.

**Before (v0.7.x and earlier):**
```jac
can add(x: int, y: int) -> int {
    return x + y;
}

node Person {
    has name;
    has age;

    can get_name {
        return self.name;
    }

    can greet with speak_to {
        return "Hello " + visitor.name + ", my name is " + self.name;
    }

    can calculate_birth_year {
        return 2025 - self.age;
    }
}
```

**After (v0.8.0+):**
```jac
def add(x: int, y: int) -> int {
    return x + y;
}

node Person {
    has name;
    has age;

    def get_name {
        return self.name;
    }

    can greet with speak_to entry {
        return "Hello " + visitor.name + ", my name is " + self.name;
    }

    def calculate_birth_year {
        return 2025 - self.age;
    }
}
```


## From: permission.md

```jac
# Allow User2 to read a post
walker grant_access {
    has target_root_id: str;  # ID of User2's root
    has access_level: str;    # ReadPerm, ConnectPerm, or WritePerm

    can grant_access with post entry {
        # Grant access to the current post
        _.allow_root(here, NodeAnchor.ref(self.target_root_id), self.access_level);
        report "Access granted!";
    }
}
```
The code snippet `_.allow_root(here, NodeAnchor.ref(self.target_root_id), self.access_level)` facilitates granting a specified level of access to a target root node from the current node.

Here's a breakdown of the components:

- `here`

  - Represents the current node, which in this context is the post node.

- `NodeAnchor.ref(self.target_root_id)`

  - This converts the target_root_id (a string identifier) into a NodeAnchor representation. This NodeAnchor then points to the specific target root node that will be granted access.

- `self.access_level`
  - This parameter specifies the level of access that the target root node will have to the current node's data (i.e., the post node's data).

In essence, this line of code enables the post node to grant the designated target root node permission to access its data, with the access permissions defined by self.access_level.
```jac
# Remove User2's access to a post
walker revoke_access {
    has target_root_id: str;  # ID of User2's root

    can revoke_access with post entry {
        # Revoke access to the current post
        _.disallow_root(here, NodeAnchor.ref(self.target_root_id));
        report "Access revoked!";
    }
}
```
The code snippet `_.disallow_root(here, NodeAnchor.ref(self.target_root_id))` performs the inverse operation of `_.allow_root`; it removes existing access permissions that a target root node had to the current node's data.

Here's how it works:

- `here`
  - This refers to the current node, which, as before, is the post node. This is the node from which the permission is being revoked.
- `NodeAnchor.ref(self.target_root_id)`
  - This converts the target_root_id (a string identifier) into a NodeAnchor representation. This NodeAnchor pinpoints the specific target root node whose access privileges are being revoked.

In essence, this line of code instructs the post node to remove the previously granted access for the designated target root node to its data.
```jac
# Make a post readable by everyone
walker make_public {
    can make_public with post entry {
        # Grant READ access to all users
        grant(here, ReadPerm);
        report "Post is now public!";
    }
}
```
The code snippet `grant(here, ReadPerm)` provides a mechanism to grant read access to all other root nodes concerning the data within the current node.

Here's a breakdown of the elements:

- `here`
  - This represents the current node, which in this case is the post node. This is the node whose data will be accessible.
- `ReadPerm`
  - This literal string specifies the type of permission being granted. In this instance, it grants read access, allowing other root nodes to view the data on the post node. They can choose one from permission levels.
```jac
# Make a post private (owner-only)
walker make_private {
    can make_private with post entry {
        # Remove all access
        revoke(here);
        report "Post is now private!";
    }
}
```
The code snippet `revoke(here)` is used to remove all previously granted access permissions from all other root nodes to the current node's data. It's the inverse operation of `grant`.

Here's a breakdown:

- `here`
  - This represents the current node (in this context, the post node) from which all access will be revoked.

Essentially, this line of code completely withdraws any permissions that were previously granted to other root nodes, making the post node's data inaccessible to them.
```jac
node A {
    # suggested to be `with access {}`
    def __jac_access__ {

        ###############################################
        #              YOUR PROCESS HERE              #
        ###############################################

        # Allowed string return NoPerm, ReadPerm, ConnectPerm, or WritePerm
        return NoPerm;

        # Allowed enum return AccessLevel.NO_ACCESS, AccessLevel.READ, AccessLevel.ConnectPerm, AccessLevel.WRITE
        # return AccessLevel.NO_ACCESS;

        # Not recommended as it may change in the future
        # Allowed int return -1 (NoPerm), 0 (ReadPerm), 1 (ConnectPerm), 2 (WritePerm)
        # return -1;

    }
}
```
```jac
node A {
    # suggested to be `with access {}`
    def __jac_access__ {

        level = _Jac.check_access_level(here, True); # True means skip custom access validation trigger to avoid infinite loop

        ###############################################
        #              YOUR PROCESS HERE              #
        ###############################################

        # Allowed string return NoPerm, ReadPerm, ConnectPerm, or WritePerm
        return "NO_ACCESS";

        # Allowed enum return AccessLevel.NO_ACCESS, AccessLevel.READ, AccessLevel.ConnectPerm, AccessLevel.WRITE
        # return AccessLevel.NO_ACCESS;

        # Not recommended as it may change in the future
        # Allowed int return -1 (NoPerm), 0 (ReadPerm), 1 (ConnectPerm), 2 (WritePerm)
        # return -1;

    }
}
```


## From: python_integration.md

Python functions can be used as tools in byLLM. Functions defined in Python are callable by the LLM to perform specific tasks:

```python linenums="1"
import jaclang
from byllm.lib import Model
llm = Model(model_name="gpt-4o")


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

@by(llm(tools=[get_weather]))
def answer_question(question: str) -> str: ...
```


## From: static_fx.md

```python
# In UniPass
def enter_node(self, node: uni.UniNode) -> None:
    method_name = f"enter_{pascal_to_snake(type(node).__name__)}"
    if hasattr(self, method_name):
        getattr(self, method_name)(node)

# In your pass
def enter_func_call(self, node: uni.FuncCall) -> None:
    # Handle function call nodes
    pass

def exit_if_stmt(self, node: uni.IfStmt) -> None:
    # Handle if statement nodes
    pass
```

##### SymTabBuildPass

**Purpose**: Constructs symbol tables for name resolution

**Location**: `jac/jaclang/compiler/passes/main/sym_tab_build_pass.py`

**Key Operations**:
- Creates scope hierarchies
- Registers symbols (variables, functions, classes)
- Links parent-child scopes
- Adds special symbols (`self`, `super`)

**Example**:
```python
def enter_archetype(self, node: uni.Archetype) -> None:
    self.push_scope_and_link(node)
    node.parent_scope.def_insert(node, access_spec=node)

def enter_ability(self, node: uni.Ability) -> None:
    self.push_scope_and_link(node)
    if node.is_method:
        # Add 'self' symbol
        node.sym_tab.def_insert(uni.Name.gen_stub_from_node(node, "self"))
```

#### Why Inlining is Necessary

PyTorch models typically have this structure:

```python
class MyModel(nn.Module):
    def forward(self, x):
        x = self.layer1(x)      # Calls another module
        x = self._helper(x)     # Calls private method
        return self.layer2(x)

    def _helper(self, x):
        return F.relu(x)
```

**Without inlining**, we'd have:
- Incomplete static analysis (can't see into `_helper`)
- Missing optimization opportunities
- Fragmented graph representation

**With inlining**, we get:
```python
def forward_inlined(self, x):
    # Inlined self.layer1(x)
    x = self.layer1.linear(x)
    # Inlined self._helper(x)
    x = F.relu(x)
    # Inlined self.layer2


## From: quickstart.md

```jac linenums="1"

enum Personality {
    INTROVERT,
    EXTROVERT,
    AMBIVERT
}

def get_personality(name: str) -> Personality {
    # Traditional approach: manual algorithm, prompt-engineered LLM call, etc.
}

with entry {
    name = "Albert Einstein";
    result = get_personality(name);
    print(f"{result} personality detected for {name}");
}
```
The `by` keyword abstraction enables functions to process inputs of any type and generate contextually appropriate outputs of the specified type:
```jac linenums="1"
def get_personality(name: str) -> Personality by llm();
```
This will auto-generate a prompt for performing the task and provide an output that strictly adheres to the type `Personality`.
```python linenums="1"
import jaclang
from byllm.lib import Model, by
from enum import Enum

llm = Model(model_name="gemini/gemini-2.0-flash")

class Personality(Enum):
    INTROVERT
    EXTROVERT
    AMBIVERT

@by(model=llm)
def get_personality(name: str) -> Personality: ...

name = "Albert Einstein"
result = get_personality(name)
print(f"{result} personality detected for {name}")
```


## From: jaclang.md

- **JavaScript Export Semantics for Public Declarations**: Declarations explicitly annotated with `:pub` now generate JavaScript `export` statements. This applies to classes (`obj :pub`), functions (`def :pub`), enums (`enum :pub`), and global variables (`glob :pub`), enabling proper ES module exports in generated JavaScript code.
- **Complete Python Function Parameter Syntax Support**: Added full support for advanced Python function parameter patterns including positional-only parameters (`/` separator), keyword-only parameters (`*` separator without type hints), and complex parameter combinations (e.g., `def foo(a, b, /, *, c, d=1, **kwargs): ...`). This enhancement enables seamless Python-to-Jac conversion (`py2jac`) by supporting the complete Python function signature syntax.
- **Fix `lambda self injection in abilities`**: Removed unintended `self` parameter in lambdas declared inside abilities/methods.
- **Fix `jac2py lambda annotations`**: Stripped type annotations from lambda parameters during jac2py conversion to ensure valid Python output while keeping them in Jac AST for type checking.
- **Function Renaming**: The `dotgen` built-in function has been renamed to `printgraph`. This change aims to make the function's purpose clearer, as `printgraph` more accurately reflects its action of outputting graph data. It can output in DOT format and also supports JSON output via the `as_json=True` parameter. Future enhancements may include support for other formats like Mermaid.
- **`def` Keyword for Functions**: The `def` keyword is now used for traditional Python-like functions and methods, while `can` is reserved for object-spatial abilities.
- **Lambda Syntax Update**: The lambda syntax has been updated from `with x: int can x;` to `lambda x: int: x * x;`, aligning it more closely with Python's lambda syntax.


## From: cli.md

The `enter` command is utilized to run the specified entrypoint function in the given .jac file.

```bash
jac enter <file_path> <entrypoint> <args>
```
Parameters to execute the enter command:
- `file_path`: The path to the .jac file.
- `entrypoint`: The name of the entrypoint function.
- `args`: Arguments to pass to the entrypoint function.

- To enter file_path Jac file
```bash
jac enter <file_path>
```


## From: create_own_lm.md

=== "Python"
    ```python linenums="1"
    from byllm.llm import BaseLLM
    from openai import OpenAI

    class MyOpenAIModel(BaseLLM):
        def __init__(self, model_name: str, **kwargs: object) -> None:
            """Initialize the MockLLM connector."""
            super().__init__(model_name, **kwargs)

        def model_call_no_stream(self, params):
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(**params)
            return response

        def model_call_with_stream(self, params):
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(stream=True, **params)
            return response
    ```
=== "Jac"
    ```jac linenums="1"
    import from byllm.llm { BaseLLM }
    import from openai { OpenAI }

    obj  MyOpenAIModel(BaseLLM){
        has model_name: str;
        has config: dict = {};

        def post_init() {
            super().__init__(model_name=self.model_name, **kwargs);
        }

        def model_call_no_stream(params: dict) {
            client = OpenAI(api_key=self.api_key);
            response = client.chat.completions.create(**params);
            return response;
        }

        def model_call_with_stream(params: dict) {
            client = OpenAI(api_key=self.api_key);
            response = client.chat.completions.create(stream=True, **params);
            return response;
        }
    }
    ```


## From: with_llm.md

=== "Jac"
    ```jac linenums="1"
    import from byllm.lib { Model }

    glob llm = Model(model_name="gpt-4o");

    def translate_to(language: str, phrase: str) -> str by llm();

    with entry {
        output = translate_to(language="Welsh", phrase="Hello world");
        print(output);
    }
    ```
=== "python"
    ```python linenums="1"
    from byllm.lib import Model, by

    llm = Model(model_name="gpt-4o")

    @by(llm)
    def translate_to(language: str, phrase: str) -> str: ...

    output = translate_to(language="Welsh", phrase="Hello world")
    print(output)
    ```

This simple piece of code replaces traditional prompt engineering without introducing additional complexity.

=== "Jac"
    ```jac linenums="1"
    import from byllm.lib { Model }
    glob llm = Model(model_name="gemini/gemini-2.0-flash");

    enum Personality {
        INTROVERT,
        EXTROVERT,
        AMBIVERT
    }

    def get_personality(name: str) -> Personality by llm();

    with entry {
        name = "Albert Einstein";
        result = get_personality(name);
        print(f"{result} personality detected for {name}");
    }
    ```
=== "Python"
    ```python linenums="1"
    from byllm.lib import Model, by
    from enum import Enum
    llm =  Model(model_name="gemini/gemini-2.0-flash")

    class Personality(Enum):
        INTROVERT
        EXTROVERT
        AMBIVERT

    @by(model=llm)
    def get_personality(name: str) -> Personality: ...

    name = "Albert Einstein"
    result = get_personality(name)
    print(f"{result} personality detected for {name}")
    ```

=== "Jac"
    ```jac linenums="1"
    import from byllm.lib { Model }
    glob llm = Model(model_name="gemini/gemini-2.0-flash");

    """Represents the personal record of a person"""
    obj Person {
        has name: str;
        has dob: str;
        has ssn: str;
    }

    sem Person.name = "Full name of the person";
    sem Person.dob = "Date of Birth";
    sem Person.ssn = "Last four digits of the Social Security Number of a person";

    """Calculate eligibility for various services based on person's data."""
    def check_eligibility(person: Person, service_type: str) -> bool by llm();
    ```
=== "Python"
    ```python linenums="1"
    from jaclang import JacRuntimeInterface as Jac
    from dataclasses import dataclass
    from byllm.lib import Model, by
    llm =  Model(model_name="gemini/gemini-2.0-flash")

    @Jac.sem('', {  'name': 'Full name of the person',
                    'dob': 'Date of Birth',
                    'ssn': 'Last four digits of the Social Security Number of a person'
                    })
    @dataclass
    class Person():
        name: str
        dob: str
        ssn: str

    @by(llm)
    def check_eligibility(person: Person, service_type: str) -> bool: ...
        """Calculate eligibility for various services based on person's data."""
    ```

Docstrings naturally enhance the semantics of their associated code constructs, while the `sem` keyword provides an elegant way to enrich the meaning of class attributes and function arguments. Our research shows these concise semantic strings are more effective than traditional multi-line prompts.


## From: FAQ.md

```jac
    print(printgraph());  # Generates a DOT graph starting from the root node
```
```jac
    print(printgraph(node_1, bfs=True, traverse=True, edge_type=["Edge1"], node_limit=100, edge_limit=900, depth=300, dot_file='graph.dot'));
```
```jac
    print(printgraph(node_1, edge_type=["CustomEdge"]));
```


## From: friendzone-lite.md

- **Memory Processing Function**: `update_memory_details()` - AI-powered memory extraction and refinement


## From: usage.md

## byLLM for Functions

### Basic Functions

Functions can be integrated with LLM capabilities by adding the `by llm` declaration. This eliminates the need for manual API calls and prompt engineering:

```jac linenums="1"
import from byllm.llm { Model }

glob llm = Model(model_name="gpt-4o");

def translate(text: str, target_language: str) -> str by llm();

def analyze_sentiment(text: str) -> str by llm();

def summarize(content: str, max_words: int) -> str by llm();
```

These functions process natural language inputs and generate contextually appropriate outputs.

### Functions with Reasoning

The `method='Reason'` parameter enables step-by-step reasoning for complex tasks:

```jac linenums="1"
import from byllm.llm { Model }

glob llm = Model(model_name="gpt-4o");

def analyze_sentiment(text: str) -> str by llm(method='Reason');

def generate_response(original_text: str, sentiment: str) -> str by llm();

with entry {
    customer_feedback = "I'm really disappointed with the product quality. The delivery was late and the item doesn't match the description at all.";

    # Function performs step-by-step sentiment analysis
    sentiment = analyze_sentiment(customer_feedback);

    # Function generates response based on sentiment
    response = generate_response(customer_feedback, sentiment);

    print(f"Customer sentiment: {sentiment}");
    print(f"Suggested response: {response}");
}
```

### Structured Output Functions

byLLM supports generation of structured outputs. Functions can return complex types:

```jac linenums="1"
obj Person {
    has name: str;
    has age: int;
    has description: str | None;
}

def generate_random_person() -> Person by llm();

with entry {
    person = generate_random_person();
    assert isinstance(person, Person);
    print(f"Generated Person: {person.name}, Age: {person.age}, Description: {person.description}");
}
```

A more complex example using object schema for context and structured output generation is demonstrated in the [game level generation](../examples/mtp_examples/rpg_game.md) example.

## Adding Explicit Context for Functions, Methods and Objects

Providing appropriate context is essential for optimal LLM performance. byLLM provides multiple methods to add context to functions and objects.

### Adding Context with Docstrings

Docstrings provide context for LLM-integrated functions. byLLM uses docstrings to understand function purpose and expected behavior.

```jac linenums="1"
import from byllm.llm { Model }

glob llm = Model(model_name="gpt-4o");

"""Translate text to the target language."""
def translate(text: str, target_language: str) -> str by llm();

"""Generate a professional email response based on the input message tone."""
def generate_email_response(message: str, recipient_type: str) -> str by llm();
```

### Adding Context with Semantic Strings (Semstrings)

Jaclang provides semantic strings using the `sem` keyword for describing object attributes and function parameters. This is useful for:

- Describing object attributes with domain-specific meaning
- Adding context to parameters
- Providing semantic information while maintaining clean code

```jac linenums="1"
obj Person {
    has name;
    has dob;
    has ssn;
}

sem Person = "Represents the personal record of a person";
sem Person.name = "Full name of the person";
sem Person.dob = "Date of Birth";
sem Person.ssn = "Last four digits of the Social Security Number of a person";

"""Calculate eligibility for various services based on person's data."""
def check_eligibility(person: Person, service_type: str) -> bool by llm();
```

### Additional Context with `incl_info`

The `incl_info` parameter provides additional context to LLM methods for context-aware processing:

```jac linenums="1"
import from byllm.llm { Model }
import from datetime { datetime }

glob llm = Model(model_name="gpt-4o");

obj Person {
    has name: str;
    has date_of_birth: str;

    # Uses the date_of_birth attribute and "today" information
    # from incl_info to calculate the person's age
    def calculate_age() -> str by llm(
        incl_info={
            "today": datetime.now().strftime("%d-%m-%Y"),
        }
    );
}
```

### When to Use Each Approach

- **Docstrings**: Use for function-level context and behavior description
- **Semstrings**: Use for attribute-level descriptions and domain-specific terminology
- **incl_info**: Use to selectively include relevant object state in method calls

The `sem` keyword can be used in [separate implementation files](../../jac_book/chapter_5.md#declaring-interfaces-vs-implementations) for improved code organization and maintainability.

In this example:

- `greet("Alice")` executes the normal function and returns `"Hello Alice"`
- `greet("Alice") by llm()` overrides the function with LLM behavior
- `format_data(user_data) by llm()` transforms data formatting into human-readable presentation

## Tool-Calling Agents with ReAct

The ReAct (Reasoning and Acting) method enables agentic behavior by allowing functions to reason about problems and use external tools. Functions can be made agentic by adding the `by llm(tools=[...])` declaration.

```jac linenums="1"
import from byllm.lib { Model }
import from datetime { datetime }

glob llm = Model(model_name="gpt-4o");

obj Person {
    has name: str;
    has dob: str;
}

"""Calculate the age of the person where current date can be retrieved by the get_date tool."""
def calculate_age(person: Person) -> int by llm(tools=[get_date]);

"""Get the current date in DD-MM-YYYY format."""
def get_date() -> str {
    return datetime.now().strftime("%d-%m-%Y");
}

with entry {
    mars = Person("Mars", "27-05-1983");
    print("Age of Mars =", calculate_age(mars));
}
```

A comprehensive tutorial on [building an agentic application is available here.](../examples/mtp_examples/fantasy_trading_game.md)

## Streaming Outputs

The streaming feature enables real-time token reception from LLM functions, useful for generating content where results should be displayed as they are produced.

Set `stream=True` in the invoke parameters to enable streaming:

```jac linenums="1"
import from byllm.lib { Model }

glob llm = Model(model_name="gpt-4o-mini");

""" Generate short essay (less than 300 words) about the given topic """
def generate_essay(topic: str) -> str by llm(stream=True);


with entry {
    topic = "The orca whale and it's hunting techniques";
    for tok in generate_essay(topic) {
        print(tok, end='', flush=True);
    }
    print(end='\n');
}
```

The `stream=True` parameter only supports `str` output type. Tool calling is not currently supported in streaming mode but will be available in future releases.


## From: streamlit.md

```jac
def simple_calculator() {
    st.title("🧮 Simple Calculator");
    st.write("A basic calculator built with Jac and Streamlit");

    # Create two columns for inputs
    columns = st.columns(2);
    col1 = columns[0];
    col2 = columns[1];

    with col1 {
        num1 = st.number_input("First number:", value=0.0);
    }

    with col2 {
        num2 = st.number_input("Second number:", value=0.0);
    }

    # Operation selection
    operation = st.selectbox(
        "Choose operation:",
        ["Add", "Subtract", "Multiply", "Divide"]
    );

    # Calculate result
    if st.button("Calculate") {
        if operation == "Add" {
            result = num1 + num2;
        } elif operation == "Subtract" {
            result = num1 - num2;
        } elif operation == "Multiply" {
            result = num1 * num2;
        } elif operation == "Divide" {
            if num2 != 0 {
                result = num1 / num2;
            } else {
                st.error("Cannot divide by zero!");
                return;
            }
        }

        st.success("Result: " + str(result));

        # Add to history
        if "history" not in st.session_state {
            st.session_state.history = [];
        }

        st.session_state.history.append(
            str(num1) + " " + operation.lower() + " " + str(num2) + " = " + str(result)
        );
    }

    # Show calculation history
    if "history" in st.session_state and st.session_state.history {
        st.subheader("📝 History");
        for calc in st.session_state.history {
            st.write("• " + calc);
        }

        if st.button("Clear History") {
            st.session_state.history = [];
            st.rerun();
        }
    }
}
```
```jac
def todo_app() {
    st.title("📋 Todo App");
    st.write("A simple todo application built with Jac and Streamlit");

    # Initialize session state
    if "todos" not in st.session_state {
        st.session_state.todos = [];
    }

    # Add new todo
    with st.form("add_todo") {
        new_todo = st.text_input("Add a new todo:");

        if st.form_submit_button("Add Todo") and new_todo {
            st.session_state.todos.append(new_todo);
            st.success("Todo added!");
        }
    }

    # Display todos
    if st.session_state.todos {
        st.subheader("📝 Your Todos");

        todos_to_remove = [];

        for todo in st.session_state.todos {
            columns = st.columns([4, 1]);

            with columns[0] {
                st.write("• " + todo);
            }

            with columns[1] {
                if st.button("Remove", key=todo) {
                    todos_to_remove.append(todo);
                }
            }
        }

        # Remove completed todos
        for todo in todos_to_remove {
            st.session_state.todos.remove(todo);
        }

        if todos_to_remove {
            st.rerun();
        }

        # Clear all button
        if st.button("Clear All") {
            st.session_state.todos = [];
            st.rerun();
        }
    } else {
        st.info("No todos yet! Add one above.");
    }

    # Show count
    if st.session_state.todos {
        st.write("Total todos: " + str(len(st.session_state.todos)));
    }
}
```
```jac
def make_api_call(token: str, endpoint: str, payload: dict) -> dict {
    response = requests.post(
        "http://localhost:8000/" + endpoint,
        json=payload,
        headers={"Authorization": "Bearer " + token}
    );
    return response.json() if response.status_code == 200 else {};
}
```


## From: fantasy_trading_game.md

```jac
def make_player() -> Person by llm();

def make_random_npc() -> Person by llm();
```
These AI functions generate characters with appropriate attributes, starting money, and themed inventory items.
```jac
def make_transaction(buyer_name: str, seller_name: str, item_name: str, price: int| None = None) -> bool {
    buyer = person_record[buyer_name];
    seller = person_record[seller_name];

    # Find item in seller's inventory
    item_to_buy = None;
    item_index = -1;
    for i in range(len(seller.inventory)) {
        if seller.inventory[i].name.lower() == item_name.lower() {
            item_to_buy = seller.inventory[i];
            item_index = i;
            break;
        }
    }

    price = price or item_to_buy.price;

    # Validate transaction
    if not item_to_buy or buyer.money < price {
        return False;
    }

    # Execute transfer
    buyer.money -= price;
    seller.money += price;
    buyer.inventory.append(item_to_buy);
    seller.inventory.pop(item_index);
    return True;
}
```
**Transaction processing:**
1. Locates the item in the seller's inventory
2. Validates the buyer has sufficient funds
3. Transfers money and items between characters

### AI Functions (Stateless)

AI-integrated functions that operate without persistent state:
- `make_player()` and `make_random_npc()` - Generate characters but don't retain memory
- These are AI-powered utilities, not agents


## From: tutorial.md

```Jac
import from byllm.lib { Model }

glob llm = Model(model_name="openai/gpt-5", verbose=True);

"""
Summarize relevant part of each option to the initial query not in current conversation history
"""
def summarize(presented_option: list[str], convo_history: list[dict]) -> str by llm();
```
Once defined, this function can be called like any regular function through byllm handling response generation and input/outputs formatting behind the scenes.
```
obj Response{
    has option: str;
    has selection: str;
    has explanation: str;
}

sem Response = "Structured response used by an agentic traversal logic.";
sem Response.option = "A control token defining action: @selected@, @query@, or @end@.";
sem Response.selection = "The chosen node, search query, or final response.";
sem Response.explanation = "A short justification for why this decision was made.";

"""Decide which option is best. Choose one of the emails our current person has sent/received, semantic search for a new email to explore, or answer the initial query"""
def choose_next_email_node(person: str, sent: list[str], received: list[str], conversation_history: list[dict]) -> Response by llm();
```
Finally, we declare the function itself. The signature includes:
- A short docstring describing the function's purpose
- Input and output type definitions
- The by llm modifier, telling Jac that this function is backed by an LLM rather than a traditional implementation.

With these three pieces in place, Jac handles everything under the hood, from building the structured prompt to formatting the model output into the expected type.

Unlike traditional prompt engineering, the docstring here does not need to carry the full cognitive load. Because byllm includes context from variable names, type signatures, and semstrings, the docstring should stay concise. Short guidance performs better than long paragraphs of instruction.

During traversal, the agent first collects all relevant context from the current node,such as emails sent and received by the person, and appends this information to the conversation history. This ensures the agent has a memory of what it has already seen.

Next, the agent calls the LLM-backed decision function:

```jac
response = choose_next_email_node(person_formatted, sent_formatted, received_formatted, conversation_history);
```

The function returns a structured Response object. Based on the option field in this response, the walker takes the appropriate action:

- @selected@: Move to the chosen neighboring node and continue traversal
- @query@: Perform a semantic search for additional relevant emails outside immediate neighbors
- @end@: Stop traversal and return the final answer to the user


## From: jac_serve.md

When you run `jac serve`, it:
1. Executes your target Jac module
2. Converts all functions into REST API endpoints with introspected signatures

#### GET /functions
List all available functions in the module.

**Example:**
```bash
curl http://localhost:8000/functions \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "functions": ["add_numbers", "greet", "calculate_stats"]
}
```

#### GET /function/<name>
Get the signature and parameter information for a specific function.

**Example:**
```bash
curl http://localhost:8000/function/add_numbers \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "name": "add_numbers",
  "signature": {
    "parameters": {
      "a": {
        "type": "int",
        "required": true,
        "default": null
      },
      "b": {
        "type": "int",
        "required": true,
        "default": null
      }
    "return_type": "int"
  }
}
```

#### POST /function/<name>
Call a function with the provided arguments.

**Request Body:**
```json
{
  "args": {
    "a": 5,
    "b": 10
  }
}
```

**Response:**
```json
{
  "result": 15,
  "reports": []
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/function/add_numbers \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"args": {"a": 5, "b": 10}}'
```

### 3. Call a function
```bash
curl -X POST http://localhost:8000/function/add_numbers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"args": {"a": 15, "b": 27}}'
```

1. **Automatic API Generation**: Functions and walkers automatically become REST endpoints
2. **Type Introspection**: Function signatures are analyzed to generate API documentation


## From: rpg_game.md

```jac
obj LevelManager {
    has current_level: int = 0, current_difficulty: int = 1,
        prev_levels: list[Level] = [], prev_level_maps: list[Map] = [];

    def create_next_level (last_levels: list[Level], difficulty: int, level_width: int, level_height: int)
    -> Level by llm();

    def create_next_map(level: Level) -> Map by llm();
}
```
- For `create_next_level()` (Line 26), we pass these arguments to retuen a complete level as the output:
    - Historical Context: last_levels ensures variety
    - Difficulty Guidance: difficulty scales challenge
    - Spatial Constraints: level_width, level_height

- For `create_next_map()` (Line 29) we return a detailed map as the output by:
    - Taking a high-level `Level`
    - Generating specific positions for walls, enemies, and player
    - Producing a balanced, playable layout
```jac
def get_next_level -> tuple(Level, Map) {
    self.current_level += 1;

    # Keeping Only the Last 3 Levels
    if len(self.prev_levels) > 3 {
        self.prev_levels.pop(0);
        self.prev_level_maps.pop(0);
    }

    # Generating the New Level
    new_level = self.create_next_level(
        self.prev_levels,
        self.current_difficulty,
        20, 20
    );

    self.prev_levels.append(new_level);

    # Generating the Map of the New Level
    new_level_map = self.create_next_map(new_level);
    self.prev_level_maps.append(new_level_map);

    # Increasing the Difficulty for end of every 2 Levels
    if self.current_level % 2 == 0 {
        self.current_difficulty += 1;
    }

    return (new_level, new_level_map);
}
```
This method executes the following sequence:

1. **Level Counter**: Increments the level number
2. **Memory Management**: Keeps only the last 3 levels
3. **AI Level Generation**: Calls the AI to create a new level
4. **AI Map Generation**: Requests the AI to generate map
5. **Difficulty Progression**: Increases difficulty every 2 levels
6. **Return Results**: Returns both the level config and detailed map
```jac
def get_map(map: Map) -> str {
    map_tiles = [['.' for _ in range(map.level.width)] for _ in range(map.level.height)];

    # Place walls
    for wall in map.walls {
        for x in range(wall.start_pos.x, wall.end_pos.x + 1) {
            for y in range(wall.start_pos.y, wall.end_pos.y + 1) {
                map_tiles[y-1][x-1] = 'B';
            }
        }
    }

    # Place obstacles, enemies, and player
    for obs in map.small_obstacles {
        map_tiles[obs.y-1][obs.x-1] = 'B';
    }
    for enemy in map.enemies {
        map_tiles[enemy.y-1][enemy.x-1] = 'E';
    }
    map_tiles[map.player_pos.y-1][map.player_pos.x-1] = 'P';

    # Add border walls
    map_tiles = [['B'] + row + ['B'] for row in map_tiles];
    map_tiles = [['B' for _ in range(map.level.width + 2)]] + map_tiles + [['B' for _ in range(map.level.width + 2)]];
    return [''.join(row) for row in map_tiles];
}
```

