# collections


## From: syntax_quick_reference.md

```jac
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
```


## From: beginners_guide_to_jac.md

### 7.1 Lists - Ordered Collections

Lists hold multiple values in order:

```jac
with entry {
    # Create a list
    fruits = ["apple", "banana", "cherry"];

    print(fruits);  # ['apple', 'banana', 'cherry']
}
```

### 7.2 Accessing List Items

Each item has an index (position), starting at 0:

```jac
with entry {
    fruits = ["apple", "banana", "cherry", "date"];

    print(fruits[0]);   # apple (first item)
    print(fruits[1]);   # banana (second item)
    print(fruits[3]);   # date (fourth item)

    # Negative indices count from the end
    print(fruits[-1]);  # date (last item)
    print(fruits[-2]);  # cherry (second to last)
}
```

### 7.3 Modifying Lists

```jac
with entry {
    numbers = [1, 2, 3];

    # Change an item
    numbers[1] = 99;
    print(numbers);  # [1, 99, 3]

    # Add to end
    numbers.append(4);
    print(numbers);  # [1, 99, 3, 4]

    # Insert at position
    numbers.insert(0, 0);  # Insert 0 at index 0
    print(numbers);  # [0, 1, 99, 3, 4]

    # Remove by value
    numbers.remove(99);
    print(numbers);  # [0, 1, 3, 4]

    # Remove by index
    numbers.pop(0);  # Remove first item
    print(numbers);  # [1, 3, 4]
}
```

### 7.4 List Operations

```jac
with entry {
    numbers = [1, 2, 3];

    # Length
    print(len(numbers));  # 3

    # Concatenation
    more_numbers = numbers + [4, 5];
    print(more_numbers);  # [1, 2, 3, 4, 5]

    # Repetition
    repeated = [0] * 5;
    print(repeated);  # [0, 0, 0, 0, 0]

    # Membership
    if 2 in numbers {
        print("Found 2!");
    }
}
```

### 7.5 Looping Through Lists

```jac
with entry {
    fruits = ["apple", "banana", "cherry"];

    # Loop through items
    for fruit in fruits {
        print(f"I like {fruit}");
    }

    # Loop with index
    for i = 0 to i < len(fruits) by i += 1 {
        print(f"{i}: {fruits[i]}");
    }
}
```

### 7.6 List Slicing

Get a portion of a list:

```jac
with entry {
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

    # [start:end] - start is included, end is excluded
    print(numbers[2:5]);   # [2, 3, 4]

    # [:end] - from beginning to end
    print(numbers[:3]);    # [0, 1, 2]

    # [start:] - from start to end of list
    print(numbers[7:]);    # [7, 8, 9]

    # [start:end:step] - with step size
    print(numbers[0:9:2]); # [0, 2, 4, 6, 8]
}
```

### 7.7 Dictionaries - Key-Value Pairs

Dictionaries store data as key-value pairs:

```jac
with entry {
    # Create a dictionary
    person = {
        "name": "Alice",
        "age": 25,
        "city": "Seattle"
    };

    # Access values by key
    print(person["name"]);  # Alice
    print(person["age"]);   # 25

    # Add or modify
    person["job"] = "Engineer";
    person["age"] = 26;

    print(person);
}
```

### 7.8 Looping Through Dictionaries

```jac
with entry {
    scores = {
        "Alice": 95,
        "Bob": 87,
        "Charlie": 92
    };

    # Loop through keys
    for name in scores {
        print(f"{name}: {scores[name]}");
    }
}
```

### 7.9 Tuples - Immutable Lists

Tuples are like lists, but they can't be changed after creation:

```jac
with entry {
    # Create a tuple
    point = (10, 20);

    # Access like a list
    print(point[0]);  # 10
    print(point[1]);  # 20

    # Unpack into variables
    (x, y) = point;
    print(f"x={x}, y={y}");

    # Can't modify!
    # point[0] = 5;  # ERROR!
}
```

### 7.10 List Comprehensions - Powerful Shortcuts

Create lists in one line:

