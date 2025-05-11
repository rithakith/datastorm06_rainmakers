import streamlit as st
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

warnings.filterwarnings("ignore")
sns.set_style("whitegrid")

# --- Load Data ---
def load_data():
    train_file_id = '15h4aMcOsI_04ArugpJnOLfgRptcQ0A1o'
    nill_file_id = '1Ybo3nY6CYH55HMThOm4X1VhVcSsDfQK1'

    train_link = f'https://drive.google.com/uc?id={train_file_id}'
    nill_link = f'https://drive.google.com/uc?id={nill_file_id}'

    train_df = pd.read_csv(train_link)
    nill_agent = pd.read_csv(nill_link)

    train_df['agent_join_month'] = pd.to_datetime(train_df['agent_join_month'], format='%m/%d/%Y', errors='coerce')
    train_df['first_policy_sold_month'] = pd.to_datetime(train_df['first_policy_sold_month'], format='%m/%d/%Y', errors='coerce')
    train_df['year_month'] = pd.to_datetime(train_df['year_month'], format='%m/%d/%Y')

    return train_df, nill_agent

def display_agent_info(df, agent_code):
    agent_data = df[df['agent_code'] == agent_code]
    if agent_data.empty:
        return f"No data found for agent {agent_code}", None

    base_info = agent_data[['agent_code', 'agent_age', 'agent_join_month', 'first_policy_sold_month']].drop_duplicates()
    base_info = base_info.reset_index(drop=True)

    # Calculate tenure in months based on latest available 'year_month' entry
    latest_date = agent_data['year_month'].max()
    join_date = base_info.at[0, 'agent_join_month']

    if pd.notnull(join_date) and pd.notnull(latest_date):
        tenure_months = (latest_date.year - join_date.year) * 12 + (latest_date.month - join_date.month)
    else:
        tenure_months = np.nan

    base_info['tenure_months'] = tenure_months

    return None, base_info



def plot_new_policy_count(agent_code, df):
    agent_data = df[df['agent_code'] == agent_code]
    if agent_data.empty:
        return None, "No data found for plotting."

    agent_data = agent_data.sort_values('year_month')
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(agent_data['year_month'], agent_data['new_policy_count'], marker='o', color='teal')
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('New Policy Count')
    ax.set_title(f'New Policy Count for Agent {agent_code}')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    min_count = agent_data['new_policy_count'].min()
    max_count = agent_data['new_policy_count'].max()

    return fig, (min_count, max_count)




def classify_agent_performance(df, agent_code):
    """Classifies agent performance as High or not based on multiple KPIs."""
    agent_data_all = df[df['agent_code'] == agent_code]
    if agent_data_all.empty:
        return "No Data"

    # Averages from all months
    avg_new_policy_count = agent_data_all['new_policy_count'].mean()
    avg_ANBP_value = agent_data_all['ANBP_value'].mean()
    avg_unique_customers = agent_data_all['unique_customers'].mean()
    avg_unique_proposal = agent_data_all['unique_proposal'].mean()
    avg_proposal_to_quotation_ratio = agent_data_all['unique_quotations'].mean()/agent_data_all['unique_proposal'].replace(0, np.nan)
    avg_quotation_to_policy_ratio = agent_data_all['unique_quotations'].mean()/ agent_data_all['new_policy_count'].mean()
    # Get most recent month data for static features
    latest_row = agent_data_all.iloc[-1]
    agent_age = latest_row['agent_age']
    agent_tenure_months = latest_row['year_month'].month - latest_row['agent_join_month'].month 

    if (
        avg_new_policy_count > 27.95 and
        avg_ANBP_value > 1.544e6 and
        avg_unique_customers <= 15.30 and
        avg_unique_proposal > 22.54 and
        avg_proposal_to_quotation_ratio <= 0.70 and
        avg_quotation_to_policy_ratio > 2.01 and
        agent_age >= 40.6 and
        agent_tenure_months >= 29.38
    ):
        return 'High'
    else:
        return 'Not High'

