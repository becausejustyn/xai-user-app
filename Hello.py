"""Home page for the public XAI study demonstration."""

import streamlit as st

from app_utils import clear_demo_state

st.set_page_config(
    page_title="XAI study demo",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("XAI study demo")
st.subheader("Explore a study interface for explainable artificial intelligence")

st.info(
    "This is a software demonstration. It is not an active research study. "
    "The app does not ask for an identifier or demographic data."
)

intro, privacy = st.columns([3, 2], gap="large")

with intro:
    st.markdown(
        """
        This app shows three tasks from an earlier research prototype. The tasks use
        **explainable artificial intelligence (XAI)** images.

        1. Compare two model explanations.
        2. Mark important points on an image.
        3. Answer four questions about the explanations.

        Select a task in the sidebar. You can do the tasks in any sequence.
        """
    )

with privacy:
    st.markdown("#### Data use")
    st.write("The app keeps your responses in the current Streamlit session.")
    st.write("The app does not use a database and does not write response files.")
    st.write("You can download your responses as a JSON file.")

st.divider()

st.markdown("### About the prototype")
st.write(
    "The original app supported research about how people assess visual model "
    "explanations. The final study used Qualtrics, so this version is a public demo."
)
st.markdown(
    "The research materials for the project are in the "
    "[saliency_map_bias_user_study repository]"
    "(https://github.com/becausejustyn/saliency_map_bias_user_study)."
)

with st.expander("Limits of this demo"):
    st.write(
        "The demo does not reproduce the full study procedure. Do not use it to collect "
        "research data without the required consent text, ethics approval, and data controls."
    )

with st.sidebar:
    st.markdown("### Demo controls")
    st.caption("A reset clears data from this session.")
    if st.button("Reset all demo data", type="secondary", width="stretch"):
        clear_demo_state(st.session_state)
        st.success("The demo data is clear.")
