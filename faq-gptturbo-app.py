
import streamlit as st
import openai
import pandas as pd

df = pd.read_csv('tbl_st.csv')
sentences = df["サンプル 応答文"].to_list()

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key # secrets に後ほどAPI Keyを保存する

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは市役所のとても優秀な粗大ごみ受付担当です"}  
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]                       # message インスタンス 
    query = st.session_state["user_input"]                        # ユーザの問い合わせ
    user_message = f"{sentences}\n\nQ: {query}\n"                 # faq と ユーザ問い合わせを結合
    messages.append({"role": "user", "content": user_message} )   # message インスタンスに追加
    response = openai.ChatCompletion.create(                      # gpt-3.5-turbo api コール
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=256
    )  

    bot_message = response["choices"][0]["message"]               # 返答
    messages.append(bot_message)                                  # 返答を追加

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使った粗大ごみFAQボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
