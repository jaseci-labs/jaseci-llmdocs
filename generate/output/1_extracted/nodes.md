# nodes


## From: jac_in_a_flash.md

A `walker` visits a chain of `turn` nodes created with `++>` edges.


## From: jac_playground.md

The Graph Visualizer makes Jac's spatial programming concepts tangible, allowing you to see exactly how your objects, walkers, and edges interact during program execution.


## From: debugger.md

Jac’s debugger includes a visual graph tool to show nodes and edges.

Example graph program:
```jac
node Person{
    has age: int;
}

with entry {
    # Create people nodes
    jonah = Person(16);
    sally = Person(17);
    teacher = Person(42);
    jonah_mom = Person(45);

    # Connect Jonah to root
    root ++> jonah;

    # Create Jonah's relationships
    jonah ++> jonah_mom;
    jonah ++> teacher;
    jonah ++> sally;
}
```
As shown in the video, these nodes will show their values and can be dragged around to better visualize the data.


## From: jac-lens.md

Jac Lens is a powerful Progressive Web App (PWA) that provides an intuitive visual interface for exploring and managing your Jac graph data. It allows you to connect to your Jac server, navigate through node relationships, and modify node properties in real-time.

- **Click on nodes** to view their properties
- **Navigate connections** between nodes
- **Zoom and pan** to explore large graphs
- **Search for specific nodes** using the search functionality

Modify node properties directly in the interface:

- **Edit node attributes** in the side panel
- **Save changes** to update your server
- **View node relationships** and connections
- **Delete nodes** when needed

-   __Graph Visualization__

    ---

    *Visual node relationships*

    Interactive graph view with zoom, pan, and node selection

-   __Property Editing__

    ---

    *Modify node attributes*

    In-place editing of node properties and metadata

-   __Search & Filter__

    ---

    *Find nodes quickly*

    Search functionality to locate specific nodes in large graphs


## From: keywords.md

**Core Archetype Keywords**

