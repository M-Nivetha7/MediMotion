# MediMotion_Streamlit

Local Streamlit web app for pose tracking, feedback and PDF report generation.

## Setup
1. Create virtual environment (recommended).
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Features
- Signup & Login (SQLite + bcrypt)
- Live webcam pose detection (MediaPipe via streamlit-webrtc)
- Joint angles displayed side-by-side with annotated video
- Rule-based feedback generation
- Save/download PDF report and CSV/Excel of recorded angles