```jac
with entry {
    # Traditional way
    squares = [];
    for i = 0 to i < 5 by i += 1 {
        squares.append(i ** 2);
    }
    print(squares);  # [0, 1, 4, 9, 16]

    # List comprehension way
    squares = [i ** 2 for i in range(5)];
    print(squares);  # [0, 1, 4, 9, 16]

    # With condition
    evens = [i for i in range(10) if i % 2 == 0];
    print(evens);  # [0, 2, 4, 6, 8]
}
```

### 7.11 Practice Exercises

**Challenge 1:** Create a list of your 5 favorite foods and print each one.

**Challenge 2:** Create a dictionary of 3 people with their ages, then print the oldest person.

```jac
with entry {
    ages = {"Alice": 25, "Bob": 30, "Charlie": 22};

    oldest_name = "";
    oldest_age = 0;

    for name in ages {
        if ages[name] > oldest_age {
            oldest_age = ages[name];
            oldest_name = name;
        }
    }

    print(f"{oldest_name} is the oldest at {oldest_age}");
}
```

```jac
with entry {
    # Collections
    numbers: list = [1, 2, 3];
    coords: tuple = (10, 20);
    person: dict = {"name": "Alice", "age": 25};
    unique: set = {1, 2, 3};

    print(f"Name: {name}, Age: {age}");
    print(f"Numbers: {numbers}");
}
```


## From: dspfoundation.md

#### Path Collections

The **path collection** ($\mathcal{P}$) introduces a higher-order topological construct that represents an ordered sequence of nodes and edges within the object-spatial structure. As first-class citizens in the programming model, path collections can be created, modified, and manipulated like any other data structure. This abstraction serves as a critical link between topology and traversal semantics, enabling concise expression of traversal patterns while maintaining the integrity of the object-spatial model.

The intent of the path collection is to provide a unified framework that bridges graph theory and computation, creating a formal way to express how walkers move through connected data structures. Rather than treating node traversals and edge traversals as separate concerns, the path collection unifies them into a single construct that preserves topological relationships while enabling richer expression of traversal algorithms.

A path collection is defined as:
$$\mathcal{P} = [p_1, p_2, \ldots, p_k]$$
where each $p_i \in N \cup E$ (i.e., each element is either a node or an edge), subject to the following constraints:

1. **Origin Connectivity:** The first element $p_1$ must be connected to an origin node $n_{\text{origin}} \in N$, either by being the origin itself or by being an edge with $n_{\text{origin}}$ as an endpoint.

2. **Sequential Connectivity:** For each element $p_i$ where $i > 1$ in $\mathcal{P}$, at least one of the following must hold:
   - If $p_i$ is a node, then there must exist at least one element $p_j$ where $j < i$ such that either:
     - $p_j$ is a node and there exists an edge $e \in E$ connecting $p_j$ and $p_i$, or
     - $p_j$ is an edge with $p_i$ as one of its endpoints

   - If $p_i$ is an edge, then at least one of its endpoints must appear as a node in $\{p_1, p_2, \ldots, p_{i-1}\}$

3. **Path Completeness:** For any element $p_i$ in $\mathcal{P}$, there must exist a path from $n_{\text{origin}}$ to $p_i$ such that all intermediate elements (nodes and edges) on that path are present in the prefix $\{p_1, p_2, \ldots, p_{i-1}\}$. This ensures that the path collection contains at least one valid traversal route to each included element.

4. **Traversal Coherence:** When multiple elements are eligible for inclusion at a given point in the sequence (e.g., multiple nodes connected to previously included elements), their relative ordering follows breadth-first search (BFS) semantics from the most recently added elements, preserving locality of traversal.

This definition ensures topological validity by anchoring all nodes to a common origin while allowing flexible expression of traversal patterns. The breadth-first ordering provides predictability and consistency for walkers traversing the path, particularly when dealing with hierarchical structures where multiple branches might need to be explored.

As first-class citizens, path collections support arbitrary modifications, including additions, removals, reorderings, and transformations, provided that the resulting collection maintains the properties of a valid path collection. Operations such as concatenation, slicing, filtering, and mapping can be applied to path collections, yielding new valid path collections. This flexibility enables algorithmic manipulation of potential traversal paths while preserving the topological integrity of the underlying data structure.

