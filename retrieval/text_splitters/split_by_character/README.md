# Split by character(按字符拆分):
- [Split by character(按字符拆分):](#split-by-character按字符拆分)
  - [文本切分函数中部分参数说明:](#文本切分函数中部分参数说明)
  - [字符数和token数:](#字符数和token数)

This is the simplest method.<br>

这是最简单的方法。<br>

This splits based on characters (by default “”) and measure chunk length by number of characters.<br>

这是基于字符（默认为“”）进行拆分，并通过字符数来测量块长度的方法。<br>

- **How the text is split:** by single character.文本如何被拆分：按单个字符。

- **How the chunk size is measured:** by number of characters.块大小如何被测量：通过字符数。


## 文本切分函数中部分参数说明:

```python
"""
Args:
    chunk_size: Maximum size of chunks to return
    chunk_overlap: Overlap in characters between chunks
    length_function: Function that measures the length of given chunks
    keep_separator: Whether to keep the separator in the chunks
    add_start_index: If `True`, includes chunk's start index in metadata
    strip_whitespace: If `True`, strips whitespace from the start and end of
                        every document
"""
```

以 **"中国对外贸易形势报告（75页）。前 10 个月，一般贸易进出口 19.5 万亿元，增长 25.1%， 比整体进出口增速高出 2.9 个百分点..."** 为例，设置 `chunk_size=50, chunk_overlap=0` 。<br>

文档切分为:<br>

```log
中国对外贸易形势报告（75页）。
前 10 个月，一般贸易进出口 19.5 万亿元，增长 25.1%，
比整体进出口增速高出 2.9 个百分点，占进出口总额的 61.7%，
较去年同期提升 1.6 个百分点。
...
```

测试一下长度:<br>

```python
data = "中国对外贸易形势报告（75页）。"
print(len(data)) # 16(长度就是字符数-characters)
```

这并不是因为langchain使用的另一种计算长度的方式，是因为`chunk_size=50` 表示文本拆分器（`ChineseRecursiveTextSplitter`）在处理文本时将尽量保持每个文本块的字符数 **不超过50个** 。<br>

这里的“字符数”是指字符的个数，包括汉字、英文字母、数字、标点符号等。<br>

`chunk_size` 是用来设置文本分割的大小的参数，目的是为了将较长的文本分割成更小的部分以便于处理，特别是在需要保持文本处理的效率和效果时。例如，在某些文本处理或机器学习任务中，输入长度可能会受到限制，使用这种分割方法可以保证每个输入块都不超过这个长度限制。<br>

此外，`keep_separator=True` 表示在分割文本时会保留分割符（比如句号、逗号等），而 `is_separator_regex=True` 表示使用正则表达式来定义何为分割符，从而更灵活地控制文本的分割方式。<br>

总结来说，`chunk_size=50` 和示例中的句子长度没有直接关系，它只是设置了文本分割器在处理任何文本时单个块的最大长度限制。<br>


## 字符数和token数:

字符数和token数并不是一个意思，它们在文本处理中有着明显的区别：<br>

1. **字符数（Character Count）**:
   - 字符数指的是文本中的字符总数，包括字母、数字、标点符号、空格等。
   - 比如在中文中，每个汉字通常都被视为一个字符。

2. **Token数（Token Count）**:
   - Token通常指的是文本中的单词、词汇单元或有意义的符号组合。
   - 在英文中，一个token可能是一个单词或一个标点符号；在中文中，一个token可以是一个汉字，也可以是一个由几个汉字组成的词组。
   - 分词（Tokenization）是将文本分割成tokens的过程，这在文本分析和自然语言处理中非常重要。

例如，对于句子 "我爱北京天安门"：<br>

- 字符数是7（每个汉字计为一个字符）。
- Token数取决于分词方法；如果分词为“我/爱/北京/天安门”，则有4个tokens。

因此，在处理具体的文本数据时，字符数和token数是需要区分开的两个概念。<br>