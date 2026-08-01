"""Task 2: mark important points on a prediction image."""

import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates

from app_utils import build_export, find_trials, load_trials

IMAGE_SIZE = 384
TRIAL_COUNT = 5


def draw_points(image_path: str, points: list[tuple[int, int]]) -> Image.Image:
    """Return a display image with a mark at each selected point."""

    with Image.open(image_path) as source:
        image = source.convert("RGB").resize((IMAGE_SIZE, IMAGE_SIZE))
    draw = ImageDraw.Draw(image)
    for x, y in points:
        radius = 7
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="#E63946")
    return image


st.set_page_config(page_title="Mark important points", page_icon="📍", layout="wide")
st.title("Task 2: Mark important points")
st.write("Mark one to three points that best explain the model prediction.")

all_trials = load_trials()
if not all_trials:
    st.warning("The app cannot find local trial images.")
    st.write("Follow the data setup instructions in `trials/README.md`.")
    st.stop()

if "xai_demo_point_trial_ids" not in st.session_state:
    st.session_state.xai_demo_point_trial_ids = [
        trial.trial_id for trial in all_trials[:TRIAL_COUNT]
    ]
if "xai_demo_point_index" not in st.session_state:
    st.session_state.xai_demo_point_index = 0
if "xai_demo_points" not in st.session_state:
    st.session_state.xai_demo_points = {}

trials = find_trials(st.session_state.xai_demo_point_trial_ids, all_trials)
index = st.session_state.xai_demo_point_index
points_by_trial = st.session_state.xai_demo_points

if index >= len(trials):
    st.success("Task 2 is complete.")
    st.write(f"You marked points on {len(points_by_trial)} images.")
    st.download_button(
        "Download demo data",
        data=build_export(
            st.session_state.get("xai_demo_preferences", {}),
            points_by_trial,
            st.session_state.get("xai_demo_survey", {}),
            IMAGE_SIZE,
        ),
        file_name="xai-demo-data.json",
        mime="application/json",
        width="stretch",
    )
    if st.button("Review the last image"):
        st.session_state.xai_demo_point_index = len(trials) - 1
        st.rerun()
    st.stop()

trial = trials[index]
points = points_by_trial.setdefault(trial.trial_id, [])

st.progress((index + 1) / len(trials), text=f"Image {index + 1} of {len(trials)}")

image_col, explanation_col = st.columns([3, 2], gap="large")
with image_col:
    st.markdown("#### Model prediction")
    marked_image = draw_points(str(trial.prediction), points)
    click = streamlit_image_coordinates(
        marked_image,
        key=f"point-{trial.trial_id}-{len(points)}",
    )
    if click is not None and len(points) < 3:
        point = (int(click["x"]), int(click["y"]))
        if point not in points:
            points.append(point)
            st.rerun()

with explanation_col:
    st.markdown("#### Explanation reference")
    st.image(str(trial.explanation_a), width=IMAGE_SIZE)
    st.caption("Use the explanation to help you select the important points.")
    st.metric("Points selected", f"{len(points)} of 3")
    if len(points) == 3:
        st.info("You selected the maximum number of points.")

clear_col, next_col = st.columns([1, 2])
with clear_col:
    if st.button("Clear points", disabled=not points, width="stretch"):
        points.clear()
        st.rerun()
with next_col:
    next_label = "Finish task" if index == len(trials) - 1 else "Save and show next image"
    if st.button(
        next_label,
        type="primary",
        disabled=not points,
        width="stretch",
    ):
        st.session_state.xai_demo_point_index += 1
        st.rerun()

st.caption("The exported point values use a scale from 0 to 1.")
