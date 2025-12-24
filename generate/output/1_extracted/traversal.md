# traversal


## From: jac_in_a_flash.md

This example shows how conventional logic can become graph traversal.


## From: keywords.md

**Walker Navigation**

| Keyword | Description |
| --- | --- |
| [`visit`](https://www.jac-lang.org/learn/jac_ref/#visit-statement) | Directs a walker to traverse to a node or edge. |
| [`spawn`](https://www.jac-lang.org/learn/jac_ref/#object-spatial-spawn-expressions) | Creates and starts a walker on a graph. |
| [`ignore`](https://www.jac-lang.org/learn/jac_ref/#ignore-statement) |Excludes a node or edge from a walker's traversal. |
| [`disengage`](https://www.jac-lang.org/learn/jac_ref/#disengage-statement) | Immediately terminates a walker's traversal. |
| [`report`](https://www.jac-lang.org/learn/jac_ref/#report-statements) | Sends a result from a walker back to its spawning context. |
| [`with entry`](https://www.jac-lang.org/learn/jac_ref/#integration-with-entry-points) | Defines the main execution block for a module. |


## From: library_mode.md

**In Jac:**
```jac
visit [-->];                      # Visit all outgoing edges
visit [edge ->:Family :->];       # Visit only Family edges
```

**In Library Mode:**
```python
from jaclang.lib import visit, refs, OPath

visit(self, refs(OPath(here).edge_out().visit()))
visit(
    self, refs(OPath(here).edge_out(edge=lambda i: isinstance(i, Family)).edge().visit())
)
```

The `OPath()` class constructs traversal paths from a given node. The `edge_out()` method specifies outgoing edges to follow, while `edge_in()` specifies incoming edges. The `edge()` method filters the path to include only edges, excluding destination nodes. The `visit()` method marks the constructed path for the walker to traverse, and `refs()` converts the path into concrete node or edge references.

| Class | Description | Usage |
|-------|-------------|-------|
| `OPath` | Object-spatial path builder | `OPath(node).edge_out()` |

| Method | Description | Returns |
|--------|-------------|---------|
| `OPath(node)` | Create path from node | ObjectSpatialPath |
| `.edge_out(edge, node)` | Filter outgoing edges | Self (chainable) |
| `.edge_in(edge, node)` | Filter incoming edges | Self (chainable) |
| `.edge_any(edge, node)` | Filter any direction | Self (chainable) |
| `.edge()` | Edges only (no nodes) | Self (chainable) |
| `.visit()` | Mark for visit traversal | Self (chainable) |


## From: example.md

Computation in OSP occurs by traversing these graphs using two key constructs:
By modeling relationships directly as graph edges and expressing computation through walkers, OSP removes much of the boilerplate needed to manage graphs, traversals, search and state. This makes complex logic simpler, clearer, and more scalable.
```jac
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
```


## From: chapter_18.md

```jac
                cached = [-->(`?WeatherData)](?city == self.city);
```
```jac
        weather_count = len([-->(`?WeatherData)]);
```
```jac
            cached = [-->(`?WeatherData)](?city == self.city);
```
```jac
            cached_cities = len([-->(`?WeatherData)]);
```


## From: jac-cloud.md

- **Jac Clouds Traverse API**: Introduced the ability to traverse graph. This API support control of the following:
  - source - Starting node/edge. Defaults to root
  - detailed - If response includes archetype context. Defaults to False
  - depth - how deep the traversal from source. Count includes edges. Defaults to 1
  - node_types - Node filter by name. Defaults to no filter
  - edge_types - Edge filter by name. Defaults to no filter
- **Support Spawning a Walker with List of Nodes and Edges**: Introduced the ability to spawn a walker on a list of nodes and edges. This feature enables initiating traversal across multiple graph elements simultaneously, providing greater flexibility and efficiency in handling complex graph structures.
- **Async Walker Support**: Introduced comprehensive async walker functionality that brings Python's async/await paradigm to object-spatial programming. Async walkers enable non-blocking spawns during graph traversal, allowing for concurrent execution of multiple walkers and efficient handling of I/O-bound operations.


## From: filtering.md

# Node and Edge Filtering

JacLang provides flexible filtering mechanisms to control graph traversal and operations, allowing precise selection of nodes and edges based on specific criteria. These filters enable developers to optimize traversal and focus only on relevant parts of the graph.

## Node-Based Filtering

Node-based filtering restricts traversal to specific nodes that satisfy predefined conditions. This is useful when you need to:

- Limit traversal to nodes with certain attributes or properties.
- Filter nodes dynamically based on walker state or external context.

## Edge-Based Filtering

Edge filtering in JacLang allows developers to control traversal by selecting edges based on specific attributes or conditions. This is especially useful in scenarios where certain edges in the graph are more relevant to the task at hand, such as weighted graphs or context-sensitive connections.


## From: walkers.md

## Graph Traversal Using Visit
Walkers navigate the graph using the ```visit``` keyword.
=== "visiting_node.jac"
    ```jac linenums="1"
    visit [node_name]; # Visits a particular node
    ```
=== "visiting_sucessor.jac"
    ```jac linenums="1"
    visit [node_name-->]; # Visits successive nodes of a node
    ```
=== "visiting_predecessor.jac"
    ```jac linenums="1"
    visit [<--node_name]; # Visits predecessor nodes of a node
    ```
- Control Movement:
    - Use ```visit``` to:
        - Direct the walker to a specific node.
        - Walk along an edge connecting nodes.

By using these principles, walkers can efficiently traverse and interact with graphs, enabling dynamic workflows.

!!! Abstract "can log_entry with entry"
    - This ability is triggered once when the walker is spawned. It is essentially the "entry point" of the walker’s operation.
    In the example, it logs the entry at the beginning, increments entry_count by 1, and prints the node where the walker starts (in this case, the root node).
    !!! Info ""
        - This DS function is called once at the beginning of the walker’s traversal before visiting any nodes.

!!! Abstract "can log_visit with test_node exit"
    - This ability is executed each time the walker visits a node of type test_node during its traversal.
    In the example, whenever the walker visits a test_node, it prints the node and appends the node to visited_nodes.
    !!! Info ""
        - This DS function operates during traversal and is called on each node of type test_node the walker visits.

!!! Abstract "can log_exit with exit"
    - This ability is triggered once when the walker finishes its traversal, marking the end of its operation.
    In the example, it logs the exit point, increments exit_count by 1, and prints the final node visited.
    !!! Info ""
        - This DS function is executed at the end of the walker's execution, after all nodes have been visited.


## From: FAQ.md

- A walker can visit all successor nodes (directly connected nodes):
  ```jac
      visit [node_name -->];
  ```
- To retrieve all the successor nodes:
  ```jac
      print([node_name -->]);
  ```
- You can traverse nodes using the visit operation, which allows you to move from one node to another along edges.
```jac
visit [node_a -->];
```


## From: utilities.md

## Traverse

This API allows for the traversal of the knowledge graph starting from a specified source.

### Endpoint

`GET /util/traverse`

### Query Parameters

| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `source`     | `string`  | The **JID** of the starting root, node, or edge for the traversal.                                                                                                                       | Current user's root |
| `detailed`   | `boolean` | If `true`, the response will include the archetype's context for each traversed item.                                                                                                    | `false`             |
| `depth`      | `integer` | The maximum number of steps to traverse. Both nodes and edges are considered one step.                                                                                                   | `1`                 |
| `node_types` | `string`  | Can be declared multiple times to filter the traversal results by node type. For example, `node_types=Node1&node_types=Node2` will include only nodes that are `Node1` or `Node2` types. | All node types      |
| `edge_types` | `string`  | Can be declared multiple times to filter the traversal results by edge type. For example, `edge_types=Edge1&edge_types=Edge2` will include only edges that are `Edge1` or `Edge2` types. | All edge types      |

### Sample Request

```bash
curl -X GET "/util/traverse?source=n::68875f383d1e672f517094ff&detailed=true&depth=2&node_types=Node1&node_types=Node2&edge_types=Edge1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Traverse Stream

This API is similar to the `/util/traverse` endpoint but streams the traversal results. It returns data incrementally, pushing results as they are processed for each step of the traversal.

### Endpoint

`GET /util/traverse-stream`

### Query Parameters

The query parameters for `/util/traverse-stream` are identical to those for `/util/traverse`:

| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `source`     | `string`  | The **JID** of the starting root, node, or edge for the traversal.                                                                                                                       | Current user's root |
| `detailed`   | `boolean` | If `true`, the response will include the archetype's context for each traversed item.                                                                                                    | `false`             |
| `depth`      | `integer` | The maximum number of steps to traverse. Both nodes and edges are considered one step.                                                                                                   | `1`                 |
| `node_types` | `string`  | Can be declared multiple times to filter the traversal results by node type. For example, `node_types=Node1&node_types=Node2` will include only nodes that are `Node1` or `Node2` types. | All node types      |
| `edge_types` | `string`  | Can be declared multiple times to filter the traversal results by edge type. For example, `edge_types=Edge1&edge_types=Edge2` will include only edges that are `Edge1` or `Edge2` types. | All edge types      |

### Sample Request

```bash
curl -X GET "/util/traverse-stream?source=n::68875f383d1e672f517094ff&detailed=true&depth=2&node_types=Node1&node_types=Node2&edge_types=Edge1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Sample Streamed Response

The response will be a continuous stream of JSON objects, each representing a "step" in the traversal. The order of `nodes` and `edges` within each step may vary depending on the traversal logic.

```json
{"nodes": [], "edges": [{"id": "e::step1_edge1", "source": "n::start_node", "target": "n::next_node_A"}]}
{"nodes": [{"id": "n::next_node_A", "edges": ["e::step1_edge1"]}], "edges": []}
{"nodes": [], "edges": [{"id": "e::step2_edge1", "source": "n::next_node_A", "target": "n::final_node_B"}]}
{"nodes": [{"id": "n::final_node_B", "edges": ["e::step2_edge1"]}], "edges": []}
... (additional steps will be streamed as the traversal continues)
```


## From: tutorial.md

- **Navigate** through relationships between data
```jac
impl visit_profile.visit_profile {
    visit [-->(`?Profile)] else {
        new_profile = here ++> Profile();
        grant(new_profile[0], level=ConnectPerm);
        visit new_profile;
    }
}
```
```jac
impl load_feed.load {
    visit [-->(`?Tweet)];
    for user_node in [->:Follow:->(`?Profile)] {
        visit [user_node-->(`?Tweet)];
    }
    report self.results;
}
```

