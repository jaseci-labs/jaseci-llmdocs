# Jac Language Reference

# 1. TYPES

`int` `float` `str` `bool` `bytes` `any`; `list[T]` `dict[K,V]` `set[T]`; `int|None` for optional

`has x: int;` `has y: str = "default";` `-> ReturnType`

`True`/`False` (true/false FAIL at runtime)

Non-default attrs MUST precede default: `has y: str; has x: int = 0;`

Tuple unpacking requires parens: `(a, b) = func();`

# 2. CONTROL

```jac
if x > 0 { print("pos"); } elif x == 0 { print("zero"); } else { print("neg"); }
for i in range(10) { print(i); }
for (i, x) in enumerate(items) { print(i, x); }  # Parens required
while cond { break; }
match x { case 1: print("one"); case "hi": print("hi"); case _: print("other"); }
try { risky(); } except ValueError as e { print(e); } finally { cleanup(); }
```

No ternary `?:` — use `(a) if cond else (b)`; no `pass` — use `{}` or comment; `case` uses COLON not braces

# 3. FUNCTIONS

```jac
def add(x: int, y: int) -> int { return x + y; }
f = lambda x: int -> int : x * 2;                    # Expression form
g = lambda x: int -> int { return x * 2; };           # Block form (MUST return)
lambda e: any -> None { 0; }                          # Empty lambda body
items.sort(key=lambda x: dict -> float : x["v"]);     # Lambda as arg
"hello" |> print;                                      # Pipe operator
glob counter: int = 0;                                 # Module-level global
```

Top-level: only declarations. Executable statements MUST go inside `with entry { }` or a function body.

Block lambdas REQUIRE `return`; expression lambdas cannot have assignments.

`f-strings`: `f"Hello {name}"` (server only; cl{} uses `+` concatenation)

# 4. IMPORTS

```jac
import os;                              # Plain import (semicolon)
import from math { sqrt }               # Named import (NO semicolon after })
include sub_module;                     # Include .jac file
```

In `__init__.jac`: `include pkg.module;` (full dotted paths)

WRONG: `import from math, sqrt;` — no `import:py` or `import:jac` exists

# 5. ARCHETYPES

```jac
node Person { has name: str; has age: int = 0; }
edge Friend { has since: int = 2020; }
walker Visitor { has target: str; }
obj Config { has debug: bool = False; }
enum Color { RED, GREEN, BLUE }
node Employee(Person) { has salary: int; }           # Inheritance
```

`can` for abilities (entry/exit triggers); `def` for regular methods

```jac
obj MyObj {
    has x: int = 0;
    has y: int by postinit;
    def postinit { self.y = self.x * 2; }
}
```

Impl blocks: `impl Walker.ability { code }`

Docstrings go BEFORE declarations, not inside bodies.

Reserved keywords (`node` `walker` `edge` `obj` `enum` `can` `has`): NEVER use as variable names.

# 6. ACCESS

`has :pub name: str;` or `has:pub name: str;` — both valid

`:pub` public; `:priv` private; `:protect` protected

# 7. GRAPH

```jac
a ++> b;                                # Untyped forward (returns list)
a +>: Friend(since=2020) :+> b;        # Typed forward
a <+: Friend() :<+ b;                  # Typed backward
a <++> b;                               # Undirected
a del--> b;                             # Disconnect
[-->]                                   # Untyped traversal
[->:Friend:->]                         # Typed traversal
[<-:Friend:<-]                         # Backward typed traversal
[->:E1:->->:E2:->]                     # Chained typed
[-->](?:Person)                         # Type filter
[-->](?:Person, age > 18)              # Type + attr filter
[-->](?age > 18)                       # Untyped attr filter
[->:Friend:since > 2020:->]           # Edge attr filter
neighbors = [city_a ->:Road:->];       # Variable node traversal
untyped = [node_var -->];              # Variable untyped
root +>: E() :+> (end := A(val=10));   # Walrus in connect
```

Untyped connect returns list; use `[0]` for single. `visit : 0 : [-->];` visits first only.

WRONG: `a ++> E() ++> b;` `[-->:E:]` `del a --> b;` `[-->:E:->]`

# 8. ABILITIES

```jac
node Room {
    can on_enter with Visitor entry { print(f"Entering {self.name}"); }
    can on_exit with Visitor exit { print(f"Leaving {self.name}"); }
}
walker Visitor {
    can act with Root | Room entry { visit [-->]; }
}
```

`self` = current archetype; `here` = current node; `visitor` = visiting walker

