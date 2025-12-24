# ai_integration


## From: contrib.md

For help interpreting this if you need it, call upon our friend Mr. ChatGPT or one of his colleagues.


## From: tour.md

The Jac programming language and Jaseci runtime build on Python (fully compatible), introducing AI-first constructs, object-spatial programming (OSP), and scale-native capabilities. These features are designed to hide common development complexity, elevate AI to a first-class citizen, and automate categories of system and DevOps work that traditionally require extensive manual effort.

Jac is designed from the ground up to integrate AI directly into the programming model to simplify development of AI-powered applications.

- `by llm` - Jac introduces language-level constructs such as the `by()` keyword that automatically generate optimized prompts. This removes the need for manual prompt engineering and enables seamless model integration. In production systems, this feature has reduced hundreds of lines of prompt code to a single line. This feature can be used alone as Python library, or natively in Jac. [Read more about byllm](https://docs.jaseci.org/learn/jac-byllm/with_llm/).

- Native Agentic AI Workflows (enabled by OSP) - By leveraging OSP’s graph-based semantics, Jac naturally supports the creation and articulation of agentic workflows, allowing developers to create flows of interacting agents that collaborate, share memory, and act on dynamic context.

As shown in shown in Figure 1, together, OSP and `by llm` form a powerful foundation for rapid agentic AI development.

- AI/ML Engineers
Jac is AI-first: language-level constructs and runtime that use machine learning models seamlessly, reducing prompt engineering and making agent workflows natural. Ideal for building LLM agents, multimodal systems, and graph-based reasoning pipelines.

- Students
Jac’s high-level abstractions hide much of the typical systems complexity, making it accessible for students while still exposing them to modern concepts like AI integration and scalable application design. It provides an approachable on-ramp to both Python and full-stack AI development.

- You want LLMs and other AI models deeply integrated into your application logic, such as Agentic AI systems where you may need prompt engineering and aritculating agent workflows.
- You already rely heavily on Python code or libraries and want a smooth path to something more structured, graph-aware, and AI-centric.


## From: byllm.md

- **Streaming with ReAct Tool Calling**: Implemented real-time streaming support for ReAct method when using tools. After tool execution completes, the LLM now streams the final synthesized answer token-by-token, providing the best of both worlds: structured tool calling with streaming responses.
- **Custom Model Declaration**: Custom model interfaces can be defined by using the `BaseLLM` class that can be imported form `byllm.lib`. A guide for using this feature is added to [documentation](https://docs.jaseci.org/learn/jac-byllm/create_own_lm/).
- **byLLM Lazy Loading**: Refactored byLLM to support lazy loading by moving all exports to `byllm.lib` module. Users should now import from `byllm.lib` in Python (e.g., `from byllm.lib import Model, by`) and use `import from byllm.lib { Model }` in Jac code. This improves startup performance and reduces unnecessary module loading.
- **NonGPT Fallback for byLLM**: Implemented automatic fallback when byLLM is not installed. When code attempts to import `byllm`, the system will provide mock implementations that return random using the `NonGPT.random_value_for_type()` utility.
- **byLLM Plugin Interface Improved**: Enhanced the byLLM plugin interface with `get_mtir` function hook interface and refactored the `by` decorator to use the plugin system, improving integration and extensibility.
- **byLLM Enhancements**:
  - Fixed bug with Enums without values not being properly included in prompts (e.g., `enum Tell { YES, NO }` now works correctly).
- **byLLM transition**: MTLLM has been transitioned to byLLM and PyPi package is renamed to `byllm`. Github actions are changed to push byllm PyPi. Alongside an mtllm PyPi will be pushed which installs latest `byllm` and produces a deprecation warning when imported as `mtllm`.
- **byLLM Feature Methods as Tools**: byLLM now supports adding methods of classes as tools for the llm using such as `tools=[ToolHolder.tool]`
- **byLLM transition**: MTLLM has been transitioned to byLLM and PyPi package is renamed to `byllm`. Github actions are changed to push byllm PyPi. Alongside an mtllm PyPi will be pushed which installs latest `byllm` and produces a deprecation warning when imported as `mtllm`.
- **Removed LLM Override**: `function_call() by llm()` has been removed as it was introduce ambiguity in the grammer with LALR(1) shift/reduce error. This feature will be reintroduced in a future release with a different syntax.
- **Semantic Strings**: Introduced `sem` strings to attach natural language descriptions to code elements like functions, classes, and parameters. These semantic annotations can be used by Large Language Models (LLMs) to enable intelligent, AI-powered code generation and execution. (mtllm)
- **LLM Function Overriding**: Introduced the ability to override any regular function with an LLM-powered implementation at runtime using the `function_call() by llm()` syntax. This allows for dynamic, on-the-fly replacement of function behavior with generative models. (mtllm)


## From: litellm_proxy.md

byLLM model can also be connected to a [LiteLLM proxy server](https://docs.litellm.ai/docs/simple_proxy). This allows you to use the byLLM model as a proxy for LiteLLM, enabling you to leverage the capabilities of byLLM in a LiteLLM environment.

To set up and deploy the LiteLLM proxy server, you can follow the instructions provided in the LiteLLM documentation:

Once The proxy server is setted up and running, you can connect to it by simply passing the URL of the proxy server to the byLLM model with the parameter `proxy_url`:

```python
from byllm.lib import Model

llm = Model(
    model_name="gpt-4o",                # The model name to be used
    api_key="your_litellm_api_key",     # LiteLLM proxy server key
    proxy_url="http://localhost:8000",  # URL of the LiteLLM proxy server
)
```

Note that the `api_key` parameter is necessary to authenticate the connection, which is not the OpenAI API key but the virtual key (or master key) generated by the LiteLLM proxy server.


## From: introduction.md

- **AI/ML Services**: Deploy machine learning models as APIs


## From: multimodality.md

```jac
import from byllm.lib { Model, Image }

glob llm = Model(model_name="gpt-4o");

'Personality of the Person'
enum Personality {
   INTROVERT,
   EXTROVERT
}

sem Personality.INTROVERT = 'Person who is shy and reticent';
sem Personality.EXTROVERT = 'Person who is outgoing and socially confident';



obj Person {
    has full_name: str,
        yod: int,
        personality: Personality;
}

def get_person_info(img: Image) -> Person by llm();

with entry {
    image = Image("photo.jpg");
    person_obj = get_person_info(image);
    print(person_obj);
}
```

```jac
import from byllm.lib { Model, Video }

glob llm = Model(model_name="gpt-4o");

def explain_the_video(video: Video) -> str by llm();

with entry {
    video_file_path = "SampleVideo_1280x720_2mb.mp4";
    target_fps = 1
    video = Video(path=video_file_path, fps=target_fps);
    print(explain_the_video(video));
}
```


## From: examples.md

## Tutorials

-   **RPG Game Level Genaration**

    ---

    *A Tutorial on building an AI-Integrated RPG Game using byLLM.*

    [Start](./../../examples/mtp_examples/rpg_game/){ .md-button }

-   **Fantacy Trading Game**

    ---

    *A text-based trading game where non-player characters are handled using large language models. Tool calling is used for game mechanics such as bargaining at shops.*

    [Start](./../../examples/mtp_examples/fantasy_trading_game/){ .md-button }

-   **AI-Powered Multimodal MCP Chatbot**

    ---

    *This Tutorial shows how to implement an agentic AI application using the byLLM package and object-spatial programming. MCP integration is also demonstrated here.*

    [Start](./../../examples/rag_chatbot/Overview/){ .md-button }

## Examples

This section collects the example byllm programs bundled in `jac-byllm/examples/`. Examples are grouped by type. For each example the source is shown in a tab so you can quickly inspect the code.

### Core Examples
Small, focused examples that show common byLLM patterns for integrating LLMs in Jac programs.

Repository location: [jac-byllm/examples/core_examples](https://github.com/Jaseci-Labs/jaseci/tree/main/jac-byllm/examples/core_examples)

??? note "Core examples (code)"

    === "personality_finder.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/core_examples/personality_finder.jac"
        ```

    === "level_genarator.jac"
        ```jac linenums="1"
        --8<-- "jac-byllm/examples/core_examples/level_genarator.jac"
        ```


## From: python_integration.md

The byLLM module is a Jaclang plugin that provides AI functionality. Since Jaclang supersets Python, byLLM can be integrated into Python applications. This guide demonstrates how to use byLLM in Python.

byLLM is a Python package that needs to be installed using:

```bash
pip install byllm
```

There are two modes of using byLLM in python.

1. [Import byLLM library into Python.](python_integration.md#1-importing-byllm-in-python)
2. [Write AI feature in Jac with byLLM plugin, and import the jac module into Python. (**Recomended**)](python_integration.md#2-implement-in-jac-then-import-to-python)

## 1. Importing byLLM in Python

byLLM functionality is accessed by importing the `byllm` module and using the `by` decorator on functions.

```python linenums="1"
import jaclang
from dataclasses import dataclass
from byllm.lib import Model, Image, by

llm = Model(model_name="gpt-4o")

@dataclass
class Person:
    full_name: str
    description: str
    year_of_birth: int


@by(llm)
def get_person_info(img: Image) -> Person: ...

img = Image("https://bricknellschool.co.uk/wp-content/uploads/2024/10/einstein3.webp")

person = get_person_info(img)
print(f"Name: {person.full_name}, Description: {person.description}, Year of Birth: {person.year_of_birth}")
```

### Model Hyper-parameters

In Jaclang, hyper-parameters are set by passing them to the LLM model:

```jac linenums="1"
import from byllm.lib { Model }

glob llm = Model(model_name="gpt-4o")

def generate_joke() -> str by llm(temperature=0.3);
```

The `temperature` hyper-parameter controls the randomness of the output. Lower values produce more deterministic output, while higher values produce more random output.

In Python, hyper-parameters are passed as follows:

```python linenums="1"
import jaclang
from byllm.lib import Model, by

llm = Model(model_name="gpt-4o")

@by(llm(temperature=0.3))
def generate_joke() -> str: ...
```

### Using Python Functions as Tools

Python functions can be used as tools in byLLM. Functions defined in Python are callable by the LLM to perform specific tasks:

```python linenums="1"
import jaclang
from byllm.lib import Model
llm = Model(model_name="gpt-4o")


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

@by(llm(tools=[get_weather]))
def answer_question(question: str) -> str: ...
```

### Using Semstrings for Semantic Enrichment

In Jac we introduced the `sem` keyword as a means to attach additional semantics to code objects such as object attributes and function argument. The syntax in jac is as follows.

```jac
obj Person {
    has name:str;
    has age:int;
    has ssn: int;
}
sem Person.ssn = "last four digits of the Social Security number"
```

Using `sem` functionality in python is a bit diferent as the attachment is done using a `@sem` decorator.

```python
from jaclang import JacRuntimeInterface as Jac
from byllm.lib import Model, by

@Jac.sem('<Person Semstring>', {
    'name' : '<name semstring>',
    'age' : '<age semstring>',
    'ssn' : "<ssn semstring>"
    }
)
@datclass
class Person:
    name: str
    age: int
    ssn: int
```

The `sem` implementation in Python is a work-in-progress. The Python way of adding semstrings may change in future releases of byLLM.

## 2. Implement in Jac, then import to Python

It is recomended to implement the AI features purely in jaclang and just import the module into python, seamlessly. This feature is allowed through jaclang's mechanism for [supersetting python](../../learn/superset_python.md#seamless-interoperability-import-jac-files-like-python-modules).

=== "main.py"
    ```python linenums="1"
    import jaclang
    from .ai import Image, Person, get_person_info

    img = Image("https://bricknellschool.co.uk/wp-content/uploads/2024/10/einstein3.webp")

    person = get_person_info(img)
    print(f"Name: {person.full_name}, Description: {person.description}, Year of Birth: {person.year_of_birth}")
    ```
=== "ai.jac"
    ```jac linenums="1"
    import from byllm.lib {Model, Image}

    glob llm = Model(model_name="gpt-4o");

    obj Person{
        has full_name: str;
        has description: str;
        has year_of_birth: int;
    }

    sem Person.description = "Short biography"

    def get_person_info(img: Image) -> Person by llm();
    ```


## From: quickstart.md

## AI-Integrated Function Example

Let's consider an example program where we attempt to categorize a person by their personality using an LLM. For simplicity we will be using names of historical figures.

**Limitations**: Defining an algorithm in code for this problem is difficult, while integrating an LLM to perform the task would require manual prompt engineering, response parsing, and type conversion to be implemented by the developer.

### byLLM Implementation

The `by` keyword abstraction enables functions to process inputs of any type and generate contextually appropriate outputs of the specified type:

#### Step 1: Configure LLM Model

```jac linenums="1"
import from byllm.lib {Model}

glob llm = Model(model_name="gemini/gemini-2.0-flash");
```

#### Step 2: Implement LLM-Integrated Function

Add `by llm` to enable LLM integration:

```jac linenums="1"
def get_personality(name: str) -> Personality by llm();
```

This will auto-generate a prompt for performing the task and provide an output that strictly adheres to the type `Personality`.

#### Step 3: Execute the Application

Set your API key and run:

```bash
export GEMINI_API_KEY="your-api-key-here"
jac run personality.jac
```

For complete usage methodologies of the `by` abstraction, refer to the [Usage Guide](./usage.md) for documentation on object methods, object instantiation, and multi-agent workflows.


### byLLM Usage in Python

As byLLM is a python package, it can be natively used in jac. The following code show the above example application built in native python with byLLM.

```python linenums="1"
import jaclang
from byllm.lib import Model, by
from enum import Enum

llm = Model(model_name="gemini/gemini-2.0-flash")

class Personality(Enum):
    INTROVERT
    EXTROVERT
    AMBIVERT

@by(model=llm)
def get_personality(name: str) -> Personality: ...

name = "Albert Einstein"
result = get_personality(name)
print(f"{result} personality detected for {name}")
```

To learn more about usage of `by` in python, please refer to [byLLM python Interface](./python_integration.md).


## From: llmdocs.md

### Mini (Recommended)
- AI integration with byLLM
- Explore [AI Integration with byLLM](byllm.md) for building AI-powered applications


## From: create_own_lm.md

# Creating a Custom Model Class

This guide shows how to create a custom Model class for byLLM that bypasses the default LiteLLM integration. This is useful when you want to use a self-hosted language model, a custom API, or any service not supported by LiteLLM. The example demonstrates this by implementing a custom class using the OpenAI SDK.

> **IMPORTANT**
>
> This assumes that you have a proper understanding on how to inference with your language model. If you are not sure about this, please refer to the documentation of your language model.

## Steps

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

Thats it! You have successfully created your own Language Model to be used with byLLM.

>  **NOTICE**
>
> This feature is under development and if you face an incompatibility, please open an issue [here](https://github.com/Jaseci-Labs/Jaseci/issues).


## From: with_llm.md

byLLM is an innovative AI integration framework built for the Jaseci ecosystem, implementing the cutting-edge Meaning Typed Programming (MTP) paradigm. MTP revolutionizes AI integration by embedding prompt engineering directly into code semantics, making AI interactions more natural and maintainable. While primarily designed to complement the Jac programming language, byLLM also provides a powerful Python library interface.

### Basic Example

Consider building an application that translates english to other languages using an LLM. This can be simply built as follows:
=== "Jac"
    ```jac linenums="1"
    import from byllm.lib { Model }

    glob llm = Model(model_name="gpt-4o");

    def translate_to(language: str, phrase: str) -> str by llm();

    with entry {
        output = translate_to(language="Welsh", phrase="Hello world");
        print(output);
    }
    ```
=== "python"
    ```python linenums="1"
    from byllm.lib import Model, by

    llm = Model(model_name="gpt-4o")

    @by(llm)
    def translate_to(language: str, phrase: str) -> str: ...

    output = translate_to(language="Welsh", phrase="Hello world")
    print(output)
    ```

This simple piece of code replaces traditional prompt engineering without introducing additional complexity.

### Power of Types with LLMs

Consider a program that detects the personality type of a historical figure from their name. This can eb built in a way that LLM picks from an enum and the output strictly adhere this type.

=== "Jac"
    ```jac linenums="1"
    import from byllm.lib { Model }
    glob llm = Model(model_name="gemini/gemini-2.0-flash");

    enum Personality {
        INTROVERT,
        EXTROVERT,
        AMBIVERT
    }

    def get_personality(name: str) -> Personality by llm();

    with entry {
        name = "Albert Einstein";
        result = get_personality(name);
        print(f"{result} personality detected for {name}");
    }
    ```
=== "Python"
    ```python linenums="1"
    from byllm.lib import Model, by
    from enum import Enum
    llm =  Model(model_name="gemini/gemini-2.0-flash")

    class Personality(Enum):
        INTROVERT
        EXTROVERT
        AMBIVERT

    @by(model=llm)
    def get_personality(name: str) -> Personality: ...

    name = "Albert Einstein"
    result = get_personality(name)
    print(f"{result} personality detected for {name}")
    ```

Similarly, custom types can be used as output types which force the LLM to adhere to the specified type and produce a valid result.

### Control! Control! Control!

Even if we are elimination prompt engineering entirely, we allow specific ways to enrich code semantics through **docstrings** and **semstrings**.

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

byLLM integrates with various LLM providers (OpenAI, Anthropic, Google, etc.) through [LiteLLM](https://litellm.ai/).


## From: Overview.md

# Build an AI-Powered Multimodal MCP Chatbot

This step-by-step guide will walk you through building a modern chatbot that can chat with your documents, images, and videos. By the end, you'll have a working multimodal AI assistant and understand how to use Jac's unique programming features to build intelligent applications.

## What You'll Build

You'll create a chatbot that can:

- Upload and chat with PDFs, text files, images, and videos
- Search your documents and provide context-aware answers
- Answer general questions using web search
- Understand and discuss images and videos using AI vision
- Route different types of questions to specialized AI handlers

## What You'll Learn

- **Mean Typed Programming (MTP)**: Let AI classify and route user queries automatically with just simple definitions
- **Model Context Protocol (MCP)**: Build modular, reusable AI tools
- **Multimodal AI**: Work with text, images, and videos in one application

## Technologies We'll Use

- **OpenAI GPT**: AI chat and vision capabilities
- **Serper API**: Real-time web search

## Step 1: Set Up Your Environment

Next, get your API keys. You'll need an OpenAI API key for the AI features. For web search, get a free API key from [Serper](https://serper.dev/).

Set your environment variables:

```bash
export OPENAI_API_KEY=<your-openai-key>
export SERPER_API_KEY=<your-serper-key>
```

## Step 2: Understanding the Architecture

**Mean Typed Programming (MTP)** lets AI automatically classify and route requests, making your application intelligent without complex rule-based logic.

The application consists of:

- **Document Processing Engine** (`tools.jac`): Processes and searches documents using vector embeddings
- **Tool Server** (`mcp_server.jac`): Exposes document and web search as MCP tools
- **Tool Client** (`mcp_client.jac`): Interfaces with the tool server
- **Main Application** (`server.jac` + `server.impl.jac`): Routes queries and manages conversations

## Step 4: Test Your Chatbot

The system will automatically route your questions:

- Document questions go to the RAG system
- General questions use web search
- Image questions use vision AI
- Video questions analyze video content

## What You've Accomplished

Congratulations! You've built a sophisticated AI application that demonstrates several advanced concepts:

- **Multimodal AI capabilities** that work with text, images, and videos
- **Intelligent routing** using AI-based classification
- **Modular architecture** with reusable tools via MCP
- **Real-time web search integration**
- **Efficient document search** with vector embeddings

## Extending Your Chatbot

Your chatbot is designed to be extensible. You could add:

- **Additional tools**: Weather APIs, database connections, or custom business logic
- **Enhanced AI models**: Different LLMs for specialized tasks
- **Advanced search**: Hybrid search combining keyword and semantic search

## Troubleshooting

- **API keys**: Verify your OpenAI and Serper API keys are set correctly

You now have the foundation to build sophisticated AI applications using Jac's unique programming paradigms. The combination of Object Spatial Programming, Mean Typed Programming, and modular tool architecture gives you a solid base for creating intelligent, scalable applications.


## From: aider-genius-lite.md

Aider Genius Lite is a simple Jac-based Streamlit application for AI-powered code generation with task planning and validation. It provides a clean, intuitive interface for generating code from natural language requests with real-time feedback and validation.

- AI feedback and validation results
- Separate Jac Streamlit frontend and backend

- `genius_lite.jac` - Backend with AI logic, task processing, and API endpoints

*Aider Genius Lite demonstrates the power of agentic AI for code generation, showcasing how intelligent systems can understand, plan, and execute complex programming tasks autonomously.*


## From: usage.md

# AI-Integrated Programming with byLLM

This guide covers different ways to use byLLM for AI-integrated software development in Jaclang. byLLM provides language-level abstractions for integrating Large Language Models into applications, from basic AI-powered functions to complex multi-agent systems. For agentic behavior capabilities, byLLM includes the ReAct method with tool integration.

## Supported Models

byLLM uses [LiteLLM](https://docs.litellm.ai/docs) to provide integration with a wide range of models.

=== "OpenAI"
    ```jac linenums="1"
    import from byllm.lib {Model}

    glob llm = Model(model_name = "gpt-4o")
    ```
=== "Gemini"
    ```jac linenums="1"
    import


## From: creating_byllm_plugins.md

# Creating byLLM Plugins

This document describes how to create plugins for byLLM (Multi-Modal Large Language Model), which is a plugin system for Jaclang's `by llm()` feature.

## Understanding the Plugin System

byLLM uses a plugin architecture based on [Pluggy](https://pluggy.readthedocs.io/), the same plugin system used by pytest. Plugins allow you to extend or modify how byLLM handles LLM calls in Jaclang programs.

### How Plugins Work

When Jaclang's `by llm()` syntax is used, the runtime system looks for registered plugins that implement the `call_llm` hook. This enables:

- Implement custom LLM providers
- Add preprocessing/postprocessing logic
- Implement caching mechanisms
- Add logging or monitoring
- Create mock implementations for testing

## Plugin Architecture Overview

The plugin system consists of three main components:

1. **Hook Specifications**: Define the interface that plugins must implement
2. **Hook Implementations**: Your plugin code that implements the hooks
3. **Plugin Registration**: How plugins are discovered and loaded

## Creating Your First Plugin

### Step 1: Set Up Your Plugin Package

Create a Python package for the plugin:

```
my-byllm-plugin/
├── pyproject.toml
├── README.md
└── my_byllm_plugin/
    ├── __init__.py
    └── plugin.py
```

### Step 2: Define Your Plugin Class

Create the plugin implementation in `my_byllm_plugin/plugin.py`:

```python
"""Custom byLLM Plugin."""

from typing import Callable

from jaclang.runtimelib.runtime import hookimpl
from byllm.llm import Model


class MybyllmRuntime:
    """Custom byLLM Plugin Implementation."""

    @staticmethod
    @hookimpl
    def call_llm(
        model: Model, caller: Callable, args: dict[str | int, object]
    ) -> object:
        """Custom LLM call implementation."""
        # Custom logic implementation
        print(f"Custom plugin intercepted call to: {caller.__name__}")
        print(f"Arguments: {args}")

        # Option 1: Modify the call and delegate to the original model
        result = model.invoke(caller, args)

        # Option 2: Implement completely custom logic
        # result = your_custom_llm_logic(caller, args)

        print(f"Result: {result}")
        return result
```

### Step 3: Configure Package Registration

Register the plugin using entry points in `pyproject.toml`:

```toml
[tool.poetry]
name = "my-byllm-plugin"
version = "0.1.0"
description = "My custom byLLM plugin"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
byllm = "*"
jaclang = "*"

[tool.poetry.plugins."jac"]
my-byllm-plugin = "my_byllm_plugin.plugin:MybyllmRuntime"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Step 4: Install and Test Your Plugin

1. Install the plugin in development mode:
   ```bash
   pip install -e .
   ```

2. Create a test Jaclang file to verify plugin functionality:
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

3. Run the test:
   ```bash
   jac run test.jac
   ```

## Advanced Plugin Examples

### Example 1: Caching Plugin

```python
"""Caching byLLM Plugin."""

import hashlib
import json
from typing import Callable, Any

from jaclang.runtimelib.runtime import hookimpl
from byllm.llm import Model


class CachingbyllmRuntime:
    """Plugin that caches LLM responses."""

    _cache: dict[str, Any] = {}

    @staticmethod
    @hookimpl
    def call_llm(
        model: Model, caller: Callable, args: dict[str | int, object]
    ) -> object:
        """Cache LLM responses."""
        # Create cache key from function and arguments
        cache_key = hashlib.md5(
            json.dumps({
                "function": caller.__name__,
                "args": str(args),
                "model": model.model_name
            }, sort_keys=True).encode()
        ).hexdigest()

        # Check cache first
        if cache_key in CachingbyllmRuntime._cache:
            print(f"Cache hit for {caller.__name__}")
            return CachingbyllmRuntime._cache[cache_key]

        # Call original implementation
        result = model.invoke(caller, args)

        # Store in cache
        CachingbyllmRuntime._cache[cache_key] = result
        print(f"Cached result for {caller.__name__}")

        return result
```

### Example 2: Logging Plugin

```python
"""Logging byLLM Plugin."""

import time
from typing import Callable

from jaclang.runtimelib.runtime import hookimpl
from byllm.llm import Model


class LoggingbyllmRuntime:
    """Plugin that logs all LLM calls."""

    @staticmethod
    @hookimpl
    def call_llm(
        model: Model, caller: Callable, args: dict[str | int, object]
    ) -> object:
        """Log LLM calls with timing information."""
        start_time = time.time()

        print(f"[LLM CALL] Starting: {caller.__name__}")
        print(f"[LLM CALL] Model: {model.model_name}")
        print(f"[LLM CALL] Args: {args}")

        try:
            result = model.invoke(caller, args)
            duration = time.time() - start_time

            print(f"[LLM CALL] Completed: {caller.__name__} in {duration:.2f}s")
            print(f"[LLM CALL] Result: {result}")

            return result

        except Exception as e:
            duration = time.time() - start_time
            print(f"[LLM CALL] Failed: {caller.__name__} after {duration:.2f}s")
            print(f"[LLM CALL] Error: {e}")
            raise
```

### Example 3: Custom Model Provider

```python
"""Custom Model Provider Plugin."""

from typing import Callable

from jaclang.runtimelib.runtime import hookimpl
from byllm.llm import Model


class CustomProviderRuntime:
    """Plugin that implements a custom model provider."""

    @staticmethod
    @hookimpl
    def call_llm(
        model: Model, caller: Callable, args: dict[str | int, object]
    ) -> object:
        """Handle custom model providers."""

        # Check if this is a custom model
        if model.model_name.startswith("custom://"):
            return CustomProviderRuntime._handle_custom_model(
                model, caller, args
            )

        # Delegate to default implementation
        return model.invoke(caller, args)

    @staticmethod
    def _handle_custom_model(
        model: Model, caller: Callable, args: dict[str | int, object]
    ) -> object:
        """Implement custom model logic."""
        model_type = model.model_name.replace("custom://", "")

        if model_type == "echo":
            # Simple echo model for testing
            return f"Echo: {list(args.values())[0]}"
        elif model_type == "random":
            # Random response model
            import random
            responses = ["Yes", "No", "Maybe", "I don't know"]
            return random.choice(responses)
        else:
            raise ValueError(f"Unknown custom model: {model_type}")
```

## Plugin Hook Reference

### call_llm Hook

The primary hook that all byLLM plugins implement:

```python
@hookimpl
def call_llm(
    model: Model,
    caller: Callable,
    args: dict[str | int, object]
) -> object:
    """
    Called when Jaclang executes a 'by llm()' statement.

    Args:
        model: The Model instance with configuration
        caller: The function being called with LLM
        args: Arguments passed to the function

    Returns:
        The result that should be returned to the Jaclang program
    """
```

## Best Practices

### 1. Handle Errors Gracefully

```python
@hookimpl
def call_llm(model: Model, caller: Callable, args: dict[str | int, object]) -> object:
    try:
        return model.invoke(caller, args)
    except Exception as e:
        # Log error and provide fallback
        print(f"LLM call failed: {e}")
        return "Error: Unable to process request"
```

### 2. Preserve Original Functionality

Unless you're completely replacing the LLM functionality, always delegate to the original implementation:

```python
@hookimpl
def call_llm(model: Model, caller: Callable, args: dict[str | int, object]) -> object:
    # Your pre-processing logic
    result = model.invoke(caller, args)  # Delegate to original
    # Your post-processing logic
    return result
```

### Use Configuration

Configure plugin behavior:

```python
class ConfigurableRuntime:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        # Load from environment, file, etc.
        return {"enabled": True, "log_level": "INFO"}

    @hookimpl
    def call_llm(self, model: Model, caller: Callable, args: dict[str | int, object]) -> object:
        if not self.config["enabled"]:
            return model.invoke(caller, args)

        # Plugin logic implementation
```

### 4. Testing Your Plugin

Create comprehensive tests:

```python
import pytest
from byllm.llm import Model
from my_byllm_plugin.plugin import MybyllmRuntime

def test_plugin():
    runtime = MybyllmRuntime()
    model = Model("mockllm", outputs=["test response"])

    def test_function(x: str) -> str:
        """Test function."""
        pass

    result = runtime.call_llm(model, test_function, {"x": "test input"})
    assert result == "test response"
```

## Plugin Discovery and Loading

Plugins are automatically discovered and loaded when:

1. They're installed as Python packages
2. They register the `"jac"` entry point in their `pyproject.toml`
3. Jaclang is imported or run

The discovery happens in `jaclang/__init__.py`:

```python
plugin_manager.load_setuptools_entrypoints("jac")
```

## Debugging Plugins

### Enable Debug Logging

Set environment variables to see plugin loading:

```bash
export JAC_DEBUG=1
jac run your_script.jac
```

### Verify Plugin Registration

Check if the plugin is loaded:

```python
from jaclang.runtimelib.runtime import plugin_manager

# List all registered plugins
for plugin in plugin_manager.get_plugins():
    print(f"Loaded plugin: {plugin}")
```

## Common Pitfalls

1. **Not using `@hookimpl` decorator**: Methods won't be recognized as hook implementations
2. **Incorrect entry point name**: Must be `"jac"` for discovery
3. **Wrong hook signature**: Must match exactly: `call_llm(model, caller, args)`
4. **Forgetting to delegate**: If `model.invoke()` is not called, original functionality is lost

## Conclusion

byLLM plugins extend Jaclang's LLM capabilities through a clean, extensible plugin system. Plugins can add caching, logging, custom providers, and other functionality to enhance the LLM experience.

Key considerations:
- Follow the hook specification exactly
- Test thoroughly with different scenarios
- Document plugin functionality
- Consider backward compatibility
- Handle errors gracefully

For more examples and advanced use cases, see the [official byLLM plugin](https://github.com/Jaseci-Labs/jaclang/tree/main/jac-byllm) implementation.


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

- OpenAI API key (for GPT-4)

The system uses GPT-4 by default. You can modify the model in `task_manager.jac`:

```jac
glob llm = Model(model_name="gpt-4o");
```

### Task Extraction Algorithm

Natural language processing extracts structured task information:

### Email Template System

Dynamic email generation based on context and purpose:

### Smart Scheduling
- **Conflict Detection**: Identifies scheduling conflicts automatically
- **Optimal Time Suggestions**: Proposes best meeting times based on availability
- **Calendar Integration**: Syncs with external calendar systems
- **Timezone Handling**: Manages tasks across different time zones

### Task Dependencies
- **Prerequisite Tracking**: Manages task dependencies and ordering
- **Automatic Prioritization**: Adjusts task priorities based on dependencies
- **Progress Monitoring**: Tracks completion of dependent tasks
- **Bottleneck Identification**: Highlights tasks blocking project progress

### Email Context Integration
- **Task-Aware Emails**: Incorporates relevant task information in emails
- **Meeting Summaries**: Generates emails with meeting outcomes and action items
- **Status Updates**: Creates progress reports based on task completion
- **Reminder Emails**: Automated follow-ups for upcoming deadlines

### Learning and Adaptation
- **User Pattern Recognition**: Learns from user preferences and habits
- **Improved Routing**: Enhances intent classification over time
- **Personalized Responses**: Adapts communication style to user preferences
- **Context Memory**: Maintains long-term conversation context


## From: fantasy_trading_game.md

This tutorial demonstrates how to build AI agents with persistent state that can conduct conversations, execute trades, and maintain context across interactions. The tutorial covers integrating AI functions for character generation and dialogue systems.

This tutorial covers building a trading game system with:
- AI-powered character generation functions
- AI agents that maintain conversation state
- Persistent conversation history
- Context-aware decision making

## Step 2: Configure the AI Model

Configure the LLM for AI operations:

```jac
import from byllm.lib {Model}

glob llm = Model(model_name="gpt-4o");
```

## Step 3: Implement AI-Powered Character Generation

Create AI-integrated functions that generate game characters:

```jac
def make_player() -> Person by llm();

def make_random_npc() -> Person by llm();
```

These AI functions generate characters with appropriate attributes, starting money, and themed inventory items.

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
1. Uses AI functions to generate characters (stateless)
2. Registers characters for transaction system
3. Uses the AI agent for NPC responses (stateful - maintains conversation history)
4. Accumulates conversation history for persistent context
5. Displays current game state after each interaction

## AI Functions vs AI Agents

### AI Functions (Stateless)

AI-integrated functions that operate without persistent state:
- `make_player()` and `make_random_npc()` - Generate characters but don't retain memory
- These are AI-powered utilities, not agents

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


## From: rpg_game.md

In this tutorial, we’ll build a dynamic RPG level generator using LLMs and Jaclang’s `by llm` syntax. The tutorial covers creating a system that uses AI to generate balanced, progressively challenging game levels.

The system creates game levels automatically through structured data types for spatial positioning and game elements, progressive difficulty scaling that adapts to player progress, and

