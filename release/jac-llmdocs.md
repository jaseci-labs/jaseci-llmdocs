# Jac Language Reference

# 1. TYPES

`int` `float` `str` `bool` `bytes` `any`; `list[T]` `dict[K,V]` `set[T]`; `int|None` for optional

`has x: int;` `has y: str = "default";` `-> ReturnType`

`True`/`False` (true/false pass syntax but FAIL at runtime)

Non-default attrs MUST precede default: `has y: str; has x: int = 0;`

# 2. CONTROL

```jac
if x > 0 { print("pos"); } elif x == 0 { print("zero"); } else { print("neg"); }
for i in range(10) { print(i); }
for (i, x) in enumerate(items) { print(i, x); }  # Parens required
while cond { break; }
match x { case 1: print("one"); case _: print("other"); }  # COLON not braces
try { risky(); } except ValueError as e { print(e); } finally { cleanup(); }
```

No ternary `?:` — use `(a) if cond else (b)`. No `pass` — use `{}` or comment. Tuple unpacking: `(a, b) = func();` parens required.

# 3. FUNCTIONS

```jac
def add(x: int, y: int) -> int { return x + y; }
f = lambda x: int -> int : x * 2;                    # Expression form
g = lambda x: int -> int { return x * 2; };          # Block form (MUST return)
items.sort(key=lambda x: dict -> float : x["v"]);    # Lambda as arg
"hello" |> print;                                     # Pipe operator
glob counter: int = 0;
def increment -> int { counter += 1; return counter; }
```

Top-level: only declarations. Executable statements MUST go inside `with entry { }` or a function body.

`glob var: T = val;` at module level only. `f"Hello {name}"` for interpolation.

# 4. IMPORTS

```jac
import os;                            # Namespace import (semicolon)
import from math { sqrt }             # Selective (NO semicolon after })
include utils;                        # C-style merge into current scope
```

WRONG: `import from math, sqrt;` — No `import:py` or `import:jac` exists.

`include` = inlines code into current scope. `import` = Python-style namespace separation. Use `include` for `.jac` modules in `__init__.jac` with full dotted paths: `include pkg.module;`

```jac
with entry { print("always runs on module load"); }
with entry:__main__ { print("only when file executed directly"); }
```

# 5. ARCHETYPES

```jac
node Person { has name: str; has age: int = 0; }
edge Friend { has since: int; has closeness: int = 5; }
walker Visitor { has target: str; can visit_node with Person entry; }
obj Config { has debug: bool = False; }
enum Priority { HIGH = 1, MEDIUM = 2, LOW = 3 }
node Student(Person) { has grade: int; }          # Inheritance
walker W(BaseW) { }
```

`can` for abilities (with entry/exit); `def` for regular methods. `impl` blocks separate declaration from implementation:

```jac
node Item { has name: str; can process with Visitor entry; }
impl Item.process { print(self.name); }
```

Postinit: `has y: int by postinit; def postinit { self.y = self.x * 2; }`

Reserved keywords: `obj node walker edge enum can has` — NEVER use as variable names.

# 6. ACCESS

`has :pub x: int;` or `has:pub x: int;` — both valid. Levels: `:pub` `:priv` `:protect`

`walker :pub W { }` = public endpoint (no auth). Without `:pub` = requires auth token.

WRONG: `static has auth: bool = False;` in `__specs__` — auth controlled by `:pub` on walker.

# 7. GRAPH

```jac
a ++> b;                              # Untyped forward
a +>: Friend(since=2020) :+> b;       # Typed forward
a <+: Friend() :<+ b;                 # Typed backward
a <++> b;                             # Undirected
a del--> b;                           # Disconnect
root +>: E() :+> (end := Node());     # Walrus in connect
```

Traversal:

```jac
[-->]                                 # Untyped forward
[->:Friend:->]                        # Typed forward
[<-:Friend:<-]                        # Typed backward
[->:E1:->->:E2:->]                    # Chained typed
[-->](?:Person)                       # Type filter
[-->](?:Person, age > 18)             # Type + attr filter
[-->](?age > 18)                      # Untyped attr filter
[->:Friend:since > 2020:->]           # Edge attr filter
neighbors = [city_a ->:Road:->];      # Variable node traversal
visit : 0 : [-->];                    # Visit first only (indexed)
```

WRONG: `a ++> E() ++> b;` `[-->:E:]` `del a --> b;` — `++>` only untyped; use `+>: E() :+>` for typed.

Untyped `a ++> Node()` returns list; use `[0]` for single node.

# 8. ABILITIES

