import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PCOS Patient Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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
        "pcos_dataset.csv"
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

    st.error(
        "PCOS dataset CSV was not found. "
        "Please keep PCOS_data.csv in your project folder."
    )

    st.stop()


# ============================================================
# FIND COLUMN FUNCTION
# ============================================================

def find_column(possible_names):

    columns = {
        str(col).strip().lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", ""): col
        for col in df.columns
    }

    for name in possible_names:

        key = (
            str(name)
            .strip()
            .lower()
            .replace(" ", "")
            .replace("_", "")
            .replace("-", "")
        )

        if key in columns:
            return columns[key]

    return None


def make_numeric(column):

    if column is not None:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return column


# ============================================================
# IMPORTANT COLUMNS
# ============================================================

AGE_COL = make_numeric(
    find_column([
        "Age",
        "Age (yrs)",
        "Age (years)"
    ])
)

BMI_COL = make_numeric(
    find_column([
        "BMI",
        "BMI (kg/m2)",
        "BMI (kg/m²)"
    ])
)

WEIGHT_COL = make_numeric(
    find_column([
        "Weight",
        "Weight (kg)",
        "Weight (Kg)"
    ])
)

PCOS_COL = find_column([
    "PCOS (Y/N)",
    "PCOS",
    "PCOS Y/N",
    "PCOS(Y/N)"
])

LH_COL = make_numeric(
    find_column([
        "LH(mIU/mL)",
        "LH",
        "LH (mIU/mL)"
    ])
)

FSH_COL = make_numeric(
    find_column([
        "FSH(mIU/mL)",
        "FSH",
        "FSH (mIU/mL)"
    ])
)

LEFT_FOLLICLE_COL = make_numeric(
    find_column([
        "Follicle No. (L)",
        "Follicle No (L)",
        "Left Follicle Count",
        "Follicle Count Left"
    ])
)

RIGHT_FOLLICLE_COL = make_numeric(
    find_column([
        "Follicle No. (R)",
        "Follicle No (R)",
        "Right Follicle Count",
        "Follicle Count Right"
    ])
)


# ============================================================
# SYMPTOM COLUMNS
# ============================================================

WEIGHT_GAIN_COL = find_column([
    "Weight gain(Y/N)",
    "Weight Gain",
    "Weight gain"
])

HAIR_GROWTH_COL = find_column([
    "hair growth(Y/N)",
    "Hair Growth",
    "Hair Growth (Hirsutism)"
])

SKIN_DARKENING_COL = find_column([
    "Skin darkening (Y/N)",
    "Skin Darkening",
    "Skin darkening"
])

HAIR_LOSS_COL = find_column([
    "Hair loss(Y/N)",
    "Hair Loss",
    "Hair loss"
])

PIMPLES_COL = find_column([
    "Pimples(Y/N)",
    "Pimples",
    "Pimples (Acne)"
])


# ============================================================
# CLEAN PCOS DATA
# ============================================================

if PCOS_COL is not None:

    def convert_pcos(value):

        if pd.isna(value):
            return np.nan

        value = str(value).strip().lower()

        if value in [
            "1",
            "yes",
            "y",
            "true",
            "positive",
            "pcos"
        ]:
            return 1

        if value in [
            "0",
            "no",
            "n",
            "false",
            "negative",
            "non-pcos"
        ]:
            return 0

        try:

            number = float(value)

            if number in [0, 1]:
                return int(number)

        except Exception:
            pass

        return np.nan


    df["_PCOS_NUMERIC"] = df[
        PCOS_COL
    ].apply(convert_pcos)

else:

    df["_PCOS_NUMERIC"] = np.nan


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   IMPORTANT TOP SPACE FIX
   ============================================================ */

[data-testid="stAppViewContainer"] {
    overflow: visible !important;
}

[data-testid="stAppViewContainer"] > .main {
    overflow: visible !important;
}

section[data-testid="stMain"] {
    overflow: visible !important;
}

section[data-testid="stMain"] > div {
    overflow: visible !important;
}


