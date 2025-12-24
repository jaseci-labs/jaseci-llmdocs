# syntax


## From: installation.md

Color-coding for Jac's syntax to make it easier to read.


## From: jac_in_a_flash.md

Statements end with a semicolon and the parent initializer is invoked via `super.init`. Program execution happens inside a `with entry { ... }` block, which replaces Python's `if __name__ == "__main__":` section.


## From: getting_started.md

- [Jac in a Flash](jac_in_a_flash.md) - See Jac's Syntax with a Toy


## From: tour.md

Jac-lang is intentionally designed as an extension of Python. It provides Python-like syntax while adding new capabilities for graph-based and AI-first programming.

Developers can freely mix Jac and Python:

- Import Python libraries and call Python functions from Jac
- Inline Python snippets inside Jac code
- Import Jac modules directly into Python programs

This tight interoperability enables teams to adopt Jac incrementally and integrate it seamlessly with existing Python ecosystems. [Read about how we super-setted Python](https://docs.jaseci.org/learn/superset_python/). [Read about using Jaseci as a Python library](https://docs.jaseci.org/learn/library_mode/)


## From: jac_import_patterns.md

## Usage Rules

### 1. Client Import Requirement
- **Default imports** (`default as Name`) and **namespace imports** (`* as Name`) **MUST** use `cl` prefix
- **Named imports** work with or without `cl` prefix (but `cl` generates JavaScript)

### 2. Syntax Patterns

```jac
# ✅ Correct Usage
cl import from react { useState }                    # Category 1: Named
cl import from react { default as React }            # Category 2: Default
cl import from react { * as React }                  # Category 4: Namespace
cl import from react { default as React, useState }  # Category 3: Mixed

# ❌ Incorrect Usage
import from react { default as React }   # Error: default requires cl
import from lodash { * as _ }            # Error: namespace requires cl
cl import from lodash { * as _, map }    # Generates invalid JS
```

### 3. String Literal Imports for Special Characters

For package names containing special characters (hyphens, @-scopes, etc.), use string literals:

```jac
# ✅ Correct Usage - String literals for hyphenated packages
cl import from "react-dom" { render }
cl import from "styled-components" { default as styled }
cl import from "react-router-dom" { BrowserRouter, Route }
cl import from "date-fns" { format, parse }

# ❌ Incorrect Usage - Without quotes
cl import from react-dom { render }  # Error: hyphen not allowed in identifier
```

**When to use string literals:**
- Package names with hyphens: `react-dom`, `styled-components`, `react-router-dom`, `date-fns`
- Package names with special characters that aren't valid in identifiers
- Any package name that would cause a syntax error without quotes

**Note:** String literals work with all import types (named, default, namespace, mixed)

### 4. Relative Path Conversion

Jac uses Python-style dots for relative imports, which are automatically converted to JavaScript format:

| Jac Syntax | JavaScript Output | Description |
|------------|-------------------|-------------|
| `.utils` | `"./utils"` | Current directory |
| `..lib` | `"../lib"` | Parent directory |
| `...config` | `"../../config"` | Grandparent directory |
| `....deep` | `"../../../deep"` | Great-grandparent directory |

### Grammar
```lark
import_path: (NAME COLON)? (dotted_name | STRING) (KW_AS NAME)?
import_item: (KW_DEFAULT | STAR_MUL | named_ref) (KW_AS NAME)?
```


## From: example.md

```jac
import from byllm.lib { Model }
glob llm = Model(model_name="gpt-4o");

enum Personality {
    INTROVERT,
    EXTROVERT,
    AMBIVERT
}

# by keyword enables the program to integrate an LLM for the needed functionality
# Jaseci runtime automatically generates an optimized prompt for the LLM,
# checks errors and converts LLM output to the correct return type
def get_personality(name: str) -> Personality by llm();

with entry {
    name = "Albert Einstein";
    result = get_personality(name);
    print(f"{result} detected for {name}");
}
```
```jac
node Person {
    has name: str;
}

# Greeter can traverse the graph.
# start and greet are two abilities of Greeter
walker Greeter {
    has greeting_count: int = 0;

    can start with `root entry {
        print("Starting journey!");
        visit [-->];
    }

    # ability greet will only execute when Greeter enters a Person type node
    can greet with Person entry {
        print(f"Hello, {here.name}!");
        self.greeting_count += 1;

        # specify how this walker can traverse the graph
        # in this case, visit all outgoing edges from the current node
        visit [-->];
    }
}

with entry {
    alice = Person(name="Alice");
    bob = Person(name="Bob");
    charlie = Person(name="Charlie");

 # specify the object graph, where root connects to alice, then bob, then charlie
    root ++> alice ++> bob ++> charlie;

    greeter = Greeter();
 # root is where the graph starts, and we will start the walker here
    root spawn greeter;
    print(f"Total greetings: {greeter.greeting_count}");
}
```
```jac
node Post {
    has content: str;
    has author: str;
}

