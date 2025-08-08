import os
import readline
from langchain_chroma.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# OllamaとChromaDBの接続情報を環境変数から取得
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# 埋め込みモデルの初期化
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url=OLLAMA_HOST
)

# 既存のベクトルデータベースをロード
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# LLMの初期化
llm = OllamaLLM(model="phi3", base_url=OLLAMA_HOST)

# プロンプトテンプレートの定義
prompt_template = """
与えられた文脈情報のみに基づいて、質問に答えてください。
もし文脈情報に答えがない場合は、「文脈情報に答えはありません。」と答えてください。
質問と関係ないことは言わないでください。

# 文脈情報
{context}

# 質問
{question}

# 回答
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# RAGチェーンの構築
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT}
)

# 質問ループ
print("ドキュメントに関する質問をしてください（終了するには 'exit' を入力）")
while True:
    question = input("> ")
    if question.lower() == 'exit':
        break
    response = rag_chain.invoke({"query": question})
    print("\n回答:", response["result"], "\n")
