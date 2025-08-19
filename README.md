# RagChatbot

> ⚠️ **注意: 本プロジェクトはプロトタイプです**
>
> このチャットボットの回答性能は、実行するPCのスペック（特にRAM容量やCPU/GPU性能）に大きく依存します。
> より高性能なモデルを使用することで回答の質は向上しますが、その分高いマシンパワーが必要になります。現在の構成は、比較的スペックの低いPCでも動作することを優先した一例です。

RagChatbotは、ローカルのPDFドキュメントに基づいて質問に答えるAIチャットボットです。Ollama、LangChain、ChromaDB、Dockerを使用して構築されています。

社内マニュアルや技術資料など、特定のドキュメントに関する質問に対し、インターネットに接続せず安全に回答するシステムを自分のPC上で実現します。

## ✨ 特徴

- **完全ローカル実行**: インターネット接続やクラウドAPIは不要です。プライバシーが完全に保護されます。
- **RAG (Retrieval-Augmented Generation)**: ドキュメントの内容を検索し、その情報に基づいて正確な回答を生成します。
- **Dockerで簡単構築**: 依存関係のインストールが不要で、簡単なコマンドで環境を立ち上げられます。
- **ドキュメントの柔軟な追加**: `documents`フォルダにPDFファイルを追加するだけで、AIの知識を簡単に拡張できます。

## 🛠️ 技術スタック

- **Ollama**: LLM（大規模言語モデル）の実行と埋め込みモデルの提供
- **LangChain**: RAGパイプラインを構築するためのフレームワーク
- **ChromaDB**: ベクトルデータを保存する軽量なデータベース
- **Docker / Docker Compose**: 各コンポーネントを隔離し、簡単に実行するためのコンテナ技術
- **Python**: メインのRAG処理を実装するための言語

## 🚀 使い方

このプロジェクトを使用するには、DockerとDocker Composeがインストールされている必要があります。

1.  **プロジェクトをクローンする**
    ```bash
    git clone https://github.com/semantic-honu/rag-chatbot.git
    cd RagChatbot
    ```

2.  **ドキュメントの準備**

    `documents` フォルダに、AIに読み込ませたいPDFファイルを配置します。
    **【重要】**
     PDFファイルは、**テキスト情報が埋め込まれているもの**に限ります。
     画像として保存されているPDF（テキストを選択・コピーできないもの）は、正しく読み込むことができませんのでご注意ください。
     Webページを印刷してPDFを作成する場合は、テキスト情報が保持されているかご確認ください。

3.  **環境の起動**

    `docker-compose.yml`で定義されたサービス（Ollama, ChromaDB, Pythonアプリ）を起動します。
    ```bash
    docker-compose up -d
    ```

4.  **モデルのダウンロード**

    Ollamaコンテナ内で使用するLLMと埋め込みモデルをダウンロードします。
    ```bash
    # LLM（大規模言語モデル）
    docker-compose exec ollama ollama pull phi3

    # 埋め込みモデル
    docker-compose exec ollama ollama pull nomic-embed-text
    ```

5.  **ドキュメントの読み込みとベクトル化**

    `load_data.py`スクリプトを実行して、`documents`フォルダ内のPDFファイルを読み込み、ベクトル化してデータベースに保存します。
    この処理は初回、またはドキュメントを更新した時に実行してください。
    ```bash
    docker-compose exec rag-app python src/load_data.py
    ```

6.  **AIチャットボットの起動**

    `chat.py`スクリプトを実行して、質問応答を開始します。
    プロンプトが表示されたら、AIに質問を入力してください。
    ```bash
    docker-compose exec rag-app python src/chat.py
    ```

7.  **終了**

    チャットを終了するには `exit` と入力します。
    すべてのサービスを停止するには、以下のコマンドを実行します。
    ```bash
    docker-compose down
    ```

## 📝 ライセンス

このプロジェクトは、MITライセンスのもとで公開されています。


## 使用ライブラリとライセンス一覧

このプロジェクトでは以下のOSSライブラリを使用しています。各ライブラリのライセンス条項に従い、著作権表示および免責事項を遵守しています。

| ライブラリ名             | ライセンス       |
|--------------------------|------------------|
| langchain                | MIT              |
| langchain-community      | MIT              |
| langchain-chroma         | MIT              |
| langchain-ollama         | MIT              |
| ollama                   | MIT              |
| pypdf                    | BSD-2-Clause     |
| phi3                     | MIT              |