walker create_post {
    has content: str, author: str;

    can func_name with `root entry {
        new_post = Post(content=self.content, author=self.author);
        here ++> new_post;
        report {"id": new_post.id, "status": "posted"};
    }
}
```
```jac
import math;
import from random { uniform }

def calc_distance(x1: float, y1: float, x2: float, y2: float) -> float {
return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

with entry { # Generate random points
(x1, y1) = (uniform(0, 10), uniform(0, 10));
(x2, y2) = (uniform(0, 10), uniform(0, 10));

    distance = calc_distance(x1, y1, x2, y2);
    area = math.pi * (distance / 2) ** 2;

    print("Distance:", round(distance, 2), ", Circle area:", round(area, 2));

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
# jac is a superset of python and contains all of its features
# You can run code with
# jac run <filename>

# Single line comment
#*
    Multi-line
    Comment
*#

# Import declaration declares library packages referenced in this file.
# Simple imports
import os;
import sys, json;
import time;

# Import with alias
import datetime as dt;

# Import from with specific items
import from math { sqrt, pi, log as logarithm }


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

def learnFlowControl() {
	x = 9;

	# All control blocks require brackets, but not parentheses
	if x < 5 {
		print("Doesn't run");
	} elif x < 10 {
		print("Run");
	} else {
		print("Also doesn't run");
	}

	# chains of if-else can be replaced with match statements
	match x {
		case 1:
			print("Exactly one");
		case int() if 10 <= x < 15:
			print("Within a range");
		case _:
			print("Everything else");
	}

	# Like if, for doesn't use parens either.
	# jac provides both indexed and range-based for loops
	for i = 10 to i <= 20 by i += 2 {
		print(f"element: {i}");
	}

	for x in ["a", "b", "c"] {
		print(f"element: {x}");
	}

	# while loops follow similar syntax
	a = 4;
	while a != 1{
		a /= 2;
	}

	learnCollections();
	learnSpecial();
}

def learnCollections() {
	# lists and slicing
	fruits = ["apple", "banana", "cherry"];
	print(fruits[1]); # banana
	print(fruits[:1]); # [apple, banana]
	print(fruits[-1]); # cherry

	# dictionary
    person = {
        "name": "Alice",
        "age": 25,
        "city": "Seattle"
    };

    # Access values by key
    print(person["name"]);  # Alice
    print(person["age"]);   # 25

	# tuples are immutable lists
	point = (10,20);
    print(point[0]);  # 10
    print(point[1]);  # 20

	# tuples can be unpacked with parentheses
	(x, y) = point;
    print(f"x={x}, y={y}");

	# list comprehensions
    squares = [i ** 2 for i in range(5)];
    print(squares);  # [0, 1, 4, 9, 16]

    # With condition
    evens = [i for i in range(10) if i % 2 == 0];
    print(evens);  # [0, 2, 4, 6, 8]

	learnClasses();
	learnOSP();
}

def learnClasses() {

    # the class keyword follows default Python behavior
    # all members are static
    class Cat {
        has name: str = "Unnamed";
        def meow {
			print(f"{self.name} says meow!");
        }
    }

    your_cat = Cat();
    my_cat = Cat();
    my_cat.name = "Shrodinger";

    my_cat.meow();   # Shrodinger says meow!
    your_cat.meow(); # Shrodinger says meow!

	# the obj keyword follows the behavior of Python dataclasses
    # all members are per-instance
	obj Dog {
		has name: str = "Unnamed";
		has age: int = 0;

		def bark {
			print(f"{self.name} says Woof!");
		}
	}
    your_dog = Dog();
    my_dog = Dog();
    my_dog.name = "Buddy";
    my_dog.age = 3;

	your_dog.bark(); # Unnamed says Woof!
	my_dog.bark();   # Buddy says Woof!

	# inheritance
	obj Puppy(Dog){
		has parent: str = 0;
		def bark { # override
			print(f"Child of {self.parent} says Woof!");
		}
	}
}

# Jac also supports graph relationships within the type system
# This is called Object Spatial Programming

# nodes are objs with special properties
node Person {
    has name: str;
    has age: int;
}

def learnOSP(){
	a = Person(name="Alice",age=25);
	b = Person(name="Bob",age=30);
	c = Person(name="Charlie",age=28);

	# connection operators create edges between nodes
	a ++>  b; # forward a->b
	b <++  c; # backward c->b
	a <++> c; # bidirectional a <-> c

	# edges can be typed, providing additional meaning
	edge Friend {
		has since: int;
	}

	a +>:Friend(since=2020):+> b;
	a +>:Friend(since=1995):+> c;


    # edges and nodes can be queried with filters

    # returns all outgoing nodes with friend edges since 2018
    old_friend_nodes = [node a ->:Friend:since > 2018:->];

    # returns all outgoing friend edges since 2018
    old_friend_edges = [edge a->:Friend:since > 2017:->];

	# Walkers are objects that "walk" across nodes doing operations
	# Walkers contain automatic methods that trigger on events
	# These methods are called abilities
	walker Visitor {
        has name: str;

        # abilities follow can <name> with <type> <operation> syntax
		# runs when walker spawns at root
		can start with `root entry {
			print(f"Starting!");
			# visit moves to an adjacent node
			visit [-->]; # [-->] corresponds to outgoing connections
			# visit [<--]; incoming connections
			# visit [<-->]; all connections
		}

		# runs when walker visits any person
		can meet_person with Person entry {
			# here refers to current node
			# self refers to walker
			print(f"Visiting {here.name} with walker {self.name}");
			if here.name == "Joe" {
				print("Found Joe");
				disengage; # stop traversal immediately
			}

            # report returns a value without stopping exeuction
            # all reported values are accessed as a list after traversal
			report here.name;
			visit [-->];
		}

		# runs when walker is done
		can finish with exit {
			print("Ending!");
		}
	}

	# nodes can also have abilities
	node FriendlyPerson(Person) {
		has name:str;
		can greet with Visitor entry{
			print(f"Welcome, visitor");
		}
	}

    f = FriendlyPerson(name="Joe",age=10);

    # root is a special named node in all graphs
    root ++> f ++> a;

    # walker can then be spawned at a node in the graph
    root spawn Visitor("Jim");
}

def learnSpecial(){
    # lambdas create anonymous functions
    add = lambda a: int, b: int -> int : a + b;
    print(add(5, 3));

    # walrus operator allow assignment within expressions
    result = (y := 20) + 10;
    print(f"y = {y}, result = {result}");

    # flow/wait is jac's equivalent to async/await for concurrency
    # in jac, these are executed in a thread pool
    def compute(x: int, y: int) -> int {
        print(f"Computing {x} + {y}");
        return x + y;
    }

    def slow_task(n: int) -> int {
        print(f"Task {n} started");
        time.sleep(1);
        print(f"Task {n} done");
        return n * 2;
    }

    task1 = flow slow_task(42);
    task2 = flow compute(5, 10);
    task3 = flow compute(3, 7);

    result1 = wait task1;
    result2 = wait task2;
    result3 = wait task3;
    print(f"Results: {result1}, {result2}, {result3}");
    #* Output:
    Task 42 started
    Computing 5 + 10
    Computing 3 + 7
    Task 42 done
    Results: 84, 15, 10
    *#
}

# all programs start from the entry node
with entry {
    # print function outputs a line to stdout
    print("Hello world!");

    # call some other function
    nextFunction();
}
```


## From: beginners_guide_to_jac.md

Every Jac program needs a place to start. We use a special block called `with entry`:

```jac
with entry {
    print("Hello, World!");
}
```

**What's happening here?**
- `with entry` - This is where your program starts
- `print()` - This is a **function** that displays text on the screen
- `"Hello, World!"` - This is text (called a **string**)
- `;` - Every instruction ends with a semicolon
- `{}` - Curly braces group instructions together

**Try it yourself:** Change "Hello, World!" to your name!

```jac
with entry {
    print("Hello, my name is Alice!");
}
```

Lines starting with `#` are comments** - they're notes for humans, the computer ignores them.

**Pro tip:** The `f` before a string lets you insert variables using `{variable_name}`

```jac
with entry {
    # Basic math
    sum = 5 + 3;        # Addition: 8
    difference = 10 - 4; # Subtraction: 6
    product = 6 * 7;     # Multiplication: 42
    quotient = 20 / 4;   # Division: 5.0

    print(sum);         # Shows: 8
    print(product);     # Shows: 42

    # More operations
    remainder = 17 % 5;  # Modulo (remainder): 2
    power = 2 ** 3;      # Exponent: 8 (2³)

    # Combined operations
    total = (5 + 3) * 2;  # Use parentheses like in math: 16

    print(total);
}
```

**Common shortcuts:**
- `x += 5` means `x = x + 5` (add 5)
- `x -= 3` means `x = x - 3` (subtract 3)
- `x *= 2` means `x = x * 2` (multiply by 2)
- `x /= 4` means `x = x / 4` (divide by 4)

**Important:** Use `==` to compare (not `=`). Use `=` to assign values!

```jac
# Comments
# Single line comment
#* Multi-line
   comment *#

# Entry point
with entry {
    # Statements end with semicolons
    x = 5;
    print(x);

    # Blocks use curly braces
    if x > 0 {
        print("positive");
    }
}
```

```jac
with entry {
    # List comprehension
    squares = [x ** 2 for x in range(10)];
    print(f"Squares: {squares}");

    # Dictionary comprehension
    square_dict = {x: x**2 for x in range(5)};
    print(f"Square dict: {square_dict}");

    # String formatting
    name = "Alice";
    age = 25;
    message = f"Hello, {name}! You are {age} years old.";
    print(message);

    # Ternary operator
    result = "adult" if age >= 18 else "minor";
    print(f"Status: {result}");

    # Multiple assignment using tuples
    (x, y) = (10, 20);
    print(f"x={x}, y={y}");

    # Swap values
    (x, y) = (y, x);
    print(f"After swap: x={x}, y={y}");
}
```


