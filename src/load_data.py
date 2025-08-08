import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# OllamaとChromaDBの接続情報を環境変数から取得
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# ドキュメントの読み込み
documents_dir = "/app/documents"
all_docs = []

# documentsフォルダ内の全PDFファイルをロード
print(f"'{documents_dir}' フォルダからドキュメントを読み込んでいます...")
for filename in os.listdir(documents_dir):
    if filename.endswith(".pdf"):
        filepath = os.path.join(documents_dir, filename)
        loader = PyPDFLoader(filepath)
        all_docs.extend(loader.load())

if not all_docs:
    print("ドキュメントが見つかりませんでした。'.pdf'ファイルを'documents'フォルダに置いてください。")
else:
    # ドキュメントの分割
    print("ドキュメントを分割しています...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)

    # 埋め込みモデルの初期化
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_HOST
    )

    # ベクトルデータベースの作成・更新
    # persist_directoryを指定することで、データは永続化される
    print("ベクトル化を行い、データベースに保存しています...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    print("ドキュメントの読み込みとベクトル化が完了しました。")
