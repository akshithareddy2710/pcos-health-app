import streamlit as st
import joblib
import numpy as np
import shap
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title="PCOS App", layout="wide")

# ---------- LOAD MODEL ----------
model = joblib.load("pcos_model.pkl")
explainer = shap.TreeExplainer(model)

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align:center; color:#0a3d62;'>💖 PCOS Health Assistant</h1>
<p style='text-align:center; font-size:18px;'>Smart AI-based Women's Health Companion</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- LAYOUT ----------
col1, col2 = st.columns([1,1])

# ---------- LEFT SIDE ----------
with col1:
    st.markdown("## 🧪 PCOS Prediction")

    age = st.number_input("Age", min_value=0.0)
    weight = st.number_input("Weight (Kg)", min_value=0.0)
    bmi = st.number_input("BMI", min_value=0.0)

    predict = st.button("Check Health")

    if predict:

        if age <= 0 or weight <= 0 or bmi <= 0:
            st.warning("⚠️ Enter valid values")

        else:
            data = np.array([[age, weight, bmi]])

            result = model.predict(data)
            prob = model.predict_proba(data)[0][1]

            # RESULT
            if result[0] == 1:
                st.warning("⚠️ There may be a risk of PCOS")
            else:
                st.success("✅ You are in a healthy range")

            st.write(f"📊 Risk Level: {prob*100:.2f}%")

            st.markdown("---")

            # ---------- SUGGESTIONS ----------
            st.subheader("💡 Personalized Suggestions")

            if result[0] == 1:
                st.write("⚠️ Based on your result, consider the following:")
                st.write("🥗 Maintain a balanced diet (low sugar, high fiber)")
                st.write("🏃‍♀️ Exercise regularly (30–45 minutes daily)")
                st.write("🧘 Practice stress management techniques")
                st.write("💧 Stay hydrated and maintain a healthy weight")
                st.write("👩‍⚕️ Consult a gynecologist for further evaluation")
            else:
                st.write("✅ You are doing well! Keep maintaining:")
                st.write("🥗 Healthy and balanced diet")
                st.write("🏃‍♀️ Regular physical activity")
                st.write("🩺 Routine health checkups")
                st.write("😌 Stress-free lifestyle")

            st.markdown("---")

            # ---------- SHAP ----------
            st.subheader("🔍 Factors Influencing Prediction")

            shap_values = explainer.shap_values(data)

            if isinstance(shap_values, list):
                shap_vals = shap_values[1][0]
            else:
                shap_vals = shap_values[0]

            if len(shap_vals.shape) > 1:
                shap_vals = shap_vals[:, 1]

            features = ["Age", "Weight", "BMI"]

            fig, ax = plt.subplots()
            ax.barh(features, shap_vals, color=["#ff4b6e","#ff9f43","#1dd1a1"])
            ax.set_xlabel("Impact")
            ax.set_title("Feature Contribution")

            st.pyplot(fig)

# ---------- RIGHT SIDE (PREMIUM INFO UI) ----------
with col2:
    st.markdown("""
    <div style="
        background: #f8f9fc;
        padding: 30px;
        border-radius: 15px;
        color: #0a3d62;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
    ">
    
    <h4 style="color:#3c6382;">💙 Your Personal Guide to PCOS</h4>

    <h1 style="font-size:40px; margin-top:10px; color:#0a3d62;">
        Understanding PCOS
    </h1>

    <p style="font-size:16px; line-height:1.7;">
    Polycystic Ovary Syndrome (PCOS) is a common hormonal condition that affects many women during their reproductive years.
    It occurs when there is an imbalance in reproductive hormones, which can interfere with normal ovulation.
    </p>

    <p style="font-size:16px; line-height:1.7;">
    PCOS can be caused by multiple factors such as genetics, insulin resistance, and lifestyle patterns.
    These factors can lead to irregular menstrual cycles, weight gain, acne, and excessive hair growth.
    </p>

    <p style="font-size:16px; line-height:1.7;">
    If left unmanaged, PCOS may increase the risk of serious health conditions like type 2 diabetes,
    high blood pressure, and heart-related issues.
    It can also impact emotional well-being and confidence.
    </p>

    <p style="font-size:16px; line-height:1.7;">
    Early detection is very important. A PCOS test helps identify symptoms at an early stage,
    allowing timely lifestyle changes and medical support.
    </p>

    <p style="font-size:16px; line-height:1.7;">
    With proper care, including a balanced diet, regular exercise, and medical guidance,
    PCOS can be effectively managed and controlled.
    </p>

    <p style="font-size:16px; line-height:1.7;">
    This application is designed to help you understand your health better and take proactive steps
    towards a healthier and more balanced life.
    </p>

    </div>
    """, unsafe_allow_html=True)