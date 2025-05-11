from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 専門家ごとのシステムプロンプト定義（日本語）
SYSTEM_PROMPTS = {
    "高校生専門教育アドバイザー": (
        "あなたは経験豊富な教育アドバイザーです。"
        "高校生の悩みや、高校生を持つ親の悩みに対し、親身にかつ適切なアドバイスをしてください。"
    ),
    "晩御飯専門料理アドバイザー": (
        "あなたは晩御飯の専門料理アドバイザーです。"
        "家庭で簡単に作れるレシピや、栄養バランスを考えた食事提案をしてください。"
    ),
    "AI活用アドバイザー": (
        "あなたは統計解析、機械学習、データ可視化に長けたAI活用アドバイザーです。"
        "最新のAIの詳細な説明、手法や具体的な導入事例を、初心者向けに丁寧に提供してください。"
    ),
}

# 入力テキストと選択された専門家タイプを受け取り、LLMからの回答を返す
def generate_response(input_text: str, expert_type: str) -> str:
    # 環境変数 OPENAI_API_KEY からAPIキーを取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEYが設定されていません。環境変数にAPIキーを設定してください。")
        return ""
    
    llm = ChatOpenAI(temperature=0.7, openai_api_key=api_key)
    system_prompt = SYSTEM_PROMPTS.get(expert_type, "あなたは有能なアシスタントです。")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]
    response = llm(messages)
    return response.content

# Streamlit アプリのメイン関数
def main():
    # カスタム CSS で見た目を改善
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
            color: #333333;
        }
        .main {
            max-width: 800px;
            margin: auto;
            padding: 20px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            font-size: 16px;
            margin-top: 10px;
            border-radius: 8px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextArea textarea {
            border: 2px solid #4CAF50;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # メインコンテナの幅を調整
    st.markdown('<div class="main">', unsafe_allow_html=True)

    st.title("AI Q&A Web アプリ")
    st.write(
        "このアプリはテキストを入力し、ラジオボタンで選択した専門家の立場で"
        "LLMによる回答を生成します。"
    )

    # 専門家タイプ選択
    expert_type = st.radio(
        "専門家を選択してください:",
        list(SYSTEM_PROMPTS.keys())
    )

    # 質問入力フォーム
    input_text = st.text_area(
        "質問を入力してください:",
        height=150
    )

    # 送信ボタン
    if st.button("送信"):
        if input_text.strip() == "":
            st.warning("質問を入力してください。")
        else:
            with st.spinner("LLM による回答を生成中..."):
                answer = generate_response(input_text, expert_type)
            st.subheader("回答結果")
            st.write(answer)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

