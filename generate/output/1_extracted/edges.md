# edges


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


## From: keywords.md

**Core Archetype Keywords**

| Keyword | Description |
| --- | --- |
| [`edge`](https://www.jac-lang.org/learn/jac_ref/#archetype-types)|Defines a directed connection between two nodes, which can have its own attributes and logic. |


## From: library_mode.md

**In Jac:**
```jac
edge Friend {}
```

**In Library Mode:**
```python
from jaclang.lib import Node, Edge


class Friend(Edge):
    pass
```

Graph nodes are implemented by inheriting from the `Node` base class, while relationships between nodes inherit from the `Edge` base class. Data fields are defined using standard Python class attributes with type annotations.

| Class | Description | Usage |
|-------|-------------|-------|
| `Edge` | Graph edge archetype | `class MyEdge(Edge):` |
| `GenericEdge` | Generic edge when no type specified | Default edge type |


## From: example.md

- edge classes (`edge`),

Instances of these node and edge classes form a graph structure that expresses semantic relationships between objects.
By modeling relationships directly as graph edges and expressing computation through walkers, OSP removes much of the boilerplate needed to manage graphs, traversals, search and state. This makes complex logic simpler, clearer, and more scalable.
```jac
root ++> alice ++> bob ++> charlie;
```
```jac
here ++> new_post;
```


## From: syntax_quick_reference.md

```jac
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
```


## From: chapter_2.md

A **literal** is a fixed value you write directly in your code, like "Alice" or 95. Jac uses common literals like *string*, *integer*, *float*, and *boolean*. It also introduces a special kind of literal called an **architype** (node, edge, and walker), which was briefly discussed in the prvious chapter.We will explore architypes in more detail later in chapter 9.


## From: chapter_10.md

In the previous chapters, you learned how to build the static structure of your application using nodes and edges.
- An `entry` ability triggers when a walker arrives at a node or edge.
- An `exit` ability triggers when a walker leaves a node or edge.

You can create specialized entry abilities that only trigger for specific node or edge types.

```jac
        edge InClass {
            has room: str;
        }
```
```jac
        edge StudyGroup {
            has subject: str;
        }
```


## From: chapter_11.md

```jac
edge FriendsWith {
    has since: str;
    has closeness: int; # 1-10 scale
}
```
```jac
edge FriendsWith {
    has since: str;
    has closeness: int; # 1-10 scale
}
```
```jac
edge ParentOf {}
```
```jac
edge ConnectedTo {
    has strength: int;
}
```


## From: chapter_8.md

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
### The `visit` Statement and `-->` Syntax

To understand how walkers move through the graph, it's important to break down the `visit` statement and the `-->` operator used in the example above.

In Jac, visit tells the walker to continue its traversal along the graph. What makes this powerful is the use of edge selectors inside the square brackets, like `[-->]`, which control how and where the walker moves.

The `-->` symbol represents a forward edge in the graph—specifically, an edge from the current node (`here`) to any of its connected child nodes. So when you write visit `[-->];`, you're instructing the walker to follow all outgoing edges from the current node to the next set of reachable nodes.

Let's walk through what each part means:

- `visit [-->];`: Move the walker along all forward edges from the current node.
- `visit [<--];`: Move backward (along incoming edges), useful for reverse traversals or backtracking.
- `visit [-->-->];`: Move along two forward edges in succession, allowing for deeper traversal into the graph.

Jac supports more complex edge selectors as well which we'll explore in subsequent chapters. For now, the key takeaway is that `visit` combined with edge selectors allows walkers to navigate the graph structure dynamically, processing nodes and edges as they go.
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

- **Edges**: First-class relationships with their own properties and behaviors


## From: chapter_9.md

In Object-Spatial Programming, **nodes** and **edges** are the fundamental building blocks of your application's graph. A node represents an entity or a location for your data, while an edge represents a typed, directional relationship between two nodes.
This chapter will show you how to define these core components and how to give your nodes special abilities, allowing them to interact with the walkers that visit them.

In Jac, edges are the pathways that connect your nodes. They are more than just simple pointers; they are first-class citizens of the graph. This means an `edge` can have its own attributes and abilities, allowing you to model rich, complex relationships like friendships, ownership, or enrollment.

Edges in Jac are not just connections - they're full objects with their own properties and behaviors. This makes relationships as important as the data they connect.

### Basic Edge Declaration

You define an edge's blueprint using the `edge` keyword, and you can give it has attributes just like a node or object.

Let's model a simple school environment with Student, Teacher, and Classroom nodes, and the various relationships that connect them.

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
Let's break down the edge creation syntax: <+:EdgeType(attributes):+>.
science_lab: The starting node (the "source" of the edge).

- `<+: ... :+>`: This syntax creates a bi-directional edge. It means the relationship can be traversed from science_lab to dr_smith and also from dr_smith back to science_lab.
- `Teaches(...)`: The type of edge we are creating, along with the data for its attributes.
- `Teacher(...)`: The destination node.

### Filtering by Edge Type and Attributes

In addition to filtering by node types and attributes, Jac also allows you to filter based on edge types and edge attributes, enabling precise control over traversal paths in complex graphs.

To traverse only edges of a specific type, use the following syntax:
```jac
visit [->:EdgeType->];
```

This tells the walker to follow only edges labeled as `EdgeType`, regardless of the type of the nodes they connect.

#### Example
```jac
# Only follow "enrolled_in"


## From: jac-cloud.md

- **Support Spawning a Walker with List of Nodes and Edges**: Introduced the ability to spawn a walker on a list of nodes and edges. This feature enables initiating traversal across multiple graph elements simultaneously, providing greater flexibility and efficiency in handling complex graph structures.
- **Support Custom Access Validation**: Introduced the ability to override access validation. `Node`/`Edge` can override `__jac_access__` reserved function (`builtin`) to have a different way of validating access. Either you cross-check it by current attribute, check from db or global vars or by just returning specific access level. [PR#1524](https://github.com/jaseci-labs/jaseci/pull/1524)


## From: chapter_19.md

```jac
edge Friend {
    has since: str;
    has strength: int = 1;  # Relationship strength for weighted algorithms
}
```


## From: quickstart.md

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


## From: jaclang.md

- **Support Spawning a Walker with List of Nodes and Edges**: Introduced the ability to spawn a walker on a list of nodes and edges. This feature enables initiating traversal across multiple graph elements simultaneously, providing greater flexibility and efficiency in handling complex graph structures.
- **Edge Ability Execution Semantics**: Enhanced edge traversal behavior with explicit edge references. By default, `[-->]` returns connected nodes, while `[edge -->]` returns edge objects. When walkers visit edges explicitly using `visit [edge -->]`, abilities are executed on both the edge and its connected node. Additionally, spawning a walker on an edge automatically queues both the edge and its target node for processing, ensuring complete traversal of the topological structure.
- **`visitor` Keyword**: Introduced the `visitor` keyword to reference the walker context within nodes/edges, replacing the ambiguous use of `here` in such contexts. `here` is now used only in walker abilities to reference the current node/edge.


## From: llmdocs.md

### Mini (Recommended)
- Objects, nodes, edges, walkers


## From: nodes_and_edges.md

Nodes can be linked using either default edges (generic connections) or custom edges, which have specific properties as shown in the following examples.
```jac linenums="1"
with entry {
  node_1 ++> node_2; # uni directional edge
  node_1 <++> node_2; # bidirectional edge
}
```
```jac linenums="1"
edge custom1 {
    has atrib1:str;
}

with entry {
  node_1 +:custom1:atrib1='val1':+> node_2; # uni directional edge
  node_1 <+:custom1:atrib1='val2':+> node_2; # bidirectional edge
}
```

To delete an edge between two nodes the `del` keyword can be used as shown below.

```jac linenums="1"
node_1 del --> node_2;
```


## From: filtering.md

# Node and Edge Filtering

JacLang provides flexible filtering mechanisms to control graph traversal and operations, allowing precise selection of nodes and edges based on specific criteria. These filters enable developers to optimize traversal and focus only on relevant parts of the graph.

## Edge-Based Filtering

Edge filtering in JacLang allows developers to control traversal by selecting edges based on specific attributes or conditions. This is especially useful in scenarios where certain edges in the graph are more relevant to the task at hand, such as weighted graphs or context-sensitive connections.

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

- Control Movement:
    - Use ```visit``` to:
        - Direct the walker to a specific node.
        - Walk along an edge connecting nodes.


## From: FAQ.md

- Nodes can be connected with generic edges (default) or custom edges (defined with specific properties).
```jac
  node_1 ++> node_2; # uni directional edge
  node_1 <++> node_2; # bidirectional edge
```
- Custom edges allow defining specific properties and behaviors for relationships between nodes
```jac
  edge edge_name{
      has edge_property: int = 10;
  }
```
- Nodes can be connected with a custom edge as follows:
```jac
  node_1 +: edge_name :+> node_2;
  node_1 +: edge_name :edge_property= 15: +> node_2; # connect with specific property value
```
- To delete a connection between nodes:
```jac
  node_1 del --> node_2;
```
- You can retrieve all the edges connected to a node by using edge filtering expressions.
```jac
    print([edge node_a-->]);
    print([edge node_a<--]);
    print([edge node_list[0]-->]);
```
- To get all edges between two nodes:
```jac
    print([edge node_1-->node_2]);
    print([edge node_list[0]-->node_list[1]]);

```
- You can connect a list of nodes to a single node in both series (one after the other) or in parallel (all at once):
```jac
    # Series connection (one after the other)
    node_1 ++> node_list[0];
    for i to i < length(node_list) by i+=1 {
        node_list[i] ++> node_list[i+1];
    }

    # Parallel connection (all at once)
    node_1 ++> node_list;
```
- A mesh connection between two lists of nodes can be established, connecting each node in the first list to each node in the second list:
```jac
    node_list_1 ++> node_list_2;
```


## From: utilities.md

| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `source`     | `string`  | The **JID** of the starting root, node, or edge for the traversal.                                                                                                                       | Current user's root |
| `edge_types` | `string`  | Can be declared multiple times to filter the traversal results by edge type. For example, `edge_types=Edge1&edge_types=Edge2` will include only edges that are `Edge1` or `Edge2` types. | All edge types      |
```json
{
  "edges": [
    {
      "id": "e::68875f483d1e672f517096a5",
      "source": "n::68875f383d1e672f517094ff",
      "target": "n:A:68875f483d1e672f517096a0"
    },
    {
      "id": "e::68875f483d1e672f517096a2",
      "source": "n:A:68875f483d1e672f517096a0",
      "target": "n:B:68875f483d1e672f517096a1"
    },
    {
      "id": "e::68875f483d1e672f517096a4",
      "source": "n:B:68875f483d1e672f517096a1",
      "target": "n:C:68875f483d1e672f517096a3"
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
| `edge_types` | `string`  | Can be declared multiple times to filter the traversal results by edge type. For example, `edge_types=Edge1&edge_types=Edge2` will include only edges that are `Edge1` or `Edge2` types. | All edge types      |


## From: agentic_ai.md

**Edges**: Create explicit connections between nodes, allowing agentic workflows to be formally defined. Edges represent relationships, dependencies, or hierarchies between agents. For example, a TaskHandler node might have edges pointing to Task nodes it created.

```jac linenums="1"
node Task {
  has task:str = "";
  has date:str = "";
  has time:str = "";
}
```

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


## From: tutorial.md

### 2. Edges: Connect Your Data

**Edges** create relationships between nodes. In LittleX:

- **Follow edges** connect users who follow each other
- **Post edges** connect users to their tweets
- **Like edges** connect users to tweets they liked

**Simple Example:**
```jac
edge Follow {}
```

This creates a "Follow" connection between users.
- **Edges** for connecting information


## From: tutorial.md

We do this by representing directed edges between a person to an email as a "sender of email" and an email to a person as a "recipient of email"
For each email uploaded, EmailBuddy:

- Extract sender and recipient addresses
- Create Person nodes if they do not already exist
- Create or skip Email node based on UUID matching
- Connect all Person and Email nodes to the root
- Create directed edges: person → email, and email → recipients

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
With these steps we will have a connected graph representation of our emails for us to traverse.

