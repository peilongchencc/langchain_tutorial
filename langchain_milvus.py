import getpass
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

# 加载txt文件
loader = TextLoader("../../modules/state_of_the_union.txt")
documents = loader.load()

# 文件分割
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 导入向量化工具
embeddings = OpenAIEmbeddings()

# 将文本转向量并存入milvus
vector_db = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"host": "127.0.0.1", "port": "19530"},
)

if __name__ == '__main__':
    # 检索示例
    query = "What did the president say about Ketanji Brown Jackson"
    docs = vector_db.similarity_search(query)
    for idx, doc in enumerate(docs, 1):
        print(f"第{idx}个相似文本为:\n{doc.page_content}")