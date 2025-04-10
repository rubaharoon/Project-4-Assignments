import streamlit as st
from datetime import datetime, timedelta
from sq_lite import (
    init_db, add_task_to_db, get_all_tasks_from_db,
    update_task_status, delete_task_from_db, update_task_text_due
)
import random

st.set_page_config("TaskSphere", page_icon="🪐", layout="wide")

# --- Background & Styles ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0bbff, #f3e5f5);
    color: #3a0d62;
}
h1, h2, h3, label, .stTextInput, .stDateInput, .stButton, .stMarkdown {
    color: #3a0d62 !important;
}
.stCheckbox > label {
    color: #3a0d62 !important;
}
footer, .css-164nlkn {
    text-align: center;
    color: #5a0080;
    font-weight: 500;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Initialize DB ---
init_db()

# --- Header ---
quotes = [
    "Stay focused. Stay graceful.",
    "Turn chaos into clarity.",
    "Create your calm through planning.",
    "Master your minutes, own your day.",
]
st.markdown("<h1 style='text-align: center;'>🪐 TaskSphere</h1>", unsafe_allow_html=True)
st.caption(f"📅 {datetime.today().strftime('%A, %B %d')} — {random.choice(quotes)}")

# --- Task Input ---
with st.form("task_form", clear_on_submit=True):
    st.subheader("Add a Task")
    col1, col2 = st.columns([3, 2])
    task = col1.text_input("Task")
    due_date = col2.date_input("Due Date", value=datetime.today())
    submitted = st.form_submit_button("➕ Add Task")
    if submitted and task:
        add_task_to_db(task, due_date)

# --- Fetch Tasks ---
tasks = get_all_tasks_from_db()
today, tomorrow = datetime.today().date(), datetime.today().date() + timedelta(days=1)

# --- Filter Controls ---
filters = ["All", "Today", "Tomorrow", "Overdue", "Completed"]
selected_filter = st.radio("📂 Filter Tasks", filters, horizontal=True)

# --- Task Stats ---
completed = [t for t in tasks if t[3]]
pending = [t for t in tasks if not t[3]]
overdue = [t for t in tasks if not t[3] and datetime.strptime(t[2], "%Y-%m-%d").date() < today]

with st.expander("📊 Task Stats", expanded=True):
    st.markdown(f"""
    - ✅ **Completed:** {len(completed)}
    - 📌 **Pending:** {len(pending)}
    - ⏰ **Overdue:** {len(overdue)}
    - 🧾 **Total:** {len(tasks)}
    """)

# --- Display Filtered Tasks ---
def show_task(task_id, text, due, done):
    cols = st.columns([0.05, 0.55, 0.2, 0.1, 0.1])
    checked = cols[0].checkbox("", value=done, key=f"done_{task_id}")
    update_task_status(task_id, checked)

    style = "line-through;" if checked else ""
    color = "#f7c6c6" if datetime.strptime(due, "%Y-%m-%d").date() < today else "#ffffff33"
    cols[1].markdown(f"<div style='padding:8px; border-radius:8px; background-color:{color}; {style}'>{text}</div>", unsafe_allow_html=True)
    cols[2].write(f"📅 {due}")

    if cols[3].button("✏️", key=f"edit_{task_id}"):
        with st.form(f"update_{task_id}"):
            new_text = st.text_input("Update task", value=text)
            new_date = st.date_input("Update date", value=datetime.strptime(due, "%Y-%m-%d"))
            update_submit = st.form_submit_button("✅ Save")
            if update_submit:
                update_task_text_due(task_id, new_text, new_date)
                st.experimental_rerun()

    if cols[4].button("🗑️", key=f"delete_{task_id}"):
        delete_task_from_db(task_id)
        st.experimental_rerun()

# --- Filter Logic ---
filtered_tasks = []
for t in tasks:
    task_id, text, due_str, done = t
    due_date_obj = datetime.strptime(due_str, "%Y-%m-%d").date()
    match selected_filter:
        case "All":
            filtered_tasks.append(t)
        case "Today":
            if due_date_obj == today:
                filtered_tasks.append(t)
        case "Tomorrow":
            if due_date_obj == tomorrow:
                filtered_tasks.append(t)
        case "Overdue":
            if due_date_obj < today and not done:
                filtered_tasks.append(t)
        case "Completed":
            if done:
                filtered_tasks.append(t)

if filtered_tasks:
    st.subheader(f"📝 Tasks – {selected_filter}")
    for t in filtered_tasks:
        show_task(*t)
else:
    st.markdown("🌈 **No tasks to display.**")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; font-weight: 500; color: #5a0080;'>"
    "✨ TaskSphere – Orbit your goals with clarity."
    "</div>",
    unsafe_allow_html=True
)
