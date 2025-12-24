# decorators


## From: library_mode.md

| Decorator | Description | Usage |
|-----------|-------------|-------|
| `@on_entry` | Entry ability decorator | Executes when walker enters node/edge |
| `@on_exit` | Exit ability decorator | Executes when walker exits node/edge |
| `@sem(doc, fields)` | Semantic string decorator | AI/LLM integration metadata |
| `by(model)` | Decorator for LLM-powered functions | `@by(model) def func(): ...` |
| `sem(semstr, inner_semstr)` | Semantic metadata decorator | `@sem("doc", {"field": "desc"})` |


## From: superset_python.md

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

    # Define walker using Jac decorators
    class TaskCreator(Walker):
        def __init__(self, title: str):
            super().__init__()
            self.title = title

        @on_entry
        def create(self, here) -> None:
            """Entry point - creates task."""
            if validate_title(self.title):
                task = Task(title=self.title)
                connect(here, task)
                print(f"✓ Created: {task.title}")
                # Note: AI features require .jac syntax
            else:
                print("✗ Title too short!")

    if __name__ == "__main__":
        creator = TaskCreator(title="Build API")
        spawn(creator, root())
    ```


## From: byllm.md

- **byLLM Plugin Interface Improved**: Enhanced the byLLM plugin interface with `get_mtir` function hook interface and refactored the `by` decorator to use the plugin system, improving integration and extensibility.


## From: python_integration.md

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
In Python, hyper-parameters are passed as follows:

```python linenums="1"
import jaclang
from byllm.lib import Model, by

llm = Model(model_name="gpt-4o")

@by(llm(temperature=0.3))
def generate_joke() -> str: ...
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


## From: quickstart.md

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


## From: with_llm.md

=== "Python"
    ```python linenums="1"
    from byllm.lib import Model, by

    llm = Model(model_name="gpt-4o")

    @by(llm)
    def translate_to(language: str, phrase: str) -> str: ...

    output = translate_to(language="Welsh", phrase="Hello world")
    print(output)
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


## From: creating_byllm_plugins.md

```python
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
1. **Not using `@hookimpl` decorator**: Methods won't be recognized as hook implementations

