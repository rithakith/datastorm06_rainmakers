import streamlit as st
import pandas as pd
import sys
import os
# Add parent directory to path so we can import from root utils.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import navbar, footer
from app import load_data, plot_new_policy_count, generate_agent_performance_chart

# Load agent performance data including nill predictions
def load_agent_perf_data():
    agent_perf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "agent_perf.csv")
    if os.path.exists(agent_perf_path):
        df = pd.read_csv(agent_perf_path)
        # Convert is_nill to proper boolean if it's stored as string
        if 'is_nill' in df.columns:
            df['is_nill'] = df['is_nill'].apply(lambda x: True if str(x).lower() == 'true' else False)
        return df
    return None

st.set_page_config(page_title="Agent", layout="wide")
navbar()

st.title("Agent Details")

# Load data
employee_df, target_df = load_data()
agent_perf_df = load_agent_perf_data()

if employee_df is not None and target_df is not None:
    # Get unique employee codes
    employee_codes = employee_df['agent_code'].unique().tolist()
    
    # Filter to only agents that exist in both datasets if agent_perf_df is available
    if agent_perf_df is not None:
        common_codes = set(employee_codes).intersection(set(agent_perf_df['agent_code'].unique().tolist()))
        employee_codes = sorted(list(common_codes))

    # Only show the select box for employees
    selected_code = st.selectbox("Select Agent", employee_codes)
    
    if selected_code:
        agent_data = employee_df[employee_df['agent_code'] == selected_code].iloc[0]
        # Determine performance status
        avg_policies = employee_df[employee_df['agent_code'] == selected_code]['new_policy_count'].mean()
        status = "High" if avg_policies > 20 else "Medium" if avg_policies > 10 else "Low"
        st.markdown(f"#### Performance Status: **{status}**")
        # Display nill prediction from agent_perf.csv if available
        st.markdown("##### Next Month Prediction")
        col1, col2 = st.columns(2)
        
        if agent_perf_df is not None and selected_code in agent_perf_df['agent_code'].values:
            agent_perf = agent_perf_df[agent_perf_df['agent_code'] == selected_code].iloc[0]
            is_nill = agent_perf['is_nill']
            nill_rate = agent_perf['nill_rate']
            
            with col1:
                # Direct prediction from is_nill column
                if is_nill == True or (isinstance(is_nill, str) and is_nill.lower() == 'true'):
                    prediction = "RISK: No policies next month"
                    prediction_color = "🔴"
                else:
                    prediction = "SAFE: Will sell policies" 
                    prediction_color = "🟢"
                st.markdown(f"### {prediction_color} {prediction}")
                st.markdown(f"Historical nill rate: **{nill_rate:.1%}**")
            with col2:
                performance_group = agent_perf['performance_group']
                recommendation = agent_perf['recommendation']
                
                st.markdown("### 📋 Action Plan")
                st.markdown(f"**Performance Group:** {performance_group}")
                st.markdown(f"**Recommendation:**")
                # Create a styled box for the recommendation
                st.markdown(f"""
                <div style="background-color:#000000;padding:10px;border-radius:5px;">
                {recommendation}                </div>
                """, unsafe_allow_html=True)
        else:
            with col1:
                st.markdown("### ⚠️ No Prediction Available")
                st.markdown("Data not available for this agent")
            with col2:
                st.markdown("### ⚠️ No Recommendation Available")
                st.markdown("Data not available for this agent")

        # Demographics in three columns
        st.markdown("#### Agent Details") # New, more readable section
        tenure_months = int((agent_data['year_month'] - agent_data['agent_join_month']).days / 30) # Ensure tenure calculation is present

        details_col1, details_col2 = st.columns(2)
        with details_col1:
            st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <strong>Agent Code:</strong><br>
                    {selected_code}
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>Age:</strong><br>
                    {int(agent_data['agent_age'])} years
                </div>
                <div>
                    <strong>Join Date:</strong><br>
                    {agent_data['agent_join_month'].strftime('%B %d, %Y')}
                </div>
            """, unsafe_allow_html=True)
        with details_col2:
            st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <strong>Tenure:</strong><br>
                    {tenure_months} months
                </div>
                <div style="margin-bottom: 10px;">
                    <strong>First Policy Sale:</strong><br>
                    {agent_data['first_policy_sold_month'].strftime('%B %d, %Y') if pd.notna(agent_data['first_policy_sold_month']) else 'N/A'}
                </div>
                <div>
                    <strong>Monthly Income:</strong><br>
                    ${agent_data.get('monthly_income', 4500):,.2f}
                </div>
            """, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True) # Add a horizontal rule for separation

        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("New Policy Count Trend")
            fig1, policy_stats = plot_new_policy_count(selected_code, employee_df)
            if fig1:
                st.pyplot(fig1)
            else:
                st.warning(policy_stats)

        with col2:
            st.subheader("Monthly Performance Overview")
            fig2, monthly_data = generate_agent_performance_chart(selected_code, employee_df)
            if fig2:
                st.pyplot(fig2)
            else:
                st.warning(monthly_data)

        # Show monthly performance data in expandable section
        if monthly_data is not None and not isinstance(monthly_data, str):
            with st.expander("View Monthly Performance Data"):
                st.dataframe(monthly_data, use_container_width=True)
else:
    st.error("Unable to load data. Please check your Google Drive file IDs and ensure the files are accessible.")

# Add footer at the end of the page
footer()
