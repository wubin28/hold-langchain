# Bug Fix: ReAct Agent Prompt Missing Required Variables

## Problem
When running the example scripts, they failed with the following error:
```
ValueError: Prompt missing required variables: {'tool_names', 'tools'}
```

## Root Cause
The `create_react_agent()` function in LangChain requires the prompt template to include specific variables:
- `{tools}` - Description of available tools
- `{tool_names}` - Names of the tools
- `{input}` - User input
- `{agent_scratchpad}` - Agent's thinking process

The original prompt templates only included `input` and `agent_scratchpad`, but were missing `tools` and `tool_names`.

## Solution
Updated the prompt templates to include the ReAct format instructions with the required variables. The system message now includes:

```python
system_prompt + "\n\nYou have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question"
```

## Files Modified
1. `example1_system_prompt_fixed.py` - Fixed prompt template
2. `example2_json_parsing_robust.py` - Fixed prompt template
3. `example3_structured_output.py` - Fixed prompt template
4. `analysis-and-langchain-v1-examples.md` - Updated documentation to match fixes

## Files NOT Modified
- `example4_function_calling.py` - Uses `create_openai_functions_agent()` which doesn't require these variables
- `example5_complete_recipe_bot.py` - Uses `create_openai_functions_agent()` which doesn't require these variables

## Verification
The fix has been verified - the prompt now contains all required variables:
- ✅ `tools`
- ✅ `tool_names`
- ✅ `input`
- ✅ `agent_scratchpad`
- ✅ `chat_history` (optional)

The examples should now run correctly (assuming the DEEPSEEK_API_KEY environment variable is set).