```jac
node Room {
    can on_enter with Visitor entry { print("Entering " + self.room_number); }
    can on_exit with Visitor exit { print("Leaving"); }
}
walker Visitor {
    can start with Root entry { visit [-->]; }
    can visit_room with Room entry { print("In " + here.room_number); }
}
```

`self` = current archetype instance; `here` = current node; `visitor` = visiting walker; Root type: `Root` (capital R). Union: `can act with Root | MyNode entry { }`

# 9. WALKERS

```jac
root spawn W();                       # Both spawn forms valid
W() spawn root;
result = root spawn MyWalker();
data = result.reports[0];             # Access reported data
```

`visit` QUEUES nodes for next step (NOT immediate). Code after `visit` continues.

```jac
visit [-->];                          # Queue all outgoing
visit [->:Road:->];                   # Queue via typed edge
visit [-->] else { print("leaf"); }   # Fallback at dead ends
visit self.target;                    # Visit specific node
```

`report` appends to `.reports` array. Prefer single report in `with Root exit`. Always check `.reports` before indexing.

`disengage;` — immediately stops walker. Exit abilities for ancestors will NOT run (v0.9.8+).

`skip;` — skips remaining code for current node, moves to next queued node (like `continue`).

Traversal order: recursive DFS with deferred exits. Entries depth-first, exits LIFO. root→A→B: Enter root, Enter A, Enter B, Exit B, Exit A, Exit root.

# 10. BY_LLM

```jac
import from byllm.lib { Model }
glob llm = Model(model_name="gpt-4o-mini");

obj Analysis {
    has sentiment: str;
    has summary: str;
}
sem Analysis.sentiment = "overall emotional tone";
sem Analysis.summary = "one-paragraph overview";

"""Analyze the given text."""
def analyze(text: str) -> Analysis by llm();

enum Category { TECH = "Technology", HEALTH = "Health", OTHER = "Other" }
"""Classify text into a category."""
def classify(text: str) -> Category by llm(temperature=0.3);
```

`by llm;` or `by llm();` both valid. `by llm(temperature=0.7)` for params. No import needed for basic `by llm`. Semstrings: `'meaning of field' has field: str;`

# 11. FILE_JSON

```jac
import json;
content = file.open("data.txt", "r");
data = json.loads(content);
output = json.dumps(data, indent=2);
```

Warning: `json` is a reserved-like name — avoid `has json: str;` as attribute name.

# 12. API

```jac
walker :pub GetItems {
    obj __specs__ { static has methods: list = ["POST"]; }
    can get with Root entry { report [-->](?:Item); }
}
```

`jac start main.jac` (not `jac serve`). `:pub` = public (no auth). Without `:pub` = requires auth token.

`:pub` walker on root: READ-ONLY. Graph writes silently fail when `here` is root. Use built-in auth for write access.

Custom auth: make ALL walkers `:pub`, handle auth manually inside walker body.

`__specs__` controls `methods`/`path`/`websocket` ONLY, NOT auth.

# 13. WEBSOCKET

```jac
async walker :pub Echo {
    obj __specs__ { static has methods: list = ["websocket"]; }
    async can echo with Root entry { report here; }
}
```

Endpoint: `ws://localhost:8000/ws/Echo`. Use `notify` for server push.

# 14. WEBHOOKS

```jac
walker :pub OnPayment {
    obj __specs__ { static has methods: list = ["POST"]; static has path: str = "/webhook/payment"; }
    can handle with Root entry { report "received"; }
}
```

# 15. SCHEDULER

```jac
walker :pub Cleanup {
    obj __specs__ { static has schedule: dict = {"trigger": "interval", "seconds": 3600}; }
    can run with Root entry { report "cleaned"; }
}
```

# 16. ASYNC

```jac
async walker :pub FetchData {
    async can fetch with Root entry { report "data"; }
}
async def process_items(items: list) -> list { return items; }
```

`flow` launches function as background task (thread pool), returns future. `wait` retrieves result (blocks if needed).

```jac
future = flow expensive_fn();
other = do_something_else();
result = wait future;
```

`async/await` = event loop (I/O-bound). `flow/wait` = thread pool (CPU-bound).

# 17. PERMISSIONS

```jac
node.__jac__.grant(root, Perm.READ);
node.__jac__.revoke(root, Perm.WRITE);
node.__jac__.check_access(root, Perm.READ);
```

Levels: `Perm.READ`, `Perm.WRITE`, `Perm.ADMIN`.

# 18. PERSISTENCE

Nodes/edges auto-persist with Jaseci runtime. `save` forces write; `commit` finalizes transaction. References maintained across sessions. `del` removes nodes.

# 19. TESTING