## From: superset_python.md

Jac is designed as a superset of Python, extending the language with additional features for modern software architecture while maintaining full compatibility with the Python ecosystem. Python developers can leverage their existing knowledge while accessing new capabilities for graph-based and object-spatial programming.

The relationship between Jac and Python is analogous to that of TypeScript and JavaScript: a superset language that compiles to a widely-adopted base language.

**Example: From Jac to Python**

The following Jac module demonstrates functions, objects, and an entrypoint:

```jac
"""Functions in Jac."""

def factorial(n: int) -> int {
    if n == 0 { return 1; }
    else { return n * factorial(n-1); }
}

obj Person {
    has name: str;
    has age: int;

    def greet() -> None {
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.");
    }
}

with entry {
    person = Person("John", 42);
    person.greet();
    print(f"5! = {factorial(5)}");
}
```

The Jac compiler converts this code into the following Python implementation:

```python
"""Functions in Jac."""
from __future__ import annotations
from jaclang.lib import Obj

def factorial(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

class Person(Obj):
    name: str
    age: int

    def greet(self) -> None:
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.")

person = Person('John', 42)
person.greet()
print(f'5! = {factorial(5)}')
```

The compiled output demonstrates how Jac's object-oriented features map to standard Python classes inheriting from `Obj` (Jac's base object archetype), with imports from the `jaclang.lib` package.

---

### **Seamless Interoperability: Import Jac Files Like Python Modules**

Jac integrates with Python through a simple import mechanism. By adding `import jaclang` to Python code, developers can import `.jac` files using standard Python import statements without requiring build steps, compilation commands, or configuration files.

**Key Integration Features:**

*   **Bidirectional Module Imports:** Python files can import Jac modules, and Jac files can import Python modules using standard import syntax. Modules written in `.jac` and `.py` can be used interchangeably within a project.

*   **Incremental Adoption:** Jac can be added to existing Python projects without restructuring the codebase. Python files can remain unchanged while Jac modules are introduced where beneficial.

*   **Standard Import Syntax:** The same `import` statements used for Python modules work with `.jac` files, requiring no special syntax or additional tools.

**Example: Importing Across Languages**

Consider a Jac module containing graph utilities:

```jac
# graph_tools.jac
node Task {
    has name: str;
    has priority: int;
}
```

This module can be imported in Python using standard import syntax:

```python
# main.py
import jaclang  # Enable Jac imports (one-time setup)
from graph_tools import Task  # Import from .jac file

# Use Jac classes in Python
my_task = Task(name="Deploy", priority=1)
```

Jac files can also import Python libraries:

```jac
# analyzer.jac
import pandas as pd;
import numpy as np;

# Use Python libraries in Jac code
```

**Implementation Details:** Jac extends Python's native import mechanism using the [PEP 302](https://peps.python.org/pep-302/) import hook system. When `import jaclang` is executed, it registers a custom importer that enables Python to locate and load `.jac` files. Subsequently, Python's import mechanism automatically checks for `.jac` files alongside `.py` files, compiles them transparently, and loads them into the program. This integration makes Jac modules function as first-class citizens within the Python environment.

---

#### **Pattern 2: Jac + Inline Python**

This pattern embeds Python code directly within `.jac` files using `::py::` blocks, enabling the use of Python-specific libraries or preservation of existing Python code.

**Use Case:** Incremental migration of Python codebases while maintaining legacy utilities

**Directory Structure:**
```
project/
├── main.jac
└── models.jac
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

    walker TaskCreator {
        can create with `root entry {
            # Use inline Python functions
            task_data = get_sample_task();

            if validate_title(task_data["title"]) {
                task = models.Task(title=task_data["title"]);
                here ++> task;
                desc = generate_desc(task.title);
                print(f"✓ Created: {task.title}");
                print(f"  AI: {desc}");
            } else {
                print("✗ Title invalid!");
            }
        }
    }

    with entry {
        root spawn TaskCreator();
    }
    ```

=== "models.jac"
    ```jac
    """Task node definition."""

    node Task {
        has title: str;
        has done: bool = False;
    }
    ```

This approach preserves tested Python code while introducing Jac features, supporting incremental migration strategies.

---

#### **Pattern 5: Pure Python + Jac Library**

This pattern uses pure Python with Jac's runtime as a library, without any `.jac` files.

**Use Case:** Conservative adoption paths, teams preferring Python syntax, or existing Python projects

**Directory Structure:**
```
project/
├── main.py
└── validators.py
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

This pattern provides graph-based capabilities in pure Python without introducing new syntax, utilizing Jac's object-spatial model through library imports.

---

### **Key Takeaways**

Jac's design as a Python superset enables complementary use of both languages rather than requiring a choice between them. Key characteristics include:

- **Incremental Adoption:** Projects can begin with Pattern 5 (pure Python + Jac library) and progressively adopt Pattern 1 (pure Jac) as requirements evolve
- **Full Ecosystem Access:** All Python libraries, frameworks, and development tools remain compatible without modification
- **Flexible Integration:** Five adoption patterns accommodate different team preferences and project requirements
- **No Vendor Lock-in:** Transpiled Python code is readable and maintainable, providing migration paths if needed
- **Transparent Interoperability:** PEP 302 import hooks enable seamless bidirectional imports between `.jac` and `.py` files


## From: quickstart.md

```jac
import time at t;

def example(){
    number = 1+2;
    print(f"Calculated {number}");
    t.sleep(2);
    if number < 4 {
        print("Small number");
    }
}

# jac's equivalent of main
with entry {
    print("Hello world!");
    example();
}
```
```jac
node Person {
    has name: str;
    has age: int;

    def greet -> str {
        return f"Hello, I'm {self.name}!";
    }

    def celebrate_birthday {
        self.age += 1;
        print(f"{self.name} is now {self.age}!");
    }
}

with entry {
    alice = Person(name="Alice", age=25);
    bob = Person(name="Bob", age=30);
    print(alice.greet());  # Standard method call
}
```
```jac
alice ++> bob;      # Alice → Bob (forward relationship)
alice <++ bob;      # Bob → Alice (backward)
alice <++> bob;     # Alice ↔ Bob (bidirectional)

# You now have a graph structure where relationships exist
# independently of any object's internal state
```
```jac
node Person { has name: str; }

edge Friend {
    has since: int;
    has strength: int = 5;

    def is_strong -> bool {
        return self.strength >= 7;
    }
}

with entry {
    alice +>:Friend(since=2015, strength=9):+> bob;

    # Query all Friend relationships from alice
    friends = [alice ->:Friend:->];
    print(f"Alice has {len(friends)} friend(s)");

    # The result is a list of Person nodes, not data structures you have to unpack
}
```
```jac
# All outgoing connections (any type)
all_out = [alice -->];

# Only Friend edges
type_out = [alice ->:Friend:->];

# Friend edges filtered by property
filtered = [alice ->:Friend:since < 2018:->];

# Each query returns a list of connected nodes, ready to use
```
```jac
node Entity {
    has id: str;
    has created: str;
}

node Person(Entity) {
    has email: str;
    def notify(msg: str) {
        print(f"To {self.email}: {msg}");
    }
}

# Person inherits from Entity, gets id/created fields
# plus its own email field and notify method
```
```jac
walker Greeter {
    has greeting_count: int = 0;

    can start with `root entry {
        print("Starting journey!");
        visit [-->];  # Begin traversal from root's outgoing edges
    }

    can greet with Person entry {
        print(f"Hello, {here.name}!");  # 'here' is current node
        self.greeting_count += 1;
        visit [-->];  # Continue to next node's connections
    }
}

