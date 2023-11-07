import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import cv2
import av

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

class VideoProcessor:
    def __init__(self):
        self.capture_frame = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if self.capture_frame:
            # 画像を保存する
            cv2.imwrite('captured_frame.png', img)
            # フラグをリセットする
            self.capture_frame = False

        return av.VideoFrame.from_ndarray(img, format="bgr24")

video_processor = VideoProcessor()
webrtc_ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor, rtc_configuration=RTC_CONFIGURATION)

if webrtc_ctx.video_processor:
    if st.button("Capture Frame"):
        # ボタンが押されたらフラグをセットする
        webrtc_ctx.video_processor.capture_frame = True