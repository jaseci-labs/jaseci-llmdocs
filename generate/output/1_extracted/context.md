# context


## From: jac-cloud.md

- **Jac Clouds Traverse API**: Introduced the ability to traverse graph. This API support control of the following:
  - source - Starting node/edge. Defaults to root
  - detailed - If response includes archetype context. Defaults to False
  - depth - how deep the traversal from source. Count includes edges. Defaults to 1
  - node_types - Node filter by name. Defaults to no filter
  - edge_types - Edge filter by name. Defaults to no filter
- **save(...) should not override root in runtime**: The previous version bypassed access validation because the target archetype root was overridden by the current root, simulating ownership of the archetype.


## From: websocket.md

```python
{
    # event type
	"type": "walker",

    # walker's name
	"walker": "your_event_name",

    # if you want to receive a notification for response
	"response": true,

    # walker's request context
	"context": {
        "val": 1
    }
}
```

```js
// TRIGGER WALKER EVENT
client.send(JSON.stringify({
	"type": "walker",
	"walker": "your_walker_name",
	"response": true,
	"context": {}
}));
```


## From: filtering.md

## Node-Based Filtering

Node-based filtering restricts traversal to specific nodes that satisfy predefined conditions. This is useful when you need to:

- Limit traversal to nodes with certain attributes or properties.
- Filter nodes dynamically based on walker state or external context.

## Edge-Based Filtering

Edge filtering in JacLang allows developers to control traversal by selecting edges based on specific attributes or conditions. This is especially useful in scenarios where certain edges in the graph are more relevant to the task at hand, such as weighted graphs or context-sensitive connections.


## From: aider-genius-lite.md

- **Context Gathering**: Identifying relevant libraries, frameworks, and patterns


## From: utilities.md

| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `detailed`   | `boolean` | If `true`, the response will include the archetype's context for each traversed item.                                                                                                    | `false`             |
| Name         | Type      | Description                                                                                                                                                                              | Default Value       |
| :----------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------ |
| `detailed`   | `boolean` | If `true`, the response will include the archetype's context for each traversed item.                                                                                                    | `false`             |


## From: usage.md

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

### Adding Context with Docstrings

Docstrings provide context for LLM-integrated functions. byLLM uses docstrings to understand function purpose and expected behavior.

```jac linenums="1"
import from byllm.llm { Model }

glob llm = Model(model_name="gpt-4o");

"""Translate text to the target language."""
def translate(text: str, target_language: str) -> str by llm();

"""Generate a professional email response based on the input message tone."""
def generate_email_response(message: str, recipient_type: str) -> str by llm();
```

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


## From: fantasy_trading_game.md

This tutorial demonstrates how to build AI agents with persistent state that can conduct conversations, execute trades, and maintain context across interactions. The tutorial covers integrating AI functions for character generation and dialogue systems.

This tutorial covers building a trading game system with:
- AI agents that maintain conversation state
- Persistent conversation history
- Context-aware decision making

```jac
obj Chat {
    has person: str;
    has message: str;
}
```
**Structure definitions:**
- **Chat**: Message history for conversation context

```jac
def chat_with_player(player: Person, npc: Person, chat_history: list[Chat]) -> Chat
    by llm(method="ReAct", tools=[make_transaction]);
```

**AI agent characteristics:**
- **Maintains State**: Uses `chat_history` to remember previous interactions
- **Reasons**: Processes conversation context using ReAct method
- **Persists Context**: Builds understanding across multiple conversation turns

**Agent capabilities:**
- Remember previous conversations through persistent `chat_history`
- Stay in character while being functional

**Game loop execution:**
3. Uses the AI agent for NPC responses (stateful - maintains conversation history)
4. Accumulates conversation history for persistent context

### AI Agents (Stateful)

AI systems that maintain persistent state across interactions:
- `chat_with_player()` with `chat_history` parameter - Retains conversation context
- Builds understanding over multiple turns
- Can reference previous interactions

### State Management

The AI agent maintains state through:
- Structured data objects (`Person`, `InventoryItem`)
- Conversation history (`Chat` objects)
- Global registries (`person_record`)

The `chat_with_player` agent maintains conversation history and can execute trades through tool integration, while character generation functions provide stateless AI capabilities. The structured datatypes serve as a vocabulary for communicating game concepts to the AI, enabling natural language interactions that result in functional game mechanics.


## From: jac_serve.md

- Each request executes in the context of the authenticated user's root node
- All walker execution happens in the context of the authenticated user