Root type is `Root` (capital R). Union: `can act with Root | MyNode entry { }`

# 9. WALKERS

```jac
root spawn MyWalker();                  # Spawn form 1
MyWalker() spawn root;                  # Spawn form 2
visit [-->];                            # Visit connected nodes
visit : 0 : [-->];                      # Visit first only
report data;                            # Add to response
disengage;                              # Stop traversal entirely
skip;                                   # Skip to next node
```

Spawn on variable: `result = root spawn W();` — `result.reports` contains reported values.

NEVER spawn on bare keyword `node`; use `root` or a variable.

# 10. BY_LLM

```jac
import from byllm.lib { Model }
glob llm = Model(model_name="gpt-4o-mini");

obj Analysis { has sentiment: str; has score: int; }
sem Analysis.sentiment = "overall emotional tone";

"""Analyze the given text."""
def analyze(text: str) -> Analysis by llm();

enum Priority { HIGH = "urgent tasks", MEDIUM = "normal tasks", LOW = "can wait" }
"""Classify priority."""
def classify(task: str) -> Priority by llm(temperature=0.3);
```

`by llm;` or `by llm();` both valid. `by llm(temperature=0.7)` for params. No import needed for basic `by llm`.

Semstrings: `sem obj.field = "description";` guides LLM output.

# 11. FILE_JSON

```jac
import json;
f = file.open("data.txt", "r");
content = f.read();
data = json.loads('{"key": "val"}');
out = json.dumps(data);
```

WARNING: avoid naming variables `file` or `json` — shadows builtins.

# 12. API

```jac
walker :pub GetItems {
    has items: list = [];
    obj __specs__ { static has methods: list = ["POST"]; }
    can collect with Root entry { self.items = [-->](?:Item); report self.items; }
}
```

`jac start main.jac` starts server. Walker endpoint: `POST /walker/GetItems`

`:pub` on walker = public (no auth). Without `:pub` = requires auth token.

`:pub` walker on root: READ-ONLY. Graph writes silently fail when `here` is root.

Custom auth: make ALL walkers `:pub`, handle auth manually inside walker body.

`__specs__` controls `methods`/`path`/`websocket` ONLY, NOT auth. WRONG: `static has auth: bool = False;`

# 13. WEBSOCKET

```jac
async walker :pub Echo {
    obj __specs__ { static has methods: list = ["websocket"]; }
    async can echo with Root entry { report "connected"; }
}
```

Endpoint: `ws://localhost:8000/ws/Echo`; use `report` to send messages; `notify` for server push.

# 14. WEBHOOKS

```jac
walker :pub OnPayment {
    obj __specs__ { static has methods: list = ["POST"]; static has path: str = "/webhook/payment"; }
    can handle with Root entry { report "ok"; }
}
```

# 15. SCHEDULER

```jac
walker :pub Cleanup {
    obj __specs__ { static has schedule: dict = {"trigger": "interval", "seconds": 60}; }
    can run with Root entry { report "cleaned"; }
}
```

# 16. ASYNC

```jac
async walker :pub LongTask {
    obj __specs__ { static has methods: list = ["POST"]; }
    async can run with Root entry { report "done"; }
}
```

Async walkers return task status; poll for completion.

# 17. PERMISSIONS

```jac
node.__jac__.grant(target_root, Perm.READ);
node.__jac__.revoke(target_root, Perm.READ);
node.__jac__.check_access(target_root);
```

Levels: `Perm.READ`, `Perm.WRITE`, `Perm.ADMIN`

# 18. PERSISTENCE

Nodes/edges auto-persist with Jaseci runtime. `save` explicit commit; references maintained across sessions; `delete` removes node and edges.

# 19. TESTING

```jac
test add_numbers { assert 1 + 1 == 2; }
test graph_build { root ++> node(); assert len([root -->]) == 1; }
```

Test names are identifiers, NOT strings. WRONG: `test "my test" { }`

# 20. STDLIB

Builtins: `print` `len` `range` `enumerate` `zip` `map` `filter` `sorted` `isinstance` `type` `str` `int` `float` `list` `dict` `set`

String: `.upper()` `.lower()` `.strip()` `.split()` `.replace()` `.startswith()` `.endswith()` `.format()`

List: `.append()` `.extend()` `.pop()` `.remove()` `.sort()` `.reverse()` `.index()`

Dict: `.keys()` `.values()` `.items()` `.get()` `.update()` `.pop()`

# 21. JSX/CLIENT

Files ending `.cl.jac` are auto client-side (no `cl{}` wrapper needed). Do NOT `include` them.

