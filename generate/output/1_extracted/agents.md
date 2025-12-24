# agents


## From: tool_suite.md

[Jac-GPT](https://jac-gpt.jaseci.org/) is an agentic chatbot that allows you to ask questions about Jac's documentation.


## From: examples.md

## Tutorials

-   **Fantacy Trading Game**

    ---

    *A text-based trading game where non-player characters are handled using large language models. Tool calling is used for game mechanics such as bargaining at shops.*

    [Start](./../../examples/mtp_examples/fantasy_trading_game/){ .md-button }

-   **AI-Powered Multimodal MCP Chatbot**

    ---

    *This Tutorial shows how to implement an agentic AI application using the byLLM package and object-spatial programming. MCP integration is also demonstrated here.*

    [Start](./../../examples/rag_chatbot/Overview/){ .md-button }

### Tool-calling examples

Examples showing how to orchestrate external tools (APIs, search, or internal tool servers) from Jac/byLLM and how to coordinate multi-agent workflows.

Repository location: [jac-byllm/examples/tool_calling](https://github.com/Jaseci-Labs/jaseci/tree/main/jac-byllm/examples/tool_calling)

??? note "Tool-calling examples (code)"
    Examples that demonstrate calling external tools, tool orchestration, or multi-agent interactions.

    === "wikipedia_react.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/tool_calling/wikipedia_react.jac"
        ```

    === "marketing_agency.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/tool_calling/marketing_agency.jac"
        ```

    === "fantasy_trading_game.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/tool_calling/fantasy_trading_game.jac"
        ```

    === "debate_agent.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/tool_calling/debate_agent.jac"
        ```

### Agentic AI examples

Small agentic patterns and lightweight multi-step reasoning examples (multi-turn planning, simple agents). These live under the agentic_ai examples folder.

Repository location: [jac-byllm/examples/agentic_ai](https://github.com/Jaseci-Labs/jaseci/tree/main/jac-byllm/examples/agentic_ai)

??? note "Agentic AI examples (code)"
    Examples that demonstrate small agentic behaviors and light-weight multi-step reasoning.

    === "friendzone_lite.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/agentic_ai/friendzone_lite.jac"
        ```

    === "genius_lite.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/agentic_ai/genius_lite.jac"
        ```


## From: llmdocs.md

### Claude Code and Command-Line Agents

```
# Jac Language Context
Include @llmdocs-jaseci-mini_v3.txt when working with .jac files
```

### Cursor

Add to `.cursorrules`:

```
When writing Jac code, reference llmdocs-jaseci-mini_v3.txt for syntax
```


## From: aider-genius-lite.md

Aider Genius Lite is a simple Jac-based Streamlit application for AI-powered code generation with task planning and validation. It provides a clean, intuitive interface for generating code from natural language requests with real-time feedback and validation.

*Aider Genius Lite demonstrates the power of agentic AI for code generation, showcasing how intelligent systems can understand, plan, and execute complex programming tasks autonomously.*


## From: task-manager-lite.md

Task Manager Lite is a lightweight AI-powered task management system that intelligently routes user requests to specialized handlers for task management, email writing, and general conversation.

### Intelligent Routing
- Automatically determines the best handler for your request
- Routes to specialized nodes: TaskHandling, EmailHandling, or GeneralChat
- Uses AI-powered classification for accurate routing

### Task Management
- **Add Tasks**: Create tasks with dates and times
- **Task Summarization**: Get summaries of all scheduled tasks
- **Smart Extraction**: Automatically extracts task details from natural language

### Email Writing
- Generate professional emails for various purposes
- Context-aware email content creation
- Support for different email types (meetings, follow-ups, etc.)

### General Chat
- Ask questions and get intelligent responses
- Get advice on productivity and time management
- General AI assistance for various topics

### Nodes
- **TaskHandling**: Manages task creation, scheduling, and summarization
- **EmailHandling**: Handles email content generation
- **GeneralChat**: Provides general AI conversation capabilities

### Walker
- **task_manager**: Main walker that routes requests and coordinates responses

*Task Manager Lite demonstrates the power of intelligent routing and specialized handling in agentic AI systems, showing how different capabilities can be combined to create comprehensive and effective task management solutions.*


## From: fantasy_trading_game.md

This tutorial demonstrates how to build AI agents with persistent state that can conduct conversations, execute trades, and maintain context across interactions. The tutorial covers integrating AI functions for character generation and dialogue systems.

This tutorial covers building a trading game system with:
- AI agents that maintain conversation state

## Step 5: Build Conversational AI Agent

Create an AI agent that maintains state and can execute actions:

```jac
def chat_with_player(player: Person, npc: Person, chat_history: list[Chat]) -> Chat
    by llm(method="ReAct", tools=[make_transaction]);
```

**AI agent characteristics:**
- **Maintains State**: Uses `chat_history` to remember previous interactions
- **Reasons**: Processes conversation context using ReAct method
- **Acts**: Can use tools like `make_transaction` when appropriate
- **Persists Context**: Builds understanding across multiple conversation turns

**Agent capabilities:**
- Remember previous conversations through persistent `chat_history`
- Execute trades when agreements are reached
- Negotiate prices within reasonable bounds
- Stay in character while being functional

## Step 6: Implement the Game Loop

Connect all components in the main execution:

```jac
with entry {
    # Generate characters using AI functions
    player = make_player();
    npc = make_random_npc();

    # Register characters for transactions
    person_record[player.name] = player;
    person_record[npc.name] = npc;

    history = [];

    while True {
        # AI agent generates response with state
        chat = chat_with_player(player, npc, history);
        history.append(chat);

        # Display game state
        for p in [player, npc] {
            print(p.name, ":  $", p.money);
            for i in p.inventory {
                print("  ", i.name, ":  $", i.price);
            }
        }

        # Show NPC response and get player input
        print("\n[[npc]] >> ", chat.message);
        inp = input("\n[[Player input]] >> ");
        history.append(Chat(person=player.name, message=inp));
    }
}
```

**Game loop execution:**
3. Uses the AI agent for NPC responses (stateful - maintains conversation history)

## AI Functions vs AI Agents

### AI Agents (Stateful)

AI systems that maintain persistent state across interactions:
- `chat_with_player()` with `chat_history` parameter - Retains conversation context
- Builds understanding over multiple turns
- Can reference previous interactions

## Implementation Concepts

### Tool Integration

The AI agent accesses application functions through tools:
- The `chat_with_player` AI agent can call `make_transaction`
- The AI extracts parameters from natural language
- Tool results are incorporated into responses

### State Management

The AI agent maintains state through:
- Structured data objects (`Person`, `InventoryItem`)
- Conversation history (`Chat` objects)
- Global registries (`person_record`)

The `chat_with_player` agent maintains conversation history and can execute trades through tool integration, while character generation functions provide stateless AI capabilities. The structured datatypes serve as a vocabulary for communicating game concepts to the AI, enabling natural language interactions that result in functional game mechanics.

