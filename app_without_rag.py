import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import time
from gemini_rag import QASystem
load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon="⛵",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Function to start a new chat session
def start_chat_session(session_key):
    if session_key not in st.session_state:
        st.session_state[session_key] = model.start_chat(history=[])

def get_function_icon(function_title):
    icons = {
        "Địa điểm": ' 🌍',
        "Ẩm thực": ' 🍽️🍴',
        "Tư vấn": ' 🤔',
        "Cẩm nang": ' 📚',
        "Thời tiết và điều kiện giao thông": ' 🚥⛅'
    }
    return icons.get(function_title, '')
# Function to display chat interface
def chat_interface(session_key, chat_history_key, function_title):
    start_chat_session(session_key)

    st.header(function_title + get_function_icon(function_title))

    chat_session = st.session_state[session_key]

    for message in chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    user_prompt = st.chat_input(f"Hỏi tôi về {function_title}...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        if(session_key == "chat_session_locations"):
            user_prompt_full = 'Địa điểm du lịch ở:' + user_prompt
        elif(session_key == 'chat_session_cuisine'):
            user_prompt_full = ' một số nhà hàng, ẩm thực ở: ' + user_prompt
        elif(session_key == 'chat_session_advice'):
            user_prompt_full = 'Tư vấn du lịch cho tôi về: ' + user_prompt
        elif(session_key == 'chat_session_guide'):
            user_prompt_full = 'Một vài cẩm nang khi du lịch ở :' + user_prompt
        else:
            user_prompt_full = user_prompt

        gemini_response = chat_session.send_message(user_prompt_full)

        # Display Gemini-Pro's complete response after typing effect
        tmp_str = ""
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            for char in gemini_response.text:
                tmp_str  = tmp_str + char
                time.sleep(0.01)  # Thời gian delay giữa các ký tự
                typing_placeholder.markdown(tmp_str)
            st.markdown(gemini_response.text)


# Main program
st.title("🤖 Trợ lý du lịch ảo")

menu = ["Trang chủ", "Địa điểm", "Ẩm thực", "Tư vấn", "Cẩm nang", "Thời tiết và điều kiện giao thông"]
choice = st.sidebar.selectbox("Chọn chức năng", menu)

if choice == "Trang chủ":
    st.header("Trang chủ")
    st.write("Chào mừng bạn đến với trợ lý du lịch ảo! Chọn một chức năng từ menu bên trái.")

elif choice == "Địa điểm":
    chat_interface("chat_session_locations", "chat_history_locations", "Địa điểm")

elif choice == "Ẩm thực":
    chat_interface("chat_session_cuisine", "chat_history_cuisine", "Ẩm thực")

elif choice == "Tư vấn":
    chat_interface("chat_session_advice", "chat_history_advice", "Tư vấn")

elif choice == "Cẩm nang":
    chat_interface("chat_session_guide", "chat_history_guide", "Cẩm nang")

elif choice == "Thời tiết và điều kiện giao thông":
    st.header("Thời tiết và điều kiện giao thông  🚥⛅")
    st.write("Chức năng tạm đóng!")
