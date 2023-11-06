import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("My first Streamlit app")
st.write("Hello, world")

webrtc_streamer(
    key="example",
    rtc_configuration={  # この設定を足す
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)