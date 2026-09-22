
import os
from io import BytesIO

import numpy as np
import pandas as pd
import streamlit as st

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Insights | PCOS Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    possible_files = [
        "PCOS_data.csv",
        "pcos_data.csv",
        "PCOS_data_cleaned.csv",
        "pcos_dataset.csv",
    ]

    for file in possible_files:
        if os.path.exists(file):
            try:
                data = pd.read_csv(file)
                if not data.empty:
                    return data
            except Exception:
                pass

    return None


df = load_data()

if df is None:
    st.error("PCOS_data.csv was not found. Please keep it in the repository root.")
    st.stop()


# ============================================================
# COLUMN HELPERS
# ============================================================

def find_column(possible_names):
    normalized = {
        str(col).strip().lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", ""): col
        for col in df.columns
    }

    for name in possible_names:
        key = (
            str(name).strip().lower()
            .replace(" ", "")
            .replace("_", "")
            .replace("-", "")
        )
        if key in normalized:
            return normalized[key]

    return None


def numeric_column(possible_names):
    col = find_column(possible_names)
    if col is not None:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return col


def binary_value(value):
    if pd.isna(value):
        return np.nan

    text = str(value).strip().lower()

    if text in {"1", "yes", "y", "true", "positive", "pcos"}:
        return 1
    if text in {"0", "no", "n", "false", "negative", "non-pcos"}:
        return 0

    try:
        number = float(text)
        if number in (0, 1):
            return int(number)
    except Exception:
        pass

    return np.nan


AGE_COL = numeric_column(["Age", "Age (yrs)", "Age (years)"])
WEIGHT_COL = numeric_column(["Weight (Kg)", "Weight (kg)", "Weight"])
HEIGHT_COL = numeric_column(["Height(Cm)", "Height (cm)", "Height"])
BMI_COL = numeric_column(["BMI"])

PCOS_COL = find_column([
    "PCOS (Y/N)",
    "PCOS",
    "PCOS Y/N",
    "PCOS(Y/N)",
])

CYCLE_COL = find_column([
    "Cycle(R/I)",
    "Cycle (R/I)",
    "Cycle",
])

SYMPTOM_COLUMNS = {
    "Weight Gain": find_column([
        "Weight gain(Y/N)",
        "Weight Gain",
        "Weight gain",
    ]),
    "Hair Growth": find_column([
        "hair growth(Y/N)",
        "Hair Growth",
    ]),
    "Skin Darkening": find_column([
        "Skin darkening (Y/N)",
        "Skin Darkening",
    ]),
    "Hair Loss": find_column([
        "Hair loss(Y/N)",
        "Hair Loss",
    ]),
    "Pimples": find_column([
        "Pimples(Y/N)",
        "Pimples",
    ]),
}

if PCOS_COL:
    df["_PCOS"] = df[PCOS_COL].apply(binary_value)
else:
    df["_PCOS"] = np.nan


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #f7f8fc;
    margin-bottom: 3px;
}

.main-subtitle {
    color: #aebbd0;
    font-size: 16px;
    margin-bottom: 22px;
}

.section-title {
    font-size: 27px;
    font-weight: 750;
    color: #f7f8fc;
    margin-top: 27px;
    margin-bottom: 4px;
}

.section-caption {
    color: #8fa3bd;
    font-size: 14px;
    margin-bottom: 14px;
}

.snapshot-card {
    background: #102945;
    border: 1px solid #28547d;
    border-radius: 14px;
    padding: 17px;
    min-height: 118px;
}

.snapshot-label {
    color: #9fb2c9;
    font-size: 13px;
}

.snapshot-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
    margin-top: 7px;
}

.snapshot-note {
    color: #8fa3bd;
    font-size: 12px;
    margin-top: 4px;
}

.insight-card {
    background: #102945;
    border: 1px solid #28547d;
    border-radius: 15px;
    padding: 19px;
    min-height: 175px;
}

.insight-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 9px;
}

