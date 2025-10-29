import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

st.set_page_config(page_title="Camera Test", layout="wide")
st.title("📸 Simple Camera Test")

def video_frame_callback(frame):
    return frame

webrtc_streamer(
    key="camera_test",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
)
