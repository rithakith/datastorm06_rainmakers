import streamlit as st
from pathlib import Path

def navbar():
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Load logo using Streamlit's image display
        logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
        st.image(str(logo_path), width=140)
    
    with col2:
        st.markdown(
            """
            <nav style="
                display: flex;
                align-items: center;
                justify-content: flex-end;
                height: 100%;
                padding: 0.5rem 0;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 2rem;
                    font-size: 16px;
                ">
                    <a href="/Home" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Dashboard</a>
                    <a href="/pages/2_Nill_Agents.py" style="
                        text-decoration: none;
                        color: white;
                        display: flex;
                        align-items: center;
                        transition: opacity 0.2s;
                        font-weight: 500;
                    ">Nill Agents</a>
                    <a href="/pages/3_Employees.py" style="
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