with entry {
    alice = Person(name="Alice");
    bob = Person(name="Bob");

    root ++> alice ++> bob;
    root spawn Greeter();  # Launch walker, it navigates autonomously
}
```
```jac
walker DataCollector {
    has counter: int = 0;          # Walker state, persists across visits
    has visited_names: list = [];  # Accumulates data during traversal

    can collect with NodeType entry {  # Executes when visiting NodeType
        self.visited_names.append(here.name);
        self.counter += 1;
        visit [-->];  # Default: depth-first traversal
    }
}
```
```jac
walker Explorer {
    can explore with Person entry {
        # Visit all outgoing connections (depth-first)
        visit [-->];

        # Visit only Friend edges
        visit [->:Friend:->];

        # Friend edges with strength > 5
        visit [->:Friend:strength > 5:->];
    }
}
```
```jac
walker FindPerson {
    has target: str;
    has found: bool = False;

    can search with Person entry {
        if here.name == self.target {
            self.found = True;
            disengage;  # Stop immediately, don't visit further
        }
        visit [-->];  # Keep searching if not found
    }
}
```
```jac
walker Tourist {
    can meet_person with Person entry {
        print(f"Met {here.name}, age {here.age}");
        visit [-->];
    }

    can visit_city with City entry {
        print(f"Visiting {here.name}, pop {here.population}");
        visit [-->];
    }
}
```
```jac
node Person {
    has name: str;

    can receive_greeting with Greeter entry {
        print(f"{self.name} acknowledges greeting");
    }
}
```
```jac
node Person {
    can greet_visitor with Visitor entry {
        print(f"{self.name} says: Welcome!");  # Executes first
    }
}

walker Visitor {
    can meet_person with Person entry {
        print(f"Visitor says: Hello, {here.name}!");  # Executes second
        visit [-->];
    }
}
```
```jac
# Visit immediate neighbors
visit [-->];

# Visit only via Friend edges
visit [->:Friend:->];

# Visit via Friend edges from before 2020
visit [->:Friend:since < 2020:->];

# Multi-hop: friends of friends
visit [here ->:Friend:-> ->:Friend:->];
```
```jac
walker AgeCollector {
    has ages: list = [];

    can collect with Person entry {
        self.ages.append(here.age);  # Accumulate in walker state
        visit [-->];
    }
}

# After execution: walker.ages contains [25, 30, 28]
```
```jac
walker FindFirstMatch {
    can search with Person entry {
        if here.name == self.target {
            report here;  # Send back the node
            disengage;    # Stop traversing immediately
        }
        visit [-->];
    }
}
```
```jac
node Task {
    has title: str;
    has status: str = "pending";
}

edge DependsOn {}

walker TaskAnalyzer {
    has ready_tasks: list = [];

    can analyze with Task entry {
        if here.status != "pending": return;

        # Get all dependencies
        deps = [here ->:DependsOn:->];

        # Check if all complete
        all_done = all(dep.status == "complete" for dep in deps);

        if all_done {
            self.ready_tasks.append(here.title);
        }

        visit [-->];  # Continue to next task
    }
}

# Usage: spawn analyzer, then check analyzer.ready_tasks
```


## From: jsx_client_serv_design.md

```lark
toplevel_stmt: KW_CLIENT? onelang_stmt
       | KW_CLIENT LBRACE onelang_stmt* RBRACE
       | py_code_block

KW_CLIENT: "cl"
```

```jac
cl import from jac:client_runtime {
    renderJsxTree,
    jacLogin,
    jacLogout,
    jacSignup,
    jacIsLoggedIn,
}
```

```jac
// Client function - executes in browser, can return JSX
cl def homepage() -> dict {
    return <div>
        <h1>Welcome</h1>
        <button onclick={load_feed()}>Load Feed</button>
    </div>;
}

// Client object - available on both client and server
cl obj ButtonProps {
    has label: str = "Hello";
    has count: int = 0;
}

// Client global - literal value sent to browser
cl let API_BASE_URL: str = "https://api.example.com";
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
<Link href="/about">About Page</Link>

# Equivalent to:
<a href="#/about" onclick={handleClick}>About Page</a>
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
// Server-side data model
node User {
    has name: str;
    has email: str;
}

// Client-side global configuration
cl let API_URL: str = "/api";

// Client-side component
cl obj CardProps {
    has title: str = "Untitled";
    has content: str = "";
}

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

