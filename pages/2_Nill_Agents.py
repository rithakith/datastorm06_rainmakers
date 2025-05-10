import streamlit as st
import pandas as pd
import sys
import os
# Add parent directory to path so we can import from root utils.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import navbar
from app import load_data, plot_new_policy_count, generate_agent_performance_chart, display_agent_info
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nill Agents", layout="wide")
navbar()

# Load data
employee_df, target_df = load_data()

if employee_df is not None and target_df is not None:
    nill_agents = len(target_df[target_df['target'] == 0])
    
    # Create a row with title and count
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Nill Agents")
    with col2:
        st.markdown(
            f'<div style="text-align: right; padding-top: 1rem;">'
            f'<h3>Count: {nill_agents}</h3>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Get list of nill agents
    nill_agent_codes = target_df[target_df['target'] == 0]['agent_code'].tolist()

    # Only show the select box for Nill Agents
    selected_agent = st.selectbox("Select Nill Agent", nill_agent_codes)

    if selected_agent:
        # Display agent basic information
        err, info_df = display_agent_info(employee_df, selected_agent)
        if err:
            st.warning(err)
        else:
            st.subheader("Agent Information")
            # Get the agent data
            agent_data = employee_df[employee_df['agent_code'] == selected_agent].iloc[0]
            tenure_months = int((agent_data['year_month'] - agent_data['agent_join_month']).days / 30)
            
            # Create two columns for agent information
            left_col, right_col = st.columns(2)
            with left_col:
                st.markdown("**Agent Code:**")
                st.write(selected_agent)
                
                st.markdown("**Age:**")
                st.write(f"{int(agent_data['agent_age'])} years")
                
                st.markdown("**Join Date:**")
                st.write(agent_data['agent_join_month'].strftime('%B %d, %Y'))
            
            with right_col:
                st.markdown("**Tenure:**")
                st.write(f"{tenure_months} months")
                
                st.markdown("**First Policy Sale:**")
                if pd.notnull(agent_data['first_policy_sold_month']):
                    st.write(agent_data['first_policy_sold_month'].strftime('%B %d, %Y'))
                else:
                    st.write("No policy sold yet")
                
                st.markdown("**Monthly Income:**")
                st.write(f"${agent_data.get('monthly_income', 3000):,.2f}")

        # Display metrics
        agent_data = employee_df[employee_df['agent_code'] == selected_agent]
        if not agent_data.empty:
            latest_data = agent_data.iloc[-1]
            average_anbp = agent_data['ANBP_value'].mean()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Latest P0 Value (ANBP)", f"${latest_data['ANBP_value']:,.2f}")
            with col2:
                st.metric("Average P0 Value (ANBP)", f"${average_anbp:,.2f}")
            with col3:
                st.metric("Latest Policy Count", str(latest_data['new_policy_count']))

        # Display performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("New Policy Count Trend")
            fig1, policy_stats = plot_new_policy_count(selected_agent, employee_df)
            if fig1:
                st.pyplot(fig1)
            else:
                st.warning(policy_stats)

        with col2:
            st.subheader("Monthly Performance Overview")
            fig2, monthly_data = generate_agent_performance_chart(selected_agent, employee_df)
            if fig2:
                st.pyplot(fig2)
            else:
                st.warning(monthly_data)

        # Show monthly performance data in expandable section
        if monthly_data is not None and not isinstance(monthly_data, str):
            with st.expander("View Monthly Performance Data"):
                st.dataframe(monthly_data, use_container_width=True)

        # Smart Plan Recommendations
        st.markdown("### Smart Plan Recommendations")
        st.markdown("""
        - 📌 **Mentorship Program**
          - Assign dedicated mentor for guidance
          - Weekly performance review sessions
        
        - 📈 **Performance Monitoring**
          - Track P0 value trends
          - Monitor policy conversion rates
        
        - 🎯 **Goal Setting**
          - Set realistic monthly targets
          - Break down goals into weekly objectives
        
        - 🛠️ **Training & Development**
          - Product knowledge enhancement
          - Sales technique workshops
        """)
else:
    st.error("Unable to load data. Please check your Google Drive file IDs and ensure the files are accessible.")
