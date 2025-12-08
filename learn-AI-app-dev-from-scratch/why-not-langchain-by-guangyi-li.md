### 5.2.1 为什么不推荐 LangChain

无论是 OpenAI 的 GPT 模型还是 Google 的 Gemini 模型，官方提供的能力都存在上限，我们常需要在社区中寻找突破点。

LangChain 作为当今最热门的框架之一，在 AI 应用开发中占据显著位置。但近来些年业内对 LangChain 的批评逐渐增多，LangChain 的劣势也日益凸显。

最直观的便是 Thoughtworks 技术雷达（Technology Radar）对 LangChain 态度的变化。技术雷达是咨询公司 Thoughtworks 每年两次定期发布的技术趋势报告，对新兴技术的成熟度与潜力进行评估，将技术分为试验、评估、采纳、淘汰等成熟度状态，为技术选型提供参考。LangChain 于 2023 年 4 月入选第 28 期技术雷达，成熟度状态为“评估”；在 2024 年 4 月第 30 期技术雷达中成熟度被降至 “暂缓”，即不推荐在项目中引入；在 2024 年 10 月第 31 期技术雷达中，LangChain 被彻底移除。LangChain 被淘汰的理由在它的成熟度被降至 “暂缓” 时，技术雷达给出了详细说明：“……我们还发现其存在 API 设计不一致且冗长的情况。因此，它经常会掩盖底层实际发生的情况，使开发者难以理解和控制 LLM 及其周围的各种模式的实际工作方式…”

这里所说的 API 并不是狭义上的 HTTP API，而是指广义上的代码间的通信接口。考虑到 API 是代码与框架的主要交互方式，对开发者而言，API 设计欠佳将使项目与框架集成之路变得困难重重。这里的批评并非空穴来风，接下来我用一个例子来说明 LangChain API 存在的问题。

在提示工程中有一类技巧叫作少样本学习（few shot learning），即在编写的提示语中有意包含一些示例，便于大模型更好地理解我们的意图以给出更精准的回答。例如，在向大模型询问 “big” 的反义词时，在提示语中提前给出反义词的相关示例，具体提示如下：

```
Give the antonym of every input
Input: happy
Output: sad
Input: tall
Output: short
Input: energetic
Output: lethargic
Input: sunny
Output: gloomy
Input: windy
Output: calm
```

大模型在读到诸多示例之后，即刻就会领悟我们想要简短直接的回答，并且回答必须契合“Input/Output”这类格式。用原生的 Python 将上述提示语抽象为代码并非难事，实现代码如下：

```python
def generate_few_shot_prompt(pairs):
    prompt = "Give the antonym of every input\n\n"
    for pair in pairs:
        input_word = pair['input']
        output_word = pair['output']
        prompt += f"Input: {input_word} \nOutput: {output_word}\n\n"
    return prompt
```

在调用该函数时，只需要将所有示例的 `input` 和 `output` 值组装成字典结构，然后以数组形式传入函数中即可：

```python
pairs = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
    {"input": "big", "output": ""}
]

few_shot_prompt = generate_few_shot_prompt(pairs)
```

现在看看使用 LangChain 框架如何实现上述功能。LangChain 为少样本学习这类业务场景提供了 `FewShotPromptTemplate` 提示模板，借助这个模板的代码实现如下：

```python
from langchain_core.example_selectors \
    import LengthBasedExampleSelector

from langchain_core.prompts \
    import FewShotPromptTemplate, PromptTemplate

examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"}
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input} \nOutput: {output}"
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {adjective} \nOutput:",
    input_variables=["adjective"]
)

print(prompt.format(adjective="big"))
```

我们对上述代码稍作分析，以便理解在 LangChain 中是如何实现少样本学习功能的。
- 需要导入 `PromptTemplate` 和 `FewShotPromptTemplate` 组件。
- `PromptTemplate` 组件用于创建常规提示，包含模板内容与变量定义，它与少样本学习场景无关。
- `FewShotPromptTemplate` 组件虽然从名称上同为“模板”，但实际上它更像是原模板的“封装”或者“改善”工具，因为从使用方式上看，它不仅为原模板补充了前缀部分（`prefix`）和提问部分（`suffix`），还负责将诸多示例（`examples`）注入提示语中。

也就是说，为了生成一个带有特定模式的提示语，在 LangChain 中我们需要导入两个模板组件（`PromptTemplate` 和 `FewShotPromptTemplate`），定义 3 个模板变量（`PromptTemplate` 中的 `input` 和 `output`，`FewShotPromptTemplate` 中的 `adjective`），还需要保证示例中数据格式与模板的变量格式相匹配。

很显然，这么做过于复杂了，别忘了我们只是想生成一个具有特定模式的字符串而已。在第 3 章的代码中可以看到，无须学习额外知识，更短的代码就可以达到同样的效果。

将少样本学习固化在代码中的做法有待商榷，因为少样本学习、思维链（chain of thought）、最少到最多提示（least to most prompting）等各类提示语技巧，本质上是解决问题的不同思路，它们为代码实现提供了多种可能性。而将思路固化在框架中与提供多种可能性的初衷背道而驰，给技巧的发挥套上了枷锁。

不仅如此，LangChain 为了支持将模板作为参数传入，还提供了与 `FewShotPromptTemplate` 几乎一样的组件 `FewShotPromptWithTemplates`，允许将原字符串类型的 `prefix` 和 `suffix` 变量替换为模板，这进一步增加了复杂度：

```python
# 在这里 prefix 与 suffix 不再是上段代码中简单的字符串，
# 而是被定义为可以用于生成提示语的模板
prefix_template = PromptTemplate(
    input_variables=["say_hi"],
    template="{say_hi}, Give the antonym of every input\n\n"
)
suffix_template = PromptTemplate(
    input_variables=["adjective"],
    template="Input: {adjective} \nOutput:"
)
few_shot_prompt_with_templates = FewShotPromptWithTemplates(
    #……
    input_variables=["adjective", "say_hi"],
    prefix=prefix_template,
    suffix=suffix_template
)
new_input = {
    "adjective": "big",
    "say_hi": "Hello"
}
prompt = few_shot_prompt_with_templates.format(**new_input)
```

在我看来这种设计存在明显问题。正确的做法应该是让组件支持更多可能性（如前端 DOM 选择器的 `querySelector()` 方法），而非为不同的可能性提供多个相似组件。这种设计给框架的维护者和使用者带来诸多不便。对维护者而言，这意味着他需要更频繁且更大幅度地对框架进行更新（这也是 LangChain API 文档更新不及时的原因之一，很多 API 在官网上只能找到参数说明，却找不到使用示例）；对使用者而言，这增加了框架的使用难度，很难精准找到适用的 API。这种设计变相降低了框架的容错性，也与我们之前所说的“容易让人把事情做对”的原则相违背。

有几篇对 LangChain 批评的文章影响力颇大，如“why we no longer use LangChain for building our AI agents”和“The Problem With LangChain”，前者在 Hacker News 上引起了广泛的讨论，后者被 Thoughtworks 技术雷达引用。如果大家有兴趣可以通过这些材料更进一步地了解 LangChain 当前存在的其他问题。

最后需要说明的是，对 LangChain 的定义存在广义和狭义之分。狭义上的 LangChain 指本章中讨论的 LangChain 框架，而广义上的 LangChain 代表 LangChain 技术品牌，旗下包含 LangChain、LangSmith（调试、测试、监控 AI 应用的平台）和 LangGraph（创建复杂工作流的 AI 应用的框架）3 类产品。本节讨论的各种问题仅针对 LangChain 框架本身。