```jac
# In .cl.jac files:
import from "@jac/runtime" { Router, Routes, Route, Link, Navigate, useNavigate }

def:pub App -> any {
    has count: int = 0;                              # has = reactive state
    <div className="app">
        <h1>{"Count: " + String(count)}</h1>
        <button onClick={lambda e: any -> None { count = count + 1; }}>
            {"Increment"}
        </button>
    </div>;
}
```

`sv import from walkers { W }` — `sv` prefix for server imports in `.cl.jac`

`useEffect(lambda -> None { fetchData(); }, []);` — lifecycle hook, NOT `can with entry`

`async def fetchData() -> None { result = root spawn GetItems(); }` — root spawn compiles to `await`, function MUST be `async def`; sends POST, walker `__specs__` MUST include `"POST"`

JS builtins in cl{}: `.length` not `len()`; `String(x)` not `str(x)`; `parseInt(x)` not `int(x)`; `Math.min/max`; `.trim()` not `.strip()`; no `range()`; no f-strings (use `+`); no tuple unpacking; no `new`; `className` not `class`

CSS: `import "./styles.css";`

Conditional rendering: `{(expr) if cond else (expr)}`; `{(<div/>) if show else (<span/>)}`

JSX comprehensions: `{[<li>{String(i)}</li> for i in items]}`

Component props/callbacks: `def:pub Child(props: dict) -> any { ... }` — pass callbacks as props

Routing: `<Router><Routes><Route path="/" element={<App/>}/></Routes></Router>`

# 22. CLIENT_AUTH

```jac
import from "@jac/runtime" { jacSignup, jacLogin, jacLogout, jacIsLoggedIn }

async def handleLogin() -> None {
    result = jacLogin(email, password);
}
```

`jacSignup(email, password)`; `jacLogin(email, password)`; `jacLogout()`; `jacIsLoggedIn()` returns bool

Per-user isolation: each authenticated user gets their own graph root.

# 23. JAC.TOML

```toml
[project]
name = "myapp"
entry-point = "main.jac"

[dependencies.npm]
jac-client-node = "1.0.4"
tailwindcss = "^4.0.0"
"@tailwindcss/postcss" = "^4.0.0"

[serve]
base_route_app = "app"
```

ALL npm deps in `jac.toml`; NEVER `npm install` in `.jac/client/`. `.jac/` is auto-generated, never modify.

# 24. FULLSTACK_SETUP

```bash
jac create --use client myapp    # Create project (not --use fullstack)
cd myapp && jac install          # Sync all dependencies
jac add --npm react-icons        # Add npm package
```

Project structure: `main.jac` (wiring/entry), `walkers.jac`, `frontend.cl.jac`, `components/*.cl.jac`

`include` in `__init__.jac`: full dotted paths (`include pkg.module;`)

# 25. DEV_SERVER

```bash
jac start main.jac --dev         # Dev mode with hot reload
jac start main.jac --port 8000   # Vite frontend port (default 8000)
jac start main.jac --api_port 8001  # Backend port (auto-proxied)
jac start main.jac --no-client   # Backend only
```

# 26. DEPLOY_ENV

```bash
jac start main.jac --scale       # Production mode (no -t flag)
```

Jaseci runtime for persistence/auth; jaclang for standalone.

`.env` not auto-loaded:
```jac
import from dotenv { load_dotenv }
glob _: bool = load_dotenv() or True;
```

Docker: standard Python image, `pip install jaclang`, `jac start main.jac`

---

# PATTERNS

## Pattern 1: Fullstack Counter (Single File)

```jac
# main.jac
node Counter { has count: int = 0; }

walker :pub GetCount {
    has count: int = 0;
    obj __specs__ { static has methods: list = ["POST"]; }
    can get with Root entry {
        counts = [-->](?:Counter);
        if counts.length == 0 { root ++> Counter(); counts = [-->](?:Counter); }
        self.count = counts[0].count;
        report self.count;
    }
}

walker :pub Increment {
    has count: int = 0;
    obj __specs__ { static has methods: list = ["POST"]; }
    can inc with Root entry {
        counts = [-->](?:Counter);
        if counts.length == 0 { root ++> Counter(); counts = [-->](?:Counter); }
        counts[0].count += 1;
        self.count = counts[0].count;
        report self.count;
    }
}

sv {
    import from walkers { GetCount, Increment }
}

cl {
    def:pub app -> any {
        has count: int = 0;

        async def fetchCount() -> None {
            result = root spawn GetCount();
            count = result;
        }

        async def doIncrement() -> None {
            result = root spawn Increment();
            count = result;
        }

        useEffect(lambda -> None { fetchCount(); }, []);

        <div className="counter">
            <h1>{"Count: " + String(count)}</h1>
            <button onClick={lambda e: any -> None { doIncrement(); }}>
                {"Increment"}
            </button>
        </div>;
    }
}
```

