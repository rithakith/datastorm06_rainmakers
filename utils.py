import streamlit as st
from pathlib import Path
import os

def navbar():
    # Hide the default menu button and navigation in the sidebar
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            .css-1vq4p4l.e1fqkh3o4 {padding-top: 2rem;}
            /* Uncomment the lines below if you want to hide the navigation sidebar */
            /* 
            .st-emotion-cache-iiif1v.ef3psqc4 {display: none;}  
            .css-h5rgaw.ef3psqc1 {display: none;}
            section[data-testid="stSidebar"] {display: none;}  
            */
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Load logo using absolute path from the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, 'assets', 'logo.png')
        try:
            st.image(logo_path, width=140)
        except Exception as e:
            st.error(f"Unable to load logo: {str(e)}")    
    with col2:
        st.markdown(
            """
            <nav style="
                display: flex;
                align-items: center;
                justify-content: flex-end;
                height: 100%;
                padding: 0.5rem 0;            ">                <div style="
                    display: flex;
                    align-items: center;
                    gap: 2rem;
                    font-size: 16px;
                ">
                    <a href="/" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Dashboard</a>
                    <a href="/2_Nill_Agents" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Nill Agents</a>
                    <a href="/3_Employees" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Employees</a>
                </div>
            </nav>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin: 0.5rem 0 1rem 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
