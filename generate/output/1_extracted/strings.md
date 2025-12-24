# strings


## From: syntax_quick_reference.md

```jac
	print(f"sum: {add} prod:{mult}"); 		 # values can be formatted with f-strings
```


## From: beginners_guide_to_jac.md

#### Text (Strings)
```jac
with entry {
    greeting = "Hello";
    name = "Bob";
    message = "Welcome to Jac!";

    print(greeting);  # Shows: Hello
}
```

Strings go inside quotes: `"like this"` or `'like this'`

**Pro tip:** The `f` before a string lets you insert variables using `{variable_name}`

```jac
with entry {
    name: str = "Alice";      # str means string (text)
    age: int = 25;            # int means integer (whole number)
    height: float = 5.6;      # float means decimal number
    is_student: bool = True;  # bool means boolean (True/False)

    print(f"{name} is {age} years old");
}
```

```jac
with entry {
    # String formatting
    name = "Alice";
    age = 25;
    message = f"Hello, {name}! You are {age} years old.";
    print(message);
}
```


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
        all_done = all(dep.status == "complete"


## From: chapter_2.md

### Strings
A string is a sequence of characters, like a name or a sentence. Strings are declared with the `str` type and are enclosed in quotes.

```jac
with entry {
    student_name: str = "Alice Johnson";
    # You can use f-strings to easily include variables in your output.
    print(f"Student Name: {student_name}");
}
```


## From: byllm.md

- **Semantic Strings**: Introduced `sem` strings to attach natural language descriptions to code elements like functions, classes, and parameters. These semantic annotations can be used by Large Language Models (LLMs) to enable intelligent, AI-powered code generation and execution. (mtllm)


## From: chapter_5.md

**Semantic strings** provide additional context to AI functions via the `sem` keyword, allowing for more nuanced understanding without cluttering your code. They're particularly useful for domain-specific applications.

```jac
# enhanced_captioner.jac
import from byllm.lib { Model, Image }

glob vision_llm = Model(model_name="gpt-4.1-mini");

obj PhotoAnalyzer {
    has photographer_name: str;
    has style_preference: str;
    has image: Image;
}

# Add semantic context for better AI understanding
sem PhotoAnalyzer = "Professional photo analysis tool for photographers";
sem PhotoAnalyzer.photographer_name = "Name of the photographer for personalized analysis";
sem PhotoAnalyzer.style_preference = "Preferred photography style (artistic, documentary, commercial)";


"""Generate caption considering photographer's style preference."""
def generate_styled_caption(pa: PhotoAnalyzer) -> str by vision_llm();

"""Provide technical photography feedback."""
def analyze_composition(pa: PhotoAnalyzer) -> list[str] by vision_llm();

"""Suggest improvements for the photo."""
def suggest_improvements(pa: PhotoAnalyzer) -> list[str] by vision_llm();


with entry {
    analyzer = PhotoAnalyzer(
        photographer_name="Alice",
        style_preference="artistic",
        image=Image("photo.jpg")
    );

    # Generate styled caption
    caption = generate_styled_caption(analyzer);
    print(f"Styled caption: {caption}");

    # Analyze composition
    composition = analyze_composition(analyzer);
    print(f"Composition analysis: {composition}");

    # Get improvement suggestions
    suggestions = suggest_improvements(analyzer);
    print(f"Suggestions: {suggestions}");
}
```


## From: jaclang.md

- **Formatted String Literals (f-strings)**: Added improved and comprehensive support for Python-style formatted string literals in Jac with full feature parity.
- **Triple Quoted F-String Support**: Added support for triple quoted f-strings in the language, enabling multi-line formatted strings with embedded expressions (e.g., `f"""Hello {name}"""`).
- **Unicode String Literal Support**: Fixed unicode character handling in string literals. Unicode characters like "✓", "○", emojis, and other international characters are now properly preserved during compilation instead of being corrupted into byte sequences.


## From: agentic_ai.md

To help the LLM make better decisions, especially during routing, you can annotate enums and objects with **semantic strings** (semstrings). These provide the LLM with natural language descriptions of each option, significantly improving decision quality.

**Why Semstrings Matter:**

When the LLM calls `plan_tasks()` or needs to route tasks, it receives the enum definition. Without semstrings, it only sees:
```
RoutingNodes.TASK_HANDLING
RoutingNodes.EMAIL_HANDLING
RoutingNodes.GENERAL_CHAT
```

With semstrings, the LLM understands the purpose of each routing option:

```jac linenums="1"
sem RoutingNodes.TASK_HANDLING = "Creating/deleting/updating/summarizing tasks to TODO";
sem RoutingNodes.EMAIL_HANDLING = "Composing and managing emails";
sem RoutingNodes.GENERAL_CHAT = "Providing intelligent answers, productivity advice, and general AI assistance across various topics.";
```

Now when the LLM decomposes a request like "Schedule a meeting and send a follow-up email", it can confidently route the first subtask to TASK_HANDLING and the second to EMAIL_HANDLING because it understands each agent's purpose.

**Best Practices:**

- Write semstrings that clearly describe **what** the agent does and **when** to use it
- Avoid generic descriptions—be specific about capabilities and use cases
- Include examples if the purpose might be ambiguous
- For objects, annotate key fields to help the LLM understand the data structure

Semstrings are a simple but powerful way to embed domain knowledge into your agentic application, enabling more reliable LLM routing and planning decisions.


## From: usage.md

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

