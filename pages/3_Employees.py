import streamlit as st
import pandas as pd
import sys
import os
# Add parent directory to path so we can import from root utils.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import navbar
from app import load_data, plot_new_policy_count, generate_agent_performance_chart

st.set_page_config(page_title="Employees", layout="wide")
navbar()

st.title("Employee Details")

# Load data
employee_df, target_df = load_data()

if employee_df is not None and target_df is not None:
    # Get unique employee codes
    employee_codes = employee_df['agent_code'].unique().tolist()

    # Only show the select box for employees
    selected_code = st.selectbox("Select Employee", employee_codes)
    
    if selected_code:
        agent_data = employee_df[employee_df['agent_code'] == selected_code].iloc[0]
        
        # Determine performance status
        avg_policies = employee_df[employee_df['agent_code'] == selected_code]['new_policy_count'].mean()
        status = "High" if avg_policies > 20 else "Medium" if avg_policies > 10 else "Low"
        st.markdown(f"#### Performance Status: **{status}**")

        # Put Predicted and Real metrics side by side using columns
        st.markdown("##### Policy Count")
        col1, col2 = st.columns(2)
        predicted = round(avg_policies * 1.15)  # Simple prediction for demo
        real = round(avg_policies)
        
        with col1:
            st.metric("Predicted", str(predicted), f"+{predicted - real}")
        with col2:
            st.metric("Real", str(real))

        # Demographics in three columns
        st.markdown("#### Demographics")
        tenure_months = int((agent_data['year_month'] - agent_data['agent_join_month']).days / 30)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Age:**")
            st.write(f"{int(agent_data['agent_age'])} years")
            
            st.markdown("**Monthly Income:**")
            st.write(f"${agent_data.get('monthly_income', 4500):,.2f}")
        
        with col2:
            st.markdown("**Join Date:**")
            st.write(agent_data['agent_join_month'].strftime('%B %d, %Y'))
            
            st.markdown("**Tenure:**")
            st.write(f"{tenure_months} months")
        
        with col3:
            st.markdown("**First Policy Sale:**")
            if pd.notnull(agent_data['first_policy_sold_month']):
                st.write(agent_data['first_policy_sold_month'].strftime('%B %d, %Y'))
            else:
                st.write("No policy sold yet")
            
            st.markdown("**P-value:**")
            st.write(f"{round(float(agent_data.get('p_value', 0.88)), 2)}")

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
