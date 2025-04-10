import streamlit as st
import matplotlib.pyplot as plt
from sq_lite import create_user_table, create_bmi_table, add_user_data, add_bmi_record, get_bmi_history
from pdf_report import generate_pdf_report
from health_tips import get_random_tip

# ---- Config ----
st.set_page_config(page_title="FitTrack: Your BMI Buddy", page_icon="💪", layout="centered")

color_theme = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #ffe6f0;
}
.stButton > button {
    background-color: #ff66b2;
    color: white;
    border: None;
    padding: 10px 20px;
    border-radius: 10px;
}
.stButton > button:hover {
    background-color: #ff3385;
}
</style>
"""
st.markdown(color_theme, unsafe_allow_html=True)

# ---- DB Setup ----
create_user_table()
create_bmi_table()

# ---- Session ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---- Login ----
if not st.session_state.logged_in:
    with st.form("login_form"):
        st.markdown("## 👤 Login to access **FitTrack**")
        name = st.text_input("Name")
        email = st.text_input("Email")
        login_btn = st.form_submit_button("🔐 Continue")

    if login_btn:
        if name.strip() == "" or email.strip() == "":
            st.error("Please enter both name and email.")
        else:
            add_user_data(name, email)
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.success(f"Welcome {name}! Redirecting to your dashboard...")

# ---- Dashboard ----
if st.session_state.logged_in:
    st.markdown(f"<h2 style='text-align: center; color: #ff3385;'>Welcome, {st.session_state.user_name} 💖</h2>", unsafe_allow_html=True)
    st.markdown("### 📊 Let's calculate your BMI")

    with st.form("bmi_form"):
        gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
        age = st.number_input("Age", min_value=1, max_value=120)
        height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0)
        weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=300.0)
        calculate = st.form_submit_button("🔥 Calculate BMI")

    def calculate_bmi(weight, height_cm):
        height_m = height_cm / 100
        return round(weight / (height_m ** 2), 2)

    def get_bmi_category(bmi):
        if bmi < 18.5:
            return "Underweight", "🦴", "You might want to gain some healthy weight."
        elif 18.5 <= bmi < 24.9:
            return "Normal", "💪", "You're doing great! Keep it up!"
        elif 25 <= bmi < 29.9:
            return "Overweight", "🏋️", "Time to balance nutrition and exercise."
        else:
            return "Obese", "🍔", "Work on small lifestyle changes for long-term health."

    def age_gender_tip(age, gender):
        if age < 18:
            return "Make sure to consult a doctor for child-specific advice."
        if gender == "Female" and age > 40:
            return "Consider bone health and calcium intake."
        if gender == "Male" and age > 40:
            return "Stay active to manage metabolism changes."
        return "Stay hydrated, eat clean, and get enough sleep."

    if calculate:
        bmi = calculate_bmi(weight, height)
        category, emoji, tip = get_bmi_category(bmi)
        user_tip = age_gender_tip(age, gender)

        add_bmi_record(st.session_state.user_name, bmi, age, gender)

        st.success(f"✅ Your BMI is **{bmi}**")
        st.markdown(f"### Category: **{category}** {emoji}")
        st.markdown(f"💡 **General Tip:** _{tip}_")
        st.markdown(f"👨‍⚕️ **Based on Age/Gender:** _{user_tip}_")

        if st.button("📄 Generate PDF Report"):
            generate_pdf_report(st.session_state.user_name, bmi, category, tip)
            st.success("✅ PDF Report saved successfully!")

    # ---- Charts & History ----
    st.markdown("## 📈 Your BMI History")

    history = get_bmi_history(st.session_state.user_name)
    if history:
        dates, bmis = zip(*history)
        fig, ax = plt.subplots()
        ax.plot(dates, bmis, marker="o", color="#ff3385")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.set_title("BMI Progress Over Time")
        st.pyplot(fig)
    else:
        st.info("No previous BMI records found.")

    # ---- Daily Health Tip ----
    st.markdown("## 🌿 Daily Health Tip")
    st.success(get_random_tip())

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ by Ruba Haroon></p>", unsafe_allow_html=True)
