# Jac Language Reference (v0.12)

# 1. TYPES
int float str bool bytes any; list[T] dict[K,V] set[T] tuple[T,...]; int|None for optionals (NOT int?)
`has x: int;` `has y: str = "default";` `-> ReturnType` for function returns
True/False capitalized (true/false pass syntax check but FAIL at runtime)
Non-default attributes MUST come before default attributes in same archetype
WRONG: `node N { has x: int = 0; has y: str; }` RIGHT: `node N { has y: str; has x: int = 0; }`
Type aliases: `type Json = str | int | float | bool | None | list[Json] | dict[str, Json];`
Generic types: `obj Result[T, E = Exception] { has value: T | None = None; }`
Static fields: `static has count: int = 0;`

# 2. CONTROL
```jac
if x < 5 { print("low"); } elif x < 10 { print("mid"); } else { print("high"); }
for item in items { print(item); }
for i=0 to i<10 by i+=1 { print(i); }
for (i, x) in enumerate(items) { print(i, x); }  # Parens required
while n > 0 { n -= 1; } else { print("done"); }
```
Match/case: COLON then statement, NO braces per case.
```jac
match value {
    case 1: print("one");
    case 2 | 3: print("two or three");
    case x if x > 5: print(f"big: {x}");
    case _: print("other");
}
```
WRONG: `case 1 { stmt; }` WRONG: `case "hi": { stmt; }` RIGHT: `case "hi": stmt;` RIGHT: `case "hi": if True { stmt1; stmt2; }`
Try/except: `try { } except TypeError as e { } finally { }` (NOT catch)
No ternary `?:` -- use `result = ("yes") if x > 0 else ("no");`
No `pass` keyword -- use `{}` or a comment

# 3. FUNCTIONS
```jac
def greet(name: str) -> str { return f"Hello, {name}!"; }
def:pub api_fn() -> dict { return {}; }       # Public endpoint
def:priv helper() -> None { }                  # Private
def area() -> float abs;                       # Abstract (no body)
```
Lambda expression: `lambda x: int -> int : x * 2;`
Lambda block (MUST return): `lambda x: int -> int { return x * 2; };`
Lambda multi-param: `lambda x: int, y: int -> int : x + y;`
Lambda as argument: `items.sort(key=lambda x: dict -> float : x["v"]);`
Lambda with assignment MUST use block: `lambda e: any -> None { input_val = e.target.value; }`
Empty lambda body: `lambda e: any -> None { 0; }` NOT `lambda e: any -> None {}`
Pipe: `"hello" |> print;` `[3,1,2] |> sorted |> list |> print;`
F-strings: `f"Value: {x}, Pi: {pi:.2f}";`
Glob: `glob counter: int = 0;` at module level. Access by name in functions. WRONG: `glob counter;` inside function body.
Top-level restriction: only declarations allowed. Executable statements MUST go inside `with entry { }` or a function body.
Docstrings go BEFORE declarations: `"""My obj.""" obj Foo { }`

# 4. IMPORTS
```jac
import os;                              # Namespace import (semicolon)
import from math { sqrt, pi }           # Selective (NO semicolon after })
import from .sibling { helper_func }    # Relative
import datetime as dt;                  # Alias
include random;                         # C-style merge into current scope
```
WRONG: `import from math, sqrt;` WRONG: `import:py from os { path }` WRONG: `import:jac from mod { X }`
`__init__.jac` required for packages. Include MUST use full dotted paths.
WRONG: `include nodes;` (passes check, fails runtime) RIGHT: `include mypackage.nodes;`
`include` = inlines code into current scope. `import` = Python-style namespace separation.
```jac
with entry { print("always runs when module loads"); }
with entry:__main__ { print("only when file executed directly"); }
```

# 5. ARCHETYPES
```jac
node Person { has name: str; has age: int = 0; }
edge Friend { has since: int = 2020; has strength: float = 1.0; }
walker Greeter { has greeting: str = "Hello"; }
obj Config { has debug: bool = False; }
enum Status { PENDING, ACTIVE, DONE }
enum Color { RED = "red", GREEN = "green" }
```
Inheritance: `obj Child(Parent) { }` `walker W(BaseW) { }` `node Employee(Person) { has dept: str; }`
`can` for abilities (with entry/exit); `def` for regular methods
Impl blocks: declare in archetype, define separately:
```jac
obj Calc { def add(n: int) -> int; }
impl Calc.add(n: int) -> int { self.value += n; return self.value; }
```
Postinit: `has f: int by postinit; def postinit { self.f = self.x * 2; }`
Boolean NOT: `not x` (Python-style). WRONG: `!x` (JS `!` does NOT exist in Jac)
Reserved keywords: obj node walker edge enum can has -- NEVER use as variable names.
WRONG: `obj = json.loads(s);` RIGHT: `data = json.loads(s);`

