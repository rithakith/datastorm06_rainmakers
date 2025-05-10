import streamlit as st
from pages.utils import navbar
from app import load_data

st.set_page_config(page_title="Nill Agents", layout="wide")
navbar()

st.title("Nill Agents")

# Load data
employee_df, target_df = load_data()

if employee_df is not None and target_df is not None:
    nill_agents = len(target_df[target_df['target'] == 0])
    st.metric("Total Nill Agents", str(nill_agents))

    # Get list of nill agents
    nill_agent_codes = target_df[target_df['target'] == 0]['agent_code'].tolist()

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Agent Code")
    with col2:
        st.selectbox("Select Nill Agent", nill_agent_codes)

    st.markdown("#### Demographics")
    if nill_agent_codes:
        selected_agent = nill_agent_codes[0]  # Default to first agent
        agent_data = employee_df[employee_df['agent_code'] == selected_agent].iloc[0]
        
        demo = {
            "Employee Code": selected_agent,
            "Age": int(agent_data['agent_age']),
            "Monthly Income": f"${agent_data.get('monthly_income', 3000):,.0f}",
            "P-value": round(float(agent_data.get('p_value', 0.73)), 2),
            "Months Worked": int((agent_data['year_month'] - agent_data['agent_join_month']).days / 30)
        }
        st.json(demo)

    # TODO: Add visualization for policy count over months
    st.markdown("#### Policy Count Over Months")
    st.markdown("⬜️ **[TODO] Add Time Series Chart Here**")

    st.markdown("#### Smart Plan Recommendations")
    st.markdown("""
    - 📌 Assign Mentor  
    - 📈 Weekly Check-ins  
    - 🎯 Personal Goal Setup  
    - 🛠️ Training Programs
    """)
else:
    st.error("Unable to load data. Please check your Google Drive file IDs and ensure the files are accessible.")
