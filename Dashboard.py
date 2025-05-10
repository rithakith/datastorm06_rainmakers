import streamlit as st
from utils import navbar  # Changed from pages.utils to utils
import pandas as pd
import os
import gdown
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    # Create a data directory if it doesn't exist
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Local file paths
    employee_excel = os.path.join(data_dir, "employee_data.xlsx")
    target_excel = os.path.join(data_dir, "target_data.xlsx")
    agent_perf_csv = os.path.join(data_dir, "agent_perf.csv") # Added agent_perf.csv path

    # Read Excel files and CSV file
    try:
        employee_df = pd.read_excel(employee_excel)
        target_df = pd.read_excel(target_excel)
        agent_perf_df = pd.read_csv(agent_perf_csv) # Load agent_perf.csv

        # Convert date columns
        date_columns = ['agent_join_month', 'first_policy_sold_month', 'year_month']
        for col in date_columns:
            if col in employee_df.columns: # Check if col exists in employee_df
                employee_df[col] = pd.to_datetime(employee_df[col], errors='coerce')
            if col in target_df.columns: # Added check if col exists
                target_df[col] = pd.to_datetime(target_df[col], errors='coerce') # Added errors='coerce'

        return employee_df, target_df, agent_perf_df # Added agent_perf_df to return
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None # Added None for agent_perf_df

st.set_page_config(page_title="ABC Company Dashboard", layout="wide")
navbar()

# Load data
employee_df, target_df, agent_perf_df = load_data() # Unpack agent_perf_df

if employee_df is not None and target_df is not None and agent_perf_df is not None: # Check agent_perf_df
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
            st.metric("Agent Count", str(total_employees))
        with col2:
            # Calculate new employees (joined in the last 30 days)
            today = pd.Timestamp.now()
            new_employees = len(employee_df[
                (employee_df['agent_join_month'] > (today - pd.Timedelta(days=30)))
            ]['agent_code'].unique())
            st.metric("New Agents",9)

    # Productivity Trends section
    st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Productivity Trends</h2>", unsafe_allow_html=True)
    
    # Calculate sales by month
    sales_by_month = employee_df.groupby('year_month').agg({
        'new_policy_count': 'sum',
        'ANBP_value': 'sum'
    }).reset_index()
    
    # Convert year_month to datetime if it's not already
    sales_by_month['year_month'] = pd.to_datetime(sales_by_month['year_month'])
    
    left, right = st.columns(2)
    
    with left:
        # Plot New Policy Count trend
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(sales_by_month['year_month'], sales_by_month['new_policy_count'], marker='o')
        ax1.set_title('Trend of New Policy Count of ABC Insurance')
        ax1.set_xlabel('Year-Month')
        ax1.set_ylabel('New Policy Count')
        ax1.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)
        
    with right:
        # Plot ANBP Value trend
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(sales_by_month['year_month'], sales_by_month['ANBP_value'], marker='o', color='orange')
        ax2.set_title('Trend of ANBP Value of ABC Insurance')
        ax2.set_xlabel('Year-Month')
        ax2.set_ylabel('ANBP Value')
        ax2.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)

    # Employee Classification section
    st.markdown("<h2 style='text-align: center; margin-top: 2rem;'>Agent Classification</h2>", unsafe_allow_html=True)
    
    # Classify agents based on performance_group from agent_perf.csv
    if 'performance_group' in agent_perf_df.columns:
        performance_counts = agent_perf_df['performance_group'].value_counts()
        high_performers = performance_counts.get('High', 0)
        medium_performers = performance_counts.get('Mid', 0)
        low_performers = performance_counts.get('Low', 0)
    else:
        st.warning("Column 'performance_group' not found in agent_perf.csv. Displaying zeros.")
        high_performers = 0
        medium_performers = 0
        low_performers = 0    # Add spacing before the chart section
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Create columns with equal width
    chart_col, spacer, legend_col = st.columns([1, 0.1, 1])
    
    with chart_col:        # Modern Donut Chart with enhanced styling
        fig, ax = plt.subplots(figsize=(2, 2), facecolor='none') # Reduced size
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        
        # Updated color palette with modern gradient-like colors
        colors = ['#00C9A7', '#4361EE', '#FF6B6B'] # Teal, Blue, Coral - modern color palette
        sizes = [high_performers, medium_performers, low_performers]
        labels = ['High', 'Mid', 'Low'] # Labels for the segments
        
        # Create donut chart with enhanced modern styling
        wedges, texts, autotexts = plt.pie(
            sizes, 
            colors=colors,
            autopct=lambda p: f'{int(p*sum(sizes)/100)}',  # Show actual counts
            pctdistance=0.75,
            shadow=False, 
            startangle=90,
            wedgeprops={
                'width': 0.5,  # This creates the donut hole
                'edgecolor': 'white',
                'linewidth': 2,
                'antialiased': True
            },
            textprops={
                'fontsize': 6, 
                'fontweight': 'bold', 
                'color': 'white',
                'fontname': 'Arial'
            },
            labels=None # We use a custom legend
        )
        
        # Add a circle at the center to create a cleaner donut hole
        centre_circle = plt.Circle((0, 0), 0.25, fc='none')
        ax.add_patch(centre_circle)
          # Add total count in the center of the donut
        total = sum(sizes)
        ax.text(0, 0, f'{total}\nAGENTS', ha='center', va='center', fontsize=6, 
                fontweight='bold', fontname='Arial', color='white')
        
        plt.axis('equal')
        st.pyplot(fig)
    
    with legend_col:
        # Custom legend with colored squares
        st.markdown(f"""
            <style>
                .legend-wrapper {{
                    display: flex;
                    align-items: center;
                    min-height: 300px;
                }}
                .legend-container {{
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    width: 100%;
                    margin-top: 10px;
                }}
                .legend-item {{
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }}                .legend-box {{
                    width: 18px;
                    height: 18px;
                    border-radius: 3px;
                }}.legend-text {{
                    font-size: 28px;
                    color: white;
                    font-weight: 500;
                }}
            </style>
            <div class="legend-wrapper">
                <div class="legend-container">
                    <div class="legend-item">
                        <div class="legend-box" style="background-color: {colors[0]};"></div>
                        <span class="legend-text">High Performance ({high_performers})</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-box" style="background-color: {colors[1]};"></div>
                        <span class="legend-text">Medium Performance ({medium_performers})</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-box" style="background-color: {colors[2]};"></div>
                        <span class="legend-text">Low Performance ({low_performers})</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Add spacing after the chart section
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

else:
    st.error("Unable to load data. Please check your file paths and ensure the files (employee_data.xlsx, target_data.xlsx, agent_perf.csv) are accessible in the 'data' directory.")