```toml
# jac.toml
[project]
name = "counter"
entry-point = "main.jac"
[dependencies.npm]
jac-client-node = "1.0.4"
[serve]
base_route_app = "app"
```

## Pattern 2: Walker Graph Traversal

```jac
node City { has name: str; has visited: bool = False; }
edge Road { has distance: int = 0; has toll: bool = False; }

walker FindReachable {
    has reachable: list = [];

    can start with Root entry { visit [-->](?:City); }

    can explore with City entry {
        if not here.visited {
            here.visited = True;
            self.reachable.append(here.name);
            visit [->:Road:->];
        }
    }

    can done with Root exit { report self.reachable; }
}

walker DeleteRoute {
    has from_city: str;
    has to_city: str;

    can start with Root entry { visit [-->](?:City, name == self.from_city); }

    can find with City entry {
        targets = [here ->:Road:->](?:City, name == self.to_city);
        for t in targets { here del--> t; }
        report f"Deleted route {self.from_city} -> {self.to_city}";
    }
}

with entry {
    nyc = City(name="NYC");
    bos = City(name="Boston");
    dc = City(name="DC");
    chi = City(name="Chicago");

    root ++> nyc;
    nyc +>: Road(distance=200) :+> bos;
    nyc +>: Road(distance=225, toll=True) :+> dc;
    bos +>: Road(distance=800) :+> chi;
    dc +>: Road(distance=700) :+> chi;

    # Variable node traversal
    nyc_roads = [nyc ->:Road:->];
    print(f"NYC connects to {len(nyc_roads)} cities");

    # Toll roads from NYC
    toll_roads = [nyc ->:Road:toll == True:->];
    print(f"Toll roads: {len(toll_roads)}");

    result = root spawn FindReachable();
    print(result.reports);

    root spawn DeleteRoute(from_city="NYC", to_city="DC");
}
```

## Pattern 3: Multi-file CRUD + Auth + AI

```jac
# === main.jac ===
include walkers;

with entry { }

# === walkers.jac ===
import from byllm.lib { Model }
glob llm = Model(model_name="gpt-4o-mini");

enum Priority {
    HIGH = "urgent or time-sensitive",
    MEDIUM = "normal priority",
    LOW = "can be deferred"
}

node Task {
    has id: str;
    has title: str;
    has done: bool = False;
    has priority: Priority = Priority.MEDIUM;
}

sem classify_priority.title = "The task description to classify";
"""Classify task priority based on title."""
def classify_priority(title: str) -> Priority by llm(temperature=0.3);

walker AddTask {
    has title: str;
    has id: str = "";
    obj __specs__ { static has methods: list = ["POST"]; }
    can add with Root entry {
        import uuid;
        p = classify_priority(self.title);
        t = Task(id=str(uuid.uuid4()), title=self.title, priority=p);
        root +>: ChildOf() :+> t;
        report {"id": t.id, "title": t.title, "priority": str(t.priority)};
    }
}

edge ChildOf { has order: int = 0; }

walker :pub ListTasks {
    has tasks: list = [];
    obj __specs__ { static has methods: list = ["POST"]; }
    can list with Root entry {
        for t in [-->](?:Task) {
            self.tasks.append({"id": t.id, "title": t.title, "done": t.done,
                               "priority": str(t.priority)});
        }
        report self.tasks;
    }
}

walker ToggleTask {
    has id: str;
    obj __specs__ { static has methods: list = ["POST"]; }
    can toggle with Root entry {
        for t in [-->](?:Task) {
            if t.id == self.id { t.done = not t.done; report t.done; disengage; }
        }
    }
}

walker DeleteTask {
    has id: str;
    obj __specs__ { static has methods: list = ["POST"]; }
    can delete with Root entry {
        for t in [-->](?:Task) {
            if t.id == self.id { root del--> t; report True; disengage; }
        }
    }
}
```

