
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
    REPORTLAB = True
except Exception:
    REPORTLAB = False

st.set_page_config(
    page_title="AI Insights | PCOS Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- DATA --------------------

def load_data():
    for p in ["PCOS_data.csv", "data/PCOS_data.csv", "../PCOS_data.csv"]:
        if os.path.exists(p):
            try:
                return pd.read_csv(p)
            except Exception:
                pass
    return None

df = load_data()
if df is None:
    st.error("PCOS_data.csv was not found in the repository root.")
    st.stop()

def find_col(names):
    lookup = {}
    for c in df.columns:
        k = str(c).strip().lower().replace(" ", "").replace("_", "").replace("-", "")
        lookup[k] = c
    for name in names:
        k = str(name).strip().lower().replace(" ", "").replace("_", "").replace("-", "")
        if k in lookup:
            return lookup[k]
    return None

def num_col(names):
    c = find_col(names)
    if c:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return c

def binary(v):
    if pd.isna(v):
        return np.nan
    s = str(v).strip().lower()
    if s in {"1","yes","y","true","positive","pcos"}: return 1
    if s in {"0","no","n","false","negative","non-pcos"}: return 0
    try:
        x = float(s)
        return int(x) if x in (0,1) else np.nan
    except Exception:
        return np.nan

AGE = num_col(["Age","Age (yrs)","Age (years)"])
BMI = num_col(["BMI","BMI (kg/m2)","BMI (kg/m²)"])
WEIGHT = num_col(["Weight","Weight (kg)","Weight (Kg)"])
LH = num_col(["LH(mIU/mL)","LH","LH (mIU/mL)"])
FSH = num_col(["FSH(mIU/mL)","FSH","FSH (mIU/mL)"])
LEFT_F = num_col(["Follicle No. (L)","Follicle No (L)","Left Follicle Count","Follicle Count Left"])
RIGHT_F = num_col(["Follicle No. (R)","Follicle No (R)","Right Follicle Count","Follicle Count Right"])
PCOS = find_col(["PCOS (Y/N)","PCOS","PCOS Y/N","PCOS(Y/N)"])
df["_pcos"] = df[PCOS].apply(binary) if PCOS else np.nan

SYMPTOMS = {
    "Weight Gain": find_col(["Weight gain(Y/N)","Weight Gain","Weight gain"]),
    "Hair Growth": find_col(["hair growth(Y/N)","Hair Growth","Hair Growth (Hirsutism)"]),
    "Skin Darkening": find_col(["Skin darkening (Y/N)","Skin Darkening","Skin darkening"]),
    "Hair Loss": find_col(["Hair loss(Y/N)","Hair Loss","Hair loss"]),
    "Pimples": find_col(["Pimples(Y/N)","Pimples","Pimples (Acne)"]),
}

# -------------------- DESIGN --------------------

st.markdown("""
<style>
.main-title{font-size:42px;font-weight:800;color:#f7f8fc;margin-bottom:2px}
.sub{font-size:16px;color:#aebbd0;margin-bottom:22px}
.section{font-size:27px;font-weight:750;color:#f7f8fc;margin:28px 0 4px}
.caption{font-size:14px;color:#8fa3bd;margin-bottom:14px}
.card{background:#102945;border:1px solid #28547d;border-radius:15px;padding:18px;min-height:165px}
.card h4{color:#fff;margin:0 0 10px;font-size:17px}
.card p{color:#c3cfde;line-height:1.6;font-size:14px;margin:0}
.snap{background:#102945;border:1px solid #28547d;border-radius:14px;padding:16px;min-height:110px}
.snap-label{color:#9fb2c9;font-size:13px}.snap-value{color:#fff;font-size:28px;font-weight:800;margin-top:7px}.snap-note{color:#8fa3bd;font-size:12px}
.overall{background:linear-gradient(135deg,#162d49,#101e34);border:1px solid #3c638b;border-radius:17px;padding:22px}
.overall h3{color:#ffd166;margin:0 0 8px}.overall p{color:#cbd5e1;line-height:1.65}
.reason{background:#0d2239;border:1px solid #24486c;border-radius:11px;padding:12px;color:#cbd5e1;margin-bottom:8px}
.rec{background:#102945;border:1px solid #28547d;border-radius:15px;padding:19px;min-height:190px}
.rec h4{color:#fff}.rec p{color:#c3cfde;line-height:1.7;font-size:14px}
.disc{background:#301a31;border:1px solid #734066;border-radius:13px;padding:16px;color:#e3cadf;font-size:13px;line-height:1.55;margin-top:25px}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Understand your PCOS-related health information in simple, data-driven language.</div>', unsafe_allow_html=True)

# -------------------- INPUT --------------------

st.markdown('<div class="section">👩 Your Health Information</div>', unsafe_allow_html=True)
st.markdown('<div class="caption">Enter the information you want the application to analyze.</div>', unsafe_allow_html=True)

with st.container(border=True):
    c1,c2,c3 = st.columns(3)
    with c1:
        age = st.number_input("Age (years)", 10, 80, 25, 1)
        weight = st.number_input("Weight (kg)", 20.0, 200.0, 55.0, 0.5)
    with c2:
        bmi = st.number_input("BMI", 10.0, 60.0, 24.5, 0.1)
        lh = st.number_input("LH Level (mIU/mL)", 0.0, 100.0, 10.0, 0.1)
    with c3:
        fsh = st.number_input("FSH Level (mIU/mL)", 0.0, 100.0, 6.0, 0.1)
        follicles = st.number_input("Total Follicle Count", 0, 100, 12, 1)

    st.markdown("**Symptoms**")
    sc = st.columns(5)
    selected = []
    for i,name in enumerate(SYMPTOMS):
        with sc[i]:
            if st.checkbox(name):
                selected.append(name)

    analyze = st.button("🔍 Analyze My Health", type="primary", use_container_width=True)

if analyze:
    st.session_state["ai_run"] = True
    st.session_state["ai_data"] = dict(age=age,weight=weight,bmi=bmi,lh=lh,fsh=fsh,follicles=follicles,selected=selected)

if not st.session_state.get("ai_run"):
    st.info("Enter your information above and select **Analyze My Health** to see your data-driven insight.")
    st.stop()

v = st.session_state["ai_data"]
age,weight,bmi,lh,fsh,follicles,selected = v["age"],v["weight"],v["bmi"],v["lh"],v["fsh"],v["follicles"],v["selected"]

def median(col, mask):
    if not col or col not in df.columns: return None
    s = pd.to_numeric(df.loc[mask,col], errors="coerce").dropna()
    return float(s.median()) if len(s) else None

pos = df["_pcos"] == 1
neg = df["_pcos"] == 0

# -------------------- SNAPSHOT --------------------

st.markdown('<div class="section">🩺 Your Health Snapshot</div>', unsafe_allow_html=True)
st.markdown('<div class="caption">A quick summary of the information you entered.</div>', unsafe_allow_html=True)

ratio = lh/fsh if fsh else None
snap = st.columns(4)
items = [
    ("BMI",f"{bmi:.1f}","Entered value"),
    ("LH / FSH",f"{ratio:.2f}" if ratio is not None else "—","Calculated"),
    ("Symptoms",str(len(selected)),"Selected"),
    ("Follicles",str(follicles),"Entered count"),
]
for col,(label,val,note) in zip(snap,items):
    with col:
        st.markdown(f'<div class="snap"><div class="snap-label">{label}</div><div class="snap-value">{val}</div><div class="snap-note">{note}</div></div>',unsafe_allow_html=True)

# -------------------- FINDINGS --------------------

bmi_pos,bmi_neg = median(BMI,pos),median(BMI,neg)
lh_pos,lh_neg = median(LH,pos),median(LH,neg)
fsh_pos,fsh_neg = median(FSH,pos),median(FSH,neg)
lf_pos,rf_pos = median(LEFT_F,pos),median(RIGHT_F,pos)

def insight(icon,title,text):
    st.markdown(f'<div class="card"><h4>{icon} {title}</h4><p>{text}</p></div>',unsafe_allow_html=True)

st.markdown('<div class="section">🔎 What Your Data May Indicate</div>', unsafe_allow_html=True)
st.markdown('<div class="caption">These are comparisons with patterns in the available dataset, not a medical diagnosis.</div>', unsafe_allow_html=True)

a,b = st.columns(2)
with a:
    if bmi_pos is not None and bmi_neg is not None:
        text=f"Your BMI is <b>{bmi:.1f}</b>. The dataset median is {bmi_pos:.1f} for PCOS-positive records and {bmi_neg:.1f} for PCOS-negative records."
    else:
        text=f"Your entered BMI is <b>{bmi:.1f}</b>. A complete dataset comparison is not available."
    insight("⚖️","BMI Pattern",text)
with b:
    if lh_pos is not None and lh_neg is not None:
        text=f"Your LH is <b>{lh:.1f}</b> and FSH is <b>{fsh:.1f}</b>. Median LH is {lh_pos:.1f} in PCOS-positive records and {lh_neg:.1f} in PCOS-negative records."
    else:
        text=f"Your LH is <b>{lh:.1f}</b> and FSH is <b>{fsh:.1f}</b>. Both are considered with the other information."
    insight("🩸","Hormonal Pattern",text)
with a:
    if selected:
        text=f"You selected <b>{len(selected)}</b> symptom(s): <b>{', '.join(selected)}</b>. These symptoms can occur with PCOS but can also have other causes."
    else:
        text="No symptoms were selected. Symptoms are only one part of a clinical assessment."
    insight("🌸","Symptoms",text)
with b:
    text=f"You entered a total follicle count of <b>{follicles}</b>. Ultrasound findings should be interpreted with the full clinical report."
    if lf_pos is not None and rf_pos is not None:
        text += f" The PCOS-positive records have median left/right counts of {lf_pos:.1f}/{rf_pos:.1f}."
    insight("🥚","Follicles",text)

# -------------------- OVERALL --------------------

evidence=[]
if bmi_pos is not None and bmi_neg is not None and abs(bmi-bmi_pos)<abs(bmi-bmi_neg):
    evidence.append("BMI is closer to the PCOS-positive group median in this dataset.")
if lh_pos is not None and lh_neg is not None and abs(lh-lh_pos)<abs(lh-lh_neg):
    evidence.append("LH is closer to the PCOS-positive group median in this dataset.")
if fsh_pos is not None and fsh_neg is not None and abs(fsh-fsh_pos)<abs(fsh-fsh_neg):
    evidence.append("FSH is closer to the PCOS-positive group median in this dataset.")
if lf_pos is not None and rf_pos is not None and follicles >= max(lf_pos,rf_pos):
    evidence.append("The entered follicle count is at or above the PCOS-positive group medians used for comparison.")

st.markdown('<div class="section">🚦 Overall Insight</div>', unsafe_allow_html=True)
if len(evidence)>=3:
    status="🟡 Further Evaluation Recommended"
    text="Several entered characteristics overlap with patterns observed in the PCOS-positive portion of this dataset. This is a dataset comparison, not a diagnosis."
elif evidence:
    status="🔵 Some Patterns Overlap"
    text="Some entered characteristics overlap with patterns observed in the dataset. The available information alone cannot confirm or exclude PCOS."
else:
    status="🟢 No Strong Dataset Overlap Identified"
    text="The entered characteristics do not show a strong overlap with the comparison patterns used from this dataset. This does not rule out PCOS or any other condition."

st.markdown(f'<div class="overall"><h3>{status}</h3><p>{text}</p></div>',unsafe_allow_html=True)

# -------------------- WHY --------------------

st.markdown('<div class="section">💡 Why This Insight?</div>', unsafe_allow_html=True)
for r in [
    "✓ BMI was included in the dataset comparison.",
    "✓ LH and FSH values were considered when available.",
    "✓ Selected symptoms were considered.",
    "✓ Follicle count was included as an ultrasound-related input.",
]:
    st.markdown(f'<div class="reason">{r}</div>',unsafe_allow_html=True)

# -------------------- NEXT STEPS --------------------

st.markdown('<div class="section">🩺 What You Can Do Next</div>', unsafe_allow_html=True)
st.markdown('<div class="caption">General educational guidance — not a personalized medical prescription.</div>', unsafe_allow_html=True)

r1,r2,r3=st.columns(3)
with r1:
    st.markdown("""<div class="rec"><h4>🌱 Lifestyle</h4><p>✓ Regular physical activity<br>✓ Balanced diet<br>✓ Healthy sleep habits<br>✓ Healthy weight management where appropriate</p></div>""",unsafe_allow_html=True)
with r2:
    st.markdown("""<div class="rec"><h4>🩺 Medical Follow-up</h4><p>✓ Discuss persistent symptoms with a qualified healthcare professional<br>✓ Consider clinical, laboratory and ultrasound findings together<br>✓ Follow professional medical advice</p></div>""",unsafe_allow_html=True)
with r3:
    st.markdown("""<div class="rec"><h4>📋 Monitoring</h4><p>✓ Track symptoms and changes over time<br>✓ Keep relevant medical reports together<br>✓ Track weight/BMI if advised by your clinician</p></div>""",unsafe_allow_html=True)

# -------------------- PDF --------------------

st.markdown('<div class="section">📄 Insight Report</div>', unsafe_allow_html=True)
if REPORTLAB:
    buf=BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=40)
    styles=getSampleStyleSheet()
    title=ParagraphStyle("T",parent=styles["Title"],alignment=TA_CENTER,fontSize=20,textColor=colors.HexColor("#17324D"))
    body=ParagraphStyle("B",parent=styles["BodyText"],fontSize=10,leading=15,textColor=colors.HexColor("#333333"))
    story=[Paragraph("PCOS AI Insights Report",title),Spacer(1,12)]
    data=[["Measure","Entered Value"],["Age",f"{age} years"],["Weight",f"{weight:.1f} kg"],["BMI",f"{bmi:.1f}"],["LH",f"{lh:.1f} mIU/mL"],["FSH",f"{fsh:.1f} mIU/mL"],["LH / FSH",f"{ratio:.2f}" if ratio is not None else "—"],["Follicles",str(follicles)],["Symptoms",", ".join(selected) if selected else "None selected"]]
    t=Table(data,colWidths=[170,300])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#17324D")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.5,colors.HexColor("#C7D2DE")),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9),("VALIGN",(0,0),(-1,-1),"TOP"),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F7FA")])]))
    story += [t,Spacer(1,15),Paragraph(f"<b>Overall insight:</b> {status}",body),Spacer(1,8),Paragraph(text,body),Spacer(1,12)]
    if evidence:
        story.append(Paragraph("<b>Data observations:</b>",body))
        for e in evidence: story.append(Paragraph("• "+e,body))
    story += [Spacer(1,15),Paragraph("<b>Medical Disclaimer:</b> This report is educational only and is not intended to diagnose or treat PCOS or any other medical condition.",body)]
    doc.build(story); buf.seek(0)
    st.download_button("📥 Download Insight Report",buf,file_name="PCOS_AI_Insight_Report.pdf",mime="application/pdf",use_container_width=True)
else:
    st.info("PDF download requires reportlab in requirements.txt.")

st.markdown('<div class="disc"><b>⚠️ Medical Disclaimer:</b> This application provides educational, data-driven insights based on the available dataset and entered information. It is not intended to diagnose, treat, cure, or prevent PCOS or any other medical condition. Clinical decisions should be made with a qualified healthcare professional.</div>',unsafe_allow_html=True)
