# Recursively split by character(按字符递归分割)
- [Recursively split by character(按字符递归分割)](#recursively-split-by-character按字符递归分割)
  - [Splitting text from languages without word boundaries(从没有单词边界的语言中分割文本)](#splitting-text-from-languages-without-word-boundaries从没有单词边界的语言中分割文本)
  - [`CharacterTextSplitter` 和 `RecursiveCharacterTextSplitter` 的区别:](#charactertextsplitter-和-recursivecharactertextsplitter-的区别)
    - [1. `CharacterTextSplitter`](#1-charactertextsplitter)
    - [2. `RecursiveCharacterTextSplitter`](#2-recursivecharactertextsplitter)
  - [什么叫 "Writing systems without word boundaries" ？这种写法和英语有什么区别？](#什么叫-writing-systems-without-word-boundaries-这种写法和英语有什么区别)


This text splitter is the recommended one for generic text. It is parameterized by a list of characters. It tries to split on them in order until the chunks are small enough.<br>

**这个文本分割器是通用文本推荐的分割器。** 它根据一个字符列表进行参数设置。它尝试 **按顺序** 分割这些字符，直到文本块足够小。<br>

The default list is `["\n\n", "\n", " ", ""]` . This has the effect of trying to keep all paragraphs (and then sentences, and then words) together as long as possible, as those would generically seem to be the strongest semantically related pieces of text.<br>

默认列表是 `["\n\n", "\n", " ", ""]` 。这样做的效果是尽可能长时间地保持所有段落（然后是句子和词语）在一起，因为这些通常看起来是语义上联系最紧密的文本部分。<br>

> `["\n\n", "\n", " ", ""]` 是适合英文的切分方式，英文出了段落外，最明显的切分就是 `" "(空格)` 。与中文不一样!‼️<br>

- How the text is split: by list of characters.文本如何被分割：通过字符列表。

- How the chunk size is measured: by number of characters.块大小如何测量：通过字符数量。


## Splitting text from languages without word boundaries(从没有单词边界的语言中分割文本)

Some writing systems do not have word boundaries, for example Chinese, Japanese, and Thai.<br>

一些书写系统没有单词边界，例如中文、日文和泰文。<br>

Splitting text with the default separator list of `["\n\n", "\n", " ", ""]` can cause words to be split between chunks.<br>

使用默认的分隔符列表 `["\n\n", "\n", " ", ""]` 来分割文本可能会导致词语在块之间被分开。<br>

To keep words together, you can override the list of separators to include additional punctuation:<br>

为了保持单词的完整性，你可以修改分隔符列表，加入额外的标点符号：<br>


- Add ASCII full-stop “.”, Unicode fullwidth full stop “．” (used in Chinese text), and ideographic full stop “。” (used in Japanese and Chinese)加入ASCII句号“.”、Unicode全角句号“．”（用于中文）、和表意文字句号“。”（用于日文和中文）

- Add Zero-width space used in Thai, Myanmar, Kmer, and Japanese.加入用于泰语、缅甸语、高棉语和日语的零宽空格。

- Add ASCII comma “,”, Unicode fullwidth comma “，”, and Unicode ideographic comma “、”加入ASCII逗号“,”、Unicode全角逗号“，”和Unicode表意文字逗号“、”。

```python
text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200B",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
    # Existing args
)
```


## `CharacterTextSplitter` 和 `RecursiveCharacterTextSplitter` 的区别:

在处理中文文本时，`CharacterTextSplitter` 和 `RecursiveCharacterTextSplitter` 都是用来将文本分割成单个字符的工具，但它们的工作方式略有不同。下面将通过具体的中文例子来说明这两者的区别：<br>

### 1. `CharacterTextSplitter`

这是一个比较直接的文本分割器，它会将输入的文本简单地按照每个字符进行分割。例如，对于中文句子：<br>

**"今天天气很好。"** <br>

使用 `CharacterTextSplitter` 处理后，结果会是一个包含每个汉字和标点符号的列表：<br>

**['今', '天', '天', '气', '很', '好', '。']** <br>

这种分割器适用于需要将文本完全分解为单个字符的情况。<br>

### 2. `RecursiveCharacterTextSplitter`

这种分割器则更加复杂，它通常用于处理需要递归分割的情况。例如，如果一个文本片段包含嵌套的结构（如括号内的文本或引号内的文本），`RecursiveCharacterTextSplitter` 可以递归地处理这些结构。对于同样的句子：<br>

**"今天天气很好。"** <br>

如果句子结构更复杂，比如包含嵌套的引号：<br>

**"她说：'今天天气很好。'"** <br>

使用 `RecursiveCharacterTextSplitter` 处理，分割器可能会首先识别外层的引号，然后递归地处理引号内的内容。但结果仍然是每个字符的单独分割：<br>

**['她', '说', '：', "'", '今', '天', '天', '气', '很', '好', '。', "'"]** <br>

递归分割器通常设计用来处理这样的结构性文本，可以适当地处理文本内的层次和嵌套，尽管在上述简单示例中，两者的输出可能看起来没有区别。<br>

总结来说，`CharacterTextSplitter` 是一个基础的字符级分割器，而 `RecursiveCharacterTextSplitter` 设计用于处理可能含有复杂结构（如嵌套括号、引号等）的文本。在实际应用中，选择哪一个分割器取决于你的具体需求和文本的结构复杂度。


## 什么叫 "Writing systems without word boundaries" ？这种写法和英语有什么区别？

所谓的“没有词界的书写系统”是指在书写时，不用空格或其他明显的标记来区分词与词之间的界限。这种书写系统常见于一些亚洲语言，如中文和日语。<br>

1. **中文**：中文书写不使用空格分开每个词。汉字连续书写，而读者需要根据语境和经验来识别词组。例如，在句子“我喜欢学习”中，没有明显的标记来区分“我”、“喜欢”和“学习”这三个词。

2. **日语**：日语也类似，尽管使用了汉字和假名的混合系统，但通常不使用空格。不过，假名（平假名和片假名）的使用有助于某种程度上区分词汇，尤其是用来标示语尾变化或助词。

与之相比，英语和其他许多使用拉丁字母的语言，在书写系统中会用空格来明确标识单词的界限。<br>

这种书写方式使得读者能够轻松地区分和识别单词。例如，句子 “I like studying” 中，空格清楚地标出了三个单词：I, like, 和 studying。<br>

这种区别对于语言学习者来说尤其重要，因为它影响了阅读策略和语言处理的方式。没有词界的语言需要读者在阅读时进行更多的语境解析和词义推断。<br>