def get_personalized_action_plan_system_binary_risk(agent_code, agent_data, target_nill_risk_flag):
    """
    agent_data: dictionary of the agent's LATEST month's data for activity,
                AND pre-calculated averages for performance classification 
                (e.g., 'avg_new_policy_count', 'avg_quotation_to_policy_ratio').
    target_nill_risk_flag: 0 if at NILL risk, 1 if not (as per your nill_agent['target'])
    """
    plan_components = []
    action_items = []
    
    # Correcting the NILL risk interpretation based on your file: target == 0 means NILL risk
    is_at_nill_risk = (target_nill_risk_flag == 0)

    plan_title = f"Personalized Action Plan for Agent {agent_code}"
    if is_at_nill_risk:
        plan_title += " (Flagged for NILL Risk)"
    else:
        # This function is primarily for at-risk agents.
        # If called for a non-at-risk agent, provide a different type of message or just basic info.
        return [f"Agent {agent_code}: Not currently flagged for NILL risk. General performance advice can be provided if needed."]

    # Classify performance based on pre-calculated averages in agent_data
    # These averages should be calculated from train_df over a recent period (e.g., 3-6 months)
    # and passed into agent_data.
    # For this example, let's assume agent_data contains:
    # 'avg_new_policy_count', 'avg_quotation_to_policy_ratio'
    performance_category = classify_agent_performance(train_df, selected_agent)
    plan_components.append(f"Recent Performance Category: {performance_category}")

    thresholds = { # These are for LATEST activity, not for overall classification
        "low_tenure": 6, # months
        "moderate_tenure": 12,
        "proposals_7d_low": 2,
        "proposals_7d_moderate": 5,
        "customers_7d_low": 2,
        "proposals_monthly_high_activity": 20, # Indicates high effort last month
        "policies_last_month_low_conversion": 2, # if high proposal activity
        "proposals_21d_very_low": 4,
        "customers_21d_very_low": 4
    }

    def get_metric(key, default=0): # Gets LATEST month's metric
        return agent_data.get(key, default)
    
    # --- ACTION PLAN LOGIC FOR AT-NILL-RISK AGENTS (is_at_nill_risk == True) ---
    if is_at_nill_risk:
        # --- Scenario 1: New Agents at NILL Risk ---
        if get_metric('tenure_months') < thresholds['low_tenure']:
            plan_components.append("Profile: New Agent at NILL Risk")
            if get_metric('unique_proposals_last_7_days') < thresholds['proposals_7d_low'] or \
               get_metric('unique_customers_last_7_days') < thresholds['customers_7d_low']:
                plan_components.append("Sub-Profile: Low Recent Activity")
                action_items.extend([
                    "T1: Attend 2-day intensive prospecting & lead generation workshop. (Time: Next 7 days)",
                    "M1: Shadow a top-performing senior agent for 3 client meetings. (Time: Next 10 days)",
                    "AG1(5, 5): Generate min. 5 unique proposals & 5 unique customer contacts weekly. (Time: Next 2 weeks)",
                    "MS1: Weekly check-ins with manager. (Time: Ongoing for 4 weeks)"
                ])
            elif get_metric('new_policy_count_last_month') == 0: # Active but no sales in latest reported month
                plan_components.append("Sub-Profile: Active but No Recent Sales (Conversion Issue)")
                action_items.extend([
                    "T2: Attend 'Closing Techniques & Objection Handling' module. (Time: Next 7 days)",
                    "SP1: Role-play 3 sales scenarios focusing on closing. (Time: Next 10 days)",
                    "M2: Weekly 30-min coaching with mentor. (Time: Next 4 weeks)",
                    "AG2(1): Aim for at least 1 new policy this month. (Time: This month)"
                ])
            else: # General support for new NILL risk agent
                action_items.append("MS1: Intensive daily check-ins with manager for 1 week to diagnose specific hurdles for new agents.")
                action_items.append("Review onboarding materials and identify knowledge gaps.")

        # --- Scenario 2: Experienced Agents at NILL Risk ---
        elif get_metric('tenure_months') >= thresholds['low_tenure']:
            plan_components.append("Profile: Experienced Agent at NILL Risk")

            # Sub-profile: High Performer anomoly (High performer suddenly at NILL risk)
            if performance_category == "High":
                plan_components.append("Sub-Profile: High Performer Anomaly")
                action_items.extend([
                    "RA1: Urgent discussion with manager: Understand external factors or sudden changes impacting performance. (Time: Next 24h)",
                    "Review recent client interactions for any negative feedback or lost deals.",
                    "MS1: Supportive check-ins, focus on problem-solving not pressure. (Time: Ongoing)"
                ])
            
            # Sub-profile: Medium Performer at NILL Risk
            elif performance_category == "Medium":
                plan_components.append("Sub-Profile: Medium Performer Dip")
                if get_metric('new_policy_count_last_month') == 0: # Stalled
                     action_items.extend([
                        "RA1: Joint review with manager on recent performance trends & pipeline health. (Time: Next 3 days)",
                        "RA2: Review top 20 dormant leads/past clients. (Time: Next 7 days)",
                        "AG1(7, 7): Re-energize pipeline: min. 7 proposals & 7 customer contacts weekly. (Time: Next 2 weeks)"
                     ])
                else: # General NILL risk for medium performer
                    action_items.append("Skill Gap Analysis: Identify specific areas (prospecting, closing, product) needing a refresher with manager.")
                    action_items.append("T3: Targeted refresher training based on gap analysis.")

            # Sub-profile: Low Performer at NILL Risk (Chronic Issue)
            elif performance_category == "Low":
                plan_components.append("Sub-Profile: Consistent Low Performer (Critical)")
                # Based on your EDA, Low performers have high unique_customers but low proposals & very bad conversion
                if get_metric('unique_proposal_last_month') < (get_metric('unique_customers_last_month') * 0.5) and get_metric('unique_customers_last_month') > 15: # High customer contact, low proposal generation
                    plan_components.append("Issue: Not converting customer interactions to proposals effectively.")
                    action_items.append("T_Qualify: Training on qualifying leads and transitioning conversations to proposals.")
                    action_items.append("SP_Propose: Role-play initial customer interactions to proposal stage.")
                elif get_metric('avg_proposal_to_quotation_ratio', 2) > 1.5 : # Using avg_ from agent_data; high ratio = bad
                    plan_components.append("Issue: Proposals not converting to Quotations (poor proposal quality/fit).")
                    action_items.append("MS2: Manager to review 5 recent proposals for quality, targeting, and value proposition.")
                    action_items.append("T_ProposalWrite: Workshop on effective proposal writing and customization.")
                elif get_metric('avg_quotation_to_policy_ratio', 1) < 1.0: # Using avg_ from agent_data; low ratio = bad
                     plan_components.append("Issue: Quotations not converting to Policies (closing/objection handling).")
                     action_items.extend([
                        "T2: Attend 'Closing Techniques & Objection Handling' module. (Time: Next 7 days)",
                        "SP1: Role-play 3 sales scenarios focusing on closing quotes. (Time: Next 10 days)"
                     ])
                else: # General for Low Performer at NILL
                    action_items.extend([
                        "PIP_Consider: Consider initiating a formal Performance Improvement Plan (PIP).",
                        "MS1: Intensive weekly coaching on fundamentals with manager.",
                        "AG2(1): Set a very small, achievable goal of 1 policy to build confidence. (Time: This month)"
                    ])
            
            # If experienced but no clear performance category or other flags for NILL risk
            if not action_items and (performance_category != "High"): # Avoid generic for High performers already handled
                plan_components.append("Sub-Profile: General NILL Risk for Experienced Agent")
                action_items.extend([
                    "RA1: Deep-dive review with manager. (Time: Next 2 days)",
                    "Identify 1 key barrier and 1 small win to achieve in the next 3 days.",
                    "MS1: Implement daily check-ins with manager for one week. (Time: Next 7 days)"
                ])

        # Fallback if no specific plan assigned yet for an at-NILL-risk agent
        if not action_items:
            action_items.append("RA_MANUAL: Agent is at NILL risk. Current metrics do not fit a predefined profile. Requires immediate manual review by manager to diagnose and plan.")
            plan_components.append("Profile: Undetermined NILL Risk (Requires Manual Review)")

    # --- Construct final plan ---
    final_plan_output = [plan_title]
    if plan_components:
        unique_insights = list(set(plan_components))

        # Create HTML blocks for each insight
        insight_boxes = ""
        for insight in unique_insights:
            insight_boxes += f"""
                <div style="
                    display: inline-block;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    padding: 10px 15px;
                    margin: 5px;
                    font-size: 14px;
                ">
                    {insight}
                </div>
            """

        # Display the insights with custom styling
        st.markdown(f"### Diagnostic Insights")
        st.markdown(insight_boxes, unsafe_allow_html=True)

    if action_items:
        final_plan_output.append("\nRecommended SMART Actions:")
        for i, item in enumerate(action_items):
            final_plan_output.append(f"{i+1}. {item}")
    elif not is_at_nill_risk: # Should have been caught earlier
        pass # Message already handled
    else: # is_at_nill_risk is True, but no actions
        final_plan_output.append("No specific automated actions identified for this NILL risk profile. Manager to conduct immediate manual review and develop a tailored plan.")

    return final_plan_output

