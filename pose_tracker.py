import cv2
import mediapipe as mp
import streamlit as st
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def start_camera():
    st.write("🎥 **MediMotion - Live Exercise Tracker**")
    st.info("Perform your exercises in front of the camera. The app will track your movements live!")

    run = st.checkbox("✅ Start Camera")
    FRAME_WINDOW = st.image([])  # Streamlit display container

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        st.error("🚫 Could not open camera. Please check permissions or try restarting Streamlit.")
        return

    pose = mp_pose.Pose()

    while run:
        ret, frame = camera.read()
        if not ret:
            st.warning("⚠️ Failed to capture frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)

    camera.release()
    st.success("✅ Camera stopped.")
