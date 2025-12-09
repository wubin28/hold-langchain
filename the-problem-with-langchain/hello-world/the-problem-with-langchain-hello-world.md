# The Problem With LangChain

[https://minimaxir.com/2023/07/langchain-problem/](https://minimaxir.com/2023/07/langchain-problem/)

July 14, 2023 · 16 min

![_The GitHub Repository of R'lyeh_, Stable Diffusion 1.5 + ControlNet 1.1](https://minimaxir.com/2023/07/langchain-problem/featured.png)

*The GitHub Repository of R’lyeh*, Stable Diffusion 1.5 + ControlNet 1.1

If you’ve been following the explosion of AI hype in the past few months, you’ve probably heard of [LangChain](https://github.com/hwchase17/langchain). LangChain, developed by Harrison Chase, is a Python and JavaScript library for interfacing with [OpenAI](https://openai.com/)’s GPT APIs (later expanding to more models) for AI text generation. More specifically, it’s an implementation of the paper [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) published October 2022, colloquially known as the ReAct paper, which demonstrates a prompting technique to allow the model to “reason” (with a chain-of-thoughts) and “act” (by being able to use a tool from a predefined set of tools, such as being able to search the internet). This combination is shown to drastically improve output text quality and give large language models the ability to correctly solve problems.

![Example ReAct flow from the ReAct paper](https://minimaxir.com/2023/07/langchain-problem/react.png)

Example ReAct flow from the ReAct paper

The ReAct workflow popularied by LangChain was particularly effective with [InstructGPT](https://openai.com/research/instruction-following)/text-davinci-003, although costly and not easy to use for small projects. In March 2023, as [ChatGPT](https://openai.com/blog/chatgpt) API usage became massively popular due to its extremely cheap API [as I accurately predicted](https://minimaxir.com/2023/03/new-chatgpt-overlord/), LangChain use also exploded, to the point that LangChain was able to raise a [$10 million seed round](https://blog.langchain.dev/announcing-our-10m-seed-round-led-by-benchmark/) and another [$20-$25 million at a $200 million valuation Series A](https://www.businessinsider.com/sequoia-leads-funding-round-generative-artificial-intelligence-startup-langchain-2023-4) despite not having any revenue nor any obvious plans how to generate revenue.

That’s where my personal experience with LangChain begins. For my work at [BuzzFeed](https://www.buzzfeed.com/), I was tasked with creating a ChatGPT-based chat bot for the [Tasty](https://tasty.co/) brand (later released as [Botatouille](https://www.buzzfeed.com/buzzfeedpress/buzzfeeds-tasty-introduces-botatouille-the-first-of-its) in the Tasty iOS app) that could chat with the user and provide relevant recipes. The source recipes are converted to embeddings and saved in a vector store: for example, if a user asked for “healthy food”, the query is converted to an embedding, and an approximate nearest neighbor search is performed to find recipes similar to the embedded query and then fed to ChatGPT as added context that can then be displayed to the user. This approach is more commonly known as [retrieval-augmented generation](https://arxiv.org/abs/2005.11401).

![Example architecture for a Chatbot using retrieval-augmented generation. via Joseph Haaga](https://minimaxir.com/2023/07/langchain-problem/1*b5r7r3-FSNjHUzlCGl3SnA-2.webp)

Example architecture for a Chatbot using retrieval-augmented generation. [via Joseph Haaga](https://tech.buzzfeed.com/the-right-tools-for-the-job-c05de96e949e)

LangChain was by-far the popular tool of choice for RAG, so I figured it was the perfect time to learn it. I spent some time reading LangChain’s rather comprehensive documentation to get a better understanding of how to best utilize it: after a *week* of research, I got nowhere. Running the LangChain demo examples did work, but any attempts at tweaking them to fit the recipe chatbot constraints broke them. After solving the bugs, the overall quality of the chat conversations was bad and uninteresting, and after intense debugging I found no solution. Eventually I had an existential crisis: am I a worthless machine learning engineer for not being able to figure LangChain out when very many other ML engineers can? We [went back](https://tech.buzzfeed.com/the-right-tools-for-the-job-c05de96e949e) to a lower-level ReAct flow, which *immediately* outperformed my LangChain implementation in conversation quality and accuracy.

In all, I wasted a month learning and testing LangChain, with the big takeway that popular AI apps may not necessarily be worth the hype. My existential crisis was resolved after coming across a [Hacker News thread](https://news.ycombinator.com/item?id=35820931) about someone [reimplementing LangChain in 100 lines of code](https://blog.scottlogic.com/2023/05/04/langchain-mini.html), with most of the comments venting all their grievances with LangChain:

![](https://minimaxir.com/2023/07/langchain-problem/hn.png)

loveparade 70 days ago prev next [-
Am I the only one who is not convinced by the value proposition of langchain? 99% of it are interface definitions and implementations for external tools, most of which are super straightforward. I can write integrations for what my app needs in less than an hour myself, why bring in a heavily opinionated external framework? It kind of feels like the npm "left-pad" to me. Everyone just uses it because it seems popular, not because they need it.

crazyedgar 69 days ago I parent next [-
For us LangChain actually caused more problems than it solved. We had a system in production which after working fine a few weeks suddenly started experiencing frequent failures (more than 30% of requests). On digging it seems that LangChain sets a default timeout of 60 seconds for every requests. And this behaviour isn't documented! Such spurious decisions made by LangChain are everywhere, and will all eventually come back to bite. In the end we replaced everything with vanilla request clients. Definitely not recommended to build a system on a library that provides very limited value while hiding a huge amount of details and decisions from you.

Spivak 70 days ago I parent I prev next [-
Langchain is absolutely perfect though, it's bad enough that you'll be driven to write something better out of pure frustration but gives you enough good ideas and breadcrumbs to actually do it. 

It's probably the best on-ramp for "practical uses of llms" because it scratches just the right developer itch.

The problem with LangChain is that it makes simple things relatively complex, and with that unnecessary complexity creates a tribalism which hurts the up-and-coming AI ecosystem as a whole. If you’re a newbie who wants to just learn how to interface with ChatGPT, definitely don’t start with LangChain.

## **“Hello World” in LangChain (or More Accurately, “Hell World”)**

The [Quickstart](https://python.langchain.com/docs/get_started/quickstart) for LangChain begins with a mini-tutorial on how to simply interact with LLMs/ChatGPT from Python. For example, to create a bot that can translate from English to French:

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

chat **=** ChatOpenAI(temperature**=**0)
chat**.**predict_messages([HumanMessage(content**=**"Translate this sentence from English to French. I love programming.")])
*# AIMessage(content="J'adore la programmation.", additional_kwargs={}, example=False)*
```

The equivalent code using [OpenAI’s official Python library](https://github.com/openai/openai-python) for ChatGPT:

```python
import openai

messages **=** [{"role": "user", "content": "Translate this sentence from English to French. I love programming."}]

response **=** openai**.**ChatCompletion**.**create(model**=**"gpt-3.5-turbo", messages**=**messages, temperature**=**0)
response["choices"][0]["message"]["content"]
*# "J'adore la programmation."*
```

LangChain uses about the same amount of code as just using the official `openai` library, expect LangChain incorporates more object classes for not much obvious code benefit.

The prompt templating example reveals the core of how LangChain works:

```python
`from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

template **=** "You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt **=** SystemMessagePromptTemplate**.**from_template(template)
human_template **=** "{text}"
human_message_prompt **=** HumanMessagePromptTemplate**.**from_template(human_template)

chat_prompt **=** ChatPromptTemplate**.**from_messages([system_message_prompt, human_message_prompt])

chat_prompt**.**format_messages(input_language**=**"English", output_language**=**"French", text**=**"I love programming.")`
```

LangChain’s vaunted prompt engineering is just [f-strings](https://realpython.com/python-f-strings/), a feature present in every modern Python installation, but with extra steps. Why do we need to use these `PromptTemplates` to do the same thing?

But what we really want to do is know how to create Agents, which incorporate the ReAct workflow we so desperately want. Fortunately there is a demo for that, which leverages [SerpApi](https://serpapi.com/) and another tool for math computations, showing how LangChain can discriminate and use two different tools contextually:

```python
`from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

*# First, let's load the language model we're going to use to control the agent.*chat **=** ChatOpenAI(temperature**=**0)

*# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.*llm **=** OpenAI(temperature**=**0)
tools **=** load_tools(["serpapi", "llm-math"], llm**=**llm)

*# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.*agent **=** initialize_agent(tools, chat, agent**=**AgentType**.**CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose**=**True)

*# Now let's test it out!*agent**.**run("Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?")`
```

How do the individual tools work? What is `AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION` anyways? The resulting output from `agent.run()` (only present with `verbose=True`) is more helpful.

```bash
`> Entering new AgentExecutor chain...
Thought: I need to use a search engine to find Olivia Wilde's boyfriend and a calculator to raise his age to the 0.23 power.
Action:
{
    "action": "Search",
    "action_input": "Olivia Wilde boyfriend"
}

Observation: Sudeikis and Wilde's relationship ended in November 2020. Wilde was publicly served with court documents regarding child custody while she was presenting Don't Worry Darling at CinemaCon 2022. In January 2021, Wilde began dating singer Harry Styles after meeting during the filming of Don't Worry Darling.
Thought:I need to use a search engine to find Harry Styles' current age.
Action:
{
    "action": "Search",
    "action_input": "Harry Styles age"
}

Observation: 29 years
Thought:Now I need to calculate 29 raised to the 0.23 power.
Action:
{
    "action": "Calculator",
    "action_input": "29^0.23"
}

Observation: Answer: 2.169459462491557

Thought:I now know the final answer.
Final Answer: 2.169459462491557

> Finished chain.
'2.169459462491557'`
```

The documentation doesn’t make it clear, but within each Thought/Action/Observation uses its own API call to OpenAI, so the chain is slower than you might think. Also, why is each action a `dict`? The answer to *that* is later, and is very silly.

Lastly, how does LangChain store the conversation so far?

```bash
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

prompt **=** ChatPromptTemplate**.**from_messages([
    SystemMessagePromptTemplate**.**from_template(
        "The following is a friendly conversation between a human and an AI. The AI is talkative and "
        "provides lots of specific details from its context. If the AI does not know the answer to a "
        "question, it truthfully says it does not know."
    ),
    MessagesPlaceholder(variable_name**=**"history"),
    HumanMessagePromptTemplate**.**from_template("{input}")
])

llm **=** ChatOpenAI(temperature**=**0)
memory **=** ConversationBufferMemory(return_messages**=**True)
conversation **=** ConversationChain(memory**=**memory, prompt**=**prompt, llm**=**llm)

conversation**.**predict(input**=**"Hi there!")
*# 'Hello! How can I assist you today?'*
```

I’m not entirely sure why any of this is necessary. What’s a `MessagesPlaceholder`? Where’s the `history`? Is that necessary for `ConversationBufferMemory`? Adapting this to a minimal `openai` implementation:

```python
import openai

messages **=** [{"role": "system", "content":
        "The following is a friendly conversation between a human and an AI. The AI is talkative and "
        "provides lots of specific details from its context. If the AI does not know the answer to a "
        "question, it truthfully says it does not know."}]

user_message **=** "Hi there!"
messages**.**append({"role": "user", "content": user_message})
response **=** openai**.**ChatCompletion**.**create(model**=**"gpt-3.5-turbo", messages**=**messages, temperature**=**0)
assistant_message **=** response["choices"][0]["message"]["content"]
messages**.**append({"role": "assistant", "content": assistant_message})
*# Hello! How can I assist you today?*
```

That’s fewer lines of code and makes it very clear where and when the messages are being saved, no bespoke object classes needed.

You can say that I’m nitpicking the tutorial examples, and I do agree that every open source library has something to nitpick (including my own!). But if there are more nitpicks than actual benefits from the library then it’s not worth using at all, since if the *quickstart* is this complicated, how painful will it be to use LangChain in practice?

