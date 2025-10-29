import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import time

# Streamlit setup
st.set_page_config(page_title="MediMotion - Exercise Tracker", page_icon="💪", layout="wide")
st.title("💪 MediMotion - AI Exercise Tracker")
st.markdown("### Track your shoulder, knee, and elbow exercises live and generate reports automatically!")

# Initialize mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Global session state
if "exercise_running" not in st.session_state:
    st.session_state.exercise_running = False
if "angles" not in st.session_state:
    st.session_state.angles = []
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Helper Functions
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def generate_feedback(avg_angle):
    if avg_angle > 160:
        return "Excellent form! Full range of motion achieved. ✅"
    elif avg_angle > 120:
        return "Good effort, but try extending a bit more. 💪"
    else:
        return "Incomplete motion detected. Try to lift higher next time. ⚠️"

def generate_pdf_report(exercise_name, reps, avg_angle, feedback):
    pdf_path = "exercise_report.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(180, 750, "MediMotion Exercise Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Exercise Name: {exercise_name}")
    c.drawString(100, 680, f"Total Repetitions: {reps}")
    c.drawString(100, 660, f"Average Joint Angle: {round(avg_angle,2)}°")
    c.drawString(100, 640, f"Feedback: {feedback}")
    c.showPage()
    c.save()
    return pdf_path

# UI Controls
exercise_name = st.selectbox("Select Exercise", ["Shoulder Raise", "Elbow Curl", "Knee Bend"])

col1, col2 = st.columns(2)
start_btn = col1.button("▶️ Start Exercise")
stop_btn = col2.button("⏹️ Stop Exercise")

FRAME_WINDOW = st.image([])

if start_btn:
    st.session_state.exercise_running = True
    st.session_state.angles = []
    st.session_state.counter = 0
    st.toast("Exercise tracking started!")

if stop_btn:
    st.session_state.exercise_running = False
    st.toast("Exercise stopped! You can now generate your report below.")

if st.session_state.exercise_running:
    cap = cv2.VideoCapture(0)
    stage = None
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while st.session_state.exercise_running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("No webcam detected.")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            try:
                landmarks = results.pose_landmarks.landmark
                if exercise_name == "Elbow Curl":
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    angle = calculate_angle(shoulder, elbow, wrist)

                elif exercise_name == "Shoulder Raise":
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    angle = calculate_angle(hip, shoulder, wrist)

                else:  # Knee Bend
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    angle = calculate_angle(hip, knee, ankle)

                st.session_state.angles.append(angle)

                if angle > 160:
                    stage = "down"
                if angle < 70 and stage == "down":
                    stage = "up"
                    st.session_state.counter += 1
                    st.toast(f"Rep Count: {st.session_state.counter}")

                cv2.putText(image, f'Angle: {int(angle)}°', (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, f'Reps: {st.session_state.counter}', (50,100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

            except:
                pass

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            FRAME_WINDOW.image(image, channels='BGR')

            if not st.session_state.exercise_running:
                break

        cap.release()
        cv2.destroyAllWindows()

# Generate Report Section
if len(st.session_state.angles) > 0 and not st.session_state.exercise_running:
    avg_angle = np.mean(st.session_state.angles)
    feedback = generate_feedback(avg_angle)
    st.success(f"🏁 Exercise completed! {feedback}")

    if st.button("📄 Generate PDF Report"):
        pdf_path = generate_pdf_report(exercise_name, st.session_state.counter, avg_angle, feedback)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download Report", f, file_name="MediMotion_Report.pdf")