```jac
test my_test { assert 1 + 1 == 2; }
test graph_build { root ++> Node(); assert [root -->] |> len > 0; }
```

Test names are identifiers, NOT strings. WRONG: `test "my test" { }`

# 20. STDLIB

Builtins: `print` `len` `range` `enumerate` `zip` `map` `filter` `type` `isinstance` `str` `int` `float` `list` `dict` `set` `sorted` `reversed` `abs` `min` `max` `sum` `any` `all` `round` `input` `open` `hasattr` `getattr`

String: `.upper()` `.lower()` `.strip()` `.split()` `.join()` `.replace()` `.startswith()` `.endswith()` `.format()` `.find()`

List: `.append()` `.extend()` `.insert()` `.pop()` `.remove()` `.sort()` `.reverse()` `.index()` `.count()`

Dict: `.keys()` `.values()` `.items()` `.get()` `.update()` `.pop()` `.setdefault()`

# 21. JSX/CLIENT

Files ending `.cl.jac` are auto client-side (no `cl{}` wrapper needed). Do NOT `include` them.

```jac
# In .cl.jac files:
import from "@jac/runtime" { Router, Routes, Route, Link, Navigate, useNavigate }
sv import from walkers { GetItems }    # sv prefix for server imports

def:pub App -> any {
    has items: list = [];
    has loading: bool = True;

    async def fetchItems -> None {
        result = root spawn GetItems();
        items = result.reports[0] if result.reports else [];
        loading = False;
    }
    useEffect(lambda -> None { fetchItems(); }, []);

    return <div className="app">
        {(loading) if (<p>{"Loading..."}</p>) else (
            <ul>{[<li key={item.id}>{item.name}</li> for item in items]}</ul>
        )}
    </div>;
}
```

`has` = reactive state (like `useState`). `root spawn` compiles to `await`; function MUST be `async def`. `root spawn` sends POST; walker `__specs__` MUST include `"POST"`.

JS builtins in `cl{}`: `.length` not `len()`; `String(x)` not `str(x)`; `parseInt(x)` not `int(x)`; `Math.min/max`; `.trim()` not `.strip()`; no `range()`; no f-strings (use `+`); no tuple unpacking; `className` not `class`.

CSS: `import "./styles.css";`. Lifecycle: `useEffect(lambda -> None { func(); }, [])` not `can with entry`.

JSX comprehensions: `{[<li>{x}</li> for x in items]}` compiles to `.map()`. With filter: `{[<li>{x}</li> for x in items if x.active]}` compiles to `.filter().map()`.

Empty lambda body: `lambda e: any -> None { 0; }` not `{}`.

Conditional rendering: `{(cond) if (<Yes/>) else (<No/>)}`

Form handling: `lambda e: any -> None { val = e.target.value; setState(val); }`

Component props/callbacks: pass as attributes `<Child onDone={handler} data={items} />`

# 22. CLIENT_AUTH

```jac
import from "@jac/runtime" { jacSignup, jacLogin, jacLogout, jacIsLoggedIn }

async def handleLogin -> None {
    result = jacLogin(email, password);
    loggedIn = jacIsLoggedIn();
}
async def handleLogout -> None { jacLogout(); }
```

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

All npm deps in `jac.toml`, NEVER `npm install` in `.jac/client/`. Tailwind v4: `tailwindcss` + `@tailwindcss/postcss`.

# 24. FULLSTACK_SETUP

```
jac create myapp --use client          # Not --use fullstack
cd myapp
jac install                            # Syncs all dependencies
jac add --npm some-package             # Add npm dependency
```

`.jac/` is auto-generated, never modify manually. Project structure:

```
main.jac              # Wiring: includes, cl{} re-exports
walkers.jac           # Server walkers
frontend.cl.jac       # Client entry (auto client-side)
components/*.cl.jac   # UI components
jac.toml              # Config
```

`cl{}` `def:pub app` must match `[serve] base_route_app` in `jac.toml`.

# 25. DEV_SERVER

```
jac start main.jac --dev               # Dev mode with hot reload
jac start main.jac --dev --port 3000   # Custom Vite port
jac start main.jac --dev --api_port 9000
jac start main.jac --no-client         # Backend only
```

`--port` = Vite frontend (default 8000); `--api_port` = backend (default 8001, auto-proxied). `jac check file.jac` for syntax checking (may have false positives/negatives).

# 26. DEPLOY_ENV

```
jac start main.jac --scale             # Production with scaling (no -t)
```

Jaseci runtime for persistence/auth; jaclang for local dev. Docker: standard Python container with `pip install jaclang`.

`.env` not auto-loaded:

