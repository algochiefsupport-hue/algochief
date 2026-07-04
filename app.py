import streamlit as st
import pandas as pd
import plotly.graph_objects as px
from datetime import datetime

# Page configuration for a clean medical theme
st.set_page_config(page_title="Medical Report Analyzer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for clean, minimalist look
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; margin-bottom: 20px; }
    .test-card { padding: 15px; border-radius: 8px; background-color: #F3F4F6; margin-bottom: 10px; cursor: pointer; }
    .range-box { padding: 10px; border-radius: 5px; background-color: #EFF6FF; border-left: 5px solid #3B82F6; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 1. Initial State Data (Sample for the tests you mentioned)
if 'medical_data' not in st.session_state:
    st.session_state.medical_data = pd.DataFrame([
        {"Date": "2026-01-10", "Test Name": "SGPT", "Value": 65.0, "Min_Normal": 0.0, "Max_Normal": 45.0, "Unit": "U/L"},
        {"Date": "2026-02-15", "Test Name": "SGPT", "Value": 48.0, "Min_Normal": 0.0, "Max_Normal": 45.0, "Unit": "U/L"},
        {"Date": "2026-03-20", "Test Name": "SGPT", "Value": 38.0, "Min_Normal": 0.0, "Max_Normal": 45.0, "Unit": "U/L"},
        
        {"Date": "2026-01-10", "Test Name": "SGOT", "Value": 55.0, "Min_Normal": 0.0, "Max_Normal": 40.0, "Unit": "U/L"},
        {"Date": "2026-03-20", "Test Name": "SGOT", "Value": 35.0, "Min_Normal": 0.0, "Max_Normal": 40.0, "Unit": "U/L"},
        
        {"Date": "2026-01-10", "Test Name": "24 Hours Urine Protein", "Value": 180.0, "Min_Normal": 0.0, "Max_Normal": 150.0, "Unit": "mg/day"},
        {"Date": "2026-03-20", "Test Name": "24 Hours Urine Protein", "Value": 140.0, "Min_Normal": 0.0, "Max_Normal": 150.0, "Unit": "mg/day"}
    ])

st.markdown('<div class="main-title">🩺 Clean Medical Report Analyzer</div>', unsafe_allow_html=True)

# Sidebar for Uploading Reports
st.sidebar.header("📁 Upload New Report")
uploaded_file = st.sidebar.file_uploader("Upload PDF or Photo (Camera not used)", type=["pdf", "jpg", "jpeg", "png"])

# Simulated Auto-Detection when user uploads a file
if uploaded_file is not None:
    if st.sidebar.button("Auto-Detect & Process Report"):
        # Real system me yahan Gemini API image/pdf ko padhega, abhi hum new data append kar rahe hain:
        today_str = datetime.now().strftime("%Y-%m-%d")
        new_records = [
            {"Date": today_str, "Test Name": "SGPT", "Value": 30.0, "Min_Normal": 0.0, "Max_Normal": 45.0, "Unit": "U/L"},
            {"Date": today_str, "Test Name": "SGOT", "Value": 28.0, "Min_Normal": 0.0, "Max_Normal": 40.0, "Unit": "U/L"},
            {"Date": today_str, "Test Name": "24 Hours Urine Protein", "Value": 125.0, "Min_Normal": 0.0, "Max_Normal": 150.0, "Unit": "mg/day"}
        ]
        new_df = pd.DataFrame(new_records)
        st.session_state.medical_data = pd.concat([st.session_state.medical_data, new_df]).drop_duplicates().reset_index(drop=True)
        st.sidebar.success("New report auto-detected and charts updated successfully!")

# Get unique test names to display on dashboard
df = st.session_state.medical_data
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
unique_tests = sorted(df['Test Name'].unique())

# Dashboard Layout: List of Test Names Only
st.write("### 📋 Select a Test to view Chart & Normal Ranges")
selected_test = st.selectbox("Dashboard Test List:", ["-- Select Test --"] + unique_tests)

if selected_test != "-- Select Test --":
    st.markdown("---")
    st.write(f"## 📊 Analysis for: {selected_test}")
    
    # Filter data for selected test
    test_df = df[df['Test Name'] == selected_test]
    
    # Get Normal Ranges from the latest record
    min_normal = test_df.iloc[-1]['Min_Normal']
    max_normal = test_df.iloc[-1]['Max_Normal']
    unit = test_df.iloc[-1]['Unit']
    
    # Display Kitna Rehna Chahiye exactly as requested
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='range-box'><b>Kitna Rehna Chahiye (Minimum Normal):</b><br><span style='font-size:20px;'>{min_normal} {unit}</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='range-box'><b>Kitna Rehna Chahiye (Maximum Normal):</b><br><span style='font-size:20px;'>{max_normal} {unit}</span></div>", unsafe_allow_html=True)
        
    # Zoomable & Pan-enabled Chart using Plotly
    fig = px.Figure()
    
    # Add Patient test values line
    fig.add_trace(px.Scatter(
        x=test_df['Date'], 
        y=test_df['Value'], 
        mode='lines+markers',
        name='Your Value',
        line=dict(color='#1E3A8A', width=3),
        marker=dict(size=10)
    ))
    
    # Add Normal Range shaded area background
    fig.add_hrect(
        y0=min_normal, 
        y1=max_normal, 
        fillcolor="rgba(16, 185, 129, 0.15)", 
        layer="below", 
        line_width=0,
        annotation_text="Normal Range Zone", 
        annotation_position="top left"
    )
    
    # Configure Chart Layout for Zoom & Scroll
    fig.update_layout(
        xaxis_title="Report Dates (Pehle -> Baad me)",
        yaxis_title=f"Value ({unit})",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20),
        height=450,
        dragmode="pan" # Enables easy swiping/scrolling right away
    )
    
    # Enable dynamic scroll zoom config
    st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})
    
    # History Table inside the dropdown view
    st.write("### 🗓️ Detailed History Table")
    history_df = test_df[['Date', 'Value', 'Unit']].copy()
    history_df['Date'] = history_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(history_df, use_container_width=True)