def generate_agent_performance_chart(agent_code, df):
    agent_data = df[df['agent_code'] == agent_code].copy()
    if agent_data.empty:
        return None, f"No data found for agent {agent_code}"

    agent_data['year_month'] = pd.to_datetime(agent_data['year_month'])

    monthly_data = agent_data.groupby(agent_data['year_month'].dt.to_period('M'))[[
        'unique_proposal', 'unique_quotations', 'unique_customers', 'ANBP_value', 'net_income',
        'number_of_policy_holders', 'number_of_cash_payment_policies']].sum().reset_index()
    monthly_data['year_month'] = monthly_data['year_month'].astype(str)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(monthly_data['year_month'], monthly_data['unique_quotations'], marker='o', label='Quotations')
    ax.plot(monthly_data['year_month'], monthly_data['unique_proposal'], marker='o', label='Proposals')
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Count')
    ax.set_title(f'Agent {agent_code} - Quotations & Proposals Over Time')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig, monthly_data

# --- Streamlit UI ---
st.set_page_config(page_title="NILL Risk Dashboard", layout="wide")
st.title("NILL Risk Action Plan Dashboard")

train_df, nill_agent = load_data()
agent_options = nill_agent[nill_agent['target'] == 0]['agent_code'].tolist()
selected_agent = st.selectbox("Select an Agent at NILL Risk", agent_options)