This generalized path collection model reflects a natural way to describe, in a declarative way, potential routes as to how walker may navigate through a data topology. By allowing both nodes and edges in the same sequence while maintaining topological context, path collections enable algorithms to be expressed in terms of the connected data structures they operate on, rather than as abstract operations that receive data as input.

#### Path Construction

Building on the definition of path collections as first-class citizens in the programming model, a path collection can be constructed in several ways:

1. **Explicit Construction**: By directly specifying the ordered sequence of nodes and optional edges:

    $$\mathcal{P} = [p_1, p_2, \ldots, p_k] \text{ where } p_i \in N \cup E$$

    When explicitly constructing path collections, the elements must satisfy the reachability and ordering constraints defined earlier, ensuring that walkers can traverse through the path in a topologically valid sequence. Edges, when included, must immediately precede the nodes they connect to on the reachability path from the origin node.

2. **Query-Based Construction**: By specifying an origin node and a traversal predicate:

    $$\mathcal{P} = \text{path}(n_{\text{origin}}, \text{predicate}, \text{includeEdges}, d)$$

    where:
    - $n_{\text{origin}} \in N$ is the origin node from which all nodes in the path must be reachable
    - $\text{predicate}: N \cup E \rightarrow \{\text{true}, \text{false}\}$ is a function that determines whether an element should be included in the path
    - $\text{includeEdges} \in \{\text{true}, \text{false}\}$ specifies whether edges should be explicitly included in the path collection
    - $d \in \{\text{outgoing}, \text{incoming}, \text{any}\}$ specifies the traversal direction for constructing the path

    The construction algorithm performs a breadth-first traversal from the origin node, adding elements to the path collection according to the predicate and the includeEdges parameter. This ensures that the resulting path maintains proper reachability relations while allowing flexible filtering of elements.

    A common example of query-based construction is creating a path that follows a specific sequence of edge types:

    $$\mathcal{P} = \text{path}(n_{\text{origin}}, \lambda e : e \in E \land \text{type}(e) \in [\tau_{\text{edge}}^1, \tau_{\text{edge}}^2, \ldots, \tau_{\text{edge}}^k] \text{ in sequence}, \text{true}, \text{outgoing})$$

    This creates a path collection starting at $n_{\text{origin}}$ and following only edges that match the specified sequence of edge types. The path resolution algorithm traverses the graph, selecting edges and their connected nodes that conform to this type pattern. A walker traversing this path would follow a route determined by these edge type constraints, enabling declarative specification of complex traversal patterns based on relationship types.

Once constructed, these path collections can be passed to walkers to guide their traversal through the topological structure, as we'll see in the next section on walker destination queues.

#### Walker Destination Queues

While path collections define potential traversal routes through the topology, **walker destination queues** ($Q_w$) represent the actual execution sequence that a walker follows during its traversal. Each active walker $w$ maintains an internal traversal queue $Q_w$ that determines its next destinations:

$$Q_w = [q_1, q_2, \ldots, q_m] \text{ where } q_i \in N \cup E$$

Walker destination queues have several key properties that govern traversal dynamics:

1. **First-In-First-Out (FIFO) Processing**: Walker destination queues follow FIFO semantics, with elements processed in the order they were added. When a walker completes execution at its current location, it automatically moves to the next element in its queue.

2. **Dynamic Modification**: Walker destination queues are designed for dynamic modification during traversal through visit statements and other control flow mechanisms:

    $$\text{visit}(w, n) \Rightarrow Q_w \leftarrow Q_w \cup [n]$$

    This allows walkers to adapt their traversal paths based on discovered data or computed conditions.

3. **Automatic Edge-to-Node Transitions**: When a walker traverses an edge, the appropriate destination node is automatically added to its queue if not already present, ensuring continuity in the traversal process.

