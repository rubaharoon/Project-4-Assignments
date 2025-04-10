import streamlit as st
import math

st.set_page_config(page_title="MathSphere Calculator", page_icon="🧮", layout="wide")

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
.stButton>button {
    background-color: #6a57d8;
    color: white;
    font-size: 16px;
    border-radius: 8px;
}
.stButton>button:hover {
    background-color: #5a49b8;
}
footer, .css-164nlkn {
    text-align: center;
    color: #5a0080;
    font-weight: 500;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🧮 MathSphere Calculator</h1>", unsafe_allow_html=True)
st.caption("✨ Make your calculations easier and more fun!")

# --- Function to Perform Calculations ---
def calculate(num1, num2, operation):
    try:
        if operation == "Add":
            return num1 + num2
        elif operation == "Subtract":
            return num1 - num2
        elif operation == "Multiply":
            return num1 * num2
        elif operation == "Divide":
            return num1 / num2 if num2 != 0 else "Error: Division by 0"
        elif operation == "Power":
            return math.pow(num1, num2)
        elif operation == "Modulus":
            return num1 % num2
        elif operation == "Square Root":
            return math.sqrt(num1) if num1 >= 0 else "Error: Negative number for sqrt"
    except Exception as e:
        return f"Error: {str(e)}"

# --- Input Fields & Operations ---
st.sidebar.header("Enter Numbers and Select Operation")
num1 = st.sidebar.number_input("Enter first number", value=0.0)
num2 = st.sidebar.number_input("Enter second number", value=0.0)
operation = st.sidebar.selectbox("Select operation", ["Add", "Subtract", "Multiply", "Divide", "Power", "Modulus", "Square Root"])

# --- Calculate Button ---
if st.sidebar.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.write(f"**Result**: {result}")

# --- Advanced Features ---
st.subheader("Want to try advanced calculations?")
advanced_ops = ["Exponentiation", "Logarithm"]
advanced_choice = st.selectbox("Choose Advanced Operation", advanced_ops)

if advanced_choice == "Exponentiation":
    exp_base = st.number_input("Base for Exponentiation", value=2.0)
    exp_power = st.number_input("Exponent", value=3.0)
    if st.button("Calculate Exponentiation"):
        exp_result = math.pow(exp_base, exp_power)
        st.write(f"**Result**: {exp_result}")

elif advanced_choice == "Logarithm":
    log_num = st.number_input("Number for Logarithm", value=10.0)
    log_base = st.number_input("Base for Logarithm", value=10.0)
    if st.button("Calculate Logarithm"):
        try:
            log_result = math.log(log_num, log_base)
            st.write(f"**Result**: {log_result}")
        except ValueError:
            st.write("Error: Invalid logarithm calculation.")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; font-weight: 500; color: #5a0080;'>"
    "✨MathSphere Calculator – Make calculations fun!"
    "</div>",
    unsafe_allow_html=True
)
