# objects


## From: tool_suite.md

- Jac Lens specifically supports graph visualization for Scale Native applications.
- Jac Lens is another tool for visualizing your Jac object-spatial graphs.
- It's a fast and beginner-friendly way to learn Jac, experiment with Object-Spatial Programming, or prototype ideas!


## From: jac_in_a_flash.md

Classes are declared with `obj`.
The second version moves attribute definitions into the class body using the `has` keyword. Fields may specify types and default values directly on the declaration.
The fourth version splits object declarations from their implementations using `impl`. The object lists method signatures (`def init;`, `override def play;`), and the actual bodies are provided later in `impl Class.method` blocks. This separation keeps the interface clean and helps organise larger codebases.


## From: jac_playground.md

The Graph Visualizer makes Jac's spatial programming concepts tangible, allowing you to see exactly how your objects, walkers, and edges interact during program execution.

### Object Spatial Programming
Jac's unique approach to spatial programming and object relationships. These advanced examples show how Jac handles complex data structures and spatial reasoning.


## From: keywords.md

**Core Archetype Keywords**

| Keyword | Description |
| --- | --- |
| [`obj`](https://www.jac-lang.org/learn/jac_ref/#archetype-types) | Defines a standard object, similar to a Python class, for holding data and behaviors. |
| [`class`](https://www.jac-lang.org/learn/jac_ref/#archetype-types) |Defines a standard Python-compatible class, allowing for seamless integration with the Python ecosystem. |


## From: tour.md

Jac introduces a new programming model that lets developers articulate relationships between objects in a graph-like structure and express computation as walkers that traverse this graph. This model is particularly effective for applications involving connected data, such as social networks, knowledge graphs, or file systems, and can greatly reduce code complexity. OSP also provides the foundation for agentic workflows and enables Jaseci’s scale-native execution, reducing backend development and deployment overhead.


## From: library_mode.md

| Class | Description | Usage |
|-------|-------------|-------|
| `Obj` | Base class for all archetypes | Generic archetype base |


## From: example.md

Traditional OOP with python classes that expresses object hierarchy and behavior is fully supported in Jac. Additionally, Jac introduces a new concept called Object-Spatial Programing (OSP). Using OSP construts, programmers can express object relationships as graphs
```jac
obj Tweet {
    has content: str, author: str, timestamp: str, likes: int = 0;

    def like() -> None;
    def unlike() -> None;
    def get_preview(max_length: int) -> str;
    def get_like_count() -> int;
}
```


## From: syntax_quick_reference.md

```jac
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
```


## From: dspfoundation.md

1. **Object Classes** ($\tau_{\text{obj}}$): These are conventional classes, analogous to traditional OOP class types. Objects can have properties that describe their intrinsic characteristics and methods that operate on those properties. They serve as the foundational building blocks from which other archetypes derive, maintaining backward compatibility with existing OOP concepts while enabling integration with object-spatial extensions.

#### Formalization

Let $C$ be the set of all class definitions in the programming model, where:

1. $\tau_{\text{obj}} \in C$ is a standard object class type, representing the universal supertype from which all other archetypes inherit.

### Instantiation Rules

To maintain object-spatial graph consistency and support higher-order topological structures, OSP enforces specific instantiation constraints for different archetypes and references:

1. **Object Instantiation**: Standard objects follow traditional OOP instantiation patterns, with constructors defining initial state.

### Lifecycle Management

OSP extends traditional object lifecycle management with specialized rules for object-spatial archetypes:

1. *Object Lifecycle*: Standard object instances follow traditional object lifecycle patterns from OOP, with standard creation, usage, and garbage collection.


## From: superset_python.md

```jac
obj Person {
    has name: str;
    has age: int;

    def greet() -> None {
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.");
    }
}
```

```python
class Person(Obj):
    name: str
    age: int

    def greet(self) -> None:
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.")
```
The compiled output demonstrates how Jac's object-oriented features map to standard Python classes inheriting from `Obj` (Jac's base object archetype), with imports from the `jaclang.lib` package.


## From: chapter_7.md

Jac fully supports the principles of Object-Oriented Programming (OOP) but enhances them to be more intuitive and efficient. This chapter will guide you through using Jac's obj archetype to create well-structured, maintainable, and powerful objects.

Jac simplifies the object creation process by providing features like **automatic constructors**, **implementation separation**, and **improved access control**, which reduce boilerplate code and allow you to focus more on the logic of your application.

## Jac `obj` Archetype
In Jac, you define a blueprint for an object using the `obj` archetype, which serves a similar purpose to the class keyword in Python. An `obj` bundles data (attributes) and behavior (methods) into a single, self-contained unit.

Let's define a `Pet` object to see how this works.

```jac
obj Pet {
    # 1. Define attributes with the 'has' keyword.
    has name: str;
    has species: str;
    has age: int;
    has is_adopted: bool = False;  # Automatic default

    # 2. Define methods with the 'def' keyword.
    # Methods use 'self' to access the object's own attributes.
    def adopt() -> None {
        self.is_adopted = True;
        print(f"{self.name} has been adopted!");
    }

    def get_info() -> str {
        status = "adopted" if self.is_adopted else "available";
        return f"{self.name} is a {self.age}-year-old {self.species} ({status})";
    }
}

with entry {
    # 3. Create an instance using the automatic constructor.
    pet = Pet(name="Buddy", species="dog", age=3);
    print(pet.get_info());
    pet.adopt();
}
```
Let's break down the key features demonstrated in this example.

1. Defining Attributes with `has`: The `has` keyword is used to declare the data fields (attributes) that each Pet object will hold. You must provide a type for each attribute, and you can optionally set a default value, like `is_adopted: bool = False`.
2. The Automatic Constructor: Notice that we did not have to write an __init__ method. Jac automatically generates a constructor for you based on the attributes you declare with has. This saves you from writing repetitive boilerplate code and allows you to create a new Pet instance with a clean and direct syntax: `Pet(name="Buddy", species="dog", age=3)`.

### Advanced Constructor Features

Sometimes, you need to run logic after an object's initial attributes have been set. For this, Jac provides the `postinit` method. This is useful for calculated properties or for validation that depends on multiple attributes.
To use it, you declare an attribute with the by `postinit` modifier. This signals that the attribute exists, but its value will be assigned within the `postinit` method.
Let's enhance our pet shop example. We'll create a PetShop object and use `postinit` to automatically set its is_open status based on whether it has reached its capacity.

```jac
obj PetShop {
    # Attributes set by the automatic constructor
    has name: str;
    has pets: list[Pet] = [];
    has capacity: int = 10;
    # This attribute's value will be calculated after initialization.
    has is_open: bool by postinit;

     # This method runs automatically after the object is created
    def postinit() -> None {
        # This logic determines the value of 'is_open'.
        self.is_open = len(self.pets) < self.capacity;
        print(f"{self.name} shop initialized with {len(self.pets)} pets");
    }
}
```

## Object Inheritance
Inheritance is a fundamental concept in OOP that allows you to create a new, specialized object based on an existing one. The new object, or subclass, inherits all the attributes and methods of the parent object, and can add its own unique features or override existing ones. This promotes code reuse and helps create a logical hierarchy.

### Simple Inheritance Example

```jac
obj Animal {
    has name: str;
    has species: str;
    has age: int;

    def make_sound() -> None {
        print(f"{self.name} makes a sound.");
    }
}
# A subclass that inherits from Animal
obj Dog(Animal) {
    has breed: str;

    def make_sound() -> None {
        print(f"{self.name} barks.");
    }
}

obj Cat(Animal) {
    has color: str;

    def make_sound() -> None {
        print(f"{self.name} meows.");
    }
}
```
In this example, both `Dog` and `Cat` automatically have the `name`, `species`, and `age` attributes from Animal. However, they each provide a specialized version of the `make_sound` method, demonstrating polymorphism.

## Access Control with `:pub`, `:priv`, `:protect`
To create robust and secure objects, it is important to control which of their attributes and methods can be accessed from outside the object's own code. This principle is called encapsulation. Unlike Python, Jac provides explicit keywords that are enforced by the runtime.

### Public Access
Public members are accessible from anywhere. This is the default behavior in Jac, so the `:pub` keyword is optional but can be used for clarity.

```jac
obj PublicExample {
    # This attribute is public by default.
    has :pub public_property: str;

    # Explicitly marking a method as public.
    def :pub public_method() -> str {
        return "This is a public method";
    }
}
with entry {
    example = PublicExample(public_property="Hello");
    # Both are accessible from outside the object.
    print(example.public_method());
    print(example.public_property);
}
```

### Private Access
Private members, marked with `:priv`, can only be accessed from within the object itself. Any attempt to access a private member from outside code will result in an error. This is essential for protecting an object's internal state.

```jac
obj PrivateExample {
    has :priv private_property: str;
    has :priv another_private_property: int = 42;

    def :priv private_method() -> str {
        return "This is a private method";
    }

    def :pub public_method() -> str {
        return self.private_method();
    }
}
with entry {
    example = PrivateExample(private_property="Secret");
    print(example.public_method());
    # print(example.private_property);  # This would raise an error
}
```

### Protected Access
Protected members, marked with `:protect`, create a middle ground between public and private. They are accessible within the object that defines them and within any of its subclasses. This is useful for creating internal logic that you want to share across a family of related objects but still keep hidden from the outside world.

```jac
obj ProtectedExample {

    has :protect protected_property: str = "Protected";
    has :protect protected_list: list[int] = [];
    has :protect protected_dict: dict[str, int] = {"key": 1};

    def :protect protected_method() -> str {
        return "This is a protected method";
    }
}
obj SubProtectedExample(ProtectedExample) {
    def :pub public_method() -> str {
        return self.protected_method();
    }
}
with entry {
    example = SubProtectedExample();
    print(example.public_method());
    print(example.protected_property);
    print(example.protected_list);
    print(example.protected_dict);
}
```

### Example: Pet Record System

Let's combine these access control concepts into a practical example. We will build a `PetRecord` object that securely manages a pet's information.

- Public information, like the pet's name, will be freely accessible.
- Protected information, like medical history, will be accessible only to specialized subclasses like a VetRecord.
- Private information, like the owner's contact details, will be strictly controlled by the object itself.

```jac
obj PetRecord {
    # Public - anyone can access
    has :pub name: str;
    has :pub species: str;

    # Private - only this class
    has :priv owner_contact: str;
    has :priv microchip_id: str;

    # Protected - only this class and subclasses
    has :protect medical_history: list[str] = [];
    has :protect last_checkup: str = "";

    # Public method
    def :pub get_basic_info() -> str {
        return f"{self.name} is a {self.species}";
    }

    # Protected method - for vets and staff
    def :protect add_medical_record(record: str) -> None {
        self.medical_history.append(record);
        print(f"Medical record added for {self.name}");
    }

    # Private method - internal use only
    def :priv validate_contact(contact: str) -> bool {
        return "@" in contact and len(contact) > 5;
    }

    def :pub update_owner_contact(new_contact: str) -> bool {
        if self.validate_contact(new_contact) {
            self.owner_contact = new_contact;
            return True;
        }
        return False;
    }
}

obj VetRecord(PetRecord) {
    has :protect vet_notes: str = "";

    def :pub add_vet_note(note: str) -> None {
        # Can access protected members from parent
        self.add_medical_record(f"Vet note: {note}");
        self.vet_notes = note;
    }

    def :pub get_medical_summary() -> str {
        # Can access protected data
        record_count = len(self.medical_history);
        return f"{self.name} has {record_count} medical records";
    }
}

with entry {
    # Create a pet record
    pet = PetRecord(
        name="Fluffy",
        species="cat",
        owner_contact="owner@example.com",
        microchip_id="123456789"
    );

    # Public access works
    print(pet.get_basic_info());
    print(f"Pet name: {pet.name}");

    # Update contact through public method
    success = pet.update_owner_contact("new_owner@example.com");
    print(f"Contact updated: {success}");

    # Vet record with access to protected methods
    vet_record = VetRecord(
        name="Rex",
        species="dog",
        owner_contact="owner2@example.com",
        microchip_id="987654321"
    );

    vet_record.add_vet_note("Annual checkup - healthy");
    print(vet_record.get_medical_summary());
}
```

## Key Differences from Python OOP
- **Automatic Constructors**: No need to write `__init__` methods
- **Enforced Access Control**: `:pub`, `:priv`, `:protect` are actually enforced
- **Clean Inheritance**: Automatic constructor chaining in inheritance
- **Type Safety**: All method parameters and returns must be typed
- **Implementation Separation**: Can separate interface from implementation

In this chapter, you've learned how Jac builds upon classic Object-Oriented Programming with features that promote cleaner, safer, and more maintainable code. You now have the tools to create robust, well-structured objects with automatic constructors, enforced access control, and clear inheritance.

These concepts form the foundation upon which Jac's most powerful paradigm is built. In the next chapter, we will make the leap from Object-Oriented to Object-Spatial Programming (OSP). We will see how these objects are extended into nodes that can exist in a graph, giving them a spatial context and unlocking a new way to handle complex, interconnected data.


## From: jsx_client_serv_design.md

```jac
// Client object - available on both client and server
cl obj ButtonProps {
    has label: str = "Hello";
    has count: int = 0;
}
```

```jac
// Client-side component
cl obj CardProps {
    has title: str = "Untitled";
    has content: str = "";
}
```


## From: chapter_6.md

Jac encourages a clean architectural pattern that separates what a component does from how it does it. This is achieved by splitting an object's or node's definition (its interface) from its method logic (its implementation).

The interface is defined in a `.jac` file, while the implementation is placed in a corresponding .`impl.jac` file. When you import the object, Jac automatically links them together.
```jac
# Interface definition
obj Calculator {
    has precision: int = 2;

    def add(a: float, b: float) -> float;
    def subtract(a: float, b: float) -> float;
    def multiply(a: float, b: float) -> float;
    def divide(a: float, b: float) -> float;
}
```
```jac
# Implementation file
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


## From: chapter_10.md

A walker is defined with the walker archetype. Like an obj, it can have has attributes to store data and def methods for internal logic. At this stage, a walker is just an object; it doesn't move or interact with the graph until it is "spawned."


## From: chapter_12.md

```jac
            obj __specs__ {
                static has auth: bool = False;
            }
```

```jac
            obj __specs__ {
                static has auth: bool = False;
            }
```

```jac
            obj __specs__ {
                static has auth: bool = False;
            }
```

```jac
    obj __specs__ {
        static has auth: bool = False;
        static has methods: list = ["get"];
    }
```

```jac
        obj __specs__ {
            static has auth: bool = False;
        }
```


## From: chapter_18.md

```jac
node WeatherData {
    has city: str;
    has temperature: float;
    has description: str;
    has last_updated: str;
}
```
```jac
node WeatherData {
    has city: str;
    has temperature: float;
    has description: str;
    has last_updated: str;
}
```


## From: chapter_11.md

```jac
node Person {
    has name: str;
    has age: int;
    has city: str;
}

edge FriendsWith {
    has since: str;
    has closeness: int; # 1-10 scale
}

with entry {
    # Create a social network
    alice = root ++> Person(name="Alice", age=25, city="NYC");
    bob = root ++> Person(name="Bob", age=30, city="SF");
    charlie = root ++> Person(name="Charlie", age=22, city="NYC");
    diana = root ++> Person(name="Diana", age=28, city="LA");

    # Create friendships
    alice +>:FriendsWith(since="2020", closeness=8):+> bob;
    alice +>:FriendsWith(since="2021", closeness=9):+> charlie;
    bob +>:FriendsWith(since="2019", closeness=6):+> diana;

    # Find all young people in NYC (age < 25)
    nyc = [root-->(`?Person)](?city == "NYC");
    print("People in NYC:");
    for person in nyc {
        print(f"  {person.name}, age {person.age}");
    }
    young_nyc = nyc(?age < 25);
    print("Young people in NYC:");
    for person in young_nyc {
        print(f"  {person.name}, age {person.age}");
    }

    # Find Alice's close friends (closeness >= 8)
    close_friends = [alice->:FriendsWith:closeness >= 8:->(`?Person)];
    print(f"Alice's close friends:");
    for friend in close_friends {
        print(f"  {friend.name}");
    }

    # Find all friendships that started before 2021
    old_friendships = [root->:FriendsWith:since < "2021":->];
    print(f"Old friendships: {len(old_friendships)} found");
}
```
```jac
node Person {
    has name: str;
    has age: int;
    has city: str;
}

edge FriendsWith {
    has since: str;
    has closeness: int; # 1-10 scale
}

with entry {
    # Create extended family network
    john = root ++> Person(name="John", age=45, city="NYC");
    emma = root ++> Person(name="Emma", age=43, city="NYC");
    alice = root ++> Person(name="Alice", age=20, city="SF");
    bob = root ++> Person(name="Bob", age=18, city="NYC");

    # Family relationships
    john +>:FriendsWith(since="1995", closeness=10):+> emma;  # Married
    [john[0], emma[0]] +>:FriendsWith(since="2004", closeness=10):+> alice;  # Parents
    [john[0], emma[0]] +>:FriendsWith(since="2006", closeness=10):+> bob;    # Parents

    # Find John's family members under 25
    young_family = [john[0]->:FriendsWith:closeness == 10:->(`?Person)](?age < 25);
    print("John's young family members:");
    for person in young_family {
        print(f"  {person.name}, age {person.age}");
    }

    # Find all people in NYC connected to John
    nyc_connections = [john[0]->:FriendsWith:->(`?Person)](?city == "NYC");
    print(f"John's NYC connections:");
    for person in nyc_connections {
        print(f"  {person.name}");
    }

    # Find friends of friends (2-hop connections)
    friends_of_friends = [john[0]->:FriendsWith:->->:FriendsWith:->(`?Person)];
    print(f"Friend of friends: {len(friends_of_friends)} found");
    for person in friends_of_friends {
        print(f"  {person.name}");
    }
}
```
```jac
node Person {
    has name: str;
    has level: int = 0;
}

edge ParentOf {}

walker BFSWalker {
    can traverse with Person entry {
        print(f"BFS visiting: {here.name} (level {here.level})");

        # Visit children - default queue behavior (breadth-first)
        children = [->:ParentOf:->(`?Person)];
        for child in children {
            child.level = here.level + 1;
        }
        visit children;
    }
}

