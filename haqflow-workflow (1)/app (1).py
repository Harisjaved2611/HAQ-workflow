
import streamlit as st

from demo_data import DEMO_MATCH_RESULT
from workflow import (
    generate_action_plan,
    update_task_status,
    calculate_progress,
    generate_follow_up,
    generate_human_handoff
)

st.set_page_config(page_title="HaqFlow", page_icon="📋", layout="wide")

st.title("HaqFlow")
st.subheader("Workflow & Action Plan")

if "tasks" not in st.session_state:
    st.session_state.tasks = generate_action_plan(DEMO_MATCH_RESULT)

tasks = st.session_state.tasks

st.header("Case Progress")

progress = calculate_progress(tasks)

st.progress(progress / 100)

st.write(f"**{progress}% completed**")

st.divider()

st.header("Action Plan")

for task in tasks:

    col1, col2, col3 = st.columns([5, 2, 2])

    with col1:
        st.write(f"**{task.title}**")
        st.caption(f"Program: {task.related_program_name}")

    with col2:
        st.write(f"Priority: **{task.priority}**")

    with col3:

        status_options = [
            "PENDING",
            "IN_PROGRESS",
            "COMPLETED",
            "BLOCKED"
        ]

        selected_status = st.selectbox(
            "Status",
            status_options,
            index=status_options.index(task.status),
            key=f"status_{task.id}"
        )

        if selected_status != task.status:
            update_task_status(
                tasks,
                task.id,
                selected_status
            )

            st.rerun()

st.divider()

st.header("Follow-Up")

follow_ups = generate_follow_up(tasks)

if follow_ups:

    for item in follow_ups:
        st.warning(item["message"])

else:
    st.success("No pending follow-ups.")

st.divider()

st.header("Human Handoff")

user_situation = {
    "education_level": "school student",
    "needs": ["education support"],
    "location": "Demo Location"
}

unresolved_questions = [
    "Identity document verification is still required."
]

handoff = generate_human_handoff(
    case_id="case_001",
    user_situation=user_situation,
    match_result=DEMO_MATCH_RESULT,
    tasks=tasks,
    unresolved_questions=unresolved_questions
)

st.write("**Case ID:**", handoff["case_id"])

st.write(
    "**Progress:**",
    f'{handoff["progress"]}%'
)

with st.expander("User Situation"):
    st.json(handoff["user_situation"])

with st.expander("Matched Programs"):
    st.json(handoff["matched_programs"])

with st.expander("Completed Evidence"):
    st.write(handoff["completed_evidence"])

with st.expander("Missing Evidence"):
    st.write(handoff["missing_evidence"])

with st.expander("Unresolved Questions"):
    st.write(handoff["unresolved_questions"])

with st.expander("Recommended Next Actions"):
    st.write(handoff["recommended_next_actions"])
