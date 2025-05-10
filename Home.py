import streamlit as st
from pages.utils import navbar

st.set_page_config(page_title="ABC Company Dashboard", layout="wide")
navbar()

# Center the main title
st.markdown("<h1 style='text-align: center;'>ABC Company</h1>", unsafe_allow_html=True)

# Create a centered container with custom styling for metrics
st.markdown("""
    <div style='
        display: flex;
        justify-content: center;
        margin: 2rem auto;
    '>
        <div style='
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 2rem;
            width: 600px;
            background: rgba(255, 255, 255, 0.05);
        '>
""", unsafe_allow_html=True)

# Metrics columns with equal width
st.markdown("<div style='display: flex; justify-content: space-around;'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.metric("Agent Count", "150")
with col2:
    st.metric("New Employees", "5")
st.markdown("</div></div></div>", unsafe_allow_html=True)

# Replace style1 with centered subtitle
st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Productivity Trends</h2>", unsafe_allow_html=True)
left, right = st.columns(2)
with left:
    st.markdown("<div style='text-align: center;'>⬜️ **[TODO] Add Graph 1 Here**</div>", unsafe_allow_html=True)
with right:
    st.markdown("<div style='text-align: center;'>⬜️ **[TODO] Add Graph 2 Here**</div>", unsafe_allow_html=True)

# Replace style1 with centered subtitle
st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Agent Classification</h2>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>⬜️ **[TODO] Add Pie Chart (High/Medium/Low)**</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>[More ➕](pages/3_Employees.py)</div>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Nill Agent Count: 15</h3>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>[Go to Nill Agents ➡️](pages/2_Nill_Agents.py)</div>", unsafe_allow_html=True)
