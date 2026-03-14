import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import zipfile

st.set_page_config(layout="wide")

st.title("Tamil Nadu Aadhaar Operational Analytics Dashboard")

zip_path = "uidai_TN_Datasets.zip"


# ------------------------------------------------
# COMMON CHART STYLE
# ------------------------------------------------

def style(fig, title):

    fig.update_layout(
        title=title,
        paper_bgcolor="#f5f5f5",
        plot_bgcolor="#f5f5f5",

        font=dict(
            family="Arial",
            size=14,
            color="#000000"
        ),

        title_font=dict(
            size=20,
            color="#000000"
        ),

        xaxis=dict(
            title_font=dict(color="#000000"),
            tickfont=dict(color="#000000"),
            gridcolor="#d3d3d3"
        ),

        yaxis=dict(
            title_font=dict(color="#000000"),
            tickfont=dict(color="#000000"),
            gridcolor="#d3d3d3"
        ),

        legend=dict(
            font=dict(color="#000000")
        )
    )

    return fig


# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

@st.cache_data
def load_data():

    with zipfile.ZipFile(zip_path) as z:

        enrol = pd.read_csv(z.open("ecd49b12-3084-4521-8f7e-ca8bf72069ba_1d8c22db516b565f8a2be77aa2e88b82.csv"))
        bio = pd.read_csv(z.open("65454dab-1517-40a3-ac1d-47d4dfe6891c_1d8c22db516b565f8a2be77aa2e88b82.csv"))
        demo = pd.read_csv(z.open("19eac040-0b94-49fa-b239-4f2fd8677d53_1d8c22db516b565f8a2be77aa2e88b82.csv"))

    for df in [enrol, bio, demo]:
        df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    enrol_state = enrol.groupby("date")[["age_0_5","age_5_17","age_18_greater"]].sum().reset_index()
    bio_state = bio.groupby("date")[["bio_age_5_17","bio_age_17_"]].sum().reset_index()
    demo_state = demo.groupby("date")[["demo_age_5_17","demo_age_17_"]].sum().reset_index()

    df = enrol_state.merge(bio_state,on="date")
    df = df.merge(demo_state,on="date")

    df["total_enrolments"] = df["age_0_5"]+df["age_5_17"]+df["age_18_greater"]
    df["total_bio_updates"] = df["bio_age_5_17"]+df["bio_age_17_"]
    df["total_demo_updates"] = df["demo_age_5_17"]+df["demo_age_17_"]

    df["EUSI"] = (df["total_bio_updates"]+df["total_demo_updates"])/df["total_enrolments"]

    df["Child_Lifecycle_Compliance"] = df["bio_age_5_17"]/(df["age_0_5"]+df["age_5_17"])
    df["Adult_Demo_Volatility"] = df["demo_age_17_"]/df["age_18_greater"]

    df["bio_trend"] = df["total_bio_updates"].rolling(3).mean()
    df["upper_band"] = df["bio_trend"]*1.15
    df["lower_band"] = df["bio_trend"]*0.85


    district_enrol = enrol.groupby("district")[["age_0_5","age_5_17","age_18_greater"]].sum().reset_index()
    district_bio = bio.groupby("district")[["bio_age_5_17","bio_age_17_"]].sum().reset_index()
    district_demo = demo.groupby("district")[["demo_age_5_17","demo_age_17_"]].sum().reset_index()

    district_df = district_enrol.merge(district_bio,on="district")
    district_df = district_df.merge(district_demo,on="district")

    district_df["total_enrolments"] = (
        district_df["age_0_5"]+
        district_df["age_5_17"]+
        district_df["age_18_greater"]
    )

    district_df["total_updates"] = (
        district_df["bio_age_5_17"]+
        district_df["bio_age_17_"]+
        district_df["demo_age_5_17"]+
        district_df["demo_age_17_"]
    )

    district_df["District_Update_Pressure"] = district_df["total_updates"]/district_df["total_enrolments"]

    district_df["norm_updates"] = district_df["total_updates"]/district_df["total_updates"].max()
    district_df["norm_enrol"] = district_df["total_enrolments"]/district_df["total_enrolments"].max()

    district_df["District_Stress_Score"] = 0.6*district_df["norm_updates"]+0.4*district_df["norm_enrol"]

    def classify(score):
        if score>0.7:
            return "High Stress"
        elif score>0.4:
            return "Medium Stress"
        else:
            return "Low Stress"

    district_df["Stress_Category"] = district_df["District_Stress_Score"].apply(classify)

    district_df["Child_Compliance_Ratio"] = district_df["bio_age_5_17"]/(district_df["age_0_5"]+district_df["age_5_17"])
    district_df["Child_Compliance_Gap"] = 1-district_df["Child_Compliance_Ratio"]

    return df,district_df


