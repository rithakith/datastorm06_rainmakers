import streamlit as st
from pages.utils import navbar
from app import load_data

st.set_page_config(page_title="Employees", layout="wide")
navbar()

st.title("Employee Details")

# Load data
employee_df, target_df = load_data()

if employee_df is not None and target_df is not None:
    # Get unique employee codes
    employee_codes = employee_df['agent_code'].unique().tolist()

    col1, col2 = st.columns(2)
    with col1:
        entered_code = st.text_input("Employee Code")
    with col2:
        selected_code = st.selectbox("Select Employee", employee_codes)
    
    # Use either entered code or selected code
    employee_code = entered_code if entered_code else selected_code
    
    if employee_code in employee_codes:
        agent_data = employee_df[employee_df['agent_code'] == employee_code].iloc[0]
        
        # Determine performance status
        avg_policies = employee_df[employee_df['agent_code'] == employee_code]['new_policy_count'].mean()
        status = "High" if avg_policies > 20 else "Medium" if avg_policies > 10 else "Low"
        st.markdown(f"#### Performance Status: **{status}**")

        st.markdown("##### Predicted vs Real Policy Count")
        predicted = round(avg_policies * 1.15)  # Simple prediction for demo
        real = round(avg_policies)
        st.metric("Predicted", str(predicted), f"+{predicted - real}")
        st.metric("Real", str(real))

        st.markdown("#### Demographics")
        demo = {
            "Employee Code": employee_code,
            "Age": int(agent_data['agent_age']),
            "Monthly Income": f"${agent_data.get('monthly_income', 4500):,.0f}",
            "P-value": round(float(agent_data.get('p_value', 0.88)), 2),
            "Months Worked": int((agent_data['year_month'] - agent_data['agent_join_month']).days / 30)
        }
        st.json(demo)

        # TODO: Add visualization for policy count over months
        st.markdown("#### Policy Count Over Months")
        st.markdown("⬜️ **[TODO] Add Line Chart**")
else:
    st.error("Unable to load data. Please check your Google Drive file IDs and ensure the files are accessible.")