```jac
import from dotenv { load_dotenv }
glob _: bool = load_dotenv() or True;
```

Docstrings go before declarations, not inside bodies.

---

# COMMON ERRORS

| # | WRONG | RIGHT |
|---|-------|-------|
| 1 | `entry { }` | `with entry { }` |
| 2 | `jac serve` | `jac start file.jac` |
| 3 | `import from math, sqrt;` | `import from math { sqrt }` |
| 4 | `import from math { sqrt };` | `import from math { sqrt }` (no semicolon) |
| 5 | `a ++> E() ++> b;` | `a +>: E() :+> b;` |
| 6 | `[-->:E:]` | `[->:E:->]` |
| 7 | `del a --> b;` | `a del--> b;` |
| 8 | `case 1 { }` | `case 1: stmt;` |
| 9 | `str?` | `str \| None` |
| 10 | `true` / `false` | `True` / `False` |
| 11 | `catch E as e { }` | `except E as e { }` |
| 12 | `test "name" { }` | `test name { }` |
| 13 | `has x: int = 0; has y: str;` | `has y: str; has x: int = 0;` |
| 14 | `result.returns[0]` | `result.reports[0]` |
| 15 | `pass` | `{}` |
| 16 | `a, b = func()` | `(a, b) = func();` |
| 17 | `can with `root entry` | `can with Root entry` |
| 18 | `[-->](?Type)` | `[-->](?:Type)` |
| 19 | `glob x;` inside function | `glob x: T = val;` at module level |
| 20 | `static has auth: bool = False;` | `walker :pub W { }` |
| 21 | `jac create --use fullstack` | `jac create --use client` |
| 22 | `lambda x: int -> int { x * 2; }` | `lambda x: int -> int { return x * 2; }` |
| 23 | `x ? a : b` | `(a) if x else (b)` |
| 24 | `len(arr)` in cl{} | `arr.length` |
| 25 | `str(x)` in cl{} | `String(x)` |
| 26 | `.map(lambda x: T -> any : <li>{x}</li>)` | `{[<li>{x}</li> for x in items]}` |
| 27 | `npm install pkg` in .jac/ | `jac add --npm pkg` |
| 28 | `class` in JSX | `className` |
| 29 | `[-->:E1:->-->:E2:->]` | `[->:E1:->->:E2:->]` |
| 30 | `import:py from math { sqrt }` | `import from math { sqrt }` |

---

# PATTERN 1: Fullstack Counter

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

```jac
# main.jac
node Counter { has count: int = 0; }

walker :pub GetCount {
    obj __specs__ { static has methods: list = ["POST"]; }
    can get with Root entry {
        counters = [-->](?:Counter);
        if counters { report counters[0].count; }
        else { root ++> Counter(); report 0; }
    }
}

walker :pub Increment {
    obj __specs__ { static has methods: list = ["POST"]; }
    can inc with Root entry {
        counters = [-->](?:Counter);
        if counters { counters[0].count += 1; report counters[0].count; }
        else {
            c = Counter(count=1);
            root ++> c;
            report 1;
        }
    }
}

cl {
    sv import from main { GetCount, Increment }

    def:pub app -> any {
        has count: int = 0;
        has loading: bool = True;

        async def fetchCount -> None {
            result = root spawn GetCount();
            count = result.reports[0] if result.reports else 0;
            loading = False;
        }
        async def doIncrement -> None {
            result = root spawn Increment();
            count = result.reports[0] if result.reports else count;
        }
        useEffect(lambda -> None { fetchCount(); }, []);

        return <div className="counter">
            <h1>{"Counter"}</h1>
            {(loading) if (<p>{"Loading..."}</p>) else (
                <div>
                    <p>{"Count: " + String(count)}</p>
                    <button onClick={lambda e: any -> None { doIncrement(); }}>
                        {"Increment"}
                    </button>
                </div>
            )}
        </div>;
    }
}
```

# PATTERN 2: Walker Graph Traversal

```jac
node City { has name: str; has visited: bool = False; }
edge Road { has distance: int; has toll: bool = False; }

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

    can start with Root entry {
        visit [-->](?:City, name == self.from_city);
    }
    can find_target with City entry {
        targets = [->:Road:->](?:City, name == self.to_city);
        for t in targets { here del--> t; }
        report "deleted";
        disengage;
    }
}

