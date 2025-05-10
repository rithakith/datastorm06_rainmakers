import streamlit as st
from pages.utils import navbar
import pandas as pd
from app import load_data

st.set_page_config(page_title="ABC Company Dashboard", layout="wide")
navbar()

# Center the main title
st.markdown("<h1 style='text-align: center;'>ABC Company</h1>", unsafe_allow_html=True)

# Load data
employee_df, target_df = load_data()

if employee_df is not None and target_df is not None:
    # Custom CSS for metrics container
    st.markdown("""
        <style>
            [data-testid="metric-container"] {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 1rem 1.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create centered container for metrics
    container = st.container()
    with container:
        # Add padding to create space at top
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Create three columns with the middle one being wider
        left_spacer, col1, middle_spacer, col2, right_spacer = st.columns([1, 1.2, 0.2, 1.2, 1])
        with col1:
            total_employees = len(employee_df['agent_code'].unique())
            st.metric("Employee Count", str(total_employees))
        with col2:
            # Calculate new employees (joined in the last 30 days)
            today = pd.Timestamp.now()
            new_employees = len(employee_df[
                (employee_df['agent_join_month'] > (today - pd.Timedelta(days=30)))
            ]['agent_code'].unique())
            st.metric("New Employees", str(new_employees))

    # Productivity Trends section
    st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Productivity Trends</h2>", unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        # Add your productivity trends visualization here using employee_df
        st.markdown("<div style='text-align: center;'>⬜️ **[TODO] Add Graph 1 Here**</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div style='text-align: center;'>⬜️ **[TODO] Add Graph 2 Here**</div>", unsafe_allow_html=True)

    # Employee Classification section
    st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Employee Classification</h2>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>⬜️ **[TODO] Add Pie Chart (High/Medium/Low)**</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>[More ➕](pages/3_Employees.py)</div>", unsafe_allow_html=True)

    # Nill Agent Count
    nill_agents = len(target_df[target_df['target'] == 0])
    st.markdown(f"<h3 style='text-align: center;'>Nill Agent Count: {nill_agents}</h3>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>[Go to Nill Agents ➡️](pages/2_Nill_Agents.py)</div>", unsafe_allow_html=True)
else:
    st.error("Unable to load data. Please check your Google Drive file IDs and ensure the files are accessible.")
