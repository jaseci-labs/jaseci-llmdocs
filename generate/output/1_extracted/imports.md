# imports


## From: litellm_proxy.md

```python
from byllm.lib import Model

llm = Model(
    model_name="gpt-4o",                # The model name to be used
    api_key="your_litellm_api_key",     # LiteLLM proxy server key
    proxy_url="http://localhost:8000",  # URL of the LiteLLM proxy server
)
```


## From: create_own_lm.md

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