# 6. ACCESS
`:pub` `:priv` `:protect` on has/def/can/walker. Both `has:priv x` and `has :priv x` valid.
```jac
obj Person { has:pub name: str; has:priv ssn: str; has:protect age: int; }
walker :pub GetUsers { }    # Public = no auth required
walker GetSecret { }        # No :pub = requires auth token
def:pub health() -> dict { return {"ok": True}; }
```

# 7. GRAPH
```jac
a ++> b;                                # Untyped forward
a +>: Friend(since=2020) :+> b;        # Typed forward
a <+: Friend() :<+ b;                  # Typed backward
a <++> b;                               # Bidirectional untyped
root ++> a ++> b ++> c;                 # Chained
a del--> b;                             # Disconnect
```
Traversal:
```jac
nodes = [root -->];                     # All outgoing (untyped)
friends = [root ->:Friend:->];          # Typed traversal
chain = [root ->:Friend:->->:Knows:->]; # Chained typed
back = [root <-:Friend:<-];             # Backward typed
edges = [edge root ->:Friend:->];       # Get edge objects
```
Filters (ALWAYS assign to variable or use in expression, never bare):
```jac
people = [-->](?:Person);               # Type filter
adults = [-->](?:Person, age > 18);     # Type + attr
old = [-->](?age > 18);                 # Attr only
close = [->:Friend:since > 2020:->];   # Edge attr filter
```
Variable node traversal: `neighbors = [city_a ->:Road:->];` `items = [node_var -->];`
Walrus: `root +>: E() :+> (end := A(val=10));`
Untyped returns list: `nodes = root ++> Person(); first = nodes[0];`
Visit indexed: `visit : 0 : [-->];` (first only)
WRONG: `a ++> Edge() ++> b;` `[-->:E:]` `del a --> b;` `[-->:E1:->-->:E2:->]`