| Keyword | Description |
| --- | --- |
| [`node`](https://www.jac-lang.org/learn/jac_ref/#archetype-types) |Represents a vertex or location in a graph, capable of storing data.|


## From: library_mode.md

**In Jac:**
```jac
node Person {
    has name: str;
}
```

**In Library Mode:**
```python
from jaclang.lib import Node, Edge


class Person(Node):
    name: str
```

Graph nodes are implemented by inheriting from the `Node` base class, while relationships between nodes inherit from the `Edge` base class. Data fields are defined using standard Python class attributes with type annotations.

| Class | Description | Usage |
|-------|-------------|-------|
| `Node` | Graph node archetype | `class MyNode(Node):` |
| `Root` | Root node type | Entry point for graphs |


## From: jac_import_patterns.md

### Type Handling
- Regular named imports: `ModuleItem.name` is `Name`
- Default imports: `ModuleItem.name` is `Token(KW_DEFAULT)`
- Namespace imports: `ModuleItem.name` is `Token(STAR_MUL)`
- String literal imports: `ModulePath.path` contains a single `String` node

### Validation
- `sym_tab_build_pass.py`: Only alias added to symbol table for default/namespace; skips symbol creation for String paths
- `esast_gen_pass.py`: Generates appropriate `ImportSpecifier`, `ImportDefaultSpecifier`, or `ImportNamespaceSpecifier`
- `parser.py`: Handles both `dotted_name` (list of Names) and `STRING` in import paths
- `unitree.py`: `ModulePath.dot_path_str` extracts string value from String literals


## From: example.md

- node classes (`node`),

Instances of these node and edge classes form a graph structure that expresses semantic relationships between objects.
Every instance of a Jac program invocation has a `root` node reference that is unique to every user and for which any other node or edge objects connected to `root` will persist across code invocations. That's it. Using `root` to access persistent user state and data, Jac deployments can be scaled from local environments infinitely into to the cloud with no code changes.
```jac
node Person {
    has name: str;
}
```
```jac
node Post {
    has content: str;
    has author: str;
}
```


## From: syntax_quick_reference.md

```jac
# nodes are objs with special properties
node Person {
    has name: str;
    has age: int;
}
```
```jac
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
```


## From: dspfoundation.md

2. **Node Classes** ($\tau_{\text{node}}$): These extend object classes and can be connected via edges. Nodes represent discrete locations or entities within a topological graph structure. They encapsulate data, compute, and the potential for connections, serving as anchoring points in the object-spatial topology of the program. In addition to object semantics, nodes bind computation to data locations through *abilities*, allowing execution to be triggered by visitation rather than explicit invocation.

#### Formalization

Let $C$ be the set of all class definitions in the programming model, where:

2. $\tau_{\text{node}} \subseteq \tau_{\text{obj}}$ represents node class types, which extend object classes with connectivity capabilities and data-bound computation. This subset relationship ensures that nodes inherit all capabilities of objects while adding topological semantics and the ability to bind computation to data locations.

Each instance $n$ of a **node class** $\tau_{\text{node}}$ is defined simply as: $n = ()$.
Nodes exist as independent entities in the topological structure, serving as primary data locations. Unlike edges which require references to nodes, nodes can exist without connections to other elements, though they typically participate in the graph structure through edges that reference them.

### Instantiation Rules

To maintain object-spatial graph consistency and support higher-order topological structures, OSP enforces specific instantiation constraints for different archetypes and references:

2. **Node Instantiation**: Nodes are instantiated like standard objects but gain the additional capability to serve as endpoints for edges and hosts for walkers. Their constructors may initialize object-spatial properties and connection capabilities. Nodes effectively become locations where data resides and computation can be triggered, rather than passive data containers.

### Lifecycle Management

OSP extends traditional object lifecycle management with specialized


## From: superset_python.md

=== "graph_tools.jac"
    ```jac
    # graph_tools.jac
    node Task {
        has name: str;
        has priority: int;
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

=== "models.jac"
    ```jac
    """Task node definition."""

    node Task {
        has title: str;
        has done: bool = False;
    }
    ```

=== "task_graph.jac"
    ```jac
    """Jac module with graph and AI features."""

    node Task {
        has title: str;
        has done: bool = False;
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
    ```


## From: chapter_7.md

In the next chapter, we will make the leap from Object-Oriented to Object-Spatial Programming (OSP). We will see how these objects are extended into nodes that can exist in a graph, giving them a spatial context and unlocking a new way to handle complex, interconnected data.


## From: chapter_2.md

A **literal** is a fixed value you write directly in your code, like "Alice" or 95. Jac uses common literals like *string*, *integer*, *float*, and *boolean*. It also introduces a special kind of literal called an **architype** (node, edge, and walker), which was briefly discussed in the prvious chapter.We will explore architypes in more detail later in chapter 9.


## From: chapter_10.md

In the previous chapters, you learned how to build the static structure of your application using nodes and edges.
- An `entry` ability triggers when a walker arrives at a node or edge.
- An `exit` ability triggers when a walker leaves a node or edge.

You can create specialized entry abilities that only trigger for specific node or edge types.

```jac
        # Basic classroom nodes
        node Student {
            has name: str;
            has messages: list[str] = [];
        }

        node Teacher {
            has name: str;
            has subject: str;
        }
```
```jac
        # Basic classroom nodes
        node Student {
            has name: str;
            has messages: list[str] = [];
        }

        node Teacher {
            has name: str;
            has subject: str;
        }
```
```jac
        node Student {
            has name: str;
            has grade_level: int;
            has messages: list[str] = [];
        }
```
```jac
        node Student {
            has name: str;
            has grade_level: int;
        }
```
- **Entry abilities** trigger when a walker arrives at a node
- **Exit abilities** trigger when a walker leaves a node
- **Context awareness**: Abilities have access to current node (`here`) and walker state


## From: chapter_12.md

```jac
        # notebook.jac - No manual API setup needed
        node Note {
            has title: str;
            has content: str;
            has author: str;
            has created_at: str = "2024-01-15";
            has id: str = "note_" + str(uuid.uuid4());
        }
```

```jac
    # validated_notebook.jac
    node Note {
        has title: str;
        has content: str;
        has author: str;
        has priority: int = 1;  # 1-5 priority level
        has tags: list[str] = [];
    }
```

```jac
    # complete_notebook.jac
    node Note {
        has title: str;
        has content: str;
        has author: str;
        has priority: int = 1;
        has created_at: str = "2024-01-15";
        has id: str;
    }
```

```jac
    # shared_notebook.jac
    node Note {
        has title: str;
        has content: str;
        has author: str;
        has shared_with: list[str] = [];
        has is_public: bool = false;
        has id: str;
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
```
```jac
node Person {
    has name: str;
    has age: int;
    has city: str;
}
```
```jac
node Person {
    has name: str;
    has level: int = 0;
}
```
```jac
node Person {
    has name: str;
    has priority: int;
}
```


## From: jac-scale.md

- Intelligent walker scheduling across multiple nodes


## From: chapter_8.md

`with entry` marks your entry point into the program's graph. This graph initially contains only the root node, which serves as the anchor for everything you will build.

Everything you create and connect within this graph space can be persisted, traversed, and reasoned about spatially.

### Creating a Node and adding it to the Graph

When the `with entry` block is executed, it creates a root node in the Jac graph. From there, we can add nodes` and `edges` to build our data structure. Lets look at an example of creating a simple node using Jac's syntax:

```jac
node Node{
    has name: str;
}

with entry {
    node_a = Node(name="A");
}
```

Here, we define a node using the `node` keyword, which is similar to defining a class in traditional OOP. The `has` keyword declares properties for the node, and we create an instance of this node within the `with entry` block.

### Connecting Nodes with Edges

When the entry point is executed, it creates a root node on the Jac graph, which can be accessed using the `root` variable. This root node serves as the starting point for the program's graph structure, enabling traversal and manipulation of connected nodes.

In the example above, we create a new node `node_a` with the name "A". However, this node is not automatically part of the graph—it exists in isolation. To incorporate it into the graph, we need to connect it to an existing node using an `edge`.

This is where the `++>` operator comes in. It creates a directional edge from the root node to `node_a`, effectively linking the two and adding `node_a` into the graph.

```jac
node Node{
    has name: str;
}

with entry {
    node_a = Node(name="A");
    root ++> node_a;  # Add node_a to the root graph
}
```

### Building out the rest of the Graph

Now that we have a basic understanding of nodes and edges, let's add a few more nodes and edges to create a more complex graph structure. We'll introduce a second node and connect it to the first one:

```jac
node Node{
    has name: str;
}

with entry {
    node_a = Node(name="A");
    node_b = Node(name="B");

    root ++> node_a;  # Add node_a to the root graph
    node_a ++> node_b;  # Connect node_a to node_b
}
```

Next let's define a terminal node that will represent the end of our graph traversal. This node will not have any outgoing edges, indicating that it is a leaf node in our graph structure:

```jac
node EndNode {}
glob END = EndNode();  # Create a global end node
```

Now we can connect our nodes to this end node, creating a complete graph structure:
```jac
node Node{
    has name: str;
}
node EndNode {}
glob END = EndNode();

with entry {
    node_a = Node(name="A");
    node_b = Node(name="B");

    root ++> node_a;  # Add node_a to the root graph
    node_a ++> node_b;  # Connect node_a to node_b
    node_b ++> END;  # Connect node_b to the end node
}
```
First, we need to enhance our graph with a starting and ending point.

```jac
node Node {
    has name: str;
}

# A special node to mark the end of a path.
node EndNode {}

# Our full graph structure
with entry {
    # Spawn nodes and attach them to the graph.
    node_a = root ++> Node(name="A");
    node_b = node_a ++> Node(name="B");
    node_c = node_b ++> Node(name="C");
    end_node = node_c ++> EndNode(); # The path ends here.
}
```
```jac
node Node{
    has name: str;
}

node EndNode {}
glob END = EndNode();

walker PathWalker {
    has input: str;

    can start with `root entry {
        visit [-->];
    }

    can visit_node  with Node entry{
        self.input += ", visiting " + here.name;
        visit [here-->];
    }

    can visit_end with EndNode entry {
        self.input += ", reached the end";
        return;
    }
}

with entry {
    root ++> Node(name="A")
         ++> Node(name="B")
         ++> END;

    my_walker = PathWalker(input="Start walking") spawn root;

    print(my_walker.input);
}
```
**Core Concepts:**

- **Nodes**: Stateful entities that hold data and can react to visitors


## From: chapter_20.md

!!! example "Jac Modern Equivalent"
    ```jac
    # library.jac - Modern Jac implementation preview
    import from datetime { datetime }

    node Book {
        has title: str;
        has author: str;
        has isbn: str;
        has is_borrowed: bool = False;
        has borrowed_date: str = "";

        def borrow(member_id: str) -> bool {
            if not self.is_borrowed {
                self.is_borrowed = True;
                self.borrowed_date = datetime.now().isoformat();
                return True;
            }
            return False;
        }

        def return_book() -> bool {
            if self.is_borrowed {
                self.is_borrowed = False;
                self.borrowed_date = "";
                return True;
            }
            return False;
        }
    }

    node Member {
        has name: str;
        has member_id: str;
    }

    edge BorrowedBy {
        has borrowed_date: str;
    }

    node Library {
        has name: str;

        def add_book(book: Book) -> None {
            self ++> book;
        }

        def add_member(member: Member) -> None {
            self ++> member;
        }

        def borrow_book(isbn: str, member_id: str) -> bool {
            book = [self --> Book](?isbn == isbn);
            member = [self --> Member](?member_id == member_id);

            if book and member and book[0].borrow(member_id) {
                member[0] +:BorrowedBy:borrowed_date=datetime.now().isoformat():+> book[0];
                return True;
            }
            return False;
        }
    }
    ```

## Step 2: Introducing Spatial Relationships

The next step leverages Jac's Object-Spatial Programming by converting relationships into nodes and edges.

### From Collections to Graph Structures

!!! example "Spatial Relationship Migration"
    === "Python Relationships"
        ```python
        # library_python.py - List-based relationships
        class Library:
            def __init__(self, name: str):
                self.name = name
                self.books = []  # List of books
                self.members = []  # List of members
                self.borrowed_books = {}  # Dict mapping book_isbn -> member_id

            def add_book(self, book):
                self.books.append(book)

            def add_member(self, member):
                self.members.append(member)

            def find_available_books(self):
                return [book for book in self.books if not book.is_borrowed]

            def find_member_books(self, member_id: str):
                member_isbns = [isbn for isbn, mid in self.borrowed_books.items() if mid == member_id]
                return [book for book in self.books if book.isbn in member_isbns]
        ```

    === "Jac Spatial Relationships"
        ```jac
        # library_spatial.jac - Graph-based relationships
        node Book {
            has title: str;
            has author: str;
            has isbn: str;
        }

        node Member {
            has name: str;
            has member_id: str;
        }

        edge Contains;  # Library contains books/members
        edge BorrowedBy {
            has borrowed_date: str;
        }

        node Library {
            has name: str;

            def add_book(book: Book) -> None {
                self +:Contains:+> book;
            }

            def add_member(member: Member) -> None {
                self +:Contains:+> member;
            }

            def find_available_books() -> list[Book] {
                all_books = [self --Contains--> Book];
                borrowed_books = [self --Contains--> Book --BorrowedBy--> Member];
                # Return books not in borrowed list
                return [book for book in all_books if book not in borrowed_books];
            }

            def find_member_books(member_id: str) -> list[Book] {
                target_member = [self --Contains--> Member](?member_id == member_id);
                if target_member {
                    return [target_member[0] <--BorrowedBy-- Book];
                }
                return [];
            }
        }
        ```

### Python-Jac Integration

!!! example "Hybrid Integration Approach"
    === "Python Wrapper"
        ```python
        # hybrid_library.py - Python wrapper for Jac code
        import subprocess
        import json

        class JacLibraryWrapper:
            def __init__(self, library_name: str):
                self.library_name = library_name
                # Initialize Jac library through subprocess or API

            def call_jac_walker(self, walker_name: str, params: dict):
                """Call Jac walker from Python"""
                # In practice, this would use jac-cloud API or subprocess
                cmd = f"jac run library.jac --walker {walker_name} --ctx '{json.dumps(params)}'"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return json.loads(result.stdout) if result.stdout else None

            def add_book_via_jac(self, title: str, author: str, isbn: str):
                """Add book using Jac walker"""
                params = {"title": title, "author": author, "isbn": isbn}
                return self.call_jac_walker("add_book", params)

            def get_available_books(self):
                """Get available books using Jac walker"""
                return self.call_jac_walker("get_available_books", {})

        # Traditional Python usage
        class PythonBook:
            def __init__(self, title: str, author: str):
                self.title = title
                self.author = author

        # Hybrid usage
        if __name__ == "__main__":
            # Use existing Python classes
            python_book = PythonBook("Old Book", "Old Author")

            # Use new Jac functionality
            jac_library = JacLibraryWrapper("My Library")
            jac_library.add_book_via_jac("New Book", "


## From: chapter_9.md

In Object-Spatial Programming, **nodes** and **edges** are the fundamental building blocks of your application's graph. A node represents an entity or a location for your data, while an edge represents a typed, directional relationship between two nodes.
This chapter will show you how to define these core components and how to give your nodes special abilities, allowing them to interact with the walkers that visit them.

In Jac, nodes are not just passive data containers. They can have their own abilities—methods that are specifically designed to trigger when a certain type of walker arrives.
This two-way dynamic enables powerful, flexible interactions between walkers and the graph they explore.

Next, we will define two different types of nodes, `Weather` and `Time`. Each one will have a special ability that only triggers for a StateAgent.

```jac
node Weather {
    has temp: int = 80;

    # This ability is only triggered when a walker of type 'StateAgent' arrives.
    can get with StateAgent entry {
        # 'visitor' is a special keyword that refers to the walker currently on this node.
        visitor.state["temperature"] = self.temp;
    }
}
```

The `Weather` node knows that when a `StateAgent` visits, it should update the agent's state dictionary by adding a "temperature" key with its own local temp value.


```jac
node Time {
    has hour: int = 12;

    # This node also has a specific ability for the StateAgent.
    can get with StateAgent entry {
        visitor.state["time"] = f"{self.hour}:00 PM";
    }
}
```
Similarly, the `Time` node updates the agent's state with the current hour.

```jac
# node_abilities.jac
walker StateAgent{
    has state: dict = {};

    can start with `root entry {
        visit [-->];
    }
}

node Weather {
    has temp: int = 80;

    can get with StateAgent entry {
        visitor.state["temperature"] = self.temp;
    }
}

node Time {
    has hour: int = 12;

    can get with StateAgent entry {
        visitor.state["time"] = f"{self.hour}:00 PM";
    }
}

with entry {
    root ++> Weather();
    root ++> Time();

    agent = StateAgent() spawn root;
    print(agent.state);
}
```

In Jac, nodes are more than just data—they can encapsulate behavior and interact with walkers. When building modular systems, it’s often useful to group nodes by type or functionality. This is where node inheritance comes in.

Let’s revisit the `Weather` and `Time` nodes from the previous example. While they each provide different types of information, they serve a common purpose: delivering contextual data to an agent. In Jac, we can express this shared role using inheritance, just like in traditional object-oriented programming.

We define a base node archetype called `Service`. This acts as a common interface for all context-providing nodes. Any node that inherits from `Service` is guaranteed to support certain interactions—either by shared methods or simply by tagging it with a common type.

```jac
node Service {}
```

Next, we will redefine `Weather` and `Time` to inherit from `Service`. This tells our system that they are both specific kinds of `Service` nodes.

```jac
# Weather is a type of Service.
node Weather(Service) {
    has temp: int = 80;

    can get with StateAgent entry {
        visitor.state["temperature"] = self.temp;
    }
}

# Time is also a type of Service.
node Time(Service) {
    has hour: int = 12;

    can get with StateAgent entry {
        visitor.state["time"] = f"{self.hour}:00 PM";
    }
}
```
The ```-->(`?NodeType)``` syntax is a powerful feature of Jac that allows you to filter nodes by type. It tells the walker to visit any node that matches the `NodeType` type, regardless of its specific implementation.

#### Step 2 - The NPC Node

Next, we'll define the `NPC` node. Its key feature is an ability that triggers when our StateAgent visits. This ability uses the get_ambient_mood function to determine its own mood based on the information the agent has already collected.


```jac

node NPC {
    can get with StateAgent entry {
        visitor.state["npc_mood"] = get_ambient_mood(visitor.state);
    }
}
```
This is where the NPC’s personality is generated—based entirely on the graph-derived context.

```jac
# Basic node for representing teachers
node Teacher {
    has name: str;
    has subject: str;
    has years_experience: int;
    has email: str;
}

# Basic node for representing students
node Student {
    has name: str;
    has age: int;
    has grade_level: int;
    has student_id: str;
}

node Classroom {
    has room_number: str;
    has capacity: int;
    has has_projector: bool = True;
}

# Edge for student enrollment
edge EnrolledIn {
    has enrollment_date: str;
    has grade: str = "Not Assigned";
    has attendance_rate: float = 100.0;
}

# Edge for teaching assignments
edge Teaches {
    has start_date: str;
    has schedule: str;  # "MWF 9:00-10:00"
    has is_primary: bool = True;
}

# Edge for friendship between students
edge FriendsWith {
    has since: str;
    has closeness: int = 5;  # 1-10 scale
}

with entry {
    # 1. Create the main classroom node and attach it to the root.
    science_lab = root ++> Classroom(
        room_number="Lab-A",
        capacity=24,
        has_projector=True
    );

    # 2. Create a teacher AND the 'Teaches' edge that connects them to the classroom.
    dr_smith = science_lab +>:Teaches(
        start_date="2024-08-01",
        schedule="TR 10:00-11:30"
    ):+> Teacher(
        name="Dr. Smith",
        subject="Chemistry",
        years_experience=12,
        email="smith@school.edu"
    );
}
```
**Spatial objects**: Nodes can be connected and automatically persist when linked to root
**Property storage**: Nodes hold data using `has` declarations with automatic constructors
**Automatic persistence**: Nodes connected to root persist between program runs
**Type safety**: All node properties must have explicit types


## From: jac-cloud.md

- **Support Spawning a Walker with List of Nodes and Edges**: Introduced the ability to spawn a walker on a list of nodes and edges. This feature enables initiating traversal across multiple graph elements simultaneously, providing greater flexibility and efficiency in handling complex graph structures.
- **Support Custom Access Validation**: Introduced the ability to override access validation. `Node`/`Edge` can override `__jac_access__` reserved function (`builtin`) to have a different way of validating access. Either you cross-check it by current attribute, check from db or global vars or by just returning specific access level. [PR#1524](https://github.com/jaseci-labs/jaseci/pull/1524)
- **Permission Update Builtin Methods**: Introduced `grant`, `revoke` builtin methods, `NoPerm`, `ReadPerm`, `ConnectPerm`, `WritePerm` builtin enums, to give the permission to a node or revoke the permission. Developers can use them by calling `grant(node_1, ConnectPerm)` or `revoke(node_1)` method.


## From: chapter_19.md

```jac
# optimized_friends.jac - Efficient graph-native design
node Person {
    has name: str;
    has age: int;
    has friend_count: int = 0;  # Cached for quick access

    def add_friend(friend: Person) -> bool {
        # Check if already connected to avoid duplicates
        existing = [self --> Friend --> Person](?name == friend.name);
        if existing {
            return false;
        }

        # Create bidirectional connection efficiently
        friendship = Friend(since="2024-01-15");
        self ++> friendship ++> friend;

        # Update cached counters
        self.friend_count += 1;
        friend.friend_count += 1;
        return true;
    }
}
```
```jac
node CacheEntry {
    has depth: int;
    has friend_names: list[str];
    has computed_at: str;
}
```
```jac
# memory_optimized.jac
# Use lightweight nodes for large-scale networks
node LightPerson {
    has name: str;
    has age: int;
    # Remove unnecessary cached data to save memory

    def get_friend_count() -> int {
        # Calculate on-demand instead of caching
        return len([self --> (`?Friend) --> (`?LightPerson)]);
    }

    def get_connections_summary() -> dict {
        friends = [self --> (`?Friend) --> (`?LightPerson)];

        return {
            "friend_count": len(friends),
            "avg_age": sum(f.age for f in friends) / len(friends) if friends else 0,
            "friend_names": [f.name for f in friends[:5]]  # Limit for memory
        };
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


## From: webhook.md

- **Direct Root Access**: Webhooks operate at the root level, not tied to any specific user
- **Customizable**: You can specify allowed walkers, nodes, and expiration dates for each API key

| Parameter | Description |
|---|---|
| nodes | A list of specific node names that are permitted to be accessed with this key. If this list is empty, all nodes are allowed. |

```python
{
  "name": "webhook1",
  "walkers": ["webhook"],
  "nodes": ["root"],
  "expiration": {
    "count": 60,
    "interval": "days"
  }
}
```

```python
{
  "id": "672203ee093fd3d208a4b6d4",
  "name": "test",
  "root_id": "6721f000ee301e1d54c3de3d",
  "walkers": ["webhook"],
  "nodes": ["root"],
  "expiration": "2025-12-24T10:01:18.206000",
  "key": "6721f000ee301e1d54c3de3d:1730282478:P4Nrs3DOLIkaw5aYsbIWNzWZZAwEyb20"
}
```
3. **Use Specific Node Restrictions**: When possible, limit which nodes can be accessed.
4. Confirm the walker and node are allowed for the API key


## From: scheduler.md

```jac
node TaskCounter {
    has val: int = 0;
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


## From: permission.md

#### **Anchors** are database-side class representations that contain:

| Name      | Description                                                       |
| --------- | ----------------------------------------------------------------- |
| id        | The database identifier.                                          |
| name      | The name of the associated archetype.                             |
| root      | The owning root anchor.                                           |
| access    | Permissions defining which nodes or roots can access this anchor. |
| archetype | The JSON representation of the actual archetype.                  |

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


## From: quickstart.md

| Endpoint Type | URL Pattern | Description |
|--------------|-------------|-------------|
| **Node Entry** | `/walker/{walker_name}/{node_id}` | Executes on a specific node |
Jac Cloud automatically serializes walker, edge, and node archetypes:

```json
{
    "id": "unique_anchor_reference_id",
    "context": {
        "attribute1": "value1",
        "attribute2": "value2"
    }
}
```


## From: async_walker.md

| `node_id`       | ID of the node where the walker was executed                   |
| `root_id`       | ID of the root node of the user who triggered the walker       |


## From: sequence.md

```jac
node Node {
    has val: str;

    can entry1 with entry {
        print(f"{self.val}-2");
    }

    can entry2 with Walker entry {
        print(f"{self.val}-3");
    }

    can exit1 with Walker exit {
        print(f"{self.val}-4");
    }

    can exit2 with exit {
        print(f"{self.val}-5");
    }
}
```


## From: jaclang.md

- **Support Spawning a Walker with List of Nodes and Edges**: Introduced the ability to spawn a walker on a list of nodes and edges. This feature enables initiating traversal across multiple graph elements simultaneously, providing greater flexibility and efficiency in handling complex graph structures.
- **Edge Ability Execution Semantics**: Enhanced edge traversal behavior with explicit edge references. By default, `[-->]` returns connected nodes, while `[edge -->]` returns edge objects. When walkers visit edges explicitly using `visit [edge -->]`, abilities are executed on both the edge and its connected node. Additionally, spawning a walker on an edge automatically queues both the edge and its target node for processing, ensuring complete traversal of the topological structure.
- **`visitor` Keyword**: Introduced the `visitor` keyword to reference the walker context within nodes/edges, replacing the ambiguous use of `here` in such contexts. `here` is now used only in walker abilities to reference the current node/edge.


## From: cli.md

- `py_uni_nodes` tool lists python ast nodes.
```bash
jac tool py_uni_nodes
```


## From: llmdocs.md

### Mini (Recommended)
- Objects, nodes, edges, walkers


## From: nodes_and_edges.md

Nodes are archetypes forming part of a graph, holding properties. They can be compared to custom classes in object-oriented programming (OOP).

```jac linenums="1"
node node_name{
    has node_property: int;
}
node node_name{
    has node_property: int = 10;
}
```

### Custom Node Types
- You can define custom node types to create specific instances within the graph.
- Each node can have `attributes` (like fields in a class) and `abilities` (similar to methods in OOP).

### Abilities in Nodes
- Callable Abilities: They are similar to standard methods in OOP. Inside any ability, the node can refer to itself using the `self` keyword, much like in OOP.

- Visit-dependent Abilities: These abilities are only triggered when a specific type of "walker" (discussed later) interacts with the node. This ensures that certain actions are performed only in response to a walker's visit. In these abilities, a special keyword `here` is used to reference the visiting walker. This allows you to access the walker's attributes and abilities directly during its interaction with the node.

- This is an example of defining a node.
```jac linenums="1"
node test_node {
    has value: int;

    can log_entry with entry {
        print(f">>> Some Walker entered the node: ", self);
    }
    can log_test_walker_entry with test_walker entry {
        print(f">>> {here} entered the node {self}");
        here.callable();
    }
    can log_test_walker_exit with test_walker exit {
        print(f"<<< {here} exited the node {self}");
    }
    can log_exit with exit {
        print(f"<<< Some Walker exited the node {self}");
    }
    def callable {
        print(f"===== Callable on {self}");
    }
}
```

### Connecting Nodes
Nodes in JacLang can establish connections in various ways, offering flexibility for building complex graphs:

- One-to-One: A single node connects to another single node.
- One-to-Many: A single node connects to multiple nodes.
- Many-to-One: Multiple nodes connect to a single node.
- Many-to-Many: A group of nodes connects to another group of nodes.

This versatility allows for creating intricate and highly interconnected graph structures, tailored to the specific needs of your application.
```jac linenums="1"
node MyNode{}

with entry{
first_node = MyNode();
second_node = MyNode();

root ++> first_node;
first_node ++> second_node;

}
```
```jac linenums="1"
node MyNode{}

with entry{
first_node = MyNode();
second_tier = [MyNode() for i in range(2)];

root ++> first_node;
first_node ++> second_tier; # one to many

}
```
```jac linenums="1"
node MyNode{}

with entry{
first_tier = [MyNode() for i in range(2)];
second_node = MyNode();
root ++> first_tier;
first_tier ++> second_node; # many to one

}
```
```jac linenums="1"
node MyNode{}

with entry{
    first_tier =[MyNode() for i in range(2)];
    second_tier =[MyNode() for i in range(2)];

    root ++> first_tier;
    first_tier ++> second_tier;

    end_tier = MyNode();
    second_tier ++> end_tier;
}
```


## From: filtering.md

# Node and Edge Filtering

JacLang provides flexible filtering mechanisms to control graph traversal and operations, allowing precise selection of nodes and edges based on specific criteria. These filters enable developers to optimize traversal and focus only on relevant parts of the graph.

## Node-Based Filtering

Node-based filtering restricts traversal to specific nodes that satisfy predefined conditions. This is useful when you need to:

- Limit traversal to nodes with certain attributes or properties.
- Filter nodes dynamically based on walker state or external context.

### Example:

We can filter specific types of nodes from a list of visitable nodes based on their type, and further apply conditions on node attributes to refine the results.
=== "Jac"
    <div class="code-block">
    ```jac
    --8<-- "jac/examples/data_spatial/filtering.jac"
    ```
    </div>
??? example "Graph"
    ```mermaid
    flowchart LR
    0 -->|"a()"| 1
    1 -->|"b()"| 2
    2 -->|"c()"| 3
    2 -->|"c()"| 4
    5 -->|"a()"| 4
    1 -->|"b()"| 5
    0["Root()"]
    1["A(val=5)"]
    2["B(val=10)"]
    3["C(val=15)"]
    4["C(val=25)"]
    5["A(val=20)"]
    ```

### Example:
We can filter nodes based on specific edge attributes, such as filtering by edge values to retrieve a subset of connected nodes.
=== "Jac"
    <div class="code-block">
    ```jac
    --8<-- "jac/examples/data_spatial/edge_filtering.jac"
    ```
    </div>

??? example "Graph"
    ```mermaid
    flowchart LR
    0 -->|"a(val=10)"| 1
    0 -->|"a(val=20)"| 2
    0 -->|"b(val=30)"| 3
    0["Root()"]
    1["A(val=10)"]
    2["A(val=20)"]
    3["A(val=30)"]
    ```


## From: walkers.md

Walkers are "worker bots" that move (walk) along the graph while performing tasks on the nodes they visit.

They play a crucial role in executing visit-dependent abilities as discussed in nodes and facilitating interactions between graph nodes and themselves.

- Similar to nodes, walkers can have their own attributes and abilities including both callable and visit-dependent abilities.

- **Visit-dependent Abilities:**
    - Ensures the ability is executed only when the walker visits a node.
    - Can be defined within:
        - **Nodes:** Triggered upon a walker's arrival.
        - **Walkers:** Specific to the walker’s operation during its visit.
- ```here```: References the current node visited by the walker, enabling access to its attributes and callable abilities.
    This allows seamless interaction between walker and node attributes.

- Walkers prioritize their visit-dependent abilities first before executing the abilities of the visited node.
- This enables flexible task delegation:
    - Define visit-dependent tasks either within the walker or in the node.


## From: FAQ.md

- Nodes are archetypes forming part of a graph, holding properties. You can define nodes with attributes and values:
```jac
  node node_name{
      has node_property: int;
  }
  node node_name{
      has node_property: int = 10;
  }
```
- You can delete a node using:
```jac
    del node_name;
```
- You can filter nodes by their type or properties when traversing the graph using filters like `(?Type)` or attribute conditions.
```jac
print([root --> -:edge_type:-> (`?NodeType)]);
print([root --> -:edge_type:-> (`?NodeType)](?attribute > value));
```
```jac
node a{
    has val:int;
}
with entry{
    end=root;
    for i in range(0,4){
        end++>(end:=[a(val=i) for i in range(0,3)]);
    }
    print(printgraph());  # Generates a DOT graph starting from the root node
}
```
```jac
node a{
    has val:int;
}
with entry{
    x=[a(val=i) for i in range(0,3)];
    end=x[1];
    for i in range(0,8){
        locals()[chr(ord('b') + i)] = (values:=[a(val=j*i+5.2*i+6) for j in range(0,3)]);
        end ++> (end:=values);
    }
}
```


## From: Overview.md

## Object Spatial Programming

Your application uses Jac's Object Spatial Programming to create a clean, modular design:

**Nodes** represent different parts of your system (Router, Chat types, Sessions). Each node has specific responsibilities and capabilities.

The combination of Object Spatial Programming, Mean Typed Programming, and modular tool architecture gives you a solid base for creating intelligent, scalable applications.


## From: friendzone-lite.md

- **Session Node**: Maintains persistent memory state across interactions


## From: utilities.md

| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `source`     | `string`  | The **JID** of the starting root, node, or edge for the traversal.                                                                                                                       | Current user's root |
| `node_types` | `string`  | Can be declared multiple times to filter the traversal results by node type. For example, `node_types=Node1&node_types=Node2` will include only nodes that are `Node1` or `Node2` types. | All node types      |
```json
{
  "nodes": [
    {
      "id": "n::68875f383d1e672f517094ff",
      "edges": ["e::68875f483d1e672f517096a5"]
    },
    {
      "id": "n:A:68875f483d1e672f517096a0",
      "edges": ["e::68875f483d1e672f517096a2", "e::68875f483d1e672f517096a5"]
    },
    {
      "id": "n:B:68875f483d1e672f517096a1",
      "edges": ["e::68875f483d1e672f517096a2", "e::68875f483d1e672f517096a4"]
    },
    {
      "id": "n:C:68875f483d1e672f517096a3",
      "edges": ["e::68875f483d1e672f517096a4"]
    }
  ]
}
```
The order of `nodes` and `edges` within each step may vary depending on the traversal logic.

```json
{"nodes": [], "edges": [{"id": "e::step1_edge1", "source": "n::start_node", "target": "n::next_node_A"}]}
{"nodes": [{"id": "n::next_node_A", "edges": ["e::step1_edge1"]}], "edges": []}
{"nodes": [], "edges": [{"id": "e::step2_edge1", "source": "n::next_node_A", "target": "n::final_node_B"}]}
{"nodes": [{"id": "n::final_node_B", "edges": ["e::step2_edge1"]}], "edges": []}
```
| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `source`     | `string`  | The **JID** of the starting root, node, or edge for the traversal.                                                                                                                       | Current user's root |
| `node_types` | `string`  | Can be declared multiple times to filter the traversal results by node type. For example, `node_types=Node1&node_types=Node2` will include only nodes that are `Node1` or `Node2` types. | All node types      |


## From: agentic_ai.md

**Nodes**: Represent locations where compute and logic execute. Nodes have attributes (data) and special abilities that trigger on preset events rather than being directly called. In an agentic system, nodes are agents that maintain local state and respond to visitor events.

**Task Node** (`node Task`)

A simple data structure for storing individual tasks. New `Task` nodes are created when `TaskHandling.add_task()` is called and linked back to the handler via `self ++> task_created;`, allowing the handler to maintain local knowledge of scheduled tasks.

This demonstrates a key OSP pattern: **parent-child relationships through edges**. The TaskHandling node "owns" Task nodes it creates, maintaining a persistent record in the graph structure.

```jac linenums="1"
node Task {
  has task:str = "";
  has date:str = "";
  has time:str = "";
}
```

**TaskHandling Node** (`node TaskHandling`)

This is the first agent in our system. It demonstrates how to build a **specialized agent with tools and LLM reasoning**.

The node exposes the following tools (member methods) that the LLM can invoke:

- `get_current_time()` — Returns a formatted timestamp (utility function for planning)
- `add_task(task, date, time)` — Creates a Task node and links it to the handler (state modification)
- `summarize_tasks()` — Queries linked task nodes and returns a summary (knowledge retrieval)

The key LLM-powered method:

- `route_and_run(utterance)` — Uses `by llm(method="ReAct", tools=(...))` to enable the LLM to reason and plan. Given a user utterance, the LLM can chain tool calls to accomplish the goal (e.g., get current time → add task → summarize tasks).

The agent's entry point is the `can execute with task_manager entry` ability. This = ability triggers **automatically** when the `task_manager` walker visits this node, making it easy to define agent behavior without explicit callbacks.

```jac linenums="1"
node TaskHandling {
  def get_current_time() -> str {
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime());
  }

  def add_task(task: str, date: str, time: str) -> str {
    task_created = Task(task=task, date=date, time=time);
    self ++> task_created;
    return "Task added successfully";
  }

  def summarize_tasks -> str {
    scheduled_tasks = [self-->(`?Task)];
    return str(scheduled_tasks);
  }

  def route_and_run(utterance: str) -> str by llm(
    method="ReAct",
    tools=([self.add_task, self.get_current_time, self.summarize_tasks])
  );

  can execute with task_manager entry {
    print("[TaskHandling Node Activated]");
    response = self.route_and_run(visitor.cur_task.task);
    print("→", response);
    report {
      "utterance": visitor.cur_task.task,
      "response": response,
      "node_type": self.__class__.__name__
    };
  }
}
```

**EmailHandling Node** (`node EmailHandling`)

Similar to TaskHandling, this agent specializes in email operations. It exposes an `write_email_content()` tool and uses `route_and_run()` to orchestrate email composition via the LLM. The pattern is identical: methods as tools, LLM reasoning, and an entry ability that runs when visited by the orchestrator.

```jac linenums="1"
node EmailHandling {
  def write_email_content(utterance: str) -> str by llm();
  def route_and_run(utterance: str) -> str by llm(
    method="ReAct",
    tools=([self.write_email_content])
  );
  can execute with task_manager entry {
    print("[EmailHandling Node Activated]");
    response = self.route_and_run(visitor.cur_task.task);
    print("→", response);
    report {
      "utterance": visitor.cur_task.task,
      "response": response,
      "node_type": self.__class__.__name__
    };
  }
}
```

**GeneralChat Node** (`node GeneralChat`)

This agent handles general conversational tasks. It provides a simpler interface with just a `chat()` method, demonstrating that not all agents need complex tool sets. The byLLM `by llm()` annotation enables the LLM to directly power the conversation.

```jac linenums="1"
node GeneralChat {
  def chat(utterance: str) -> str by llm();
  can execute with task_manager entry {
    print("[GeneralChat Node Activated]");
    response = self.chat(visitor.cur_task.task);
    print("→", response);
    report {
      "utterance": visitor.cur_task.task,
      "response": response,
      "node_type": self.__class__.__name__
    };
  }
}
```


## From: tutorial.md

### 1. Nodes: Store Your Data

**Nodes** hold information. In LittleX:

- **Profile nodes** store user information
- **Tweet nodes** store message content
- **Comment nodes** store replies

**Simple Example:**
```jac
node User {
    has username: str;
}
```

This creates a user object with a username.
### Profile Node
```jac
node Profile {
    has username: str = "";

    can update with update_profile entry;
    can get with get_profile entry;
    can follow with follow_request entry;
    can un_follow with un_follow_request entry;
}
```

This stores user information and defines what users can do.

### Tweet Node
```jac
node Tweet {
    has content: str;
    has embedding: list;
    has created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");

    can update with update_tweet exit;
    can delete with remove_tweet exit;
    can like_tweet with like_tweet entry;
    can remove_like with remove_like entry;
    can comment with comment_tweet entry;

    def get_info() -> TweetInfo;
    can get with load_feed entry;
}
```

This stores tweet content and handles all tweet interactions.
- **Nodes** for storing data


## From: task-manager-lite.md

### Nodes
- **TaskHandling**: Manages task creation, scheduling, and summarization
- **EmailHandling**: Handles email content generation
- **GeneralChat**: Provides general AI conversation capabilities


## From: tutorial.md

We can represent both emails and people as nodes on a graph. Each node can contain information relevant to itself as shown below:

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
EmailBuddy handles email uploads by allowing users to upload a json file in the following format:

```json
[
  {
    "date": "2025-10-09T06:20:18+00:00",
    "from": "Lily Carter <lcarter@protonmail.com>",
    "to": "Evan Brooks <evan.brooks@gmail.com>",
    "subject": "Hows it going",
    "body": "Hey Evan! We haven't spoken in a while, let's catch up soon."
  }
]
```

These json files are parsed in Jac and are used to create our nodes. We handle node creation by treating our 2 node types (Person & Email) as 3 (Sender, Recipients, & Email).


For each email uploaded, EmailBuddy:

- Extract sender and recipient addresses
- Create Person nodes if they do not already exist
- Create or skip Email node based on UUID matching
- Connect all Person and Email nodes to the root
- Create directed edges: person → email, and email → recipients


We must connect ALL nodes (Email and Person) to the root node so we can access them later.

The root node in Jac acts as a fundamental global pointer on the graph. It is a special node that is always accessible in every request context, especially when running Jac in server mode (jac serve). Think of the root node as the front door or lobby of your email graph. When a 'walker' (our search agent) arrives, it always starts at the root. By connecting every new Person and Email to this root, we ensure the walker can find them, like adding a new room's key to the lobby's key rack.

This design ensures that no nodes get "lost" since all nodes are directly or indirectly connected to the root node, making them accessible to the program. This persistent organization facilitates data traversal and manipulation across the graph.

This is particularly useful for us since every node is connected to root, we can always find any email, even if we don't know who sent it or who received it.

Now that we have all the nodes created (and connected to root) our graph will likely look something like this:

The issue with this graph is that we don't have any connections between People and Emails

This can be accomplished by something like the following

```Jac
recipientNodes: list[People];
senderNode: People;
emailNode: Email;

senderNode ++> emailNode;
for node in recipientNodes{
    emailNode ++> node;
}
```
- `can <attributeName> with <nodeType> entry`: Assigns walker behavior when it is on the node type (root must have `` `root ``)
- `visit [-->]`: Tells the walker to explore all nodes reachable from this one along outgoing edges.
This walkers goal is to find a specific Person node and return the value. The walker will search through ALL people nodes connected to root until it finds its target or runs out of People to search. If the walker does not find a matching Person node, self.person stays None.
When the FindSenderNode walker is initialized, the walker is passed a target email address as a member variable to find a Person node attached to it.
```Jac
FindSend = FindSenderNode(target=sender_email);
```
Once the walker is initialized, it behaves just like any other object in OOP: it has member variables and functions you can access. It doesn't actually do anything until we spawn it. Spawning a walker means placing it on a starting node in the graph and letting it run until it reaches its stopping condition. While the walker is active, it can move between nodes and perform actions, such as creating new nodes or modifying existing ones.