if st.button("Generate Action Plan"):
    row = nill_agent[nill_agent['agent_code'] == selected_agent].iloc[0]
    agent_profile_row = train_df[train_df['agent_code'] == selected_agent]

    if agent_profile_row.empty:
        st.warning(f"No profile data found for {selected_agent}.")
    else:
        agent_profile_data = agent_profile_row.iloc[0].to_dict()
        plan = get_personalized_action_plan_system_binary_risk(selected_agent, agent_profile_data, row['target'])

        with st.expander("View Action Plan", expanded=True):
            for line in plan:
                st.markdown(f"- {line}")

        st.subheader("Agent Basic Information")
        err, info_df = display_agent_info(train_df, selected_agent)
        if err:
            st.warning(err)
        else:
            st.dataframe(info_df.style.set_properties(**{'text-align': 'left'}), use_container_width=True)

        # Add Monthly Performance Table to Basic Info
        fig_perf, monthly_data = generate_agent_performance_chart(selected_agent, train_df)
        with st.expander("Monthly Performance Data"):
            if monthly_data is not None:
                st.dataframe(monthly_data, use_container_width=True)

        # Charts in smaller columns
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("New Policy Count Trend")
            fig2, policy_stats = plot_new_policy_count(selected_agent, train_df)
            if fig2:
                col_min, col_max = st.columns(2)
                col_min.metric("Min Policy Count", policy_stats[0])
                col_max.metric("Max Policy Count", policy_stats[1])
                st.markdown('<div style="border:1px solid #ccc; padding:10px;">', unsafe_allow_html=True)
                st.pyplot(fig2)
                st.markdown('</div>', unsafe_allow_html=True)

                
            else:
                st.warning(policy_stats)

        with col2:
            st.subheader("Monthly Performance Overview")
            if fig_perf:
                st.markdown('<div style="border:1px solid #ccc; padding:10px;">', unsafe_allow_html=True)
                st.pyplot(fig_perf)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No performance chart available.")
