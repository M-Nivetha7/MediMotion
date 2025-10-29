def generate_feedback(angles_data=None):
    """
    Generates simple AI-style feedback based on detected joint angles.
    If no angle data is provided, returns a general feedback string.
    """

    if not angles_data or not isinstance(angles_data, dict):
        return "⚙️ Keep a steady posture and maintain consistent movement during exercise."

    feedbacks = []

    for joint, angle in angles_data.items():
        if angle < 30:
            feedbacks.append(f"🦵 {joint}: Try to extend more — your angle is only {angle:.1f}°.")
        elif angle > 150:
            feedbacks.append(f"💪 {joint}: Great flexibility! {angle:.1f}° looks perfect.")
        else:
            feedbacks.append(f"✅ {joint}: Good form maintained at {angle:.1f}°.")

    return "\n".join(feedbacks)