We can spawn the walker on root by doing the following command.

```Jac
root spawn FindSend;
```
Once the walker terminates, we can extract the node as follows.

```Jac
sender: Person = FindSend.person;
```
If no matching Person is found, the walker finishes naturally and FindSend.person will still be None.
EmailBuddy has two other helper walkers (FindEmailNode and FindRecipientNodes) that follow a very similar pattern, however the main traversal/query walker (ask_email) works differently. To learn more read about this last walker continue reading about [AI Agents](#ai-agents).

Common OSP pitfalls

| Mistake                                 | Symptom                             | Fix                                    |
| --------------------------------------- | ----------------------------------- | -------------------------------------- |
| Forgot to connect nodes to root         | Walker can't find anything          | `root ++> newNode`                     |
| Email duplicate created twice           | Graph has repeated email nodes      | Check UUID before creation             |
| Walker never stops                      | Infinite graph crawl                | Use `disengage` when end condition met |
| Walker doesn't do anything after spawn  | Attribute undefined for node type   | `can <attrName> with <nodeType> entry` |


## From: jac_serve.md

3. Creates a user management system where each user has their own persistent root node

**Response:**
```json
{
  "username": "alice",
  "token": "abc123...",
  "root_id": "uuid-of-root-node"
}
```

**Response:**
```json
{
  "username": "alice",
  "token": "abc123...",
  "root_id": "uuid-of-root-node"
}
```

- Each user has their own **persistent root node** stored in the session file
- All nodes created by a user are attached to their root and persist across API calls
- Different users have isolated graph spaces - they cannot access each other's nodes

- Each request executes in the context of the authenticated user's root node

- The `target_node` field for walkers is optional and defaults to the user's root node
- If `target_node` is specified, it should be a valid node ID (hex string)

