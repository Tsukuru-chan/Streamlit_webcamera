import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import cv2
import av
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
load_dotenv()

openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class VideoProcessor:
    def __init__(self):
        self.capture_frame = False
        self.image_saved = False
        self.image_path = ''

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if self.capture_frame:
            # 画像を保存する
            self.image_path = 'captured_frame.png'
            cv2.imwrite(self.image_path, img)
            # フラグをリセットする
            self.capture_frame = False
            self.image_saved = True

        return av.VideoFrame.from_ndarray(img, format="bgr24")

video_processor = VideoProcessor()
webrtc_ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor, rtc_configuration=RTC_CONFIGURATION)

if webrtc_ctx.video_processor:
    if st.button("Capture Frame"):
        # ボタンが押されたらフラグをセットする
        webrtc_ctx.video_processor.capture_frame = True

    # 画像が保存されていれば表示する
    if webrtc_ctx.video_processor.image_saved:
        if os.path.exists(webrtc_ctx.video_processor.image_path):
            st.image(webrtc_ctx.video_processor.image_path)

            # 画像を読み込み、base64に変換する
            with open(webrtc_ctx.video_processor.image_path, "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode("utf-8")

            # OpenAI APIにリクエストを送信する
            
            with st.spinner('OpenAI APIにリクエストを送信中...'):
                response = openai.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                "Please explain specifically what you see there and what the situation is. Please be sure to use Japanese. No comments other than explanations are accepted.",
                                {"image": base64_image, "resize": 768},
                            ],
                        },
                    ],
                    max_tokens=500,
                )
            # レスポンスを表示する
            st.write(response.choices[0].message.content)

            webrtc_ctx.video_processor.image_saved = False
        else:
            st.write(f"画像ファイルが存在しません: {webrtc_ctx.video_processor.image_path}")