# 8. ABILITIES
```jac
node Room {
    has name: str;
    can on_enter with Visitor entry { print(f"Welcome to {self.name}"); }
    can on_exit with Visitor exit { print(f"Leaving {self.name}"); }
    can on_any with entry { print("any walker entered"); }
    can on_multi with Admin | Inspector entry { print("authorized"); }
}
```
`self` = current archetype instance; `here` = current node (in walker abilities); `visitor` = visiting walker (in node abilities)
Root type: capital R `Root`. WRONG: `` `root ``. Union: `can act with Root | MyNode entry { }`

# 9. WALKERS
Spawn (BOTH valid): `root spawn Walker();` and `Walker() spawn root;`
WRONG: `node spawn W();` (node is keyword). Use variable: `my_node spawn W();`
```jac
walker Crawler {
    has target: str;
    has found: list = [];
    can start with Root entry { visit [-->]; }
    can search with Person entry {
        if here.name == self.target { report here; disengage; }
        self.found.append(here.name);
        visit [-->] else { print("dead end"); }
    }
    can finish with Root exit { report self.found; }
}
```
`visit` QUEUES nodes for next step (NOT immediate). Code after visit continues.
`visit [-->];` `visit [->:E:->];` `visit self.target;` `visit : 0 : [-->];`
`visit [-->] else { fallback; }` for dead ends.
`report` appends to `.reports` array: `result = root spawn W(); data = result.reports[0];`
Always check `.reports` before indexing. Prefer single report in `with Root exit`.
`disengage` immediately terminates walker. Exit abilities for ancestor nodes will NOT execute.
`skip` skips remaining code for current node, moves to next queued node (like continue).
DFS traversal order: entries depth-first, exits LIFO. root->A->B: Enter root, Enter A, Enter B, Exit B, Exit A, Exit root.

# 10. BY_LLM
```jac
def classify(text: str) -> str by llm;
def classify2(text: str) -> str by llm();           # Both valid
def summarize(t: str) -> str by llm(temperature=0.7);
result = "Explain quantum computing" by llm;         # Inline
```
Semstrings: `has desc: str = "" """hint for LLM""";` (default value required before hint)
Sem annotations: `sem Obj.field = "description";` `sem func.param = "hint";`
Enum classification: `enum Cat { WORK, PERSONAL, OTHER }` `def categorize(t: str) -> Cat by llm();`
Model import: `import from byllm.lib { Model }` `glob llm = Model(model_name="gpt-4o-mini");`
Structured output: return type `-> list[MyObj]` fills all fields via LLM.
Tools: `def answer(q: str) -> str by llm(tools=[get_weather, search_web]);`
Context: `def agent(q: str) -> str by llm(incl_info={"ctx": data});`

# 11. FILE_JSON
```jac
with entry {
    with open("data.json") as f { raw = f.read(); }
    data = json.loads(raw);           # NOT obj = json.loads(raw)
    output = json.dumps(data, indent=2);
    with open("out.json", "w") as f { f.write(output); }
}
```
WRONG: `obj = json.loads(s);` (obj is keyword) RIGHT: `data = json.loads(s);`

# 12. API
CLI: `jac start file.jac` (NOT `jac serve`). `jac check file.jac` for syntax checking.
ALL walkers register at `POST /walker/<WalkerName>`. `GET /walker/<Name>` returns metadata only (does NOT execute).
`__specs__` is VESTIGIAL in 0.10.2 -- methods, path, path_prefix are IGNORED by server.
`:pub` on walker = public (no auth). Without `:pub` = requires auth token.
Auth endpoints: `POST /user/register` and `POST /user/login`.
`:pub` walker root access is READ-ONLY. Graph writes silently fail when `here` is root.
Walkers CANNOT access HTTP headers, query params, cookies, or request object. ALL data via `has` fields in POST body.
Walker `has` fields = POST body params. Non-default `has` = REQUIRED in POST body.
Response format: `{"ok":true, "data":{"result":..., "reports":[...]}, "error":null}`
Client fetch: `response.data.reports[0]` for reported values.
OAuth GET redirects cannot hit walkers (POST-only). Redirect to frontend, then POST to walker.
SSO routes (`/sso/{platform}/{operation}`) and OpenAPI (`/docs`) = jac-scale plugin only.
Custom auth: make ALL walkers `:pub`, handle auth manually in walker body via `has token: str;`.

# 13. WEBSOCKET
```jac
async walker :pub Echo {
    async can echo with Root entry { report here; }
}
# In __specs__: static has methods: list = ["websocket"];
# Connect: ws://host/walker/Echo
```
`socket.notify_users(ids, msg);` `socket.notify_channels(names, msg);` `broadcast=True` for all.
Remove `:pub` for authenticated websocket.

# 14. WEBHOOKS
```jac
walker :pub WebhookHandler {
    obj __specs__ { static has webhook: dict = {"type": "header", "name": "X-Sig"}; }
    can handle with Root entry { report "ok"; }
}
```

# 15. SCHEDULER
```jac
walker ScheduledTask {
    obj __specs__ {
        static has schedule: dict = {"trigger": "cron", "hour": "9"};
        static has private: bool = True;
    }
    can run with Root entry { report "done"; }
}
```
Triggers: cron, interval, date.

# 16. ASYNC
```jac
async walker AsyncW { async can crawl with Root entry { visit [-->]; } }
async def fetch_data() -> str { await asyncio.sleep(1); return "data"; }
```
`flow` launches background task (thread pool), returns future. `wait` retrieves result (blocks).
Use flow/wait for CPU-bound parallel. async/await for I/O-bound event loop.

# 17. PERMISSIONS
```jac
node.__jac__.grant(root, WritePerm);
node.__jac__.revoke(root, WritePerm);
node.__jac__.check_access(root);
```
Levels: NoPerm ReadPerm ConnectPerm WritePerm.

# 18. PERSISTENCE
Nodes connected to root auto-persist. `save(node);` `commit();` `&id` for reference. `del node; commit();`
`jid(node)` returns unique Jac ID. `printgraph(root)` for debugging.

# 19. TESTING
```jac
test { assert 1 + 1 == 2; }
test { assert fib(5) == 5, "fib failed"; }
```
0.10.2: names REMOVED. WRONG: `test "name" { }` WRONG: `test my_test { }`

# 20. STDLIB
Builtins: print, len, range, enumerate, zip, map, filter, sorted, sum, min, max, abs, type, isinstance, hasattr, getattr, setattr
String: .upper() .lower() .strip() .split() .join() .replace() .startswith() .endswith() .format() f-strings
List: .append() .extend() .insert() .pop() .remove() .sort() .reverse() .index() .count()
Dict: .keys() .values() .items() .get() .update() .pop() .setdefault()
Null-safe: `x?.attr` `x?[0]` returns None on null/missing

# 21. JSX/CLIENT
TWO approaches: (1) `.cl.jac` files = entire file is client-side (no cl{} wrapper). (2) `cl{}` blocks inside `.jac` files = mixed server+client.
`.cl.jac` auto-compiled to JS, never `include` them.
`cl import` / `sv import` prefixes at TOP LEVEL (outside cl{} block) for cross-context imports.
```jac
cl import from react { useEffect }
sv import from __main__ { GetCount, Increment }

