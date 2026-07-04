import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Medical Report Analyzer", layout="wide", initial_sidebar_state="expanded")

# Custom UI Styling
st.markdown("""
    <style>
    .main-title { font-size: 24px; font-weight: bold; color: #1e3d59; margin-bottom: 20px; }
    .normal-range-box { 
        background-color: #e8f4f8; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #17a2b8;
        margin-bottom: 20px;
    }
    .range-title { font-size: 14px; color: #6c757d; font-weight: bold; }
    .range-value { font-size: 18px; color: #17a2b8; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Database Session
if 'medical_data' not in st.session_state:
    st.session_state.medical_data = {
        "24 Hours Urine Protein": {
            "min_normal": 0, "max_normal": 150, "unit": "mg/day",
            "history": [{"date": "2026-01-10", "value": 120}, {"date": "2026-03-15", "value": 185}, {"date": "2026-05-20", "value": 140}]
        },
        "SGPT (ALT)": {
            "min_normal": 0, "max_normal": 45, "unit": "U/L",
            "history": [{"date": "2026-01-10", "value": 35}, {"date": "2026-03-15", "value": 68}, {"date": "2026-05-20", "value": 42}]
        },
        "SGOT (AST)": {
            "min_normal": 0, "max_normal": 40, "unit": "U/L",
            "history": [{"date": "2026-01-10", "value": 28}, {"date": "2026-03-15", "value": 55}, {"date": "2026-05-20", "value": 38}]
        }
    }

# Sidebar
with st.sidebar:
    st.markdown("### 📤 Upload New Report")
    uploaded_file = st.file_uploader("Choose PDF or Photo Report", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        st.success("Report Auto-Detected!")
        with st.expander("Verify & Save Data", expanded=True):
            new_date = st.date_input("Report Date", datetime.now()).strftime("%Y-%m-%d")
            select_test = st.selectbox("Detected Test", list(st.session_state.medical_data.keys()))
            new_val = st.number_input("Value", value=0.0)
            if st.button("Save to Chart"):
                st.session_state.medical_data[select_test]["history"].append({"date": new_date, "value": new_val})
                st.success("Chart Updated!")
                st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Select Medical Test")
    selected_test = st.radio("Choose a test:", list(st.session_state.medical_data.keys()))

# Main Content
st.markdown(f"<div class='main-title'>{selected_test} Analysis Dashboard</div>", unsafe_allow_html=True)
test_info = st.session_state.medical_data[selected_test]

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='normal-range-box'><div class='range-title'>Kitna Rehna Chahiye (Minimum Normal)</div><div class='range-value'>{test_info['min_normal']} {test_info['unit']}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='normal-range-box'><div class='range-title'>Kitna Rehna Chahiye (Maximum Normal)</div><div class='range-value'>{test_info['max_normal']} {test_info['unit']}</div></div>", unsafe_allow_html=True)

df = pd.DataFrame(test_info['history'])
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

fig = go.Figure()
fig.add_hrect(y0=test_info['min_normal'], y1=test_info['max_normal'], fillcolor="rgba(23, 162, 184, 0.1)", line_width=0)
fig.add_trace(go.Scatter(x=df['date'], y=df['value'], mode='lines+markers', line=dict(color='#1e3d59', width=3), marker=dict(size=10, color='#ff6e40')))

fig.update_layout(margin=dict(l=40, r=40, t=20, b=40), height=450, dragmode='pan')
st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})
st.info("💡 Mobile par chart ko aage-piche karne ke liye drag karein aur zoom karne ke liye do fingers se pinch karein.")
