"""Task 1: compare two visual explanations."""

import secrets

import streamlit as st

from app_utils import build_export, find_trials, load_trials, select_trials

TRIAL_COUNT = 10

st.set_page_config(page_title="Compare explanations", page_icon="⚖️", layout="wide")
st.title("Task 1: Compare explanations")
st.write("Select the explanation that best shows why the model made its prediction.")

all_trials = load_trials()
if not all_trials:
    st.warning("The app cannot find local trial images.")
    st.write("Follow the data setup instructions in `trials/README.md`.")
    st.stop()

trial_count = min(TRIAL_COUNT, len(all_trials))
if "xai_demo_preference_trial_ids" not in st.session_state:
    seed = secrets.randbits(32)
    st.session_state.xai_demo_preference_trial_ids = [
        trial.trial_id for trial in select_trials(all_trials, trial_count, seed)
    ]
if "xai_demo_preference_index" not in st.session_state:
    st.session_state.xai_demo_preference_index = 0
if "xai_demo_preferences" not in st.session_state:
    st.session_state.xai_demo_preferences = {}

trials = find_trials(st.session_state.xai_demo_preference_trial_ids, all_trials)
index = st.session_state.xai_demo_preference_index
responses = st.session_state.xai_demo_preferences

if index >= len(trials):
    st.success("Task 1 is complete.")
    st.write(f"You compared {len(responses)} image sets.")
    st.download_button(
        "Download demo data",
        data=build_export(
            responses,
            st.session_state.get("xai_demo_points", {}),
            st.session_state.get("xai_demo_survey", {}),
        ),
        file_name="xai-demo-data.json",
        mime="application/json",
        width="stretch",
    )
    if st.button("Review the last comparison"):
        st.session_state.xai_demo_preference_index = len(trials) - 1
        st.rerun()
    st.stop()

trial = trials[index]
selection = responses.get(trial.trial_id)

st.progress((index + 1) / len(trials), text=f"Image set {index + 1} of {len(trials)}")

prediction_col, explanation_a_col, explanation_b_col = st.columns(3, gap="large")

with prediction_col:
    st.markdown("#### Model prediction")
    st.image(str(trial.prediction), width="stretch")
    st.caption("Use this image as the reference.")

with explanation_a_col:
    st.markdown("#### Explanation A")
    st.image(str(trial.explanation_a), width="stretch")
    if st.button(
        "Select explanation A",
        type="primary" if selection == "A" else "secondary",
        width="stretch",
    ):
        responses[trial.trial_id] = "A"
        st.rerun()

with explanation_b_col:
    st.markdown("#### Explanation B")
    st.image(str(trial.explanation_b), width="stretch")
    if st.button(
        "Select explanation B",
        type="primary" if selection == "B" else "secondary",
        width="stretch",
    ):
        responses[trial.trial_id] = "B"
        st.rerun()

if selection:
    st.success(f"You selected explanation {selection}.")
else:
    st.warning("Select one explanation before you continue.")

back_col, next_col = st.columns([1, 2])
with back_col:
    if st.button("Previous image set", disabled=index == 0, width="stretch"):
        st.session_state.xai_demo_preference_index -= 1
        st.rerun()
with next_col:
    next_label = "Finish task" if index == len(trials) - 1 else "Next image set"
    if st.button(
        next_label,
        type="primary",
        disabled=selection is None,
        width="stretch",
    ):
        st.session_state.xai_demo_preference_index += 1
        st.rerun()

with st.expander("How to read the images"):
    st.write("The first image shows the model prediction.")
    st.write("The other images show two explanation methods.")
    st.write("Bright areas show image regions that have more relevance to the prediction.")
