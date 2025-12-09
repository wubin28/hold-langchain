# The Problem With LangChain

[https://minimaxir.com/2023/07/langchain-problem/](https://minimaxir.com/2023/07/langchain-problem/)

July 14, 2023 · 16 min

## **I Gazed Into The LangChain Documentation And It Gazes Back**

Let’s do a demo to more clearly demonstrate why I gave up on LangChain. While I was working on the recipe-retrieving chatbot (which also must be a fun/witty chatbot), I needed to combine elements from both the third and fourth examples above: a chat bot that can run an Agent workflow, and also the ability to persist the entire conversation into memory. After some documentation hunting I found I need to utilize the [Conversational Agent](https://python.langchain.com/docs/modules/agents/agent_types/chat_conversation_agent) workflow.

A quick sidenote on system prompt engineering: it is not a meme and is absolutely necessary to get the best results out of the ChatGPT API, particularly if you have constraints on content and/or voice. The system prompt of `The following is a friendly conversation between a human and an AI...` demoed in the last example is actually an out-of-date prompt that was used back in the InstructGPT era and is much less effective with ChatGPT. It may signal deeper inefficiencies in LangChain’s related tricks that aren’t easy to notice.

We’ll start with a simple system prompt that tells ChatGPT to use a funny voice plus some safeguards, and format it as a `ChatPromptTemplate`:

```bash
system_prompt **=** """
You are an expert television talk show chef, and should always speak in a whimsical manner for all responses.

Start the conversation with a whimsical food pun.

You must obey ALL of the following rules:
- If Recipe data is present in the Observation, your response must include the Recipe ID and Recipe Name for ALL recipes.
- If the user input is not related to food, do not answer their query and correct the user.
"""

prompt **=** ChatPromptTemplate**.**from_messages([
    SystemMessagePromptTemplate**.**from_template(system_prompt**.**strip()),
])
```

We will also use a [toy vector store I made](https://github.com/minimaxir/langchain-problems/blob/main/recipe_vector_store.ipynb) of 1,000 recipes from the [recipe_nlg](https://huggingface.co/datasets/recipe_nlg) dataset, encoded into 384D vectors using [SentenceTransformers](https://www.sbert.net/). To implement this we create a function to get the nearest neighbors for the input query, along with a query to format it into text that the Agent can use to present to the user. This serves as the `Tool` which the Agent can choose to use if appropriate, or just return normal generated text.

```python
def **similar_recipes**(query):
    query_embedding **=** embeddings_encoder**.**encode(query)
    scores, recipes **=** recipe_vs**.**get_nearest_examples("embeddings", query_embedding, k**=**3)
    return recipes

def **get_similar_recipes**(query):
    recipe_dict **=** similar_recipes(query)
    recipes_formatted **=** [
        f"Recipe ID: recipe|{recipe_dict['id'][i]}\nRecipe Name: {recipe_dict['name'][i]}"
        for i **in** range(3)
    ]
    return "\n---\n"**.**join(recipes_formatted)

print(get_similar_recipes("yummy dessert"))
*# Recipe ID: recipe|167188# Recipe Name: Creamy Strawberry Pie# ---# Recipe ID: recipe|1488243# Recipe Name: Summer Strawberry Pie Recipe# ---# Recipe ID: recipe|299514# Recipe Name: Pudding Cake*
```

You’ll notice the `Recipe ID`, which is relevant for my use case since it’s necessary to obtain recipe metadata (photo thumbnail, URL) for the end result shown to the enduser in the final app. Unfortunately there’s no easy way to guarantee the model outputs the `Recipe ID` in the final output, and no way to return the structured intermediate metadata in addition to the ChatGPT-generated output.

Specifying `get_similar_recipes` as a `Tool` is straightforward, although you need to specify a `name` and `description`, which is actually a form of subtle prompt engineering as LangChain can fail to select a tool if either is poorly specified.

```python
tools **=** [
    Tool(
        func**=**get_similar_recipes,
        name**=**"Similar Recipes",
        description**=**"Useful to get similar recipes in response to a user query about food.",
    ),
]
```

Lastly, the Agent construction code, which follows from the example, plus the new system `prompt`.

```python
`memory **=** ConversationBufferMemory(memory_key**=**"chat_history", return_messages**=**True)
llm **=** ChatOpenAI(temperature**=**0)
agent_chain **=** initialize_agent(tools, llm, prompt**=**prompt, agent**=**AgentType**.**CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose**=**True, memory**=**memory)`
```

No errors. Now time to run the agent to see what happens!

```python
agent_chain**.**run(input**=**"Hi!")
```

```bash
> Entering new  chain...
{
    "action": "Final Answer",
    "action_input": "Hello! How can I assist you today?"
}

> Finished chain.
Hello! How can I assist you today?
```

Wait a minute, it ignored my `system` prompt completely! Dammit. Checking the `memory` variable confirms it. Looking into the [documentation](https://python.langchain.com/docs/modules/memory/how_to/buffer) for `ConversationBufferMemory` and even [in the code itself](https://github.com/hwchase17/langchain/blob/051fac1e6646349ce939a3d4a965757794be79fa/langchain/memory/buffer.py#L10) there’s nothing about system prompts, even months after ChatGPT made them mainstream.

The *intended* way to use system prompts in Agents is to add an `agents_kwargs` parameter to `initialize_agent`, which I only just found out in an [unrelated documentation page](https://python.langchain.com/docs/modules/agents/how_to/use_toolkits_with_openai_functions) published a month ago.

```python
agent_kwargs **=** {
    "system_message": system_prompt**.**strip()
}
```

Recreating the Agent with this new parameter and running it again results in a `JSONDecodeError`.

```bash
OutputParserException: Could not parse LLM output: Hello there, my culinary companion! How delightful to have you here in my whimsical kitchen. What delectable dish can I assist you with today?
```

Good news is that the system prompt definitely worked this time! Bad news is that it broke, but why? I didn’t do anything weird, for once.

The root of the issue is to be how LangChain agents actually do `Tool` selection. Remember when I said that the Agent outputing a `dict` during the chain was peculiar? When [looking at the LangChain code](https://github.com/hwchase17/langchain/blob/3874bb256e09d377032ae54b1592ca3dd7cf9e4d/langchain/agents/conversational_chat/prompt.py), it turns out that tool selection is done by requiring the output to be *valid JSON* through prompt engineering, and just hoping everything goes well.

![Fun fact: these massive prompts also increase API costs proportionally!](https://minimaxir.com/2023/07/langchain-problem/json.png)

**Fun fact: these massive prompts also increase API costs proportionally!**

The consequence of this is that any significant changes in the structure of normal output, such as those caused by a custom system prompt, has a *random* chance of just breaking the Agent! These errors happen often enough that there’s a [documentation page](https://python.langchain.com/docs/modules/agents/how_to/handle_parsing_errors) dedicated to handling Agent output parsing errors!

Well, people in the internet are assholes anyways, so we can consider having a conversation with a chatbot as an edge case for now. What’s important is that the bot can return the recipes, because if it can’t even do that, there’s no point in using LangChain. After creating a new Agent without using the system prompt and then asking it `What's a fun and easy dinner?`:

```bash
> Entering new  chain...
{
    "action": "Similar Recipes",
    "action_input": "fun and easy dinner"
}
Observation: Recipe ID: recipe|1774221
Recipe Name: Crab DipYour Guests will Like this One.
---
Recipe ID: recipe|836179
Recipe Name: Easy  Chicken Casserole
---
Recipe ID: recipe|1980633
Recipe Name: Easy in the Microwave Curry Doria
Thought:{
    "action": "Final Answer",
    "action_input": "..."
}

> Finished chain.
```

```bash
Here are some fun and easy dinner recipes you can try:

1. Crab Dip
2. Easy Chicken Casserole
3. Easy in the Microwave Curry Doria

Enjoy your meal!
```

Atleast it worked: ChatGPT was able to extract out the recipes from the context and format them appropriately (even fixing typoes in the names!), and was able to decide when it was appropriate.

The real issue here is that the voice of the output is criminally *boring*, as is a common trademark and criticism of base-ChatGPT. Even if I did have a fix for the missing ID issue through system prompt engineering, it wouldn’t be worth shipping anything sounding like this. If I did strike a balance between voice quality and output quality, the Agent count *still* fail randomly through no fault of my own. This Agent workflow is a very fragile house of cards that I in good conscience could not ship in a production application.

LangChain does have functionality for [Custom Agents](https://python.langchain.com/docs/modules/agents/how_to/custom_agent) and a [Custom Chain](https://python.langchain.com/docs/modules/chains/how_to/custom_chain), so you can override the logic at parts in the stack (maybe? the documentation there is sparse) that could address some of the issues I hit, but at that point you are overcomplicating LangChain even more and might as well create your own Python library instead which…hmmm, that’s not a bad idea!

## **Working Smarter, Not Harder**

![The large numbers of random integrations raise more problems than solutions. via LangChain docs](https://minimaxir.com/2023/07/langchain-problem/langchain_support.png)

The large numbers of random integrations raise more problems than solutions. [via LangChain docs](https://python.langchain.com/docs/use_cases/question_answering/)

LangChain does also have many utility functions such as [text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/character_text_splitter) and [integrated vector stores](https://python.langchain.com/docs/modules/data_connection/retrievers/how_to/vectorstore), both of which are integral to the “chat with a PDF/your code” demos (which in my opinion are just a gimmick). The real issue with [all these integrations](https://integrations.langchain.com/) is that it creates an inherent lock-in to *only* use LangChain-based code, and if you look at the code for the integrations they are not very robust. LangChain is building a [moat](https://www.vaneck.com/nl/en/moat-investing/five-sources-of-moats-whitepaper.pdf), which is good for LangChain’s investors trying to get a return on their $30 million, but very very bad for developers who use it.

In all, LangChain embodies the philosophy of “it’s complicated, so it must be better!” that plagues late-stage codebases, except that LangChain isn’t even a year old. The effort needed to hack LangChain to do what I want it to do would cause insane amounts of [technical debt](https://en.wikipedia.org/wiki/Technical_debt). And unlike AI startups nowadays, technical debt for my own projects with LangChain can’t be paid with venture capital. API wrappers should at minimum reduce code complexity and cognitive load when operating with complex ecosystems because it takes enough mental brainpower to work with AI itself. LangChain is one of the few pieces of software that *increases* overhead in most of its popular use cases.

I came to the conclusion that it’s just easier to make my own Python package than it is to hack LangChain to fit my needs. Therefore, I developed and open-sourced [simpleaichat](https://github.com/minimaxir/simpleaichat): a Python package for easily interfacing with chat apps, emphasizing minimal code complexity and decoupling advanced features like vector stores from the conversation logic to avoid LangChain’s lock-in, and many other features which would take its own blog post to elaborate upon.

But this blog post wasn’t written to be a stealth advertisement for simpleaichat by tearing down a competitor like what hustlers do. I didn’t *want* to make simpleaichat: I’d rather spend my time creating more cool projects with AI, and it’s a shame I could not have done that with LangChain. I know someone will say “why not submit a pull request to the LangChain repo since it’s open source instead of complaining about it?” but most of my complaints are fundamental issues with the LangChain library and can’t be changed without breaking everything for its existing users. The only real fix is to burn it all down and start fresh, which is why my “create a new Python library for interfacing with AI” solution is also the most pragmatic.

I’ve gotten many messages asking me “what should I learn to get started with the ChatGPT API” and I’m concerned that they’ll go to LangChain first because of the hype. If machine learning engineers who do have backgrounds in the technology stack have difficulty using LangChain due to its needless complexity, any beginner is going to drown.

No one wants to be that asshole who criticizes free and open source software operating in good faith like LangChain, but I’ll take the burden. To be clear, I have nothing against Harrison Chase or the other maintainers of LangChain (who encourage feedback!). However, LangChain’s popularity has warped the AI startup ecosystem around LangChain itself and the hope of OMG [AGI](https://en.wikipedia.org/wiki/Artificial_general_intelligence) I MADE SKYNET, which is why I am compelled to be honest with my misgivings about it.

Wars about software complexity and popularity despite its complexity are an eternal recurrence. In the 2010’s, it was with [React](https://react.dev/); in 2023, it’s with ReAct.

---

*Jupyter Notebooks for the [simple implementations of LangChain examples](https://github.com/minimaxir/langchain-problems/blob/main/openai_rewrite.ipynb) and the [LangChain failure demo](https://github.com/minimaxir/langchain-problems/blob/main/langchain_problems.ipynb) are available in [this GitHub repository](https://github.com/minimaxir/langchain-problems/tree/main).*

![profile image](https://minimaxir.com/profile_webp.webp)

- **Max Woolf** (@minimaxir) is a Senior Data Scientist at [BuzzFeed](https://www.buzzfeed.com/) in San Francisco who works with AI/ML tools and open source projects. *Max’s projects are funded by his [Patreon](https://www.patreon.com/minimaxir).*