walker DFSWalker {
    can traverse with Person entry {
        print(f"DFS visiting: {here.name} (level {here.level})");

        # Visit children with :0: (stack behavior for depth-first)
        children = [->:ParentOf:->(`?Person)];
        for child in children {
            child.level = here.level + 1;
        }
        visit :0: children;
    }
}

with entry {
    # Create family tree
    grandpa = root ++> Person(name="Grandpa");
    dad = root ++> Person(name="Dad");
    mom = root ++> Person(name="Mom");
    child1 = root ++> Person(name="Alice");
    child2 = root ++> Person(name="Bob");
    grandchild = root ++> Person(name="Charlie");

    # Create relationships
    grandpa +>:ParentOf:+> dad;
    grandpa +>:ParentOf:+> mom;
    dad +>:ParentOf:+> child1;
    mom +>:ParentOf:+> child2;
    child1 +>:ParentOf:+> grandchild;

    print("=== Breadth-First Search ===");
    grandpa[0] spawn BFSWalker();

    # Reset levels
    all_people = [root-->(`?Person)];
    for person in all_people {
        person.level = 0;
    }

    print("\n=== Depth-First Search ===");
    grandpa[0] spawn DFSWalker();
}
```
```jac
node Person {
    has name: str;
    has priority: int;
}

edge ConnectedTo {
    has strength: int;
}

walker PriorityWalker {
    can visit_by_priority with Person entry {
        print(f"Visiting: {here.name} (priority: {here.priority})");

        # Get all connections
        connections = [->:ConnectedTo:->(`?Person)];

        if connections {
            print(f"  Found {len(connections)} connections");
            for conn in connections {
                print(f"    {conn.name} (priority: {conn.priority})");
            }

            # Visit highest priority first using :0:
            visit :0: connections;
        }
    }
}

with entry {
    # Create network with different priorities
    center = root ++> Person(name="Center", priority=5);
    high_priority = root ++> Person(name="VIP", priority=10);
    medium_priority = root ++> Person(name="Regular", priority=5);
    low_priority = root ++> Person(name="Basic", priority=1);

    # Create connections
    center +>:ConnectedTo(strength=8):+> high_priority;
    center +>:ConnectedTo(strength=5):+> medium_priority;
    center +>:ConnectedTo(strength=3):+> low_priority;

    print("=== Priority-Based Traversal ===");
    center[0] spawn PriorityWalker();
}
```


## From: chapter_8.md

In Object-Oriented Programming, your objects are stationary. You call a method on an object, and the logic executes within that object's context.

Walkers are more than simple graph crawlers. Because they are a subtype of the `object` archetype, they can,

- Maintain State: A walker can have its own attributes (has fields) to store information it collects during its journey.
- Execute Logic: A walker has methods (can abilities) that are automatically triggered when it "lands on" a specific type of node or edge.
- Make Decisions: Based on the data it finds at its current location, a walker can decide where to go next.


## From: chapter_20.md

## Step 1: Converting Classes to Objects

The first migration step involves converting Python classes to Jac objects while maintaining similar functionality.

### Basic Class to Object Migration

!!! example "Class to Object Conversion"
    === "Python Class"
        ```python
        # book.py - Python class
        class Book:
            def __init__(self, title: str, author: str, isbn: str):
                self.title = title
                self.author = author
                self.isbn = isbn
                self.is_borrowed = False

            def get_info(self) -> str:
                status = "Available" if not self.is_borrowed else "Borrowed"
                return f"{self.title} by {self.author} - {status}"

            def borrow(self) -> bool:
                if not self.is_borrowed:
                    self.is_borrowed = True
                    return True
                return False
        ```

    === "Jac Object"
        ```jac
        # book.jac - Jac object
        obj Book {
            has title: str;
            has author: str;
            has isbn: str;
            has is_borrowed: bool = False;

            def get_info() -> str {
                status = "Available" if not self.is_borrowed else "Borrowed";
                return f"{self.title} by {self.author} - {status}";
            }

            def borrow() -> bool {
                if not self.is_borrowed {
                    self.is_borrowed = True;
                    return True;
                }
                return False;
            }
        }
        ```

!!! tip "Key Migration Changes"
    - `class` → `obj`
    - `__init__` → automatic constructor with `has`
    - `:` → `;` for statement termination
    - `{}` for code blocks instead of indentation

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

### Pitfall 1: Direct Syntax Translation

!!! warning "Avoid Direct Translation"
    Don't directly translate Python syntax without considering Jac's spatial capabilities.

!!! example "Poor vs Good Migration"
    === "Poor Migration (Direct Translation)"
        ```jac
        # poor_migration.jac - Direct syntax translation
        obj LibraryManager {
            has books: list[dict] = [];  # Still thinking in lists
            has members: list[dict] = [];

            def add_book(book_data: dict) -> None {
                self.books.append(book_data);  # Missing spatial benefits
            }

            def find_book(isbn: str) -> dict | None {
                for book in self.books {  # Manual iteration
                    if book["isbn"] == isbn {
                        return book;
                    }
                }
                return None;
            }
        }
        ```

    === "Good Migration (Spatial Thinking)"
        ```jac
        # good_migration.jac - Embracing spatial programming
        node Book {
            has title: str;
            has author: str;
            has isbn: str;
        }

        node Library {
            has name: str;

            def add_book(title: str, author: str, isbn: str) -> Book {
                new_book = Book(title=title, author=author, isbn=isbn);
                self ++> new_book;  # Spatial relationship
                return new_book;
            }

            def find_book(isbn: str) -> Book | None {
                # Spatial filtering - much cleaner
                found_books = [self --> Book](?isbn == isbn);
                return found_books[0] if found_books else None;
            }
        }
        ```
        </div>

!!! summary "What We've Learned"
    **Migration Strategies:**

    - **Incremental approach**: Gradual migration reduces risk and allows learning
    - **Syntax translation**: Converting Python classes to Jac objects with automatic constructors
    - **Spatial transformation**: Moving from collections to graph-based relationships
    - **Hybrid integration**: Running Python and Jac code together during transition

    **Technical Benefits:**

    - **Automatic constructors**: Eliminate boilerplate code with `has` declarations
    - **Type safety**: Mandatory typing catches errors earlier in development
    - **Graph relationships**: Natural representation of connected data
    - **Performance gains**: Optimized execution for both local and distributed environments

!!! tip "Try It Yourself"
    Practice migration by:
    - Converting a simple Python class to a Jac object
    - Transforming list-based relationships into graph structures
    - Creating hybrid applications that use both Python libraries and Jac features
    - Building comprehensive test suites to validate migration correctness

    Remember: Successful migration is about embracing spatial thinking, not just syntax conversion!


## From: jac-cloud.md

- **Async Walker Support**: Introduced comprehensive async walker functionality that brings Python's async/await paradigm to object-spatial programming. Async walkers enable non-blocking spawns during graph traversal, allowing for concurrent execution of multiple walkers and efficient handling of I/O-bound operations.


## From: chapter_5.md

```jac
# image_captioner.jac
import from byllm.lib { Model, Image }

glob vision_llm = Model(model_name="gpt-4o-mini");

obj ImageCaptioner {
    has name: str;

    """Generate a brief, descriptive caption for the image."""
    def generate_caption(image: Image) -> str by vision_llm();

    """Extract specific objects visible in the image."""
    def identify_objects(image: Image) -> list[str] by vision_llm();

    """Determine the mood or atmosphere of the image."""
    def analyze_mood(image: Image) -> str by vision_llm();
}

with entry {
    captioner = ImageCaptioner(name="AI Photo Assistant");
    image = Image("photo.jpg");

    # Generate basic caption
    caption = captioner.generate_caption(image);
    print(f"Caption: {caption}");

    # Identify objects
    objects = captioner.identify_objects(image);
    print(f"Objects found: {objects}");

    # Analyze mood
    mood = captioner.analyze_mood(image);
    print(f"Mood: {mood}");
}
```

```console
$ jac run image_captioner.jac

Caption: A stylish French Bulldog poses confidently in a black and yellow "WOOF" sweatshirt,
accessorized with a chunky gold chain against a vibrant yellow backdrop.

Objects found: ['dog', 'sweater', 'chain', 'yellow background']

Mood: The mood of the image is playful and cheerful. The bright yellow background and
the stylish outfit of the dog contribute to a fun and lighthearted atmosphere.
```

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


## From: chapter_15.md

```jac
        node ChatRoom {
            has name: str;
            has users: list[str] = [];
            has messages: list[dict] = [];
            has created_at: str;

            can add_user(username: str) -> bool {
                if len(self.users) >= chat_config["max_users"] {
                    return False;
                }
                if username not in self.users {
                    self.users.append(username);
                }
                return True;
            }
        }
```

```jac
        node ChatRoom {
            has name: str;
            has users: list[str] = [];
            has message_count: int = 0;
        }
```

```jac
        node ChatMessage {
            has content: str;
            has sender: str;
            has timestamp: str;
            has room_name: str;
            has id: str = "msg_" + str(uuid4());
        }

        node ChatRoom {
            has name: str;
            has users: list[str] = [];
            has message_count: int = 0;

            def add_message(sender: str, content: str) -> ChatMessage {
                new_message = ChatMessage(
                    content=content,
                    sender=sender,
                    timestamp=datetime.now().isoformat(),
                    room_name=self.name
                );
                self ++> new_message;
                self.message_count += 1;
                return new_message;
            }

            def get_recent_messages(limit: int = 20) -> list[dict] {
                messages = [self --> (`?ChatMessage)];
                recent = messages[-limit:] if len(messages) > limit else messages;
                return [
                    {
                        "content": msg.content,
                        "sender": msg.sender,
                        "timestamp": msg.timestamp
                    }
                    for msg in recent
                ];

            }
        }
```

```jac
    node WebhookLog {
        has source: str;
        has event_type: str;
        has data: dict;
        has received_at: str;
    }
```

```jac
    node LogEntry {
        has level: str;
        has message: str;
        has timestamp: str;
        has context: dict = {};
    }
```


## From: chapter_13.md

```jac
walker get_counter {
    obj __specs__ {
        static has auth: bool = False;
    }

    can get_counter_endpoint with `root entry {
        counter_nodes = [root --> Counter];


        if not counter_nodes {
            counter = Counter();
            root ++> counter;
        } else {
            counter = counter_nodes[0];
        }

        report {"value": counter.get_value()};
    }
}
```

```jac
walker increment_counter {
    obj __specs__ {
        static has auth: bool = False;
    }

    can increment_counter_endpoint with `root entry {
        counter_nodes = [root --> Counter];
        if not counter_nodes {
            counter = Counter();
            root ++> counter;
        } else {
            counter = counter_nodes[0];
        }
        new_value = counter.increment();
        report {"value": new_value};
    }
}
```

```jac
walker get_counter_with_history {
    obj __specs__ {
        static has auth: bool = False;
    }

    can get_counter_with_history_endpoint with `root entry {
        counter_nodes = [root --> Counter];
        if not counter_nodes {
            counter = Counter(created_at=str(datetime.now()));
            root ++> counter;
            report {
                "value": 0,
                "status": "created",
                "history": []
            };
        } else {
            counter = counter_nodes[0];
            report {
                "value": counter.value,
                "status": "existing",
                "history": counter.get_history()
            };
        }
    }
}
```

```jac
walker increment_with_history {
    obj __specs__ {
        static has auth: bool = False;
    }

    can increment_with_history_endpoint with `root entry {
        counter_nodes = [root --> Counter];
        if not counter_nodes {
            counter = Counter(created_at=str(datetime.now()));
            root ++> counter;
        } else {
            counter = counter_nodes[0];
        }

        new_value = counter.increment();
        report {
            "value": new_value,
            "history": counter.get_history()
        };
    }
}
```

```jac
walker create_counter {
    has name: str;

    obj __specs__ {
        static has auth: bool = False;
    }

    can create_counter_endpoint with `root entry {
        manager_nodes = [root --> CounterManager];
        if not manager_nodes {
            manager = CounterManager(created_at=str(datetime.now()));
            root ++> manager;
        } else {
            manager = manager_nodes[0];
        }

        result = manager.create_counter(self.name);
        report result;
    }
}
```

```jac
walker increment_named_counter {
    has name: str;
    has amount: int = 1;

    obj __specs__ {
        static has auth: bool = False;
    }

    can increment_named_counter_endpoint with `root entry {
        manager_nodes = [root --> CounterManager];
        if not manager_nodes {
            report {"error": "No counter manager found"};
            return;
        }

        manager = manager_nodes[0];
        counters = [manager --> Counter](?name == self.name);

        if not counters {
            report {"error": f"Counter {self.name} not found"};
            return;
        }

        counter = counters[0];
        new_value = counter.increment(self.amount);
        report {"name": self.name, "value": new_value};
    }
}
```

```jac
walker get_all_counters {
    obj __specs__ {
        static has auth: bool = False;
    }

    can get_all_counters_endpoint with `root entry {
        manager_nodes = [root --> CounterManager];
        if not manager_nodes {
            report {"counters": [], "total": 0};
            return;
        }

        manager = manager_nodes[0];
        report {
            "counters": manager.list_counters(),
            "total": manager.get_total()
        };
    }
}
```


## From: breaking_changes.md

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

#### 4. `visitor` keyword introduced

Instead of using `here` keyword to represent the other object context while `self` is the self referencial context. Now `here` can only be used in walker abilities to reference a node or edge, and `visitor` must be used in nodes/edges to reference the walker context.

**Before (v0.7.x and earlier):**
```jac
node Person {
    has name;

    can greet {
        self.name = self.name.upper();
        return "Hello, I am " + self.name;
    }

    can update_walker_info {
        here.age = 25;  # 'here' refers to the walker
    }
}

walker PersonVisitor {
    has age;

    can visit: Person {
        here.name = "Visitor";  # 'here' refers to the current node
        report here.greet();
    }
}
```

**After (v0.8.0+):**
```jac
node Person {
    has name;

    can greet {
        self.name = self.name.upper();
        return "Hello, I am " + self.name;
    }

    can update_walker_info {
        visitor.age = 25;  # 'visitor' refers to the walker
    }
}

walker PersonVisitor {
    has age;

    can visit: Person {
        here.name = "Visitor";  # 'here' still refers to the current node in walker context
        report here.greet();
    }
}
```

This change makes the code more intuitive by clearly distinguishing between:
- `self`: The current object (node or edge) referring to itself
- `visitor`: The walker interacting with a node/edge
- `here`: Used only in walker abilities to reference the current node/edge being visited


## From: multimodality.md

```jac
obj Person {
    has full_name: str,
        yod: int,
        personality: Personality;
}
```


## From: chapter_14.md

```jac
        node Note {
            has title: str;
            has content: str;
            has owner: str;
            has shared_with: list[str] = [];
            has created_at: str = "2024-01-15";
        }
```
```jac
        node Note {
            has title: str;
            has content: str;
            has owner: str;
            has is_private: bool = True;
            has id: str = "note_" + str(uuid.uuid4());
        }
```
```jac
        node Note {
            has title: str;
            has content: str;
            has owner: str;
            has shared_with: list[str] = [];
            has is_public: bool = False;
            has permissions: dict = {"read": True, "write": False};
            has id: str = "note_" + str(uuid.uuid4());
        }
```
```jac
    enum Role {
        VIEWER = "viewer",
        EDITOR = "editor",
        ADMIN = "admin"
    }

    node UserProfile {
        has email: str;
        has role: Role = Role.VIEWER;
        has created_at: str = "2024-01-15";
    }

    node Note {
        has title: str;
        has content: str;
        has owner: str;
        has required_role: Role = Role.VIEWER;
        has is_sensitive: bool = False;
    }
```
```jac
    enum Role {
        VIEWER = "viewer",
        EDITOR = "editor",
        ADMIN = "admin"
    }

    node UserProfile {
        has email: str;
        has role: Role = Role.VIEWER;
        has created_at: str = "2024-01-15";
    }

    node Note {
        has title: str;
        has content: str;
        has owner: str;
        has required_role: Role = Role.VIEWER;
        has is_sensitive: bool = False;
    }
```


## From: quickstart.md

```jac
walker my_walker {
    has data: str;

    # This is where you configure your endpoint behavior
    obj __specs__ {
        static has methods: list = ["get", "post"];   # Supports both GET and POST
        static has auth: bool = False;                # No authentication required
        static has as_query: list = ["data"];         # "data" will be a query parameter
        static has private: bool = True;              # Skip auto endpoint generation from walker
    }
}
```
```jac
import from datetime {datetime}

# Public endpoint (no authentication)
walker public_info {
    obj __specs__ {
        static has methods: list = ["get"];
        static has auth: bool = False;
    }

    can get_current_time with `root entry{
        report {
            "timestamp": datetime.now().isoformat()
        };
    }
}
```
```jac
# GET endpoint with query parameters
walker search_users {
    has query: str;
    static has users: list = [
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"}
    ];

    obj __specs__ {
        static has methods: list = ["get"];
        static has as_query: list = ["query"];
        static has auth: bool = False;
    }

    can search_by_name with `root entry{
        for user in self.users {
            if user['username'] == self.query {
                report user;
                return;
            }
        }

        report {
            "error": f"User with username {self.query} not found"
        };
    }
}
```
```jac
# upload_file.jac
import from fastapi { UploadFile }

# Single file upload
walker single_file_upload {
    has file: UploadFile;

    obj __specs__ {
        static has methods: list = ["post"];
        static has auth: bool = False;
    }

    can enter with `root entry {
        report {
            "output": f"Received file: {self.file.filename}"
        };
    }
}

```
To save a walker or object to memory (queued for later database commit):

```jac
# Save a walker instance
save(my_walker_instance)

# Save an object instance
save(my_object_instance)
```


## From: jaclang.md

- **JavaScript Export Semantics for Public Declarations**: Declarations explicitly annotated with `:pub` now generate JavaScript `export` statements. This applies to classes (`obj :pub`), functions (`def :pub`), enums (`enum :pub`), and global variables (`glob :pub`), enabling proper ES module exports in generated JavaScript code.
- **OPath Designation for Object Spatial Paths**: Moved Path designation for object spatial paths to OPath to avoid conflicts with Python's standard library `pathlib.Path`. This change ensures better interoperability when using Python's path utilities alongside Jac's object-spatial programming features.
- **Typed Context Blocks (OSP)**: Fully implemented typed context blocks (`-> NodeType { }` and `-> WalkerType { }`) for Object-Spatial Programming, enabling conditional code execution based on runtime types.
- **`impl` Keyword for Implementation**: Introduced the `impl` keyword for a simpler, more explicit way to implement abilities and methods for objects, nodes, edges, and other types, replacing the previous colon-based syntax.
- **Updated Inheritance Syntax**: Changed the syntax for specifying inheritance from colons to parentheses (e.g., `obj Car(Vehicle)`) for better alignment with common object-oriented programming languages.
- **Object-Spatial Arrow Notation Update**: Typed arrow notations `-:MyEdge:->` and `+:MyEdge:+>` are now `->:MyEdge:->` and `+>:MyEdge:+>` respectively, to avoid conflicts with Python-style list slicing.


## From: llmdocs.md

### Mini (Recommended)
- Objects, nodes, edges, walkers


## From: create_own_lm.md

- Create a new class that inherits from `BaseModel` class.

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

- Initialize your model with the required parameters.

```jac
# Initialize as global variable
glob llm = MyLLM(model_name="gpt-4o");
```


## From: with_llm.md

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


## From: Overview.md

## Object Spatial Programming

Your application uses Jac's Object Spatial Programming to create a clean, modular design:

**Nodes** represent different parts of your system (Router, Chat types, Sessions). Each node has specific responsibilities and capabilities.

**Walkers** move through your node network, carrying information and executing logic. They represent the actions your system can perform.

**Implementation Separation**: The `server.jac` file contains the high-level structure and logic, while `server.impl.jac` provides the detailed function implementations. Jac seamlessly imports the implementation file, allowing for clean separation of concerns.

The combination of Object Spatial Programming, Mean Typed Programming, and modular tool architecture gives you a solid base for creating intelligent, scalable applications.


## From: friendzone-lite.md

```jac
obj Response {
    has follow_up_questions: str;    # Next question to ask
    has summary: str;                # Concise memory summary
    has when: str;                   # Date in YYYY-MM-DD format
    has who: List[str];              # Names of people involved
    has what: str;                   # What the memory is about
    has where: List[str];            # Relevant locations
    has terminate_conversation: bool; # Completion flag
    has show_summary: bool;          # Display summary flag
}
```


## From: agentic_ai.md

```jac linenums="1"
obj TaskPartition {
  has task: str;
  has agent_type: RoutingNodes;
}
```


## From: usage.md

### Allowed Arguments for the Model Object.

| Argument | Description |
|---|---|
| `model_name` | (Required) The model name to use (e.g., "gpt-4o", "claude-3-5-sonnet-20240620") |
| `api_key` | (Optional) API key for the model provider |
| `base_url` | (Optional) Base URL for the API endpoint (same as `host`, `api_base`)|
| `proxy_url` | (Optional) Proxy URL, automatically sets `base_url` |
| `verbose` | (Optional) Boolean to enable verbose logging for debugging |
| `method` | (Optional) Specifies the LLM method ('Reason' enables step-by-step reasoning, default is standard generation) |
| `tools` | (Optional) List of tool functions to enable agentic behavior with ReAct tool-calling |
| `hyperparams` | (Optional) Additional model-specific parameters supported by LiteLLM (e.g., `temperature`, `max_tokens`, `top_p`, etc.) |

## Context-Aware byLLM Methods

Methods can be integrated with LLM capabilities to process object state and context:

When integrating LLMs for methods of a class, byLLM automatically adds attributes of the initialized object into the prompt of the LLM, adding extra context to the LLM.

```jac linenums="1"
import from byllm.llm { Model }

glob llm = Model(model_name="gpt-4o");

obj Person {
    has name: str;
    has age: int;

    def introduce() -> str by llm();
    def suggest_hobby() -> str by llm();
}

with entry {
    alice = Person("Alice", 25);
    print(alice.introduce());
    print(alice.suggest_hobby());
}
```

## Adding Explicit Context for Functions, Methods and Objects

Providing appropriate context is essential for optimal LLM performance. byLLM provides multiple methods to add context to functions and objects.

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


## From: task-manager-lite.md

```jac
obj Task {
    has title: str;
    has description: str;
    has due_date: str;
    has priority: str;
    has status: str;
    has assignee: str;
}
```
```jac
obj EmailTemplate {
    has subject: str;
    has greeting: str;
    has body: str;
    has closing: str;
    has tone: str; # formal, casual, urgent
}
```


## From: fantasy_trading_game.md

```jac
obj InventoryItem {
    has name: str;
    has price: float;
}

obj Person {
    has name: str;
    has age: int;
    has hobby: str;
    has description: str;
    has money: float;
    has inventory: list[InventoryItem];
}

obj Chat {
    has person: str;
    has message: str;
}
```

**Structure definitions:**
- **InventoryItem**: Tradeable objects with name and price
- **Person**: Character data including stats, money, and items
- **Chat**: Message history for conversation context


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
Traditional object-oriented programming (OOP) would have similar "classes" to represent this information, however OSP allows for assigning connections between the nodes helps us better understand the relationship between individual nodes. We do this by representing directed edges between a person to an email as a "sender of email" and an email to a person as a "recipient of email"
```
obj Response{
    has option: str;
    has selection: str;
    has explanation: str;
}
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
- `Position` (Lines 1-2) defines a point in 2D space. `Wall` (Lines 6-7) uses two positions (`start_pos` and  `end_pos`) to define a barrier.
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
- `Level` (Lines 9-13) describes rules. `Map` (Lines 16-20) describes actual placement of objects.
```jac
obj LevelManager {
    has current_level: int = 0, current_difficulty: int = 1,
        prev_levels: list[Level] = [], prev_level_maps: list[Map] = [];

    def create_next_level (last_levels: list[Level], difficulty: int, level_width: int, level_height: int)
    -> Level by llm();

    def create_next_map(level: Level) -> Map by llm();
}
```