// Server-side walker - called from client via spawn
walker LoadUsers {
    has users: list = [];

    can process with `root entry {
        # Fetch users from database
        self.users = [{"name": "Alice"}, {"name": "Bob"}];
        report self.users;
    }
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


## From: chapter_1.md

```jac
node Person {
    has name: str;
}

edge FriendsWith;
```
```jac
# Create people
alice = root ++> Person(name="Alice");
bob = root ++> Person(name="Bob");
charlie = root ++> Person(name="Charlie");

# Create relationships naturally
alice <+:FriendsWith:+> bob;
bob <+:FriendsWith:+> charlie;
```
```jac
node User {
    has username: str;
    has email: str;
    has created_at: str;
}

node Post {
    has title: str;
    has content: str;
    has likes: int = 0;
}

with entry {
    # This is where your program starts.
    # We will create the nodes in the graph here.
    user = root ++> User(
        username="alice",
        email="alice@example.com",
        created_at="2024-01-01"
    );

    post = user ++> Post(
        title="Hello Jac!",
        content="My first post in Jac"
    );

    print(f"User {user[0].username} created post: {post[0].title}");
}
```
```jac
node Person {
    has name: str;
    has age: int;
}

edge FamilyRelation {
    # Edges can also have properties
    has relationship_type: str;
}

with entry {
    # First, let's create our family members as nodes
    parent = root ++> Person(name="John", age=45);
    child1 = root ++> Person(name="Alice", age=20);
    child2 = root ++> Person(name="Bob", age=18);

    # Now, let's create the relationships between them
    parent +>:FamilyRelation(relationship_type="parent"):+> child1;
    parent +>:FamilyRelation(relationship_type="parent"):+> child2;
    child1 +>:FamilyRelation(relationship_type="sibling"):+> child2;

     # You can now ask questions about these relationships
    children = [parent[0]->:FamilyRelation:relationship_type=="parent":->(`?Person)];

    print(f"{parent[0].name} has {len(children)} children:");
    for child in children {
        print(f"  - {child.name} (age {child.age})");
    }
}
```
```jac
node Person {
    has name: str;
    has visited: bool = False;  # To keep track of who we've greeted
}

edge FriendsWith;

# This walker will greet every person it meets
walker GreetFriends {
    can greet with Person entry {
        if not here.visited {
            here.visited = True;
            print(f"Hello, {here.name}!");

            # Now, tell the walker to go to all connected friends
            visit [->:FriendsWith:->];
        }
    }
}

with entry {
    # Create friend network
    alice = root ++> Person(name="Alice");
    bob = root ++> Person(name="Bob");
    charlie = root ++> Person(name="Charlie");

    # Connect friends
    alice +>:FriendsWith:+> bob +>:FriendsWith:+> charlie;
    alice +>:FriendsWith:+> charlie;  # Alice also friends with Charlie

    # Start the walker on the 'alice' node to greet everyone
    alice[0] spawn GreetFriends();
}
```
```jac
node Counter {
    has count: int = 0;

    def increment() -> None;
}

impl Counter.increment {
    self.count += 1;
    print(f"Counter is now: {self.count}");
}

with entry {
    # Get or create counter
    counters = [root-->(`?Counter)];
    if not counters {
        counter = root ++> Counter();
        print("Created new counter");
    }

    # Increment and save automatically
    counter[0].increment();
}
```
```jac
jac serve counter.jac
```
```jac
node UserProfile {
    has username: str;
    has bio: str = "";
}

walker GetProfile {
    can get_user_info with entry {
         # 'root' automatically points to the current user's graph
        profiles = [root-->(`?UserProfile)];
        if profiles {
            profile = profiles[0];
            print(f"Profile: {profile.username}");
            print(f"Bio: {profile.bio}");
        } else {
            print("No profile found");
        }
    }
}

walker CreateProfile {
    has username: str;
    has bio: str;

    can create with entry {
        # It looks for the profile connected to the current user's root
        profile = root ++> UserProfile(
            username=self.username,
            bio=self.bio
        );
        print(f"Created profile for {profile[0].username}");
    }
}

with entry {
    # This code works for any user automatically
    CreateProfile(username="alice", bio="Jac developer") spawn root;
    GetProfile() spawn root;
}
```
```jac
# Variables and functions work similarly
def calculate_average(numbers: list[float]) -> float {
    if len(numbers) == 0 {
        return 0.0;
    }
    return sum(numbers) / len(numbers);
}

with entry {
    scores = [85.5, 92.0, 78.5, 96.0, 88.5];
    avg = calculate_average(scores);
    print(f"Average score: {avg}");

    # Control flow is familiar
    if avg >= 90.0 {
        print("Excellent performance!");
    } elif avg >= 80.0 {
        print("Good performance!");
    } else {
        print("Needs improvement.");
    }
}
```
```jac
node Person {
    has name: str;
    has age: int;
    has interests: list[str] = [];
}

edge FriendsWith {
    has since: str;
    has closeness: int;  # 1-10 scale
}
```
```jac
# Create friend network
alice = root ++> Person(
    name="Alice",
    age=25,
    interests=["coding", "music", "hiking"]
);

bob = root ++> Person(
    name="Bob",
    age=27,
    interests=["music", "sports", "cooking"]
);

charlie = root ++> Person(
    name="Charlie",
    age=24,
    interests=["coding", "gaming", "music"]
);

# Create friendships with metadata
alice +>:FriendsWith(since="2020-01-15", closeness=8):+> bob;
alice +>:FriendsWith(since="2021-06-10", closeness=9):+> charlie;
bob +>:FriendsWith(since="2020-12-03", closeness=7):+> charlie;
```
```jac
walker FindCommonInterests {
    # The walker needs to know who we're comparing against.
    has target_person: Person;
    # It will store the results of its search here.
    has common_interests: list[str] = [];

    # This ability runs automatically whenever the walker lands on a Person node.
    can find_common with Person entry {
        # We don't want to compare the person with themselves.
        if here == self.target_person {
            return;  # Skip self
        }

        # Find any interests this person shares with our target_person
        shared = [];
        for interest in here.interests {
            if interest in self.target_person.interests {
                shared.append(interest);
            }
        }

        # If we found any, print them and add them to our list.
        if shared {
            self.common_interests.extend(shared);
            print(f"{here.name} and {self.target_person.name} both like: {', '.join(shared)}");
        }
    }
}
```
```jac
node Person {
    has name: str;
    has age: int;
    has interests: list[str] = [];
}

edge FriendsWith {
    has since: str;
    has closeness: int;  # 1-10 scale
}

walker FindCommonInterests {
    has target_person: Person;
    has common_interests: list[str] = [];

    can find_common with Person entry {
        if here == self.target_person {
            return;  # Skip self
        }

        # Find shared interests
        shared = [];
        for interest in here.interests {
            if interest in self.target_person.interests {
                shared.append(interest);
            }
        }

        if shared {
            self.common_interests.extend(shared);
            print(f"{here.name} and {self.target_person.name} both like: {', '.join(shared)}");
        }
    }
}

with entry {
    # Create friend network
    alice = root ++> Person(
        name="Alice",
        age=25,
        interests=["coding", "music", "hiking"]
    );

    bob = root ++> Person(
        name="Bob",
        age=27,
        interests=["music", "sports", "cooking"]
    );

    charlie = root ++> Person(
        name="Charlie",
        age=24,
        interests=["coding", "gaming", "music"]
    );

    # Create friendships with metadata
    alice +>:FriendsWith(since="2020-01-15", closeness=8):+> bob;
    alice +>:FriendsWith(since="2021-06-10", closeness=9):+> charlie;
    bob +>:FriendsWith(since="2020-12-03", closeness=7):+> charlie;

    print("=== Friend Network Analysis ===");

    # 1. Find all nodes connected to Alice by a FriendsWith edge
    alice_friends = [alice[0]->:FriendsWith:->(`?Person)];
    print(f"Alice's friends: {[f.name for f in alice_friends]}");

    # 2. Create an instance of our walker, telling it to compare against Alice
    finder = FindCommonInterests(target_person=alice[0]);

    # 3. Send the walker to visit each of Alice's friends
    for friend in alice_friends {
        friend spawn finder;
    }

    # Find close friendships (closeness >= 8)
    close_friendships = [root-->->:FriendsWith:closeness >= 8:->];
    print(f"Close friendships ({len(close_friendships)} found):");
}
```
If you have experience with Python, you'll find Jac's syntax easy to learn. Core programming concepts like variables, functions, and control flow work in a very similar way.

This familiar foundation makes it easier for you to get started and begin building with Jac's unique features like nodes, edges, and walkers.


## From: byllm.md

- **`is` Keyword for Semstrings**: Added support for using `is` as an alternative to `=` in semantic string declarations (e.g., `sem MyObject.value is "A value stored in MyObject"`).
- **Removed LLM Override**: `function_call() by llm()` has been removed as it was introduce ambiguity in the grammer with LALR(1) shift/reduce error. This feature will be reintroduced in a future release with a different syntax.


## From: chapter_20.md

!!! tip "Key Migration Changes"
    - `class` → `obj`
    - `__init__` → automatic constructor with `has`
    - `:` → `;` for statement termination
    - `{}` for code blocks instead of indentation


## From: chapter_9.md

Let's break down the edge creation syntax: <+:EdgeType(attributes):+>.
science_lab: The starting node (the "source" of the edge).

- `<+: ... :+>`: This syntax creates a bi-directional edge. It means the relationship can be traversed from science_lab to dr_smith and also from dr_smith back to science_lab.
- `Teaches(...)`: The type of edge we are creating, along with the data for its attributes.
- `Teacher(...)`: The destination node.

### Directional Traversal
- `-->` : Follows outgoing edges from the current node.
- `<--` : Follows incoming edges to the current node.

These can be wrapped in a visit statement to direct walker movement:
```jac
visit [-->];   # Move to all connected child nodes
visit [<--];   # Move to all parent nodes
```

### Filter by Node Type
To narrow traversal to specific node types, use the filter syntax:
```jac
-->(`?NodeType)
```

This ensures the walker only visits nodes of the specified archetype.
```jac
# Example: Visit all Student nodes connected to the root
walker FindStudents {
    can start with `root entry {
        visit [-->(`?Student)];
    }
}
```
This allows your walker to selectively traverse part of the graph, even in the presence of mixed node types.

### Filtering by Node Attributes
To make your walkers more intelligent, you can instruct them to only visit nodes of a specific type. You achieve this using the (?NodeType) filter. It's also called **attribute-based filtering**.


```jac
-->(`?NodeType: attr1 op value1, attr2 op value2, ...)
```
Where:

- `NodeType` is the node archetype to match (e.g., `Student`)
- `attr1`, `attr2` are properties of that node
- `op` is a comparison operator


#### Supported Operators

| Operator   | Description                    | Example                             |
|------------|--------------------------------|-------------------------------------|
| `==`       | Equality                       | `grade == 90`                        |
| `!=`       | Inequality                     | `status != "inactive"`              |
| `<`        | Less than                      | `age < 18`                           |
| `>`        | Greater than                   | `score > 70`                         |
| `<=`       | Less than or equal to          | `temp <= 100`                       |
| `>=`       | Greater than or equal to       | `hour >= 12`                        |
| `is`       | Identity comparison            | `mood is "happy"`                   |
| `is not`   | Negative identity comparison   | `type is not "admin"`              |
| `in`       | Membership (value in list)     | `role in ["student", "teacher"]`    |
| `not in`   | Negative membership            | `status not in ["inactive", "banned"]` |

#### Example
```jac
# Find all students with a grade above 85
walker FindTopStudents {
    can start with `root entry {
        visit [-->(`?Student: grade > 85)];
    }
}
```
This walker will only visit `Student` nodes where the `grade` property is greater than 85.

### Filtering by Edge Type and Attributes

In addition to filtering by node types and attributes, Jac also allows you to filter based on edge types and edge attributes, enabling precise control over traversal paths in complex graphs.

To traverse only edges of a specific type, use the following syntax:
```jac
visit [->:EdgeType->];
```

This tells the walker to follow only edges labeled as `EdgeType`, regardless of the type of the nodes they connect.

#### Example
```jac
# Only follow "enrolled_in" edges
visit [->:enrolled_in->];
```

### Edge Atribute Filtering
You can further refine edge traversal by applying attribute-based filters directly to the edge:
```jac
visit [->:EdgeType: attr1 op val1, attr2 op val2:->];
```
This format allows you to filter based on metadata stored on the edge itself, not the nodes.

#### Example
```jac
# Follow "graded" edges where score is above 80
visit [->:graded: score > 80:->];
```

**Creation syntax**: Use `++>` to create new connections, `-->` to reference existing ones
**Navigation patterns**: `[-->]` for outgoing, `[<--]` for incoming connections
**Filtering support**: Apply conditions to find specific nodes or edges


## From: chapter_4.md

Lambda functions use the syntax lambda `lambda parameters: return_type: expression`. They can be assigned to a variable or used directly as an argument to another function.They are also useful for functional programming patterns like map, filter, and reduce.

For example, a simple add function can be defined as a lambda:

```jac
# This lambda takes two `float` parameters, `a` and `b`, and returns their sum as a `float`. It can be called just like a regular function.
add = lambda x: float, y: float: x + y;
```
<br />


```jac
with entry {
    add = lambda x: float, y: float: x + y;

    a: float = 10.0;
    b: float = 5.0;

    # Using the lambda function
    result: float = add(a, b);
    print(f"Result of add({a}, {b}) = {result}");
}
```
<br />
Decorators provide a clean way to add functionality to functions without modifying their core logic. The general syntax for using decorators in Jac is:

```jac
@decorator_name
def function_name(parameters) -> return_type {
    # function body
}
```
<br />


## From: chapter_3.md

Jac enforces type annotations for all collections, ensuring type safety and clarity.

The list comprehension syntax in Jac is similar to Python:
```[expression for item in iterable if condition]``` where,
`expression` is the value to include in the new list,
`item` is the variable representing each element in the original collection,
`iterable` is the collection being processed, and
`condition` is an optional filter.
Jac uses control flow statements like `if`, `elif`, and `else` for this, using curly braces {} to group the code for each block.
An `if` statement allows you to execute code conditionally based on whether a certain condition is true. In Jac, we use curly braces `{}` to define the block of code that should be executed if the condition is met.
Jac introduces a special `for-to-by` loop that gives you precise control over a sequence of numbers. This is useful when you need to iterate within a specific range with a defined step.
When you have a variable that could be one of many different types or values, a long chain of if-elif-else statements can become hard to read. Pattern matching provides a cleaner and more powerful way to handle these complex situations.
```jac
def process_grade_input(input: any) -> str {
    # The 'match' statement checks the input against several possible patterns.
    match input {
        case int() if 90 <= input <= 100:
            return f"Excellent work! Score: {input}";
        case int() if 80 <= input < 90:
            return f"Good job! Score: {input}";
        case int() if 70 <= input < 80:
            return f"Satisfactory. Score: {input}";
        case int() if 0 <= input < 70:
            return f"Needs improvement. Score: {input}";
        case str() if input in ["A", "B", "C", "D", "F"]:
            return f"Letter grade received: {input}";
        case list() if len(input) > 0:
            avg = sum(input) / len(input);
            return f"Average of {len(input)} grades: {avg}";
        # The 'catch-all' case: If no other pattern matched.
        case _:
            return "Invalid grade input";
    }
}

with entry {
    print(process_grade_input(95));        # Number grade
    print(process_grade_input("A"));       # Letter grade
    print(process_grade_input([88, 92, 85])); # List of grades
}
```
Exception handling allows you to anticipate these potential errors and manage them without crashing your program.

In Jac, you use a `try...except` block to do this. You put the code that might cause an error inside the `try` block, and the code to handle the error inside the `except` block. You can also use the raise keyword to create your own custom errors.
```jac
def safe_calculate_gpa(grades: list[int]) -> float {
    try {
        if len(grades) == 0 {
            # If the list of grades is empty, we create our own error.
            raise ValueError("No grades provided");
        }

        total = sum(grades);
        return total / len(grades);

    } except ValueError as e {
        # If a ValueError occurs, this block will run.
        print(f"Error: {e}");
        return 0.0;
    }
}

def validate_grade(grade: int) -> None {
    if grade < 0 or grade > 100 {
        raise ValueError(f"Grade {grade} is out of valid range (0-100)");
    }
}

with entry {
    # Test 1: A valid calculation.
    valid_grades: list[int] = [85, 90, 78];
    gpa: float = safe_calculate_gpa(valid_grades);
    print(f"The calculated GPA is: {gpa}");

     # Test 2: Handling a custom validation error.
    try {
        validate_grade(150);
    } except ValueError as e {
        print(f"A validation error occurred: {e}");
    }
}
```
Comments help document your Jac code clearly. Jac supports both single-line and multiline comments.

```jac
with entry {
    # This is a single-line comment
    student_name: str = "Alice";

    #*
        This is a
        multi-line comment.
    *#

    grades: list[int] = [88, 92, 85];

    print(student_name);
    print(grades);
}
```
Most beginner issues stem from Jac's stricter type requirements compared to Python. Here are the most common mistakes and their solutions.

| **Issue** | **Solution** |
|-----------|--------------|
| Missing semicolons | Add `;` at the end of statements |
| Missing type annotations | Add types to all variables: `x: int = 5;` |
| No entry block | Add `with entry { ... }` for executable scripts |
| Python-style indentation | Use `{ }` braces instead of indentation |

### Example of Common Fixes
Someone unfamiliar with Jac might write code like this:

```jac
# This won't work - missing types and semicolons
def greet(name) {
    return f"Hello, {name}"
}

# Missing entry block
print(greet("World"))
```
The corrected version of the code would be:
```jac
# This works - proper types and syntax
def greet(name: str) -> str {
    return f"Hello, {name}";
}

with entry {
    print(greet("World"));
}
```


## From: breaking_changes.md

#### 1. `check` Keyword Removed - Use `assert` in Test Blocks

The `check` keyword has been removed from Jaclang. All testing functionality is now unified under `assert` statements, which behave differently depending on context: raising exceptions in regular code and reporting test failures within `test` blocks.

**Before**

```jac
glob a: int = 5;
glob b: int = 2;

test test_equality {
    check a == 5;
    check b == 2;
}

test test_comparison {
    check a > b;
    check a - b == 3;
}

test test_membership {
    check "a" in "abc";
    check "d" not in "abc";
}

test test_function_result {
    check almostEqual(a + b, 7);
}
```

**After**

```jac
glob a: int = 5;
glob b: int = 2;

test test_equality {
    assert a == 5;
    assert b == 2;
}

test test_comparison {
    assert a > b;
    assert a - b == 3;
}

test test_membership {
    assert "a" in "abc";
    assert "d" not in "abc";
}

test test_function_result {
    assert almostEqual(a + b, 7);
}
```

**Key Changes:**
- Replace all `check` statements with `assert` statements in test blocks
- `assert` statements in test blocks report test failures without raising exceptions
- `assert` statements outside test blocks continue to raise `AssertionError` as before
- Optional error messages can be added: `assert condition, "Error message";`

This change unifies the testing and validation syntax, making the language more consistent while maintaining all testing capabilities.

#### 1. Global, Nonlocal Operators Updated to `global`, `nonlocal`

This renaming aims to make the operator's purpose align with python, as `global`, `nonlocal` more aligned with python.

**Before**

```jac
glob x = "Jaclang ";

def outer_func -> None {
    :global: x; # :g: also correct

    x = 'Jaclang is ';
    y = 'Awesome';
    def inner_func -> tuple[str, str] {
        :nonlocal: y; #:nl: also correct

        y = "Fantastic";
        return (x, y);
    }
    print(x, y);
    print(inner_func());
}

with entry {
    outer_func();
}
```

**After**

```jac
glob x = "Jaclang ";

def outer_func -> None {
    global x;

    x = 'Jaclang is ';
    y = 'Awesome';
    def inner_func -> tuple[str, str] {
        nonlocal y;

        y = "Fantastic";
        return (x, y);
    }
    print(x, y);
    print(inner_func());
}

with entry {
    outer_func();
}
```

#### 1. `impl` keyword introduced to simplify Implementation

The new `impl` keyword provides a simpler and more explicit way to implement abilities and methods for objects, nodes, edges, and other types. This replaces the previous more complex colon-based syntax for implementation.

**Before (v0.7.x):**
```jac
:obj:Circle:def:area -> float {
    return math.pi * self.radius * self.radius;
}

:node:Person:can:greet with Room entry {
    print("Hello, I am " + self.name);
}

:def:calculate_distance(x: float, y: float) -> float {
    return math.sqrt(x*x + y*y);
}
```

**After (v0.8.0+):**
```jac
impl Circle.area -> float {
    return math.pi * self.radius * self.radius;
}

impl Person.greet with Room entry {
    return "Hello, I am " + self.name;
}

impl calculate_distance(x: float, y: float) -> float {
    return math.sqrt(x*x + y*y);
}
```

This change makes the implementation syntax more readable, eliminates ambiguity, and better aligns with object-oriented programming conventions by using the familiar dot notation to indicate which type a method belongs to.

#### 2. Inheritance base classes specification syntax changed

The syntax for specifying inheritance has been updated from using colons to using parentheses, which better aligns with common object-oriented programming languages.

**Before (v0.7.x):**
```jac
obj Vehicle {
    has wheels: int;
}

obj Car :Vehicle: {
    has doors: int = 4;
}

node BaseUser {
    has username: str;
}

node AdminUser :BaseUser: {
    has is_admin: bool = true;
}
```

**After (v0.8.0+):**
```jac
obj Vehicle {
    has wheels: int;
}

obj Car(Vehicle) {
    has doors: int = 4;
}

node BaseUser {
    has username: str;
}

node AdminUser(BaseUser) {
    has is_admin: bool = true;
}
```

This change makes the inheritance syntax more intuitive and consistent with languages like Python, making it easier for developers to understand class hierarchies at a glance.

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

#### 5. Changes to lambda syntax and `lambda` instroduced

Instead of using the `with x: int can x;` type syntax the updated lambda syntax now replaces `with` and `can` with `lambda` and `:` repsectively.

**Before (v0.7.x):**
```jac
# Lambda function syntax with 'with' and 'can'
with entry {
    square_func = with x: int can x * x;
}
```

**After (v0.8.0+):**
```jac
# Updated lambda
with entry {
    square_func = lambda x: int: x * x;
}
```

This change brings Jac's lambda syntax closer to Python's familiar `lambda parameter: expression` pattern, making it more intuitive for developers coming from Python backgrounds while maintaining Jac's type annotations.

#### 6. Data spatial arrow notation updated

The syntax for typed arrow notations are updated as `-:MyEdge:->` and `+:MyEdge:+>` is now `->:MyEdge:->` and `+>:MyEdge:+> for reference and creations.

**Before (v0.7.x):**
```jac
friends = [-:Friendship:->];
alice <+:Friendship:strength=0.9:+ bob;
```

**After (v0.8.0+):**
```jac
friends = [->:Friendship:->];
alice <+:Friendship:strength=0.9:<+ bob;
```

This change was made to eliminate syntax conflicts with Python-style list slicing operations (e.g., `my_list[:-1]` was forced to be written `my_list[: -1]`). The new arrow notation provides clearer directional indication while ensuring that object-spatial operations don't conflict with the token parsing for common list operations.

#### 7. Import `from` syntax updated for clarity

The syntax for importing specific modules or components from a package has been updated to use curly braces for better readability and to align with modern language conventions.

**Before (v0.7.x):**
```jac
import from pygame_mock, color, display;
import from utils, helper, math_utils, string_formatter;
```

**After (v0.8.0+):**
```jac
import from pygame_mock { color, display };
import from utils { helper, math_utils, string_formatter };
```

This new syntax using curly braces makes it clearer which modules are being imported from which package, especially when importing multiple items from different packages.

#### 8. Import statement are auto resolved (no language hints needed)

The language-specific import syntax has been simplified by removing the explicit language annotations (`:py` and `:jac`). The compiler now automatically resolves imports based on context and file extensions.

**Before (v0.7.x):**
```jac
import:py requests;
import:jac graph_utils;
import:py json, os, sys;
```

**After (v0.8.0+):**
```jac
import requests;
import graph_utils;
import json, os, sys;
```

This change simplifies the import syntax, making code cleaner while still maintaining the ability to import from both Python and Jac modules. The Jac compiler now intelligently determines the appropriate language context for each import.


## From: jaclang.md

- **Support iter for statement**: Iter for statement is supported in order to utilize traditional for loop in javascript.
- **JavaScript Export Semantics for Public Declarations**: Declarations explicitly annotated with `:pub` now generate JavaScript `export` statements. This applies to classes (`obj :pub`), functions (`def :pub`), enums (`enum :pub`), and global variables (`glob :pub`), enabling proper ES module exports in generated JavaScript code.
- **Optional Ability Names**: Ability declarations now support optional names, enabling anonymous abilities with event clauses (e.g., `can with entry { ... }`). When a name is not provided, the compiler automatically generates a unique internal name based on the event type and source location. This feature simplifies walker definitions by reducing boilerplate for simple entry/exit abilities.
- **Formatted String Literals (f-strings)**: Added improved and comprehensive support for Python-style formatted string literals in Jac with full feature parity.
- **Switch Case Statement**: Switch statement is introduced and javascript style fallthrough behavior is also supported.
- **Triple Quoted F-String Support**: Added support for triple quoted f-strings in the language, enabling multi-line formatted strings with embedded expressions (e.g., `f"""Hello {name}"""`).
- **Clean generator expression within function calls**: Enhanced the grammar to support generator expressions without braces in a function call. And python to jac conversion will also make it clean.
- **Support attribute pattern in Match Case**: With the latest bug fix, attribute pattern in match case is supported. Therefore developers use match case pattern like `case a.b.c`.
- **Check Statements Removed**: The `check` keyword has been removed from Jaclang. All testing functionality previously provided by `check` statements is now handled by `assert` statements within test blocks. Assert statements now behave differently depending on context: in regular code they raise `AssertionError` exceptions, while within `test` blocks they integrate with Jac's testing framework to report test failures. This unification simplifies the language by using a single construct for both validation and testing purposes.
- **Complete Python Function Parameter Syntax Support**: Added full support for advanced Python function parameter patterns including positional-only parameters (`/` separator), keyword-only parameters (`*` separator without type hints), and complex parameter combinations (e.g., `def foo(a, b, /, *, c, d=1, **kwargs): ...`). This enhancement enables seamless Python-to-Jac conversion (`py2jac`) by supporting the complete Python function signature syntax.
- **Unicode String Literal Support**: Fixed unicode character handling in string literals. Unicode characters like "✓", "○", emojis, and other international characters are now properly preserved during compilation instead of being corrupted into byte sequences.
- **Removed Ignore Statements**: The `ignore` keyword and ignore statements have been removed as this functionality can be achieved more elegantly by modifying path collection expressions directly in visit statements.
- **`impl` Keyword for Implementation**: Introduced the `impl` keyword for a simpler, more explicit way to implement abilities and methods for objects, nodes, edges, and other types, replacing the previous colon-based syntax.
- **Updated Inheritance Syntax**: Changed the syntax for specifying inheritance from colons to parentheses (e.g., `obj Car(Vehicle)`) for better alignment with common object-oriented programming languages.
- **`def` Keyword for Functions**: The `def` keyword is now used for traditional Python-like functions and methods, while `can` is reserved for object-spatial abilities.
- **Lambda Syntax Update**: The lambda syntax has been updated from `with x: int can x;` to `lambda x: int: x * x;`, aligning it more closely with Python's lambda syntax.
- **Object-Spatial Arrow Notation Update**: Typed arrow notations `-:MyEdge:->` and `+:MyEdge:+>` are now `->:MyEdge:->` and `+>:MyEdge:+>` respectively, to avoid conflicts with Python-style list slicing.
- **Import `from` Syntax Update**: The syntax for importing specific modules from a package now uses curly braces (e.g., `import from utils { helper, math_utils }`) for improved clarity.
- **Auto-Resolved Imports**: Removed the need for explicit language annotations (`:py`, `:jac`) in import statements; the compiler now automatically resolves imports.


## From: creating_byllm_plugins.md

When Jaclang's `by llm()` syntax is used, the runtime system looks for registered plugins that implement the `call_llm` hook.

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


## From: tutorial.md

```Jac
node Person{
    has name: str;
    has email: str;
}

node EmailNode{
    has sender: str;
    has recipients: str;
    has date: str;
    has subject: str;
    has body: str;
    has email_uuid: str;
}
```
```Jac
recipientNodes: list[People];
senderNode: People;
emailNode: Email;

senderNode ++> emailNode;
for node in recipientNodes{
    emailNode ++> node;
}
```
```Jac
walker FindSenderNode {
    has target: str;
    has person: Person = None;

    can start with `root entry {
        visit [-->];
        return self.person;
    }

    can search with Person entry {
        if here.email == self.target {
            self.person = here;
            disengage;
        }
    }
}
```
- `has <memberVariable>: <type>`: Create member variables for walker
- `can <attributeName> with <nodeType> entry`: Assigns walker behavior when it is on the node type (root must have `` `root ``)
- `disengage`: Stops the walker immediately so it doesn't keep searching.
- `visit [-->]`: Tells the walker to explore all nodes reachable from this one along outgoing edges.
```Jac
FindSend = FindSenderNode(target=sender_email);
```
```Jac
root spawn FindSend;
```
```Jac
sender: Person = FindSend.person;
```
```Jac
import from byllm.lib { Model }

glob llm = Model(model_name="openai/gpt-5", verbose=True);

"""
Summarize relevant part of each option to the initial query not in current conversation history
"""
def summarize(presented_option: list[str], convo_history: list[dict]) -> str by llm();
```
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
```jac
response = choose_next_email_node(person_formatted, sent_formatted, received_formatted, conversation_history);
```


## From: rpg_game.md

```jac
obj Position {
    has x: int, y: int;     # 2D coordinate

}

obj Wall {
    has start_pos: Position, end_pos: Position;       # wall starts and ends here
}
```
```jac
obj Level {
    has name: str, difficulty: int;     # difficulty scaling
    has width: int, height: int, num_wall: int; # spatial constraints
    has num_enemies: int; time_countdown: int;  # enemies + time
    n_retries_allowed: int;     # retries allowed
}

obj Map {
    has level: Level, walls: list[Wall];    # embeds Level + walls
    has small_obstacles: list[Position];    # extra blocks
    has enemies: list[Position];    # enemy positions
    has player_pos: Position;       # player start
}
```
```jac
import from byllm.lib { Model }

glob llm = Model(model_name="gpt-4o", verbose=True);
```
```jac
obj LevelManager {
    has current_level: int = 0, current_difficulty: int = 1,
        prev_levels: list[Level] = [], prev_level_maps: list[Map] = [];

    def create_next_level (last_levels: list[Level], difficulty: int, level_width: int, level_height: int)
    -> Level by llm();

    def create_next_map(level: Level) -> Map by llm();
}
```
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
```jac
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

