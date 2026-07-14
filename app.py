import streamlit as st

from components.navbar import render_navbar
from components.hero import render_hero
from components.job_card import render_job_card
from components.summary import render_summary
from components.charts import render_charts
from components.roadmap import render_roadmap


st.set_page_config(
    page_title="SkillMirror",
    page_icon="SM",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(
            circle at top,
            #111827 0%,
            #020617 45%,
            #000814 100%
        );

        color: #ffffff;
    }

    .block-container {
        padding-top: 3.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


render_navbar()

user_skills, analyze_clicked = render_hero()


if analyze_clicked:

    if not user_skills.strip():
        st.warning("Please enter at least one skill.")

    else:
        st.markdown("## Recommended Jobs")

        jobs = [
            {
                "job_title": "Data Analyst",
                "company_name": "Infosys",
                "location": "Bengaluru",
                "experience_raw": "0-2 Years",
                "work_mode": "Hybrid",
                "company_rating": "4.1",
                "score": 92,
                "required_skills": [
                    "Python",
                    "SQL",
                    "Excel"
                ],
                "learned_skills": [
                    "Python",
                    "SQL"
                ],
                "missing_skills": [
                    "Excel"
                ],
                "next_skills": [
                    "Excel"
                ],
                "career_prediction": "Data Analyst",
                "job_url": "https://www.naukri.com/"
            },

            {
                "job_title": "Business Analyst",
                "company_name": "Accenture",
                "location": "Noida",
                "experience_raw": "0-1 Years",
                "work_mode": "Remote",
                "company_rating": "4.3",
                "score": 88,
                "required_skills": [
                    "Excel",
                    "Power BI",
                    "SQL"
                ],
                "learned_skills": [
                    "Excel"
                ],
                "missing_skills": [
                    "Power BI",
                    "SQL"
                ],
                "next_skills": [
                    "SQL"
                ],
                "career_prediction": "Business Analyst",
                "job_url": "https://www.naukri.com/"
            },

            {
                "job_title": "BI Analyst",
                "company_name": "Deloitte",
                "location": "Gurgaon",
                "experience_raw": "0-2 Years",
                "work_mode": "Office",
                "company_rating": "4.4",
                "score": 84,
                "required_skills": [
                    "SQL",
                    "Tableau",
                    "Power BI"
                ],
                "learned_skills": [
                    "SQL"
                ],
                "missing_skills": [
                    "Tableau",
                    "Power BI"
                ],
                "next_skills": [
                    "Power BI"
                ],
                "career_prediction": "BI Analyst",
                "job_url": "https://www.naukri.com/"
            }
        ]

        col1, col2, col3 = st.columns(3)

        with col1:
            render_job_card(jobs[0])

        with col2:
            render_job_card(jobs[1])

        with col3:
            render_job_card(jobs[2])

        render_summary(
            best_match="Data Analyst at Infosys",
            strong_skills=[
                "Python",
                "SQL",
                "Excel"
            ],
            missing_skills=[
                "Power BI",
                "Tableau",
                "Django"
            ],
            next_priority="Power BI"
        )

        render_charts()

        roadmap_steps = [
            {
                "title": "Learn Power BI Basics",
                "tasks": [
                    "Understand the Power BI interface",
                    "Import and clean datasets",
                    "Create basic visualizations"
                ]
            },
            {
                "title": "Build a Dashboard",
                "tasks": [
                    "Learn data modelling",
                    "Create calculated columns",
                    "Build an interactive dashboard"
                ]
            },
            {
                "title": "Learn Tableau Basics",
                "tasks": [
                    "Understand Tableau worksheets",
                    "Connect different data sources",
                    "Create charts and dashboards"
                ]
            },
            {
                "title": "Complete a Project",
                "tasks": [
                    "Build an analytics project",
                    "Upload it to GitHub",
                    "Add it to your resume"
                ]
            }
        ]

        render_roadmap(roadmap_steps)