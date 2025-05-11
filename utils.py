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
    
    with col1:        # Load logo using absolute path from the current directory
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
                    <a href="/" target="_self" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Dashboard</a>
                    <a href="/Nill_Agents" target="_self" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Nill Agents</a>
                    <a href="/Agents" target="_self" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Agents</a>
                </div>
            </nav>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin: 0.5rem 0 1rem 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

def footer():
    st.markdown(
        """
        <style>
            footer {
                margin-top: 10px;
                padding: 10px 0;
                background-color: rgba(38, 39, 48, 0.9);
                border-top: 1px solid rgba(250, 250, 250, 0.1);
                text-align: center;
                color: rgba(250, 250, 250, 0.8);
                font-size: 14px;
                margin-left: -75px;  /* Remove left margin/padding from Streamlit */
                margin-right: -75px; /* Remove right margin/padding from Streamlit */
                width: calc(100% + 150px); /* Compensate for the negative margins */
                margin-bottom: 0;
            }
            footer p {
                margin: 0;
                padding: 0 15px; /* Add padding for small screens */
                word-wrap: break-word; /* Ensure text wraps on small screens */
            }
            /* Responsive adjustments for mobile */
            @media screen and (max-width: 640px) {
                footer {
                    margin-left: -20px; /* Smaller negative margin for mobile */
                    margin-right: -20px;
                    width: calc(100% + 40px);
                }
                footer p {
                    font-size: 12px; /* Smaller font on mobile */
                }
            }
            /* Remove bottom spacing from Streamlit containers */
            .element-container:has(footer) {
                margin-bottom: 0 !important;
            }
            .block-container {
                padding-bottom: 0 !important;
            }
            /* Remove spacing after footer */
            footer + * {
                display: none !important;
            }
        </style>
        <footer>
            <p>Created by Team "RainMakers" &copy; 2025 | DataStorm 6.0 Competition</p>
        </footer>
        """,
        unsafe_allow_html=True
    )