```jac
# === frontend.cl.jac ===
import from "@jac/runtime" { jacLogin, jacSignup, jacLogout, jacIsLoggedIn,
                              Router, Routes, Route, Navigate }
sv import from walkers { AddTask, ListTasks, ToggleTask, DeleteTask }

def:pub app -> any {
    has loggedIn: bool = jacIsLoggedIn();
    <Router>
        <Routes>
            <Route path="/login" element={<LoginPage onAuth={lambda -> None {
                loggedIn = True;
            }}/>}/>
            <Route path="/" element={
                ((<TaskPage/>) if loggedIn else (<Navigate to="/login"/>))
            }/>
        </Routes>
    </Router>;
}

def:pub LoginPage(props: dict) -> any {
    has email: str = "";
    has password: str = "";
    has isSignup: bool = False;

    async def handleSubmit() -> None {
        result = (jacSignup(email, password)) if isSignup else (jacLogin(email, password));
        props["onAuth"]();
    }

    <div className="login">
        <input value={email} onChange={lambda e: any -> None { email = e.target.value; }}/>
        <input type="password" value={password}
               onChange={lambda e: any -> None { password = e.target.value; }}/>
        <button onClick={lambda e: any -> None { handleSubmit(); }}>
            {("Sign Up") if isSignup else ("Log In")}
        </button>
    </div>;
}

def:pub TaskPage -> any {
    has tasks: list = [];
    has newTitle: str = "";

    async def load() -> None { tasks = root spawn ListTasks(); }
    async def add() -> None { root spawn AddTask(title=newTitle); newTitle = ""; load(); }
    async def toggle(id: str) -> None { root spawn ToggleTask(id=id); load(); }
    async def remove(id: str) -> None { root spawn DeleteTask(id=id); load(); }

    useEffect(lambda -> None { load(); }, []);

    <div>
        <input value={newTitle} onChange={lambda e: any -> None { newTitle = e.target.value; }}/>
        <button onClick={lambda e: any -> None { add(); }}>{"Add"}</button>
        {[<div key={t["id"]}>
            <span className={("done") if t["done"] else ("")}>{t["title"]}</span>
            <span>{" [" + t["priority"] + "]"}</span>
            <button onClick={lambda e: any -> None { toggle(t["id"]); }}>{"✓"}</button>
            <button onClick={lambda e: any -> None { remove(t["id"]); }}>{"✕"}</button>
        </div> for t in tasks]}
    </div>;
}
```

---

# COMMON ERRORS

| # | WRONG | RIGHT |
|---|-------|-------|
| 1 | `entry { }` | `with entry { }` |
| 2 | `jac serve file.jac` | `jac start file.jac` |
| 3 | `import from math, sqrt;` | `import from math { sqrt }` |
| 4 | `import from math { sqrt };` | `import from math { sqrt }` |
| 5 | `a ++> Edge() ++> b;` | `a +>: Edge() :+> b;` |
| 6 | `[-->:E:]` | `[->:E:->]` |
| 7 | `del a --> b;` | `a del--> b;` |
| 8 | `str?` | `str \| None` |
| 9 | `true` / `false` | `True` / `False` |
| 10 | `case 1 { stmt; }` | `case 1: stmt;` |
| 11 | `test "name" { }` | `test name { }` |
| 12 | `catch E as e { }` | `except E as e { }` |
| 13 | `pass` | `{}` |
| 14 | `x = 1` (top-level) | `with entry { x = 1; }` |
| 15 | `` can f with `root entry `` | `can f with Root entry` |
| 16 | `[-->](?Type)` | `[-->](?:Type)` |
| 17 | `has x: int = 0; has y: str;` | `has y: str; has x: int = 0;` |
| 18 | `glob c; (inside func)` | `glob c: int = 0; (module level)` |
| 19 | `static has auth: bool = False;` | `:pub` on walker declaration |
| 20 | `jac create --use fullstack` | `jac create --use client` |
| 21 | `len(arr)` (in cl{}) | `arr.length` |
| 22 | `str(x)` (in cl{}) | `String(x)` |
| 23 | `f"hi {x}"` (in cl{}) | `"hi " + String(x)` |
| 24 | `class="btn"` (in JSX) | `className="btn"` |
| 25 | `can with entry` (in cl{}) | `useEffect(lambda -> None { }, [])` |
| 26 | `npm install pkg` (in .jac/) | `jac add --npm pkg` |
| 27 | `lambda -> None { }` | `lambda -> None { 0; }` |
| 28 | `a, b = func()` | `(a, b) = func();` |
| 29 | `[-->:E1:->-->:E2:->]` | `[->:E1:->->:E2:->]` |
| 30 | `x ? a : b` | `(a) if x else (b)` |
| 31 | `items = items + [x]` (cl{}) | `items.append(x)` |
| 32 | `def app` (cl{} entry) | `def:pub app` matching `base_route_app` |