df,district_df = load_data()


# ------------------------------------------------
# KPI SUMMARY
# ------------------------------------------------

total_enrol = df["total_enrolments"].sum()
total_bio = df["total_bio_updates"].sum()
total_demo = df["total_demo_updates"].sum()

k1,k2,k3 = st.columns(3)

k1.metric("Total Aadhaar Enrolments", f"{int(total_enrol):,}")
k2.metric("Total Biometric Updates", f"{int(total_bio):,}")
k3.metric("Total Demographic Updates", f"{int(total_demo):,}")


# ------------------------------------------------
# CHART FUNCTIONS
# ------------------------------------------------

def enrolment_composition():

    child = df["age_0_5"].sum()+df["age_5_17"].sum()
    adult = df["age_18_greater"].sum()

    fig = px.pie(
        values=[child,adult],
        names=["Child","Adult"]
    )

    return style(fig,"Enrolment Composition")


def update_composition():

    fig = px.pie(
        values=[df["total_bio_updates"].sum(),df["total_demo_updates"].sum()],
        names=["Biometric Updates","Demographic Updates"],
        hole=0.5
    )

    return style(fig,"Overall Update Composition")


def age_stack():

    fig = px.area(df,x="date",y=["age_0_5","age_5_17","age_18_greater"])

    return style(fig,"Age-wise Aadhaar Enrolment Composition")


def update_trend():

    fig = px.line(df,x="date",y=["total_bio_updates","total_demo_updates"])

    return style(fig,"Biometric vs Demographic Update Trends")


def eusi():

    fig = px.line(df,x="date",y="EUSI")

    return style(fig,"Enrolment–Update Stress Index")


def lifecycle():

    fig = px.area(df,x="date",y="Child_Lifecycle_Compliance")

    return style(fig,"Child Lifecycle Compliance Trend")


def volatility():

    fig = px.scatter(df,x="total_enrolments",y="Adult_Demo_Volatility")

    return style(fig,"Adult Demographic Volatility")


def bio_variation():

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df["date"],y=df["total_bio_updates"],name="Actual"))
    fig.add_trace(go.Scatter(x=df["date"],y=df["bio_trend"],name="Trend"))

    return style(fig,"Biometric Update Demand Trend")


def district_pressure():

    top = district_df.sort_values("District_Update_Pressure",ascending=False).head(10)

    fig = px.bar(top,x="District_Update_Pressure",y="district")

    return style(fig,"Top Districts by Update Pressure")


def stress():

    fig = px.histogram(district_df,x="Stress_Category")

    return style(fig,"District Stress Classification")


def compliance_gap():

    worst = district_df.sort_values("Child_Compliance_Gap",ascending=False).head(10)

    fig = px.bar(worst,x="Child_Compliance_Gap",y="district")

    return style(fig,"Child Compliance Gap by District")


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.header("Other Charts")

all_charts = {

"Age Enrolment Composition": age_stack,
"Update Trend": update_trend,
"EUSI Index": eusi,
"Child Lifecycle Compliance": lifecycle,
"Adult Volatility": volatility,
"Biometric Demand Trend": bio_variation,
"Update Composition": update_composition,
"District Update Pressure": district_pressure,
"Stress Classification": stress,
"Child Compliance Gap": compliance_gap

}

chart1 = st.sidebar.selectbox(
"Chart Slot 1",
list(all_charts.keys())
)

chart2 = st.sidebar.selectbox(
"Chart Slot 2",
list(all_charts.keys())
)

def get_chart(name):
    return all_charts[name]()


# ------------------------------------------------
# DASHBOARD LAYOUT
# ------------------------------------------------

# ------------------------------------------------
# DASHBOARD LAYOUT
# ------------------------------------------------

# ------------------------------------------------
# DASHBOARD LAYOUT
# ------------------------------------------------

c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(enrolment_composition(),use_container_width=True)

with c2:
    st.plotly_chart(update_composition(),use_container_width=True)


c3,c4 = st.columns(2)

# Detect duplicate selections
if (
    chart1 == chart2 or
    chart1 == "Update Composition" or
    chart2 == "Update Composition"
):

    st.warning("⚠️ The same chart has been selected in multiple slots. Please choose different charts.")

else:

    with c3:
        st.plotly_chart(get_chart(chart1),use_container_width=True)

    with c4:
        st.plotly_chart(get_chart(chart2),use_container_width=True)
