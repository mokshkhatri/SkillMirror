import streamlit as st
from textwrap import dedent


def render_hero():

    st.markdown(
        dedent("""
<style>
.hero-section {
    text-align: center;
    padding-top: 55px;
    padding-bottom: 30px;
}

.hero-title {
    font-size: 56px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
}

.hero-subtitle {
    color: #9CA3AF;
    font-size: 17px;
    margin-top: 10px;
    margin-bottom: 36px;
}

div[data-testid="stTextInput"] {
    max-width: 760px;
    margin: auto;
}

div[data-testid="stTextInput"] input {
    background: #111827;
    color: white;
    border: 1px solid #374151;
    border-radius: 12px;
    height: 58px;
    padding-left: 18px;
    font-size: 15px;
}

div[data-testid="stTextInput"] input:focus {
    border: 1px solid #6366F1;
    box-shadow: 0 0 0 2px rgba(99,102,241,.15);
}

div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

div[data-testid="stButton"] button {
    background: #6366F1;
    color: white;
    border: none;
    border-radius: 10px;
    height: 48px;
    width: 230px;
    font-size: 15px;
    font-weight: 600;
}

div[data-testid="stButton"] button:hover {
    background: #4F46E5;
}
</style>

<div class="hero-section">
    <div class="hero-title">Enter Your Skills</div>
    <div class="hero-subtitle">
        Compare your skills with real industry requirements.
    </div>
</div>
"""),
        unsafe_allow_html=True
    )

    user_skills = st.text_input(
        label="Skills",
        placeholder="Python, SQL, Excel, Power BI, Machine Learning",
        label_visibility="collapsed"
    )

    left, center, right = st.columns([2, 1, 2])

    with center:
        analyze_clicked = st.button(
            "Analyze My Skills",
            use_container_width=True
        )

    return user_skills, analyze_clicked