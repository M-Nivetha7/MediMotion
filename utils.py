import pandas as pd
import os
from datetime import datetime

def save_feedback_data(patient_name, age, exercise_name, feedback_text, performance_score):
    """
    Saves feedback and performance details into an Excel file.
    Creates 'data/feedback_data.xlsx' if it doesn't exist.
    """

    os.makedirs("data", exist_ok=True)
    file_path = "data/feedback_data.xlsx"

    new_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Patient Name": [patient_name],
        "Age": [age],
        "Exercise": [exercise_name],
        "Performance Score": [performance_score],
        "Feedback": [feedback_text]
    }

    df_new = pd.DataFrame(new_data)

    if os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(file_path, index=False)
    return file_path
