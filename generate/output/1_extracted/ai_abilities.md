# ai_abilities


## From: byllm.md

- **Streaming with ReAct Tool Calling**: Implemented real-time streaming support for ReAct method when using tools. After tool execution completes, the LLM now streams the final synthesized answer token-by-token, providing the best of both worlds: structured tool calling with streaming responses.
- **byLLM Feature Methods as Tools**: byLLM now supports adding methods of classes as tools for the llm using such as `tools=[ToolHolder.tool]`
- **Semantic Strings**: Introduced `sem` strings to attach natural language descriptions to code elements like functions, classes, and parameters. These semantic annotations can be used by Large Language Models (LLMs) to enable intelligent, AI-powered code generation and execution. (mtllm)
- **LLM Function Overriding**: Introduced the ability to override any regular function with an LLM-powered implementation at runtime using the `function_call() by llm()` syntax. This allows for dynamic, on-the-fly replacement of function behavior with generative models. (mtllm)

