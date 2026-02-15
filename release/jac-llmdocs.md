# Jac Language Reference

# 1. TYPES
int float str bool bytes any; list[T] dict[K,V] set[T] tuple; int|None for optionals (NOT int?)
`has x: int;` `has y: str = "default";` `-> ReturnType` for function returns
True/False capitalized (true/false pass syntax check but FAIL at runtime)
Non-default attributes MUST come before default attributes in same archetype
WRONG: `node N { has x: int = 0; has y: str; }` RIGHT: `node N { has y: str; has x: int = 0; }`
Access modifiers: `has:priv x: int;` or `has :priv x: int;` both valid; :pub :priv :protect

# 2. CONTROL
```jac
if x > 0 { print("pos"); } elif x == 0 { print("zero"); } else { print("neg"); }
for item in items { print(item); }
for i=0 to i<10 by i+=1 { print(i); }
for (i, x) in enumerate(items) { print(i, x); }
while cond { stmt; }
match x { case 1: print("one"); case "hi": print("hi"); case _: print("other"); }
try { risky(); } except ValueError as e { print(e); } finally { cleanup(); }
```
No ternary `?:` -- use `result = ("yes") if x > 0 else ("no");`
No `pass` keyword -- use `{}` or a comment
match/case uses COLON not braces: `case 1: stmt;` NOT `case 1 { stmt; }`
`except` not `catch`; parens required on `for (i, x) in enumerate()`
Tuple unpacking: `(a, b) = func();` parens required

# 3. FUNCTIONS
```jac
def add(x: int, y: int) -> int {
    return x + y;
}
def greet(name: str, greeting: str = "Hello") -> str {
    return f"{greeting}, {name}!";
}
```
Lambda expression: `f = lambda x: int -> int : x * 2;`
Lambda block (MUST have return): `f = lambda x: int -> int { return x * 2; };`
Lambda multi-param: `g = lambda x: int, y: int -> int : x + y;`
Lambda as argument: `items.sort(key=lambda x: dict -> float : x["v"]);`
Lambda with assignment MUST use block: `lambda e: any -> None { input_val = e.target.value; }`
Empty lambda body: `lambda e: any -> None { 0; }` NOT `{}`
Pipe: `"hello" |> print;`
f-strings: `f"Hello {name}"` (server-side only, NOT in cl{})
`glob var: T = val;` at module level; access by name in functions; `global var;` to mutate
Top-level: only declarations allowed. Executable statements MUST go inside `with entry { }` or a function body
Docstrings go BEFORE declarations, not inside bodies. Never name abilities list/dict/str/int or other builtins.