cl {
    def:pub app() -> JsxElement {
        has count: int = 0;       # has = React useState
        async can with entry {    # useEffect mount
            result = root spawn GetCount();
            if result.reports { count = result.reports[0]; }
        }
        return <div>
            <p>Count: {count}</p>
            <button onClick={lambda e: any -> None {
                async def inc() -> None {
                    root spawn Increment();
                    count = count + 1;
                }
                inc();
            }}>+</button>
        </div>;
    }
}
```
Component return type: `-> JsxElement` (NOT `-> any` which conflicts with builtin)
JSX comprehensions: `{[<li>{item}</li> for item in items]}` compiles to .map()
With filter: `{[<li>{x}</li> for x in items if x.active]}`
`has` in client components = reactive state (useState). Assignment triggers re-render.
Lifecycle: `async can with entry { }` = useEffect mount. `can with exit { }` = cleanup.
`className` not `class`; `.length` not `len()`; `String(x)` not `str()`; `parseInt(x)` not `int()`
`Math.min/max`; `.trim()` not `.strip()`; no `range()`; no f-strings (use `+`); no tuple unpacking
`new` keyword does NOT exist. Use `Reflect.construct(Date, [val])` instead of `new Date(val)`.
`None` compiles to `null` in cl{} context. Use `None` in Jac source.
List concat in cl{}: use `items.append(x)` not `items = items + [x]`
CSS: `import "./styles.css";` or `import '.styles.css';`
`.jac/` auto-generated, never modify manually.

# 22. CLIENT_AUTH
```jac
cl import from "@jac/runtime" { jacSignup, jacLogin, jacLogout, jacIsLoggedIn }
```
`jacSignup(email, password)` `jacLogin(email, password)` `jacLogout()` `jacIsLoggedIn()` returns bool.
Per-user graph isolation: each authenticated user gets their own root graph.

# 23. JAC.TOML
```toml
[project]
name = "myapp"
entry-point = "main.jac"

[dependencies]
python-dotenv = ">=1.0.0"

[dependencies.npm]
tailwindcss = "^4.0.0"
"@tailwindcss/postcss" = "^4.0.0"

[dependencies.npm.dev]
"@jac-client/dev-deps" = "1.0.0"

[serve]
base_route_app = "app"
port = 8000

[plugins.client]
port = 5173

[build]
output = "dist"