.insight-text {
    color: #c3cfde;
    font-size: 14px;
    line-height: 1.65;
}

.overall-card {
    background: linear-gradient(135deg, #162d49, #101e34);
    border: 1px solid #3c638b;
    border-radius: 17px;
    padding: 23px;
}

.overall-status {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 8px;
}

.overall-text {
    color: #cbd5e1;
    line-height: 1.65;
    font-size: 15px;
}

.reason-card {
    background: #0d2239;
    border: 1px solid #24486c;
    border-radius: 11px;
    padding: 13px 15px;
    color: #cbd5e1;
    margin-bottom: 8px;
}

.recommend-card {
    background: #102945;
    border: 1px solid #28547d;
    border-radius: 15px;
    padding: 19px;
    min-height: 185px;
}

.recommend-title {
    color: #ffffff;
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 10px;
}

.recommend-text {
    color: #c3cfde;
    font-size: 14px;
    line-height: 1.7;
}

.disclaimer {
    background: #301a31;
    border: 1px solid #734066;
    border-radius: 13px;
    padding: 16px 19px;
    color: #e3cadf;
    font-size: 13px;
    line-height: 1.55;
    margin-top: 26px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI Insights</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">Understand your PCOS-related health information in simple, data-driven language.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# PATIENT INPUTS
# ============================================================

st.markdown(
    '<div class="section-title">👩 Your Health Information</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">Enter information you normally know about yourself. No laboratory or ultrasound values are required.</div>',
    unsafe_allow_html=True,
)

input_container = st.container()
with input_container:
    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input(
            "Age (years)",
            min_value=10,
            max_value=80,
            value=25,
            step=1,
        )

    with c2:
        height_cm = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=220.0,
            value=160.0,
            step=0.5,
        )

    with c3:
        weight_kg = st.number_input(
            "Weight (kg)",
            min_value=20.0,
            max_value=200.0,
            value=55.0,
            step=0.5,
        )

    cycle_options = [
        "Regular",
        "Irregular",
        "Not sure",
    ]

    cycle = st.selectbox(
        "Menstrual Cycle",
        cycle_options,
        help="Choose the option that best describes your usual cycle.",
    )

    st.markdown("**Symptoms**")

    symptom_cols = st.columns(5)
    selected_symptoms = []

    for i, symptom in enumerate(SYMPTOM_COLUMNS.keys()):
        with symptom_cols[i]:
            if st.checkbox(symptom, key=f"ai_symptom_{i}"):
                selected_symptoms.append(symptom)

    analyze = st.button(
        "🔍 Analyze My Health",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# CALCULATE BMI
# ============================================================

height_m = height_cm / 100
calculated_bmi = weight_kg / (height_m ** 2)


def bmi_category(value):
    if value < 18.5:
        return "Below standard BMI range"
    if value < 25:
        return "Within standard BMI range"
    if value < 30:
        return "Above standard BMI range"
    return "Higher BMI range"


# ============================================================
# ANALYSIS HELPERS
# ============================================================

def median_for_group(column, mask):
    if column is None or column not in df.columns:
        return None

    values = pd.to_numeric(df.loc[mask, column], errors="coerce").dropna()

    if values.empty:
        return None

    return float(values.median())


def symptom_rate(column, mask):
    if column is None or column not in df.columns:
        return None

    values = df.loc[mask, column].apply(binary_value).dropna()

    if values.empty:
        return None

    return float(values.mean() * 100)


def snapshot_card(label, value, note):
    st.markdown(
        f"""
        <div class="snapshot-card">
            <div class="snapshot-label">{label}</div>
            <div class="snapshot-value">{value}</div>
            <div class="snapshot-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(icon, title, text):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{icon} {title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ANALYZE
# ============================================================

if analyze:
    st.session_state["ai_result"] = {
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": calculated_bmi,
        "cycle": cycle,
        "symptoms": selected_symptoms,
    }


if "ai_result" not in st.session_state:
    st.info(
        "Enter your information above and select **Analyze My Health** to generate your insight."
    )
    st.stop()


result = st.session_state["ai_result"]

age = result["age"]
height_cm = result["height_cm"]
weight_kg = result["weight_kg"]
calculated_bmi = result["bmi"]
cycle = result["cycle"]
selected_symptoms = result["symptoms"]


# ============================================================
# DATA GROUPS
# ============================================================

pcos_mask = df["_PCOS"] == 1
non_pcos_mask = df["_PCOS"] == 0

bmi_pcos = median_for_group(BMI_COL, pcos_mask)
bmi_non_pcos = median_for_group(BMI_COL, non_pcos_mask)

# Dataset cycle distribution among PCOS-positive records.
pcos_cycle_values = None
if CYCLE_COL:
    pcos_cycle_values = (
        df.loc[pcos_mask, CYCLE_COL]
        .astype(str)
        .str.strip()
        .str.upper()
    )


# ============================================================
# HEALTH SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-title">🩺 Your Health Snapshot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">A quick summary calculated from the information you entered.</div>',
    unsafe_allow_html=True,
)

snapshot_columns = st.columns(4)

with snapshot_columns[0]:
    snapshot_card(
        "BMI",
        f"{calculated_bmi:.1f}",
        bmi_category(calculated_bmi),
    )

with snapshot_columns[1]:
    snapshot_card(
        "Age",
        str(age),
        "Years",
    )

with snapshot_columns[2]:
    snapshot_card(
        "Cycle",
        cycle,
        "Your selection",
    )

with snapshot_columns[3]:
    snapshot_card(
        "Symptoms",
        str(len(selected_symptoms)),
        "Selected",
    )


# ============================================================
# WHAT YOUR DATA MAY INDICATE
# ============================================================

st.markdown(
    '<div class="section-title">🔎 What Your Data May Indicate</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">The application compares your information with patterns in the available PCOS dataset. These comparisons are not a diagnosis.</div>',
    unsafe_allow_html=True,
)

findings_left, findings_right = st.columns(2)

with findings_left:
    if bmi_pcos is not None and bmi_non_pcos is not None:
        if abs(calculated_bmi - bmi_pcos) < abs(calculated_bmi - bmi_non_pcos):
            bmi_text = (
                f"Your calculated BMI is <b>{calculated_bmi:.1f}</b>. "
                f"In this dataset, it is closer to the PCOS-positive group median "
                f"of <b>{bmi_pcos:.1f}</b> than the PCOS-negative group median "
                f"of <b>{bmi_non_pcos:.1f}</b>."
            )
        else:
            bmi_text = (
                f"Your calculated BMI is <b>{calculated_bmi:.1f}</b>. "
                f"The dataset medians are <b>{bmi_pcos:.1f}</b> for PCOS-positive "
                f"records and <b>{bmi_non_pcos:.1f}</b> for PCOS-negative records."
            )
    else:
        bmi_text = (
            f"Your calculated BMI is <b>{calculated_bmi:.1f}</b>. "
            "A complete dataset comparison is not available."
        )

    insight_card("⚖️", "BMI Pattern", bmi_text)

with findings_right:
    if cycle == "Regular":
        cycle_text = (
            "You selected a regular cycle. Regularity is one part of health information "
            "and should be considered together with symptoms and other clinical information."
        )
    elif cycle == "Irregular":
        cycle_text = (
            "You selected an irregular cycle. Irregular cycles can occur for several reasons, "
            "including PCOS, and should not be used alone to identify a condition."
        )
    else:
        cycle_text = (
            "You selected 'Not sure'. If your cycle pattern is difficult to determine, "
            "tracking it over time can provide useful information for a healthcare professional."
        )

    insight_card("🩸", "Menstrual Pattern", cycle_text)

with findings_left:
    if selected_symptoms:
        symptom_text = (
            f"You selected <b>{len(selected_symptoms)}</b> symptom(s): "
            f"<b>{', '.join(selected_symptoms)}</b>. "
            "These symptoms may occur with PCOS but can also have other causes."
        )
    else:
        symptom_text = (
            "You did not select any of the listed symptoms. "
            "The absence of selected symptoms does not by itself rule out PCOS."
        )

    insight_card("🌸", "Symptoms", symptom_text)

with findings_right:
    if selected_symptoms:
        available_rates = []

        for symptom in selected_symptoms:
            column = SYMPTOM_COLUMNS.get(symptom)
            rate = symptom_rate(column, pcos_mask)
            if rate is not None:
                available_rates.append((symptom, rate))

        if available_rates:
            most_common = max(available_rates, key=lambda x: x[1])
            symptom_data_text = (
                f"Among PCOS-positive records in this dataset, "
                f"<b>{most_common[0]}</b> appears in approximately "
                f"<b>{most_common[1]:.0f}%</b> of records."
            )
        else:
            symptom_data_text = (
                "The selected symptoms could not be compared with the dataset."
            )
    else:
        symptom_data_text = (
            "Select symptoms above to see how they compare with the available dataset."
        )

    insight_card("📊", "Dataset Context", symptom_data_text)


# ============================================================
# OVERALL INSIGHT
# ============================================================

evidence = []

if bmi_pcos is not None and bmi_non_pcos is not None:
    if abs(calculated_bmi - bmi_pcos) < abs(calculated_bmi - bmi_non_pcos):
        evidence.append("BMI is closer to the PCOS-positive group median in this dataset.")

if cycle == "Irregular" and pcos_cycle_values is not None:
    irregular_values = {"I", "IRREGULAR", "IRREGULAR "}
    irregular_rate = pcos_cycle_values.isin(irregular_values).mean() * 100
    if irregular_rate >= 50:
        evidence.append(
            f"Irregular cycles are common in the PCOS-positive records in this dataset "
            f"({irregular_rate:.0f}%)."
        )

for symptom in selected_symptoms:
    rate = symptom_rate(SYMPTOM_COLUMNS.get(symptom), pcos_mask)
    if rate is not None and rate >= 50:
        evidence.append(
            f"{symptom} is reported by at least half of the PCOS-positive records in this dataset."
        )

st.markdown(
    '<div class="section-title">🚦 Overall Insight</div>',
    unsafe_allow_html=True,
)

if len(evidence) >= 3:
    status = "🟡 Several Dataset Patterns Overlap"
    status_color = "#ffd166"
    overall_text = (
        "Several of the characteristics you entered overlap with patterns observed "
        "in the PCOS-positive portion of this dataset. This is only a data comparison "
        "and does not mean that you have PCOS."
    )
elif len(evidence) >= 1:
    status = "🔵 Some Dataset Patterns Overlap"
    status_color = "#67b7ff"
    overall_text = (
        "Some of the characteristics you entered overlap with patterns observed in "
        "the dataset. The available information cannot confirm or exclude PCOS."
    )
else:
    status = "🟢 Limited Dataset Overlap"
    status_color = "#68e0b0"
    overall_text = (
        "The information you entered does not show strong overlap with the comparison "
        "patterns used from this dataset. This does not rule out PCOS."
    )

st.markdown(
    f"""
    <div class="overall-card">
        <div class="overall-status" style="color:{status_color};">{status}</div>
        <div class="overall-text">{overall_text}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WHY THIS INSIGHT?
# ============================================================

st.markdown(
    '<div class="section-title">💡 Why This Insight?</div>',
    unsafe_allow_html=True,
)

reasons = [
    "Your BMI was calculated automatically from your height and weight.",
    "Your menstrual-cycle selection was considered.",
    "Your selected symptoms were considered.",
    "Your information was compared with patterns in the available dataset.",
]

for reason in reasons:
    st.markdown(
        f'<div class="reason-card">✓ {reason}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# WHAT YOU CAN DO NEXT
# ============================================================

st.markdown(
    '<div class="section-title">🩺 What You Can Do Next</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-caption">General educational guidance, not a personalized medical prescription.</div>',
    unsafe_allow_html=True,
)

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(
        """
        <div class="recommend-card">
            <div class="recommend-title">🌱 Lifestyle</div>
            <div class="recommend-text">
                ✓ Maintain regular physical activity.<br>
                ✓ Follow a balanced diet.<br>
                ✓ Maintain healthy sleep habits.<br>
                ✓ Focus on sustainable healthy habits.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2:
    st.markdown(
        """
        <div class="recommend-card">
            <div class="recommend-title">🩺 When to Seek Advice</div>
            <div class="recommend-text">
                ✓ Discuss persistent or concerning symptoms with a qualified healthcare professional.<br>
                ✓ Share your cycle and symptom history during your consultation.<br>
                ✓ Follow professional medical advice.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r3:
    st.markdown(
        """
        <div class="recommend-card">
            <div class="recommend-title">📋 Keep Track</div>
            <div class="recommend-text">
                ✓ Track menstrual cycles.<br>
                ✓ Track changes in symptoms.<br>
                ✓ Track weight changes if useful.<br>
                ✓ Keep relevant medical reports for clinical visits.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PDF REPORT
# ============================================================

st.markdown(
    '<div class="section-title">📄 Insight Report</div>',
    unsafe_allow_html=True,
)

if REPORTLAB_AVAILABLE:
    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=colors.HexColor("#17324D"),
        spaceAfter=15,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#333333"),
    )

    report_story = [
        Paragraph("PCOS AI Insights Report", title_style),
        Paragraph(
            "Educational, data-driven interpretation based on the information entered into the application.",
            body_style,
        ),
        Spacer(1, 12),
    ]

    report_data = [
        ["Measure", "Entered / Calculated Value"],
        ["Age", f"{age} years"],
        ["Height", f"{height_cm:.1f} cm"],
        ["Weight", f"{weight_kg:.1f} kg"],
        ["BMI", f"{calculated_bmi:.1f}"],
        ["BMI Category", bmi_category(calculated_bmi)],
        ["Menstrual Cycle", cycle],
        [
            "Symptoms",
            ", ".join(selected_symptoms) if selected_symptoms else "None selected",
        ],
    ]

    report_table = Table(report_data, colWidths=[170, 300])

    report_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C7D2DE")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F3F7FA")],
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    report_story.extend(
        [
            report_table,
            Spacer(1, 16),
            Paragraph(f"<b>Overall insight:</b> {status}", body_style),
            Spacer(1, 8),
            Paragraph(overall_text, body_style),
            Spacer(1, 12),
        ]
    )

    if evidence:
        report_story.append(
            Paragraph("<b>Data observations:</b>", body_style)
        )
        for item in evidence:
            report_story.append(
                Paragraph("• " + item, body_style)
            )

    report_story.extend(
        [
            Spacer(1, 18),
            Paragraph(
                "<b>Medical Disclaimer:</b> This report is for educational purposes only. "
                "It is not intended to diagnose, treat, cure, or prevent PCOS or any other "
                "medical condition. Please consult a qualified healthcare professional.",
                body_style,
            ),
        ]
    )

    document.build(report_story)
    pdf_buffer.seek(0)

    st.download_button(
        "📥 Download Insight Report",
        data=pdf_buffer,
        file_name="PCOS_AI_Insight_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
else:
    st.info(
        "PDF download requires ReportLab. Add `reportlab` to requirements.txt."
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.markdown(
    """
    <div class="disclaimer">
        <b>⚠️ Medical Disclaimer:</b>
        This application provides educational, data-driven insights based on the
        available dataset and information entered by the user. It is not intended
        to diagnose, treat, cure, or prevent PCOS or any other medical condition.
        Clinical decisions should always be made with a qualified healthcare professional.
    </div>
    """,
    unsafe_allow_html=True,
)