4. **Path-to-Queue Conversion**: When a walker spawns on or visits a path collection, the path is converted into queue entries according to traversal requirements:

    $$\text{visit}(w, \mathcal{P}) \Rightarrow Q_w \leftarrow Q_w \cup \text{expandPath}(\mathcal{P}, L(w))$$

    where $\text{expandPath}(\mathcal{P}, L(w))$ transforms the path collection into a physically traversable sequence from the walker's current location $L(w)$. This function ensures that:

    - All elements in $\mathcal{P}$ are included in the expanded queue
    - Any necessary intermediate nodes or edges required for physical traversal between non-adjacent elements are inserted
    - The resulting sequence maintains the relative ordering of elements in the original path collection
    - The expanded path respects the connectivity constraints of the topological structure

    This conversion enables walkers to traverse path collections that express higher-level traversal intent without requiring explicit specification of every intermediate step.

5. **Activity Persistence**: Once a walker transitions to an active state via spawn, it remains active until its queue is exhausted or it is explicitly disengaged. This ensures computational continuity during traversal, maintaining the walker's contextual state throughout its path exploration. When a walker's queue becomes empty after all abilities at its current location have executed, it automatically transitions back to an inactive state. However, while at a node with an empty queue, it temporarily preserves its active status, allowing for potential reactivation through new visit statements before the current execution cycle completes.

The relationship between the path collection ($\mathcal{P}$) and the dynamic walker queue ($Q_w$) creates a flexible yet deterministic traversal model, allowing for both declarative path specifications and runtime adaptation of traversal behavior.