/*
   THIS IS THE MAIN FIX.

   The title gets a large permanent top gap,
   so it can never go underneath Streamlit's
   top navigation/header.
*/

section[data-testid="stMain"] .block-container {

    max-width: 1500px !important;

    padding-top: 6rem !important;

    padding-left: 2rem !important;

    padding-right: 2rem !important;

    padding-bottom: 4rem !important;

    margin-top: 0 !important;

    overflow: visible !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.dashboard-header {

    width: 100%;

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    gap: 30px;

    position: relative;

    z-index: 100;

    margin: 0 0 25px 0 !important;

    padding: 0 !important;

    overflow: visible !important;
}


/* LEFT SIDE */

.dashboard-header-left {

    flex: 1;

    min-width: 0;

    overflow: visible !important;
}


/* ============================================================
   TITLE
   ============================================================ */

.dashboard-title {

    color: #ffffff !important;

    font-size: 34px !important;

    font-weight: 800 !important;

    line-height: 1.35 !important;

    margin: 0 !important;

    padding: 0 !important;

    display: block !important;

    white-space: nowrap !important;

    overflow: visible !important;

    text-overflow: clip !important;

    position: relative;

    z-index: 101;
}


/* ============================================================
   SUBTITLE
   ============================================================ */

.dashboard-subtitle {

    color: #8fc7ff !important;

    font-size: 16px !important;

    line-height: 1.5 !important;

    margin-top: 7px !important;

    padding: 0 !important;
}


/* ============================================================
   RIGHT HEADER
   ============================================================ */

.dashboard-header-right {

    flex-shrink: 0;

    display: flex;

    flex-direction: column;

    align-items: flex-end;

    gap: 8px;

    padding-top: 2px;

    position: relative;

    z-index: 102;
}


/* LAST REFRESHED */

.last-refreshed {

    color: #b8c4d6 !important;

    font-size: 12px !important;

    line-height: 1.4 !important;

    white-space: nowrap !important;
}


/* POWER BI */

.powerbi-button {

    display: inline-flex;

    align-items: center;

    justify-content: center;

    padding: 10px 18px;

    min-width: 175px;

    border: 1px solid #536783;

    border-radius: 8px;

    background: #111c2e;

    color: #ffffff !important;

    text-decoration: none !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    white-space: nowrap !important;

    cursor: pointer;

    transition: 0.2s ease;
}

.powerbi-button:hover {

    background: #182b46;

    border-color: #7da9dc;

    color: #ffffff !important;
}


/* ============================================================
   DIVIDER
   ============================================================ */

.dashboard-divider {

    width: 100%;

    height: 1px;

    background: #284563;

    margin-top: 25px;

    margin-bottom: 28px;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {

    color: #ffffff;

    font-size: 25px;

    font-weight: 750;

    margin-top: 5px;

    margin-bottom: 15px;
}


/* ============================================================
   FILTER BOX
   ============================================================ */

.filter-box {

    background: #0c2039;

    border: 1px solid #294766;

    border-radius: 10px;

    padding: 18px;

    min-height: 500px;

    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.kpi-card {

    background: #0c2039;

    border: 1px solid #294766;

    border-radius: 10px;

    padding: 15px;

    min-height: 120px;

    overflow: hidden;
}

.kpi-title {

    color: #d7e2ef;

    font-size: 13px;

    font-weight: 600;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}

.kpi-value {

    color: #ffffff;

    font-size: 27px;

    font-weight: 800;

    margin-top: 8px;
}

.kpi-subtitle {

    color: #8fa1b7;

    font-size: 12px;

    margin-top: 6px;
}


/* ============================================================
   GRAPH TITLE
   ============================================================ */

.graph-title {

    color: #ffffff;

    font-size: 15px;

    font-weight: 700;

    margin-bottom: 5px;
}


/* ============================================================
   FILTER / INTERACTIVE TEXT
   ============================================================ */

.interactive-line {

    background: #102a46;

    border-left: 3px solid #65a9ff;

    border-radius: 6px;

    padding: 11px 14px;

    color: #d7e7f8;

    font-size: 15px;

    font-weight: 600;

    line-height: 1.6;

    margin-top: 15px;

    margin-bottom: 20px;
}


/* ============================================================
   DOWNLOAD
   ============================================================ */

.download-box {

    background: #0c2039;

    border: 1px solid #294766;

    border-radius: 10px;

    padding: 18px;

    margin-top: 15px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 1000px) {

    section[data-testid="stMain"] .block-container {

        padding-top: 5rem !important;

        padding-left: 1rem !important;

        padding-right: 1rem !important;
    }

    .dashboard-header {

        flex-direction: column;

        align-items: flex-start;

        gap: 15px;
    }

    .dashboard-header-right {

        align-items: flex-start;
    }

    .dashboard-title {

        font-size: 28px !important;

        white-space: normal !important;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

last_refreshed = datetime.now().strftime(
    "%d %b %Y, %I:%M %p"
)


# YOUR POWER BI LINK

POWER_BI_URL = (
    "https://app.powerbi.com/groups/me/reports/"
    "9001922a-00a3-431a-9f8b-8ca8ad7a6e6c/"
    "5e101a4200c909238e53"
    "?experience=power-bi"
)


st.markdown(
    f"""
    <div class="dashboard-header">

        <div class="dashboard-header-left">

            <div class="dashboard-title">
                📊 PCOS Patient Analytics Dashboard
            </div>

            <div class="dashboard-subtitle">
                Comprehensive analysis of PCOS patient dataset
            </div>

        </div>


        <div class="dashboard-header-right">

            <div class="last-refreshed">
                Last Refreshed: {last_refreshed}
            </div>

            <a
                href="{POWER_BI_URL}"
                target="_blank"
                class="powerbi-button"
            >
                📊 Open in Power BI ↗
            </a>

        </div>

    </div>

    <div class="dashboard-divider"></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATIENT OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">👥 Patient Overview</div>',
    unsafe_allow_html=True
)


# ============================================================
# FILTERS + OVERVIEW
# ============================================================

filter_col, overview_col = st.columns(
    [1.05, 4.95],
    gap="medium"
)


# ============================================================
# FILTER BOX
# ============================================================

with filter_col:

    st.markdown(
        '<div class="filter-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color:white;
            font-size:22px;
            font-weight:750;
            margin-bottom:18px;
        ">
            🔎 Patient Filters
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # AGE FILTER
    # --------------------------------------------------------

    if AGE_COL:

        age_min = int(df[AGE_COL].min())
        age_max = int(df[AGE_COL].max())

        age_range = st.slider(
            "Age Range",
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max),
            step=1
        )

    else:

        age_range = (0, 100)


    # --------------------------------------------------------
    # BMI FILTER
    # --------------------------------------------------------

    if BMI_COL:

        bmi_min = float(df[BMI_COL].min())
        bmi_max = float(df[BMI_COL].max())

        bmi_range = st.slider(
            "BMI Range",
            min_value=float(round(bmi_min, 1)),
            max_value=float(round(bmi_max, 1)),
            value=(
                float(round(bmi_min, 1)),
                float(round(bmi_max, 1))
            ),
            step=0.1
        )

    else:

        bmi_range = (0.0, 50.0)


    # --------------------------------------------------------
    # WEIGHT FILTER
    # --------------------------------------------------------

    if WEIGHT_COL:

        weight_min = float(df[WEIGHT_COL].min())
        weight_max = float(df[WEIGHT_COL].max())

        weight_range = st.slider(
            "Weight Range (kg)",
            min_value=float(round(weight_min, 1)),
            max_value=float(round(weight_max, 1)),
            value=(
                float(round(weight_min, 1)),
                float(round(weight_max, 1))
            ),
            step=1.0
        )

    else:

        weight_range = (0.0, 150.0)


    # --------------------------------------------------------
    # PCOS STATUS
    # --------------------------------------------------------

    pcos_status = st.selectbox(
        "PCOS Status",
        [
            "All",
            "PCOS Positive",
            "PCOS Negative"
        ]
    )


    # --------------------------------------------------------
    # USE FILTERS LINE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="interactive-line">

            💡 <b>All visuals are interactive.</b><br>

            Use filters to explore data.

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


# AGE

if AGE_COL:

    filtered_df = filtered_df[
        filtered_df[AGE_COL].between(
            age_range[0],
            age_range[1]
        )
    ]


# BMI

if BMI_COL:

    filtered_df = filtered_df[
        filtered_df[BMI_COL].between(
            bmi_range[0],
            bmi_range[1]
        )
    ]


# WEIGHT

if WEIGHT_COL:

    filtered_df = filtered_df[
        filtered_df[WEIGHT_COL].between(
            weight_range[0],
            weight_range[1]
        )
    ]


# PCOS

if pcos_status == "PCOS Positive":

    filtered_df = filtered_df[
        filtered_df["_PCOS_NUMERIC"] == 1
    ]

elif pcos_status == "PCOS Negative":

    filtered_df = filtered_df[
        filtered_df["_PCOS_NUMERIC"] == 0
    ]


# ============================================================
# PATIENT OVERVIEW KPIs
# ============================================================

with overview_col:

    total_patients = len(filtered_df)


    pcos_positive = int(
        (
            filtered_df["_PCOS_NUMERIC"] == 1
        ).sum()
    )


    pcos_negative = int(
        (
            filtered_df["_PCOS_NUMERIC"] == 0
        ).sum()
    )


    if BMI_COL and not filtered_df.empty:

        avg_bmi = filtered_df[BMI_COL].mean()

    else:

        avg_bmi = 0


    if AGE_COL and not filtered_df.empty:

        avg_age = filtered_df[AGE_COL].mean()

    else:

        avg_age = 0


    if WEIGHT_COL and not filtered_df.empty:

        avg_weight = filtered_df[WEIGHT_COL].mean()

    else:

        avg_weight = 0


    k1, k2, k3, k4, k5, k6 = st.columns(
        6,
        gap="small"
    )


    def create_kpi(
        container,
        icon,
        title,
        value,
        subtitle
    ):

        with container:

            st.markdown(
                f"""
                <div class="kpi-card">

                    <div class="kpi-title">
                        {icon} {title}
                    </div>

                    <div class="kpi-value">
                        {value}
                    </div>

                    <div class="kpi-subtitle">
                        {subtitle}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    create_kpi(
        k1,
        "👥",
        "Total Patients",
        f"{total_patients:,}",
        "Filtered patients"
    )


    create_kpi(
        k2,
        "👩",
        "PCOS Positive",
        f"{pcos_positive:,}",
        "PCOS cases"
    )


    create_kpi(
        k3,
        "🛡️",
        "PCOS Negative",
        f"{pcos_negative:,}",
        "Non-PCOS"
    )


    create_kpi(
        k4,
        "⚖️",
        "Average BMI",
        f"{avg_bmi:.2f}",
        "kg/m²"
    )


    create_kpi(
        k5,
        "📈",
        "Average Age",
        f"{avg_age:.2f}",
        "Years"
    )


    create_kpi(
        k6,
        "👜",
        "Average Weight",
        f"{avg_weight:.2f}",
        "kg"
    )


    st.markdown(
        f"""
        <div style="
            color:#8fa8c5;
            font-size:13px;
            margin-top:10px;
        ">
            Showing <b>{total_patients}</b>
            filtered patients out of
            <b>{len(df)}</b> total patients
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# VISUAL SECTION DIVIDER
# ============================================================

st.markdown(
    """
    <div style="
        height:1px;
        background:#284563;
        margin-top:22px;
        margin-bottom:18px;
    "></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GRAPH LAYOUT FUNCTION
# ============================================================

def graph_layout(fig):

    fig.update_layout(

        height=235,

        margin=dict(
            l=30,
            r=12,
            t=5,
            b=35
        ),

        paper_bgcolor="#0c2039",

        plot_bgcolor="#0c2039",

        font=dict(
            color="#ffffff",
            size=10
        ),

        xaxis=dict(
            gridcolor="#294766",
            zerolinecolor="#294766",
            title_font=dict(size=10),
            tickfont=dict(size=9)
        ),

        yaxis=dict(
            gridcolor="#294766",
            zerolinecolor="#294766",
            title_font=dict(size=10),
            tickfont=dict(size=9)
        )
    )

    return fig


# ============================================================
# ROW 1
# AGE | BMI | PCOS
# ============================================================

col1, col2, col3 = st.columns(
    3,
    gap="small"
)


# ============================================================
# AGE DISTRIBUTION
# ============================================================

with col1:

    st.markdown(
        '<div class="graph-title">📈 Age Distribution</div>',
        unsafe_allow_html=True
    )

    if AGE_COL and not filtered_df.empty:

        fig = px.histogram(
            filtered_df,
            x=AGE_COL,
            nbins=10
        )

        fig.update_traces(
            marker_color="#5B9BE6"
        )

        fig.update_layout(
            xaxis_title="Age",
            yaxis_title="Patients",
            showlegend=False
        )

        fig = graph_layout(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info("No age data available.")


# ============================================================
# BMI DISTRIBUTION
# ============================================================

with col2:

    st.markdown(
        '<div class="graph-title">⚖️ BMI Distribution</div>',
        unsafe_allow_html=True
    )

    if BMI_COL and not filtered_df.empty:

        fig = px.histogram(
            filtered_df,
            x=BMI_COL,
            nbins=10
        )

        fig.update_traces(
            marker_color="#D65391"
        )

        fig.update_layout(
            xaxis_title="BMI",
            yaxis_title="Patients",
            showlegend=False
        )

        fig = graph_layout(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info("No BMI data available.")


# ============================================================
# PCOS VS NON-PCOS
# ============================================================

with col3:

    st.markdown(
        '<div class="graph-title">🩺 PCOS vs Non-PCOS</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "PCOS Positive",
                    "PCOS Negative"
                ],
                values=[
                    pcos_positive,
                    pcos_negative
                ],
                hole=0.55,
                textinfo="value+percent",
                marker=dict(
                    colors=[
                        "#D65391",
                        "#5B9BE6"
                    ]
                )
            )
        ]
    )

    fig.update_layout(
        height=235,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),
        paper_bgcolor="#0c2039",
        plot_bgcolor="#0c2039",
        font=dict(
            color="white",
            size=10
        ),
        legend=dict(
            font=dict(size=9)
        )
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# ROW 2
# HORMONES | LH/FSH | FOLLICLES
# ============================================================

col4, col5, col6 = st.columns(
    3,
    gap="small"
)


# ============================================================
# HORMONE ANALYSIS
# ============================================================

with col4:

    st.markdown(
        '<div class="graph-title">🧪 Hormone Analysis</div>',
        unsafe_allow_html=True
    )

    if (
        LH_COL
        and FSH_COL
        and not filtered_df.empty
    ):

        hormone_df = pd.DataFrame(
            {
                "Hormone": [
                    "LH",
                    "FSH"
                ],
                "Average": [
                    filtered_df[LH_COL].mean(),
                    filtered_df[FSH_COL].mean()
                ]
            }
        )

        fig = px.bar(
            hormone_df,
            x="Hormone",
            y="Average"
        )

        fig.update_traces(
            marker_color="#5B9BE6"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Average"
        )

        fig = graph_layout(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info("Hormone data unavailable.")


# ============================================================
# LH / FSH RATIO
# ============================================================

with col5:

    st.markdown(
        '<div class="graph-title">📊 LH / FSH Ratio</div>',
        unsafe_allow_html=True
    )

    if (
        LH_COL
        and FSH_COL
        and not filtered_df.empty
    ):

        ratio_df = filtered_df[
            [
                LH_COL,
                FSH_COL
            ]
        ].dropna().copy()

        ratio_df["LH_FSH_Ratio"] = (
            ratio_df[LH_COL]
            /
            ratio_df[FSH_COL].replace(
                0,
                np.nan
            )
        )

        ratio_df = ratio_df.dropna()

        if not ratio_df.empty:

            fig = px.histogram(
                ratio_df,
                x="LH_FSH_Ratio",
                nbins=10
            )

            fig.update_traces(
                marker_color="#9B68D1"
            )

            fig.update_layout(
                xaxis_title="LH / FSH Ratio",
                yaxis_title="Patients",
                showlegend=False
            )

            fig = graph_layout(fig)

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False
                }
            )

        else:

            st.info(
                "LH/FSH ratio unavailable."
            )

    else:

        st.info(
            "LH/FSH data unavailable."
        )


# ============================================================
# FOLLICLE COUNT
# ============================================================

with col6:

    st.markdown(
        '<div class="graph-title">🌸 Follicle Count Analysis</div>',
        unsafe_allow_html=True
    )

    if (
        LEFT_FOLLICLE_COL
        and RIGHT_FOLLICLE_COL
        and not filtered_df.empty
    ):

        follicle_df = pd.DataFrame(
            {
                "Ovary": [
                    "Left Ovary",
                    "Right Ovary"
                ],
                "Average": [
                    filtered_df[
                        LEFT_FOLLICLE_COL
                    ].mean(),

                    filtered_df[
                        RIGHT_FOLLICLE_COL
                    ].mean()
                ]
            }
        )

        fig = px.bar(
            follicle_df,
            x="Ovary",
            y="Average"
        )

        fig.update_traces(
            marker_color="#D65391"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Average Follicles"
        )

        fig = graph_layout(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "Follicle data unavailable."
        )


# ============================================================
# ROW 3
# WEIGHT | SYMPTOMS | BMI
# ============================================================

col7, col8, col9 = st.columns(
    3,
    gap="small"
)


# ============================================================
# WEIGHT BY PCOS
# ============================================================

with col7:

    st.markdown(
        '<div class="graph-title">👜 Weight by PCOS Status</div>',
        unsafe_allow_html=True
    )

    if (
        WEIGHT_COL
        and PCOS_COL
        and not filtered_df.empty
    ):

        plot_df = filtered_df.copy()

        plot_df["Status"] = np.where(
            plot_df["_PCOS_NUMERIC"] == 1,
            "PCOS Positive",
            "PCOS Negative"
        )

        fig = px.box(
            plot_df,
            x="Status",
            y=WEIGHT_COL
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Weight (kg)"
        )

        fig = graph_layout(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "Weight data unavailable."
        )


# ============================================================
# SYMPTOMS
# ============================================================

with col8:

    st.markdown(
        '<div class="graph-title">💗 Symptoms Frequency</div>',
        unsafe_allow_html=True
    )

    symptom_columns = []
    symptom_names = []


    if WEIGHT_GAIN_COL:

        symptom_columns.append(
            WEIGHT_GAIN_COL
        )

        symptom_names.append(
            "Weight Gain"
        )


    if HAIR_GROWTH_COL:

        symptom_columns.append(
            HAIR_GROWTH_COL
        )

        symptom_names.append(
            "Hair Growth"
        )


    if SKIN_DARKENING_COL:

        symptom_columns.append(
            SKIN_DARKENING_COL
        )

        symptom_names.append(
            "Skin Darkening"
        )


    if HAIR_LOSS_COL:

        symptom_columns.append(
            HAIR_LOSS_COL
        )

        symptom_names.append(
            "Hair Loss"
        )


    if PIMPLES_COL:

        symptom_columns.append(
            PIMPLES_COL
        )

        symptom_names.append(
            "Pimples"
        )


    symptom_results = []


    for col, name in zip(
        symptom_columns,
        symptom_names
    ):

        positive_count = (
            filtered_df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(
                [
                    "1",
                    "yes",
                    "y",
                    "true"
                ]
            )
            .sum()
        )

        symptom_results.append(
            {
                "Symptom": name,
                "Patients": int(
                    positive_count
                )
            }
        )


    if symptom_results:

        symptom_df = pd.DataFrame(
            symptom_results
        )

        symptom_df = symptom_df.sort_values(
            "Patients",
            ascending=True
        )

        fig = px.bar(
            symptom_df,
            x="Patients",
            y="Symptom",
            orientation="h"
        )

        fig.update_traces(
            marker_color="#9B68D1"
        )

        fig.update_layout(
            xaxis_title="Patients",
            yaxis_title="",
            showlegend=False
        )

        fig = graph_layout(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "Symptom data unavailable."
        )


# ============================================================
# BMI BY PCOS
# ============================================================

with col9:

    st.markdown(
        '<div class="graph-title">⚖️ BMI by PCOS Status</div>',
        unsafe_allow_html=True
    )

    if (
        BMI_COL
        and PCOS_COL
        and not filtered_df.empty
    ):

        plot_df = filtered_df.copy()

        plot_df["Status"] = np.where(
            plot_df["_PCOS_NUMERIC"] == 1,
            "PCOS Positive",
            "PCOS Negative"
        )

        fig = px.box(
            plot_df,
            x="Status",
            y=BMI_COL
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="BMI"
        )

        fig = graph_layout(fig)

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )

    else:

        st.info(
            "BMI data unavailable."
        )


# ============================================================
# INTERACTIVE MESSAGE
# ============================================================

st.markdown(
    """
    <div class="interactive-line">

        💡 <b>All visuals are interactive.</b>
        Use filters to explore data.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DOWNLOAD REPORT
# ============================================================

st.markdown(
    '<div class="section-title">📥 Download Report</div>',
    unsafe_allow_html=True
)


download_col1, download_col2 = st.columns(
    2,
    gap="medium"
)


# ============================================================
# CSV
# ============================================================

with download_col1:

    csv_df = filtered_df.drop(
        columns=[
            "_PCOS_NUMERIC"
        ],
        errors="ignore"
    )

    csv_data = csv_df.to_csv(
        index=False
    )

    st.download_button(
        "📊 Download CSV",
        data=csv_data,
        file_name="PCOS_Filtered_Patient_Report.csv",
        mime="text/csv",
        width="stretch"
    )


# ============================================================
# PDF
# ============================================================

with download_col2:

    try:

        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=35,
            leftMargin=35,
            topMargin=35,
            bottomMargin=35
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "PCOS Patient Analytics Report",
                styles["Title"]
            )
        )

        story.append(
            Spacer(1, 15)
        )

        report_data = [
            [
                "Metric",
                "Value"
            ],
            [
                "Total Patients",
                str(total_patients)
            ],
            [
                "PCOS Positive",
                str(pcos_positive)
            ],
            [
                "PCOS Negative",
                str(pcos_negative)
            ],
            [
                "Average BMI",
                f"{avg_bmi:.2f}"
            ],
            [
                "Average Age",
                f"{avg_age:.2f}"
            ],
            [
                "Average Weight",
                f"{avg_weight:.2f} kg"
            ]
        ]

        table = Table(
            report_data,
            colWidths=[
                220,
                180
            ]
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(
                            "#1f4e79"
                        )
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        8
                    )
                ]
            )
        )

        story.append(table)

        story.append(
            Spacer(1, 20)
        )

        story.append(
            Paragraph(
                f"Generated: {last_refreshed}",
                styles["Normal"]
            )
        )

        doc.build(story)

        buffer.seek(0)

        st.download_button(
            "📄 Download PDF",
            data=buffer,
            file_name="PCOS_Patient_Analytics_Report.pdf",
            mime="application/pdf",
            width="stretch"
        )

    except ImportError:

        st.info(
            "PDF download requires reportlab. "
            "Run: pip install reportlab"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7188a8;
        font-size:11px;
        margin-top:25px;
        padding-top:15px;
        border-top:1px solid #203e5c;
    ">
        Source: PCOS Patient Dataset
        &nbsp; • &nbsp;
        PCOS Patient Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)