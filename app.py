import nltk
import pandas as pd
import streamlit as st


# ---------------------------------
# Download Required NLTK Resources
# ---------------------------------

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


# ---------------------------------
# Import Streamlit Components
# ---------------------------------

from components.navbar import render_navbar
from components.hero import render_hero
from components.job_card import render_job_card
from components.summary import render_summary
from components.charts import render_charts
from components.roadmap import render_roadmap


# ---------------------------------
# Import Mahi's Recommendation Files
# ---------------------------------

from src.tokenizer import tokenize_dataframe
from src.tfidf_model import build_tfidf_matrix
from src.similarity import search


# ---------------------------------
# Import Akshat's Backend Files
# ---------------------------------

from src.skill_validator import (
    validate_skills,
    get_final_skills
)

from src.skill_gap import analyze_recommended_jobs

from src.career_predictor import (
    generate_report as generate_career_report
)

from src.roadmap import generate_complete_roadmap


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="SkillMirror",
    page_icon="SM",
    layout="wide"
)


# ---------------------------------
# Global Styling
# ---------------------------------

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


# ---------------------------------
# Load Recommendation Engine
# ---------------------------------

@st.cache_resource
def load_recommendation_engine():
    """
    Loads the prepared jobs dataset and builds the
    TF-IDF recommendation engine once.
    """

    jobs_df = pd.read_csv(
        "data/skills_ready_jobs.csv"
    )

    required_columns = {
        "job_title",
        "company_name",
        "location",
        "experience_raw",
        "work_mode",
        "company_rating",
        "job_url",
        "skills_required"
    }

    missing_columns = required_columns.difference(
        jobs_df.columns
    )

    if missing_columns:
        raise ValueError(
            "Missing columns in skills_ready_jobs.csv: "
            + ", ".join(sorted(missing_columns))
        )

    jobs_df = tokenize_dataframe(
        jobs_df
    )

    vectorizer, tfidf_matrix = build_tfidf_matrix(
        jobs_df
    )

    return jobs_df, vectorizer, tfidf_matrix


# ---------------------------------
# Load Engine Safely
# ---------------------------------

try:
    jobs_df, vectorizer, tfidf_matrix = (
        load_recommendation_engine()
    )

except Exception as error:
    st.error(
        f"Could not load recommendation engine: {error}"
    )

    st.stop()


# ---------------------------------
# Render Navbar and Hero
# ---------------------------------

render_navbar()

user_skills, analyze_clicked = render_hero()


# ---------------------------------
# Analyze Button
# ---------------------------------

if analyze_clicked:

    if not user_skills.strip():

        st.warning(
            "Please enter at least one skill."
        )

    else:

        # ---------------------------------
        # Validate User Skills
        # ---------------------------------

        accepted_skills, suggestions, ignored_skills = (
            validate_skills(user_skills)
        )

        final_skills = get_final_skills(
            user_skills
        )

        if not final_skills:

            st.warning(
                "No valid technical skills were found. "
                "Try entering skills such as Python, SQL, "
                "Java, Excel or Power BI."
            )

            st.stop()


        # ---------------------------------
        # Show Corrections
        # ---------------------------------

        if suggestions:

            corrected_text = ", ".join(
                f"{wrong.title()} → {correct.title()}"
                for wrong, correct in suggestions.items()
            )

            st.info(
                f"Corrected skills: {corrected_text}"
            )


        # ---------------------------------
        # Show Ignored Inputs
        # ---------------------------------

        if ignored_skills:

            ignored_text = ", ".join(
                skill.title()
                for skill in ignored_skills
            )

            st.warning(
                f"Ignored inputs: {ignored_text}"
            )


        # ---------------------------------
        # Prepare Validated Query
        # ---------------------------------

        validated_query = ", ".join(
            final_skills
        )


        # ---------------------------------
        # Get Real Job Recommendations
        # ---------------------------------

        with st.spinner(
            "Analyzing your skills and finding matching jobs..."
        ):

            recommended_jobs = search(
                query=validated_query,
                df=jobs_df,
                vectorizer=vectorizer,
                tfidf_matrix=tfidf_matrix,
                top_n=3
            )


        if not recommended_jobs:

            st.warning(
                "No matching jobs were found."
            )

            st.stop()


        # ---------------------------------
        # Add Job-Specific Skill Gaps
        # ---------------------------------

        analyzed_jobs = analyze_recommended_jobs(
            user_skills=final_skills,
            recommended_jobs=recommended_jobs,
            next_skill_limit=3
        )


        # ---------------------------------
        # Generate Career Prediction
        # ---------------------------------

        career_report = generate_career_report(
            final_skills
        )

        recommended_career = career_report.get(
            "recommended_career"
        )

        if recommended_career:

            career_name = recommended_career.get(
                "career",
                analyzed_jobs[0]["job_title"]
            )

        else:

            career_name = analyzed_jobs[0][
                "job_title"
            ]


        # Add career prediction to each card
        for job in analyzed_jobs:

            job["career_prediction"] = career_name


        # ---------------------------------
        # Display Recommended Jobs
        # ---------------------------------

        st.markdown(
            "## Recommended Jobs"
        )

        job_columns = st.columns(
            len(analyzed_jobs)
        )

        for column, job in zip(
            job_columns,
            analyzed_jobs
        ):

            with column:

                render_job_card(
                    job
                )


        # ---------------------------------
        # Build Dynamic Summary
        # ---------------------------------

        best_job = analyzed_jobs[0]

        strong_skills = best_job.get(
            "learned_skills",
            []
        )

        missing_skills = best_job.get(
            "missing_skills",
            []
        )

        next_skills = best_job.get(
            "next_skills",
            []
        )

        if next_skills:

            next_priority = next_skills[0]

        else:

            next_priority = (
                "No major skill gap"
            )


        render_summary(
            best_match=(
                f"{best_job['job_title']} at "
                f"{best_job['company_name']}"
            ),
            strong_skills=strong_skills,
            missing_skills=missing_skills[:3],
            next_priority=next_priority
        )


        # ---------------------------------
        # Dynamic Charts
        # ---------------------------------

        career_chart_data = career_report.get(
            "chart_data",
            []
        )

        render_charts(
            skill_match=best_job.get(
                "skill_match",
                0
            ),
            career_data=career_chart_data
        )


        # ---------------------------------
        # Generate Dynamic Roadmap
        # ---------------------------------

        roadmap_steps = generate_complete_roadmap(
            missing_skills=missing_skills,
            total_weeks=4
        )

        if roadmap_steps:

            render_roadmap(
                roadmap_steps
            )

        else:

            st.markdown(
                "## Personalized Roadmap"
            )

            st.success(
                "You already possess all detected skills "
                "required for the best matching job."
            )