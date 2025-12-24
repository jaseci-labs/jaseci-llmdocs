# filtering


## From: jac-lens.md

-   __Search & Filter__

    ---

    *Find nodes quickly*

    Search functionality to locate specific nodes in large graphs


## From: jac-cloud.md

- **Jac Clouds Traverse API**: Introduced the ability to traverse graph. This API support control of the following:
  - source - Starting node/edge. Defaults to root
  - detailed - If response includes archetype context. Defaults to False
  - depth - how deep the traversal from source. Count includes edges. Defaults to 1
  - node_types - Node filter by name. Defaults to no filter
  - edge_types - Edge filter by name. Defaults to no filter


## From: logging.md

Now you can view your logs in Kibana with powerful filtering, visualization, and alerting capabilities!

## Understanding Log Structure

Jac Cloud logs contain these key components:

```json
{
  "timestamp": "2024-04-10T14:25:36.789Z",
  "level": "INFO",
  "message": "Request processed successfully",
  "request": {
    "method": "POST",
    "path": "/walker/create_user",
    "headers": {"authorization": "Bearer ***", "content-type": "application/json"},
    "body": {"username": "example_user", "email": "user@example.com"}
  },
  "response": {
    "status_code": 200,
    "body": {"status": 200, "reports": ["User created successfully"]}
  },
  "duration": 125,
  "client_ip": "192.168.1.1"
}
```

This format makes it easy to filter and search for specific information.


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


## From: utilities.md

| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `node_types` | `string`  | Can be declared multiple times to filter the traversal results by node type. For example, `node_types=Node1&node_types=Node2` will include only nodes that are `Node1` or `Node2` types. | All node types      |
| `edge_types` | `string`  | Can be declared multiple times to filter the traversal results by edge type. For example, `edge_types=Edge1&edge_types=Edge2` will include only edges that are `Edge1` or `Edge2` types. | All edge types      |
| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `node_types` | `string`  | Can be declared multiple times to filter the traversal results by node type. For example, `node_types=Node1&node_types=Node2` will include only nodes that are `Node1` or `Node2` types. | All node types      |
| `edge_types` | `string`  | Can be declared multiple times to filter the traversal results by edge type. For example, `edge_types=Edge1&edge_types=Edge2` will include only edges that are `Edge1