# 4. IMPORTS
```jac
import os;                            # Namespace import (semicolon)
import from math { sqrt }             # Selective (NO semicolon after })
import from os { getenv }             # Standard lib
```
WRONG: `import from math, sqrt;` WRONG: `import:py from os { path }`
`include utils;` = C-style merge into current scope (inlines code)
`import` = Python-style namespace separation
`__init__.jac` required for packages. Use FULL dotted paths in include:
WRONG: `include nodes;` (passes check, fails runtime) RIGHT: `include mypackage.nodes;`
`with entry { }` always runs when module loads
`with entry:__main__ { }` only runs when file executed directly (Jac's `if __name__ == "__main__"`)

# 5. ARCHETYPES
```jac
node City { has name: str; has pop: int = 0; }
edge Road { has dist: int; has toll: bool = False; }
walker Explorer { has visited: list = []; can explore with City entry { } }
obj Config { has debug: bool = False; def validate -> bool { return True; } }
enum Priority { LOW, MEDIUM, HIGH }
```
Inheritance: `obj Child(Parent) { }` `walker W(BaseW) { }` `node Special(City) { }`
`can` for abilities (with entry/exit); `def` for regular methods
Impl blocks: `impl W.ability { code }` separates declaration from implementation
Postinit: `has f: T by postinit; def postinit { self.f = val; }`
Reserved keywords: obj node walker edge enum can has -- NEVER use as variable names
WRONG: `obj = json.loads(s);` RIGHT: `data = json.loads(s);`
Boolean NOT: `not x` (Python-style). WRONG: `!x` (JS `!` does NOT exist in Jac)

# 6. ACCESS
`:pub` `:priv` `:protect` on has/def/can/walker
`has:priv x: int;` or `has :priv x: int;` both valid
`def:pub render` for public methods; `walker :pub W { }` for public endpoints
`walker:priv W { }` or `walker W { }` (without :pub) = requires auth token

# 7. GRAPH
```jac
a ++> b;                              # Untyped forward
a +>: Friend(since=2020) :+> b;       # Typed forward
a <++> b;                             # Undirected (both ways)
a <+: Road(dist=5) :<+ b;            # Backward typed
a del--> b;                           # Disconnect
people = [-->](?:Person);             # Type filter
adults = [-->](?:Person, age > 18);   # Type+attr filter
old = [-->](?age > 18);              # Untyped attr filter
friends = [->:Friend:since > 2020:->]; # Edge attr filter
neighbors = [city_a ->:Road:->];      # Variable node traversal
untyped = [node_var -->];             # Variable untyped
```
Typed traverse: `[->:E:->]` Chained: `[->:E1:->->:E2:->]` Backward: `[<-:E:<-]`
Untyped returns list: `nodes = root ++> Person(); first = nodes[0];`
Walrus: `root +>: E() :+> (end := A(val=10));`
Visit indexed: `visit : 0 : [-->];`
WRONG: `a ++> Edge() ++> b;` `[-->:E:]` `del a --> b;` `[-->:E1:->-->:E2:->]`
Always assign filter results to variable or use in expression -- never bare statement

# 8. ABILITIES
```jac
node Room {
    can on_enter with Visitor entry {
        print(f"Entering {self.name}");
    }
    can on_exit with Visitor exit {
        print(f"Leaving {self.name}");
    }
}
walker Visitor {
    can start with Root entry { visit [-->]; }
    can visit_room with Room entry { print(here.name); }
    can done with Root exit { print("finished"); }
}
```
`self` = the archetype instance; `here` = current node; `visitor` = the walker visiting
Root type: capital R `Root` in event clauses. WRONG: `can act with root entry` RIGHT: `can act with Root entry`
Union types: `can act with Root | MyNode entry { visit [-->]; }`

# 9. WALKERS
Spawn both forms valid: `root spawn Walker();` and `Walker() spawn root;`
Use root or variable, NEVER bare keyword: WRONG: `node spawn W();`
```jac
walker Searcher {
    has target: str;
    can search with Root entry {
        visit [-->];
    }
    can check with Person entry {
        if here.name == self.target {
            report here;
            disengage;
        }
        visit [-->];
    }
}
with entry {
    result = root spawn Searcher(target="Alice");
    data = result.reports[0] if result.reports else None;
}
```
`visit` QUEUES nodes for next step (NOT immediate). Code after visit continues executing.
`visit [-->] else { print("leaf"); }` for dead ends. `visit self.target;` for specific node.
`report` appends to `.reports` array. Always check `.reports` before indexing.
`disengage` immediately terminates walker. Exit abilities for ancestors will NOT execute (v0.9.8+).
`skip` skips remaining code in current node's ability, moves to next queued node (like continue).
DFS traversal: entries depth-first, exits LIFO (post-order). root->A->B: Enter root, Enter A, Enter B, Exit B, Exit A, Exit root.

# 10. BY_LLM
```jac
import from byllm.lib { Model }
glob llm = Model(model_name="gpt-4o-mini");

obj Sentiment {
    has tone: str;
    has score: float;
}
# sem Sentiment.tone = "overall emotional tone"
# sem Sentiment.score = "confidence 0.0-1.0"

"""Analyze the sentiment of this text."""
def analyze(text: str) -> Sentiment by llm();
```
`by llm;` or `by llm();` both valid. `by llm(temperature=0.7)` for params. No import needed for `by llm`.
Semstrings: `has desc: str = "" """hint for LLM""";` default value required before hint.
Sem annotations go OUTSIDE code blocks or as comments: `# sem Obj.field = "description";`
Enum classification: `enum Category { TECH, SPORTS, POLITICS } def classify(text: str) -> Category by llm;`
Inline: `summary = "long text" by llm(method="Summarize", temperature=0.3);`

# 11. FILE_JSON
```jac
import json;
with entry {
    f = open("data.json", "r");
    data = json.loads(f.read());
    f.close();
    output = json.dumps(data, indent=2);
}
```
WRONG: `obj = json.loads(s);` (obj is keyword) RIGHT: `data = json.loads(s);`

# 12. API
`jac start main.jac` starts server (NOT `jac serve`)
Every walker becomes an API endpoint at `/walker/<walker_name>`
```jac
walker :pub GetItems {
    obj __specs__ {
        static has methods: list = ["GET"];
        static has path_prefix: str = "/api";
    }
    can get with Root entry {
        report [-->](?:Item);
    }
}
walker :pub AddItem {
    has title: str;
    obj __specs__ {
        static has methods: list = ["POST"];
    }
    can add with Root entry {
        here ++> Item(title=self.title);
        report "created";
    }
}
```
`:pub` on walker = public (no auth). Without `:pub` = requires auth token.
WRONG: `static has auth: bool = False;` in __specs__. RIGHT: `walker :pub W { }`
Auth endpoints: POST `/user/register` and POST `/user/login` for built-in auth tokens.
`:pub` walker root access is READ-ONLY. Graph writes silently fail when `here` is root.
Custom auth (OAuth/JWT): make ALL walkers `:pub`, handle auth manually inside walker body.
`__specs__` controls: methods, path, path_prefix, websocket, schedule, webhook ONLY. NOT auth.

# 13. WEBSOCKET
```jac
async walker :pub Echo {
    obj __specs__ {
        static has methods: list = ["websocket"];
    }
    async can echo with Root entry {
        report here;
    }
}
```
Connect: `ws://localhost:8000/walker/Echo`
`socket.notify_users(ids, msg);` `socket.notify_channels(names, msg);` `broadcast=True` for all.
Remove `:pub` for authenticated websocket.

# 14. WEBHOOKS
```jac
walker :pub GithubHook {
    obj __specs__ {
        static has methods: list = ["POST"];
        static has webhook: dict = {"type": "header", "name": "X-Hub-Signature-256"};
    }
    can handle with Root entry { report "received"; }
}
```
Endpoint: POST `/walker/GithubHook`

# 15. SCHEDULER
```jac
walker CleanupTask {
    obj __specs__ {
        static has schedule: dict = {"trigger": "cron", "hour": "9", "minute": "0"};
        static has private: bool = True;
    }
    can run with Root entry { report "cleaned"; }
}
```
Triggers: cron (hour/minute/day_of_week), interval (seconds/minutes/hours), date (run_date)
`static has private: bool = True;` for private scheduled tasks.

# 16. ASYNC
```jac
async walker :pub AsyncWork {
    obj __specs__ { static has methods: list = ["POST"]; }
    async can work with Root entry { report "done"; }
}
```
`flow` launches function as background task (thread pool), returns future. `wait` retrieves result.
`flow` for CPU-bound parallel tasks; `async/await` for I/O-bound event loop tasks.
Task status: `task.__jac__.status;` `task.__jac__.reports;` `task.__jac__.error;`

# 17. PERMISSIONS
```jac
import from jaclang.runtimelib.access { NoPerm, ReadPerm, ConnectPerm, WritePerm }
node.__jac__.grant(root, WritePerm);
node.__jac__.revoke(root);
node.__jac__.check_access(root);
```
Levels: NoPerm < ReadPerm < ConnectPerm < WritePerm

# 18. PERSISTENCE
Nodes connected to root auto-persist across requests.
`save(node);` explicit save; `commit();` flush to DB; `&id` for node reference; `del node; commit();` delete.
Env: `DATABASE_URL` for persistence backend.

# 19. TESTING
```jac
test addition { assert 1 + 1 == 2; }
test graph_ops {
    n = Node(val=5);
    assert n.val == 5;
}
```
Test names are identifiers not strings. WRONG: `test "my test" { }` RIGHT: `test my_test { }`

# 20. STDLIB
Builtins: print len range type isinstance str int float list dict set tuple sorted reversed zip map filter
String: .upper() .lower() .strip() .split() .join() .replace() .startswith() .endswith() .format() f"..."
List: .append() .extend() .pop() .insert() .remove() .sort() .reverse() .index() .count()
Dict: .keys() .values() .items() .get() .update() .pop() .setdefault()

# 21. JSX/CLIENT
`.cl.jac` files auto-compile to client-side JS. Do NOT include via `include`.
```jac
import from react { useEffect, useState }
import from "@jac/runtime" { Router, Routes, Route, Link }
sv import from __main__ { GetCount, Increment }
import "./styles.css";

def:pub app {
    has count: int = 0;

    async def fetchCount -> None {
        result = root spawn GetCount();
        self.count = result.reports[0];
    }

    async def doIncrement -> None {
        root spawn Increment();
        self.fetchCount();
    }

    useEffect(lambda -> None { self.fetchCount(); }, []);

    <div className="app">
        <h1>{"Count: " + String(self.count)}</h1>
        <button onClick={lambda e: any -> None { self.doIncrement(); }}>
            Increment
        </button>
    </div>;
}
```
`has` = reactive state (like useState). `def:pub` = exported component.
`root spawn` compiles to await; function MUST be `async def`.
`root spawn` sends POST; walker `__specs__` MUST include "POST".
`sv import` prefix for server imports in `.cl.jac`.
Lifecycle: `useEffect(lambda -> None { func(); }, [])` not `can with entry`.
JSX comprehensions: `{[<li>{item}</li> for item in items]}` compiles to `.map()`.
Filter+map: `{[<li>{x}</li> for x in items if x.active]}`
Conditional rendering: `{<span>{"yes"}</span> if cond else <span>{"no"}</span>}`
Form handling: `lambda e: any -> None { input_val = e.target.value; }` (block form)
cl{} JS builtins: `.length` not `len()`; `String(x)` not `str(x)`; `parseInt(x)` not `int(x)`
`Math.min/max`; `.trim()` not `.strip()`; no `range()`; no f-strings (use `+`); no tuple unpacking
`className` not `class`; no `new` keyword; `items.append(x)` not `items = items + [x]` in cl{}

# 22. CLIENT_AUTH
```jac
import from "@jac/runtime" { jacSignup, jacLogin, jacLogout, jacIsLoggedIn }
```
`jacSignup(email, password)` `jacLogin(email, password)` `jacLogout()` `jacIsLoggedIn() -> bool`
Per-user graph isolation: each authenticated user gets their own root node.

# 23. JAC.TOML
```toml
[project]
name = "myapp"
entry-point = "main.jac"

[dependencies]
python-dotenv = ">=1.0.0"
byllm = ">=0.1.0"

[dependencies.npm]
jac-client-node = "1.0.4"

[dependencies.npm.dev]
"@jac-client/dev-deps" = "1.0.0"

[serve]
base_route_app = "app"
port = 8000

[plugins.client]
port = 5173
```
`[serve] base_route_app` must match `def:pub app` in cl{} and `[serve]` section.
Tailwind v4: add `tailwindcss` + `@tailwindcss/postcss` in `[dependencies.npm]`.
ALL npm deps go in jac.toml. NEVER `npm install` in `.jac/client/`.

# 24. FULLSTACK_SETUP
`jac create --use client` (NOT `--use fullstack`); `jac install` syncs all deps; `jac add --npm pkg`
`.jac/` directory auto-generated, never modify manually.
Project structure: `main.jac` (server+entry), `main.cl.jac` (client), `jac.toml`, `__init__.jac`
`__init__.jac` uses full dotted paths: `include mypackage.nodes;`

# 25. DEV_SERVER
`jac start main.jac --dev` for development with hot reload.
`--port` = Vite frontend (default 8000); `--api_port` = backend (default 8001, auto-proxied).
Proxy routes: `/walker/*` `/function/*` `/user/*` forwarded to backend.
`--no-client` to run backend only.

# 26. DEPLOY_ENV
```dockerfile
FROM python:3.11-slim
RUN pip install jaseci
COPY . /app
WORKDIR /app
CMD ["jac", "start", "main.jac"]
```
`jaseci` = full runtime (persistence/auth plugins). `jaclang` = compiler-only.
`jac start --scale` for production scaling.
Env vars: `DATABASE_URL` `JAC_SECRET_KEY` `OPENAI_API_KEY`
.env not auto-loaded: `import from dotenv { load_dotenv }` then `glob _: bool = load_dotenv() or True;`

# COMMON ERRORS
WRONG: `true/false` -> RIGHT: `True/False`
WRONG: `entry { }` -> RIGHT: `with entry { }`
WRONG: `import from math, sqrt;` -> RIGHT: `import from math { sqrt }`
WRONG: `import:py from os { path }` -> RIGHT: `import from os { path }`
WRONG: `node spawn W();` -> RIGHT: `root spawn W();` (node is keyword)
WRONG: `a ++> Edge() ++> b;` -> RIGHT: `a +>: Edge() :+> b;`
WRONG: `[-->:E:]` -> RIGHT: `[->:E:->]`
WRONG: `[-->:E1:->-->:E2:->]` -> RIGHT: `[->:E1:->->:E2:->]`
WRONG: `del a --> b;` -> RIGHT: `a del--> b;`
WRONG: `(?Type)` -> RIGHT: `(?:Type)`
WRONG: `(?Type:attr>v)` -> RIGHT: `(?:Type, attr > v)`
WRONG: `can act with root entry` -> RIGHT: `can act with Root entry`
WRONG: `test "name" { }` -> RIGHT: `test name { }`
WRONG: `obj = json.loads(s);` -> RIGHT: `data = json.loads(s);`
WRONG: `str?` -> RIGHT: `str | None`
WRONG: `jac serve file.jac` -> RIGHT: `jac start file.jac`
WRONG: `jac create --use fullstack` -> RIGHT: `jac create --use client`
WRONG: `static has auth: bool = False;` -> RIGHT: `walker :pub W { }`
WRONG: `<div class="x">` -> RIGHT: `<div className="x">`
WRONG: `len(items)` in cl{} -> RIGHT: `items.length`
WRONG: `str(x)` in cl{} -> RIGHT: `String(x)`
WRONG: `f"Hello {x}"` in cl{} -> RIGHT: `"Hello " + x`
WRONG: `items = items + [x]` in cl{} -> RIGHT: `items.append(x)`
WRONG: `lambda e: any -> None {}` -> RIGHT: `lambda e: any -> None { 0; }`
WRONG: `include nodes;` in __init__.jac -> RIGHT: `include mypackage.nodes;`
WRONG: `npm install` in .jac/client/ -> RIGHT: `jac add --npm pkgname`
WRONG: `print("x");` at top level -> RIGHT: `with entry { print("x"); }`
WRONG: `case 1 { stmt; }` -> RIGHT: `case 1: stmt;`
WRONG: `catch Error as e { }` -> RIGHT: `except Error as e { }`
WRONG: `result = x > 0 ? "y" : "n";` -> RIGHT: `result = ("y") if x > 0 else ("n");`
WRONG: `has x: int = 0; has y: str;` -> RIGHT: `has y: str; has x: int = 0;`
WRONG: `glob counter;` inside function -> RIGHT: just use `counter` directly
WRONG: `result.returns[0]` -> RIGHT: `result.reports[0]`
WRONG: `.map(lambda x -> ...)` in JSX -> RIGHT: `{[<li>{x}</li> for x in items]}`
WRONG: `pass` -> RIGHT: `{}` or comment
WRONG: `!x` -> RIGHT: `not x`

# PATTERN 1: Fullstack Counter App
```jac
# main.jac
node Counter {
    has count: int = 0;
}

walker :pub GetCount {
    obj __specs__ {
        static has methods: list = ["POST"];
    }
    can get with Root entry {
        counts = [-->](?:Counter);
        if counts {
            report counts[0].count;
        } else {
            report 0;
        }
    }
}

walker :pub Increment {
    obj __specs__ {
        static has methods: list = ["POST"];
    }
    can inc with Root entry {
        counts = [-->](?:Counter);
        if counts {
            counts[0].count += 1;
            report counts[0].count;
        }
    }
}

with entry {
    existing = [-->](?:Counter);
    if not existing {
        root ++> Counter(count=0);
    }
}
```
```jac
# main.cl.jac
import from react { useEffect }
sv import from __main__ { GetCount, Increment }

def:pub app {
    has count: int = 0;

    async def fetchCount -> None {
        result = root spawn GetCount();
        if result.reports {
            self.count = result.reports[0];
        }
    }

    async def doIncrement -> None {
        root spawn Increment();
        self.fetchCount();
    }

    useEffect(lambda -> None { self.fetchCount(); }, []);

    <div className="counter-app">
        <h1>{"Count: " + String(self.count)}</h1>
        <button onClick={lambda e: any -> None { self.doIncrement(); }}>
            {"Increment"}
        </button>
    </div>;
}
```
```toml
# jac.toml
[project]
name = "counter"
entry-point = "main.jac"

[dependencies.npm]
jac-client-node = "1.0.4"

[dependencies.npm.dev]
"@jac-client/dev-deps" = "1.0.0"

[serve]
base_route_app = "app"
port = 8000
```

# PATTERN 2: Walker Graph Traversal
```jac
node City {
    has name: str;
    has pop: int = 0;
}

edge Road {
    has dist: int;
    has toll: bool = False;
}

walker FindReachable {
    has reachable: list = [];

    can start with Root entry {
        visit [-->](?:City);
    }
    can explore with City entry {
        self.reachable.append(here.name);
        visit [->:Road:->];
    }
    can done with Root exit {
        report self.reachable;
    }
}

walker DeleteRoute {
    has from_city: str;
    has to_city: str;

    can start with Root entry {
        cities = [-->](?:City, name == self.from_city);
        if cities {
            visit cities[0];
        }
    }
    can find_target with City entry {
        targets = [->:Road:->](?:City, name == self.to_city);
        if targets {
            here del--> targets[0];
            report f"Deleted route {self.from_city} -> {self.to_city}";
        }
        disengage;
    }
}

with entry {
    nyc = City(name="NYC", pop=8000000);
    bos = City(name="Boston", pop=700000);
    dc = City(name="DC", pop=700000);
    chi = City(name="Chicago", pop=2700000);

    root ++> nyc;
    root ++> chi;
    nyc +>: Road(dist=200, toll=True) :+> bos;
    nyc +>: Road(dist=225, toll=False) :+> dc;
    bos +>: Road(dist=450, toll=True) :+> chi;

    # Variable node traversal
    nyc_roads = [nyc ->:Road:->];
    toll_roads = [nyc ->:Road:toll == True:->];
    print(f"NYC connects to {nyc_roads.length if nyc_roads else 0} cities");

    result = root spawn FindReachable();
    print(result.reports);

    root spawn DeleteRoute(from_city="NYC", to_city="Boston");
}
```

# PATTERN 3: API Endpoints with __specs__
```jac
node Todo {
    has id: str;
    has title: str;
    has done: bool = False;
    has priority: str = "medium";
}

walker :pub ListTodos {
    obj __specs__ {
        static has methods: list = ["GET", "POST"];
        static has path_prefix: str = "/api";
    }
    can list with Root entry {
        report [-->](?:Todo);
    }
}

walker :pub AddTodo {
    has title: str;
    has priority: str = "medium";

    obj __specs__ {
        static has methods: list = ["POST"];
    }
    can add with Root entry {
        import uuid;
        new_todo = Todo(
            id=str(uuid.uuid4()),
            title=self.title,
            priority=self.priority
        );
        here ++> new_todo;
        report new_todo;
    }
}

walker :pub FilterTodos {
    has filter_by: str = "all";

    obj __specs__ {
        static has methods: list = ["POST"];
    }
    can filter with Root entry {
        todos = [-->](?:Todo);
        match self.filter_by {
            case "high": report [t for t in todos if t.priority == "high"];
            case "done": report [t for t in todos if t.done];
            case "pending": report [t for t in todos if not t.done];
            case _: report todos;
        }
    }
}

walker :pub CompleteTodo {
    has todo_id: str;

    obj __specs__ {
        static has methods: list = ["POST"];
    }
    can complete with Root entry {
        todos = [-->](?:Todo, id == self.todo_id);
        if todos {
            todos[0].done = True;
            report todos[0];
        } else {
            report {"error": "not found"};
        }
    }
}
```