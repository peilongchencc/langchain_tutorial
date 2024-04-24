# Text Splitters
- [Text Splitters](#text-splitters)
  - [Types of Text Splitters(文本分割器的类型):](#types-of-text-splitters文本分割器的类型)

Once you've loaded documents, you'll often want to transform them to better suit your application.<br>

加载文档后，通常会希望对其进行转换，以更好地适应您的应用。<br>

The simplest example is you may want to split a long document into smaller chunks that can fit into your model's context window.<br>

最简单的例子是您可能想将长文档分成较小的块，以适应您模型的上下文窗口。<br>

LangChain has a number of built-in document transformers that make it easy to split, combine, filter, and otherwise manipulate documents.<br>

LangChain具有许多内置的文档转换器，使得将文档分割、合并、过滤和其他操作变得简单。<br>

🚨When you want to deal with long pieces of text, it is necessary to split up that text into chunks.<br>

当您想要处理长篇文本时，有必要将文本分割成块。<br>

🔥As simple as this sounds, there is a lot of potential complexity here.<br>

尽管听起来很简单，但这里存在许多潜在的复杂性。<br>

Ideally, you want to keep the semantically related pieces of text together.<br>

理想情况下，您希望将语义相关的文本片段保持在一起。<br>

What "semantically related" means could depend on the type of text.<br>

“语义相关”的含义可能取决于文本的类型。<br>

> “语义相关”的含义可能取决于文本的类型？这里有点不是特别明白？难道是同样是json文件，更可能表示数据？当然语义相关这个范围太广，例如 "大象"、"狮子"是不同事物，如果按照动植物这个范围划分，它们又同样属于动物。

This notebook showcases several ways to do that.<br>

本笔记本展示了实现这一目标的几种方法。<br>

At a high level, text splitters work as following(在高层次上，文本分割器的工作方式如下):<br>

1. Split the text up into small, semantically meaningful chunks (often sentences). 将文本分割成小的、语义上有意义的块（通常是句子）。

2. Start combining these small chunks into a larger chunk until you reach a certain size (as measured by some function). 开始将这些小块组合成一个较大的块，直到达到某个特定的大小（由某个函数衡量）。

3. Once you reach that size, make that chunk its own piece of text and then start creating a new chunk of text with some overlap (to keep context between chunks). 一旦达到那个大小，将该块作为自己的一部分文本，然后开始创建一个新的文本块，并且有一些重叠（以保持块之间的上下文）。

That means there are two different axes along which you can customize your text splitter(这意味着您可以沿两个不同的轴线定制您的文本分割器):<br>

1. How the text is split 文本如何分割

2. How the chunk size is measured 块大小如何衡量


## Types of Text Splitters(文本分割器的类型):

LangChain offers many different types of text splitters. These all live in the `langchain-text-splitters` package. Below is a table listing all of them, along with a few characteristics:<br>

LangChain提供许多不同类型的文本分割器。所有这些都包含在 `langchain-text-splitters` 软件包中。下面是一个表格，列出了它们所有的信息，以及一些特征：<br>

**Name:** Name of the text splitter 名称：文本分割器的名称<br>

**Splits On:** How this text splitter splits text 分割方式：该文本分割器如何分割文本<br>

**Adds Metadata:** Whether or not this text splitter adds metadata about where each chunk came from. 添加元数据：该文本分割器是否添加关于每个块来自何处的元数据。<br>

**Description:** Description of the splitter, including recommendation on when to use it. 描述：分割器的描述，包括何时建议使用它。<br>

英文版:<br>

Name             |Splits On                                |Adds Metadata|Description
-----------------|-----------------------------------------|-------------|---------------
Recursive        | A list of user defined characters       |             | Recursively splits text. Splitting text recursively serves the purpose of trying to keep related pieces of text next to each other. This is the recommended way to start splitting text.
HTML             | HTML specific characters                | ✅           | Splits text based on HTML-specific characters. Notably, this adds in relevant information about where that chunk came from (based on the HTML)
Markdown         | Markdown specific characters            | ✅           | Splits text based on Markdown-specific characters. Notably, this adds in relevant information about where that chunk came from (based on the Markdown)
Code             | Code (Python, JS) specific characters   |              | Splits text based on characters specific to coding languages. 15 different languages are available to choose from.
Token            | Tokens                                  |              | Splits text on tokens. There exist a few different ways to measure tokens.
Character        | A user defined character                |              | Splits text based on a user defined character. One of the simpler methods.
[Experimental] Semantic Chunker | Sentences                |              | First splits on sentences. Then combines ones next to each other if they are semantically similar enough. Taken from [Greg Kamradt](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb).
[AI21 Semantic Text Splitter](https://python.langchain.com/docs/integrations/document_transformers/ai21_semantic_text_splitter/) | Semantics |✅ | Identifies distinct topics that form coherent pieces of text and splits along those.

中文版:<br>

名称             |分割依据                                |添加元数据|描述
-----------------|-----------------------------------------|-------------|---------------
递归分割         |用户定义的字符列表                      |             | 递归地分割文本。递归地分割文本的目的是尽量保持相关的文本片段相邻。这是开始分割文本的推荐方式。
HTML             |HTML 特定字符                           | ✅           | 根据 HTML 特定字符分割文本。值得注意的是，这会添加有关该块来自何处的相关信息（基于 HTML）。
Markdown         |Markdown 特定字符                      | ✅           | 根据 Markdown 特定字符分割文本。值得注意的是，这会添加有关该块来自何处的相关信息（基于 Markdown）。
代码             |代码（Python、JS）特定字符             |              | 根据特定于编程语言的字符分割文本。可供选择 15 种不同的语言。
标记(Token)             |标记(Tokens)                                   |              | 根据标记(Tokens)分割文本。有几种不同的方式来衡量标记。
字符             |用户定义的字符                          |              | 根据用户定义的字符分割文本。这是较简单的方法之一。
[实验性] 语义块分割器 |句子                               |              | 首先按句子分割。然后，如果它们在语义上足够相似，就将它们组合在一起。取自 [Greg Kamradt](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb)。
[AI21 语义文本分割器](https://python.langchain.com/docs/integrations/document_transformers/ai21_semantic_text_splitter/) |语义 |✅ | 识别形成连贯文本片段的不同主题，并沿着这些主题分割。