[scripts]
dev = "jac start --dev main.jac"
```
npm deps: ALL in jac.toml. NEVER `npm install` in `.jac/client/`.

# 24. FULLSTACK_SETUP
`jac create --use client` (NOT `--use fullstack`). `jac install` syncs all deps. `jac add --npm pkg` adds npm dep.
Project structure: `main.jac` `__init__.jac` `jac.toml` `.jac/` (auto-gen)
`__init__.jac` must use full dotted paths: `include mypackage.nodes;` NOT `include nodes;`

# 25. DEV_SERVER
`jac start --dev main.jac` for hot reload.
`--port` = Vite frontend (default 8000); `--api_port` = backend (default 8001, auto-proxied).
Proxy routes: `/walker/*` `/function/*` `/user/*` forwarded to backend.
`--no-client` for backend-only. `jac start main.jac` for production.

# 26. DEPLOY_ENV
```dockerfile
FROM python:3.11-slim
RUN pip install jaseci
COPY . /app
WORKDIR /app
CMD ["jac", "start", "main.jac"]
```
`jaseci` = full runtime (persistence/auth plugins). `jaclang` = compiler-only.
`jac start --scale` for scaled deployment (no `-t` flag).
Env vars: `DATABASE_URL` `JAC_SECRET_KEY` `OPENAI_API_KEY`
.env not auto-loaded: `import from dotenv { load_dotenv }` `glob _: bool = load_dotenv() or True;`
`import from os { getenv }` then `getenv("MY_VAR")`

# PATTERN 1: Fullstack Counter (single-file with cl{} block)
```jac
# main.jac
import json;

node Counter { has val: int = 0; }

walker :pub GetCount {
    can get with Root entry {
        counters = [-->](?:Counter);
        if counters { report counters[0].val; }
        else { report 0; }
    }
}

walker :pub Increment {
    can inc with Root entry {
        counters = [-->](?:Counter);
        if counters { counters[0].val += 1; report counters[0].val; }
    }
}

with entry { root ++> Counter(val=0); }

cl import from react { useEffect }
sv import from __main__ { GetCount, Increment }

cl {
    def:pub app() -> JsxElement {
        has count: int = 0;
        has loaded: bool = False;

        async can with entry {
            response = await fetch("/walker/GetCount", {"method": "POST"});
            data = await response.json();
            if data.data.reports.length > 0 {
                count = data.data.reports[0];
            }
            loaded = True;
        }

        async def do_increment() -> None {
            response = await fetch("/walker/Increment", {"method": "POST"});
            data = await response.json();
            if data.data.reports.length > 0 {
                count = data.data.reports[0];
            }
        }

        if not loaded { return <p>Loading...</p>; }
        return <div>
            <h1>Count: {count}</h1>
            <button onClick={lambda e: any -> None { do_increment(); }}>
                Increment
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
[serve]
base_route_app = "app"
```

# PATTERN 2: Walker Graph Traversal (Cities/Roads)
```jac
node City { has name: str; has pop: int = 0; }
edge Road { has dist: int = 0; has toll: bool = False; }

walker FindReachable {
    has reachable: list = [];
    can start with Root entry { visit [-->]; }
    can explore with City entry {
        self.reachable.append({"name": here.name, "pop": here.pop});
        visit [->:Road:->];
    }
    can finish with Root exit { report self.reachable; }
}

walker DeleteRoute {
    has from_city: str;
    has to_city: str;
    has deleted: bool = False;
    can start with Root entry { visit [-->]; }
    can find with City entry {
        if here.name == self.from_city {
            targets = [here ->:Road:->](?:City, name == self.to_city);
            for t in targets { here del--> t; self.deleted = True; }
        }
        if not self.deleted { visit [->:Road:->]; }
    }
    can finish with Root exit { report self.deleted; }
}

with entry {
    sf = City(name="SF", pop=800000);
    la = City(name="LA", pop=4000000);
    sv = City(name="SV", pop=250000);
    root ++> sf;
    sf +>: Road(dist=380, toll=False) :+> la;
    sf +>: Road(dist=45, toll=True) :+> sv;
    la +>: Road(dist=100, toll=True) :+> sv;

    # Traverse from variable node
    sf_neighbors = [sf ->:Road:->];
    toll_roads = [sf ->:Road:toll == True:->];
    print(f"SF neighbors: {sf_neighbors}");
    print(f"Toll destinations: {toll_roads}");

    result1 = root spawn FindReachable();
    print(f"Reachable: {result1.reports[0]}");

    result2 = root spawn DeleteRoute(from_city="SF", to_city="LA");
    print(f"Deleted: {result2.reports[0]}");
}
```

# PATTERN 3: API Endpoints (Todo CRUD)
```jac
import json;

node Todo { has title: str; has done: bool = False; has priority: str = "medium"; }

walker :pub ListTodos {
    can list with Root entry {
        todos = [-->](?:Todo);
        report [{"title": t.title, "done": t.done, "priority": t.priority} for t in todos];
    }
}

walker :pub AddTodo {
    has title: str;
    has priority: str = "medium";
    can add with Root entry {
        new_todo = (here ++> Todo(title=self.title, priority=self.priority))[0];
        report {"title": new_todo.title, "priority": new_todo.priority};
    }
}

walker :pub FilterTodos {
    has filter_by: str = "all";
    can filter with Root entry {
        todos = [-->](?:Todo);
        match self.filter_by {
            case "high": report [{"title": t.title} for t in todos if t.priority == "high"];
            case "done": report [{"title": t.title} for t in todos if t.done];
            case "pending": report [{"title": t.title} for t in todos if not t.done];
            case _: report [{"title": t.title} for t in todos];
        }
    }
}

with entry {
    root ++> Todo(title="Buy groceries", priority="high");
    root ++> Todo(title="Read book", priority="low");
}
# All walkers auto-register: POST /walker/ListTodos, POST /walker/AddTodo, etc.
# Client fetch:
# fetch("/walker/ListTodos", {method:"POST"}).then(r=>r.json()).then(d=>d.data.reports[0])
# fetch("/walker/AddTodo", {method:"POST", headers:{"Content-Type":"application/json"},
#   body:JSON.stringify({"title":"New task","priority":"high"})})
```

# COMMON ERRORS
WRONG: `true` / `false` -> RIGHT: `True` / `False`
WRONG: `entry { }` -> RIGHT: `with entry { }`
WRONG: `import from math, sqrt;` -> RIGHT: `import from math { sqrt }`
WRONG: `import:py from os { path }` -> RIGHT: `import from os { path }`
WRONG: `node spawn W();` -> RIGHT: `root spawn W();` (node is keyword)
WRONG: `a ++> Edge() ++> b;` -> RIGHT: `a +>: Edge() :+> b;`
WRONG: `[-->:E:]` -> RIGHT: `[->:E:->]`
WRONG: `[-->:E1:->-->:E2:->]` -> RIGHT: `[->:E1:->->:E2:->]`
WRONG: `del a --> b;` -> RIGHT: `a del--> b;`
WRONG: `(?Type)` or `` (`?Type) `` -> RIGHT: `(?:Type)`
WRONG: `` (`?Type:attr>v) `` -> RIGHT: `(?:Type, attr > v)`
WRONG: `` can act with `root entry `` -> RIGHT: `can act with Root entry`
WRONG: `test "name" { }` -> RIGHT: `test { }` (no names in 0.10.2)
WRONG: `test my_test { }` -> RIGHT: `test { }`
WRONG: `obj = json.loads(s);` -> RIGHT: `data = json.loads(s);`
WRONG: `str?` -> RIGHT: `str | None`
WRONG: `jac serve file.jac` -> RIGHT: `jac start file.jac`
WRONG: `jac create --use fullstack` -> RIGHT: `jac create --use client`
WRONG: `static has auth: bool = False;` in __specs__ -> RIGHT: `walker :pub W { }`
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
WRONG: `case "hi": { stmt; }` -> RIGHT: `case "hi": if True { stmt; }`
WRONG: `catch Error as e { }` -> RIGHT: `except Error as e { }`
WRONG: `result = x > 0 ? "y" : "n";` -> RIGHT: `result = ("y") if x > 0 else ("n");`
WRONG: `has x: int = 0; has y: str;` -> RIGHT: `has y: str; has x: int = 0;`
WRONG: `glob counter;` inside function -> RIGHT: just use `counter` directly
WRONG: `result.returns[0]` -> RIGHT: `result.reports[0]`
WRONG: `.map(lambda x -> ...)` in JSX -> RIGHT: `{[<li>{x}</li> for x in items]}`
WRONG: `pass` -> RIGHT: `{}` or comment
WRONG: `!x` -> RIGHT: `not x`
WRONG: `__specs__ methods/path` to customize routes -> RIGHT: ignored in 0.10.2; all POST /walker/<Name>
WRONG: `new Date()` in cl{} -> RIGHT: `Reflect.construct(Date, [val])`
WRONG: `def:pub app() -> any` -> RIGHT: `def:pub app() -> JsxElement`
WRONG: `fetch("/api/todos")` -> RIGHT: `fetch("/walker/ListTodos", {"method": "POST"})`
WRONG: `ExecutionContext.get()` for headers -> RIGHT: pass as walker `has` field in POST body
WRONG: `has x: list;` (no default) -> RIGHT: `has x: list = [];` (non-default = required POST param)
WRONG: `GET /walker/Name` to execute -> RIGHT: `POST /walker/Name` (GET = metadata only)
WRONG: OAuth redirect to `/walker/Callback` -> RIGHT: redirect to frontend, then POST to walker