with entry {
    a = City(name="NYC");
    b = City(name="Boston");
    c = City(name="Philly");

    root ++> a;
    a +>: Road(distance=200) :+> b;
    a +>: Road(distance=100, toll=True) :+> c;
    b +>: Road(distance=300) :+> c;

    # Variable node traversal
    nearby = [a ->:Road:->];
    toll_roads = [a ->:Road:toll == True:->];

    result1 = root spawn FindReachable();
    print(result1.reports[0]);

    result2 = root spawn DeleteRoute(from_city="NYC", to_city="Philly");
    print(result2.reports[0]);
}
```

# PATTERN 3: Multi-file CRUD + Auth + AI

```jac
# === main.jac ===
include walkers;

cl {
    sv import from walkers { AddTask, ListTasks, ToggleTask, DeleteTask }
    include frontend;
}
```

```jac
# === walkers.jac ===
import from byllm.lib { Model }
glob llm = Model(model_name="gpt-4o-mini");

enum Category {
    WORK = "Work",
    PERSONAL = "Personal",
    HEALTH = "Health",
    OTHER = "Other"
}

node Task {
    has id: str;
    has title: str;
    has done: bool = False;
    has category: Category = Category.OTHER;
}

sem classify_task.title = "The task description to classify";
"""Classify this task into the most appropriate category."""
def classify_task(title: str) -> Category by llm(temperature=0.3);

walker :pub AddTask {
    has title: str;
    obj __specs__ { static has methods: list = ["POST"]; }
    can add with Root entry {
        import uuid;
        cat = classify_task(self.title);
        t = Task(id=str(uuid.uuid4()), title=self.title, category=cat);
        root ++> t;
        report {"id": t.id, "title": t.title, "category": str(t.category)};
    }
}

walker :pub ListTasks {
    obj __specs__ { static has methods: list = ["POST"]; }
    can list with Root entry {
        tasks = [-->](?:Task);
        report [{"id": t.id, "title": t.title, "done": t.done,
                 "category": str(t.category)} for t in tasks];
    }
}

walker :pub ToggleTask {
    has task_id: str;
    obj __specs__ { static has methods: list = ["POST"]; }
    can toggle with Root entry {
        for t in [-->](?:Task) {
            if t.id == self.task_id { t.done = not t.done; report t.done; disengage; }
        }
    }
}

walker :pub DeleteTask {
    has task_id: str;
    obj __specs__ { static has methods: list = ["POST"]; }
    can remove with Root entry {
        for t in [-->](?:Task) {
            if t.id == self.task_id { here del--> t; report "deleted"; disengage; }
        }
    }
}
```

```jac
# === frontend.cl.jac ===
import from "@jac/runtime" { jacLogin, jacLogout, jacIsLoggedIn,
    Router, Routes, Route, Navigate }

def:pub LoginPage -> any {
    has email: str = "";
    has password: str = "";

    async def handleLogin -> None {
        jacLogin(email, password);
    }

    return <div className="login">
        <input value={email}
            onChange={lambda e: any -> None { email = e.target.value; }} />
        <input type="password" value={password}
            onChange={lambda e: any -> None { password = e.target.value; }} />
        <button onClick={lambda e: any -> None { handleLogin(); }}>
            {"Login"}
        </button>
    </div>;
}

def:pub TaskList -> any {
    has tasks: list = [];
    has newTitle: str = "";

    async def load -> None {
        result = root spawn ListTasks();
        tasks = result.reports[0] if result.reports else [];
    }
    async def add -> None {
        result = root spawn AddTask(title=newTitle);
        newTitle = "";
        load();
    }
    async def toggle(tid: str) -> None {
        root spawn ToggleTask(task_id=tid);
        load();
    }
    async def remove(tid: str) -> None {
        root spawn DeleteTask(task_id=tid);
        load();
    }
    useEffect(lambda -> None { load(); }, []);

    return <div>
        <input value={newTitle}
            onChange={lambda e: any -> None { newTitle = e.target.value; }} />
        <button onClick={lambda e: any -> None { add(); }}>{"Add"}</button>
        <ul>{[<li key={t["id"]}>
            <span className={("done") if t["done"] else ("")}>
                {t["title"] + " [" + t["category"] + "]"}
            </span>
            <button onClick={lambda e: any -> None { toggle(t["id"]); }}>
                {"✓"}
            </button>
            <button onClick={lambda e: any -> None { remove(t["id"]); }}>
                {"✗"}
            </button>
        </li> for t in tasks]}</ul>
        <button onClick={lambda e: any -> None { jacLogout(); }}>
            {"Logout"}
        </button>
    </div>;
}

def:pub app -> any {
    has loggedIn: bool = False;
    useEffect(lambda -> None { loggedIn = jacIsLoggedIn(); }, []);

    return <Router>
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/tasks" element={
                (loggedIn) if (<TaskList />) else (<Navigate to="/login" />)
            } />
        </Routes>
    </Router>;
}
```