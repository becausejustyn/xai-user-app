"""Task 3: answer questions about the explanations."""

import streamlit as st

from app_utils import build_export

QUESTIONS = {
    "helpful": "The explanations helped me understand the model prediction.",
    "model_fair": "I think the model made a fair prediction.",
    "data_fair": "I think the data represented people fairly.",
    "trust": "I would trust this model in a real application.",
}
CHOICES = (
    "Strongly disagree",
    "Disagree",
    "Somewhat disagree",
    "Somewhat agree",
    "Agree",
    "Strongly agree",
)

st.set_page_config(page_title="Review explanations", page_icon="📝", layout="wide")
st.title("Task 3: Review the explanations")
st.write("Select one answer for each statement.")

saved_answers = st.session_state.get("xai_demo_survey", {})

with st.form("explanation-review"):
    answers = {}
    for key, question in QUESTIONS.items():
        default_index = CHOICES.index(saved_answers[key]) if key in saved_answers else None
        answers[key] = st.radio(
            question,
            CHOICES,
            index=default_index,
            horizontal=True,
            key=f"survey-{key}",
        )
        st.divider()

    submitted = st.form_submit_button("Save answers", type="primary", width="stretch")

if submitted:
    if any(answer is None for answer in answers.values()):
        st.error("Answer all four statements.")
    else:
        st.session_state.xai_demo_survey = answers
        st.success("Task 3 is complete. Your answers are in this session only.")

if st.session_state.get("xai_demo_survey"):
    st.download_button(
        "Download all demo data",
        data=build_export(
            st.session_state.get("xai_demo_preferences", {}),
            st.session_state.get("xai_demo_points", {}),
            st.session_state.xai_demo_survey,
        ),
        file_name="xai-demo-data.json",
        mime="application/json",
        width="stretch",
    )