## From: chapter_1.md

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
```
```jac
node Person {
    has name: str;
    has age: int;
    has interests: list[str] = [];
}
```
```jac
walker FindCommonInterests {
    # The walker needs to know who we're comparing against.
    has target_person: Person;
    # It will store the results of its search here.
    has common_interests: list[str] = [];
```
```jac
node Person {
    has name: str;
    has age: int;
    has interests: list[str] = [];
}
```


## From: chapter_10.md

```jac
            has visited_locations: list[str] = [];
```
```jac
            has messages: list[str] = [];
```
```jac
            has rooms_visited: set[str] = {};
```
```jac
            has present_students: list[str] = [];
            has absent_students: list[str] = [];
```


## From: chapter_17.md

```jac
walker debug_graph {
    has visited_nodes: list[str] = [];
    has visited_edges: list[str] = [];
    has max_depth: int = 3;
    has current_depth: int = 0;
```

```jac
walker feed_loader {
    has user_id: str;
    has loaded_tweets: list[dict] = [];
    has users_visited: set[str] = set();
    has errors: list[str] = [];
```

```jac
walker get_recommendations(visit_profile) {
    has limit: int = 5;
    has algorithm: str = "hybrid";
    has recommendations: list[dict] = [];
```

```jac
def calculate_recommendation_score(
    current_user: Profile,
    candidate: Profile,
    followed_users: list[Profile]
) -> float {
```

```jac
def get_recommendation_reason(
    current_user: Profile,
    candidate: Profile,
    followed_users: list[Profile]
) -> str {
```


## From: chapter_4.md

```jac
# A global dictionary to map operation names to their corresponding functions.
glob operations: dict[str, callable] = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide
};
```
<br />

Finally, let's put it all together. Our main execution block can now use the calculator function and the operations dictionary to perform calculations dynamically.

``` jac

# Main entry point for the program
with entry {
    a: float = 10.0;
    b: float = 5.0;

    # To test other operations, simply change this string.
    operation_name: str = "add";

    # Check if the requested operation exists in our dictionary.
    if operation_name in operations {
        # Look up the function in the dictionary and pass it to the calculator.
        selected_operation_func = operations[operation_name];
        result: float = calculator(a, b, selected_operation_func);
        print(f"Result of {operation_name}({a}, {b}) = {result}");
    } else {
        print(f"Operation '{operation_name}' is not supported.");
    }
}

```
This design is highly flexible. To add a new operation, like exponentiation, you would simply define a new `power` function and add it to the operations dictionary. You wouldn't need to change the core calculator logic at all. This demonstrates the power of treating functions as first-class data.

<br />


### Lambda Functions
In Jac, a lambda function is a concise, single-line, anonymous function. These are useful for short, specific operations where defining a full function with def would be unnecessarily verbose.

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

### Higher-Order Functions
A higher-order function is a function that either takes another function as an argument, returns a function, or both. This is a powerful concept that enables functional programming patterns, promoting code that is abstract, reusable, and composable.

The `callable` type hint is used to specify that a parameter or return value is expected to be a function.

```jac
# Higher-order function that applies operation to list
def apply_operation(numbers: list[float], operation: callable) -> list[float] {
    return [operation(num) for num in numbers];
}

# Function that creates specialized functions
def create_multiplier(factor: float) -> callable[[float], float] {
    return lambda x: float: x * factor;
}

# Function composition
def compose(f: callable, g: callable) -> callable {
    return lambda x: any: f(g(x));
}

with entry {
    print("=== Higher-Order Functions Demo ===");

    numbers = [1.0, 2.0, 3.0, 4.0, 5.0];

    # Create specialized multiplier functions
    triple = create_multiplier(3.0);
    quadruple = create_multiplier(4.0);

    # Apply operations
    tripled = apply_operation(numbers, triple);
    quadrupled = apply_operation(numbers, quadruple);

    print(f"Original: {numbers}");
    print(f"Tripled: {tripled}");
    print(f"Quadrupled: {quadrupled}");
}
```
<br />

### Built-in Higher-Order Functions `map`, `filter`, and `sorted`
Jac supports Python's essential built-in higher-order functions, which are powerful tools for working with lists and other collections without writing explicit loops.

### *filter*

The `filter` function constructs a new iterable from elements of an existing one for which a given function returns True.

Its signature is `filter(function, iterable)`.

Let's revisit our grade-filtering example from Chapter 3. Instead of a list comprehension, we can use filter with a lambda function to define our condition.


```jac
with entry {
    # Raw test scores
    test_scores: list = [78, 85, 92, 69, 88, 95, 72];

    # Get passing grades (70 and above)
    passing_scores: list = [score for score in test_scores if score >= 70];
    print(f"Passing scores: {passing_scores}");
}
```
<br />

The same result can be achieved using the `filter` function along with a lambda function to define the filtering condition.

```jac
with entry {
    test_scores: list[int] = [78, 85, 92, 69, 88, 95, 72];

    # The lambda `lambda score: bool: score >= 70` returns True for passing scores.
    # 'filter' applies this lambda to each item in 'test_scores'.
    passing_scores_iterator = filter(lambda score: float: score >= 70, test_scores);

    # The result of 'filter' is an iterator, so we convert it to a list to see the results.
    passing_scores: list[int] = list(passing_scores_iterator);
    print(f"Passing scores: {passing_scores}");
}
```
<br />


### *map*
The `map` function applies a given function to every item of an iterable and returns an iterator of the results.
Its signature is `map(function, iterable)`. This is ideal for transforming data without writing explicit loops.

```jac
def classify_grade(score: int) -> str {
    if score >= 90 {
        return "A";
    } elif score >= 80 {
        return "B";
    } elif score >= 70 {
        return "C";
    } elif score >= 60 {
        return "D";
    } else {
        return "F";
    }
}

with entry {
    # Raw test scores
    test_scores = [78, 85, 92, 69, 88, 95, 72];


## From: chapter_3.md

Since Jac is a super-set of Python, it supports the same collection types: lists, dictionaries, sets, and tuples. However, Jac enforces type annotations for all collections, ensuring type safety and clarity.

### Lists
Lists are ordered collections of items that can be of mixed types. In Jac, lists are declared with the `list` type.

Let's create a list to store a student's grades.

```jac
with entry {
    # Create an empty list for storing integer grades
    alice_grades: list[int] = [];

    # Append grades to the list
    alice_grades.append(88); # [88]
    alice_grades.append(92); # [88, 92]
    alice_grades.append(85); # [88, 92, 85]

    # Access grades by index
    first_grade: int = alice_grades[0];  # 88
    print(f"Alice's first grade: {first_grade}");

    # print the entire list of grades
    print(f"Alice's grades: {alice_grades}");
}
```
```text
$ jac run example.jac
Alice's first grade: 88
Alice's grades: [88, 92, 85]
```

### Dictionaries
Dictionaries are perfect for storing data as key-value pairs, which allows you to look up a value instantly if you know its key. You declare a dictionary with the `dict` type, specifying the type for the keys and the values.

Here is how you could use a dictionary to create a gradebook where student names are the keys and their grades are the values.

```jac
with entry {
    # Class gradebook
    math_grades: dict[str, int] = {
        "Alice": 92,
        "Bob": 85,
        "Charlie": 78
    };

    # Access grades by student name
    print(f"Alice's Math grade: {math_grades['Alice']}");
    print(f"Bob's Math grade: {math_grades['Bob']}");
    print(f"Charlie's Math grade: {math_grades['Charlie']}");
}
```
```text
$ jac run example.jac
Alice's Math grade: 92
Bob's Math grade: 85
Charlie's Math grade: 78
```

### Sets
A set is an unordered collection that does not allow duplicate items. This makes them very useful for tasks like tracking unique entries or comparing two groups of data. You declare a set with the `set` type.

In this example, we'll use sets to find out which courses two students have in common.

```jac
with entry {
    # Track unique courses
    alice_courses: set[str] = {"Math", "Science", "English"};
    bob_courses: set[str] = {"Math", "History", "Art"};

    # Find common courses
    common_courses = alice_courses.intersection(bob_courses);
    print(f"Common courses: {common_courses}");

    # All unique courses
    all_courses = alice_courses.union(bob_courses);
    print(f"All courses: {all_courses}");
}
```
The `intersection` method finds items that are present in both sets, while the `union` method combines both sets into one, automatically removing any duplicates. These are standard operations provided by Python’s built-in `set` type, and Jac supports them as well. For a more comprehensive overview of collection-related functions in Python, refer to the [official Python documentation](https:#docs.python.org/3/tutorial/datastructures.html).


## Collection Comprehensions
Jac supports list and dictionary comprehensions, which are a concise and powerful way to create new collections by processing existing ones. Let's see how you can use them to work with a gradebook.

Imagine you have a list of test scores and you want to quickly create a new list containing only the passing grades.

```jac
with entry {
    # Raw test scores
    test_scores: list[int] = [78, 85, 92, 69, 88, 95, 72];

    # Get passing grades (70 and above)
    passing_scores: list[int] = [score for score in test_scores if score >= 70];
    print(f"Passing scores: {passing_scores}");
}
```
The list comprehension syntax in Jac is similar to Python:
```[expression for item in iterable if condition]``` where,
`expression` is the value to include in the new list,
`item` is the variable representing each element in the original collection,
`iterable` is the collection being processed, and
`condition` is an optional filter.

Now, what if you wanted to apply a curve by adding 5 points to every score? A comprehension makes this simple too.

```jac
with entry {
    # Raw test scores
    test_scores: list[int] = [78, 85, 92, 69, 88, 95, 72];

    # Get passing grades (70 and above)
    passing_scores: list[int] = [score for score in test_scores if score >= 70];
    print(f"Passing scores: {passing_scores}");

    # Create a new list where each score is 5 points higher.
    curved_scores: list[int] = [score + 5 for score in test_scores];
    print(f"Curved scores: {curved_scores}");
}
```


## From: chapter_13.md

```jac
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
```

```jac
def list_counters() -> list[dict] {
    counters = [self --> Counter];
    return [
        {"name": c.name, "value": c.value}
        for c in counters
    ];
}
```


## From: chapter_14.md

```jac
            has shared_with: list[str] = [];
```


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


## From: rpg_game.md

```jac
obj Map {
    has level: Level, walls: list[Wall];    # embeds Level + walls
    has small_obstacles: list[Position];    # extra blocks
    has enemies: list[Position];    # enemy positions
    has player_pos: Position;       # player start
}
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
def create_next_level (last_levels: list[Level], difficulty: int, level_width: int, level_height: int)
-> Level by llm();
```

