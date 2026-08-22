import nltk
import pandas as pd
import streamlit as st
from collections import Counter


nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

from components.navbar import render_navbar
from components.hero import render_hero
from components.job_card import render_job_card
from components.summary import render_summary
from components.charts import render_charts
from components.roadmap import render_roadmap

from src.tokenizer import tokenize_dataframe
from src.tfidf_model import build_tfidf_matrix
from src.similarity import search

from src.skill_validator import (
    validate_skills,
    get_final_skills
)

from src.skill_gap import analyze_recommended_jobs

from src.career_predictor import (
    generate_report as generate_career_report
)

from src.roadmap import generate_complete_roadmap

from src.market_analysis import (
    get_market_skill_frequency,
    get_common_missing_skills,
    calculate_market_readiness
)

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
    header[data-testid="stHeader"] {
        background: transparent;
    }
    .insight-row {
        display: flex;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #1e293b;
        gap: 12px;
    }
    .insight-skill {
        font-size: 0.9rem;
        color: #e2e8f0;
        font-weight: 500;
        min-width: 120px;
    }
    .insight-bar-wrap {
        flex: 1;
        background: #1e293b;
        border-radius: 4px;
        height: 6px;
        overflow: hidden;
    }
    .insight-bar {
        height: 6px;
        border-radius: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    .insight-count {
        font-size: 0.8rem;
        color: #64748b;
        min-width: 50px;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_resource
def load_recommendation_engine():
    jobs_df = pd.read_csv("data/skills_ready_jobs.csv")

    required_columns = {
        "job_title", "company_name", "location",
        "experience_raw", "work_mode", "company_rating",
        "job_url", "skills_required"
    }

    missing_columns = required_columns.difference(jobs_df.columns)

    if missing_columns:
        raise ValueError(
            "Missing columns in skills_ready_jobs.csv: "
            + ", ".join(sorted(missing_columns))
        )

    jobs_df = tokenize_dataframe(jobs_df)
    vectorizer, tfidf_matrix = build_tfidf_matrix(jobs_df)
    return jobs_df, vectorizer, tfidf_matrix


try:
    jobs_df, vectorizer, tfidf_matrix = load_recommendation_engine()
except Exception as error:
    st.error(f"Could not load recommendation engine: {error}")
    st.stop()


render_navbar()
user_skills, analyze_clicked = render_hero()


if analyze_clicked:

    if not user_skills.strip():
        st.warning("Please enter at least one skill.")

    else:
        accepted_skills, suggestions, ignored_skills = validate_skills(user_skills)
        final_skills = get_final_skills(user_skills)

        if not final_skills:
            st.warning(
                "No valid technical skills were found. "
                "Try entering skills such as Python, SQL, Java, Excel or Power BI."
            )
            st.stop()

        if suggestions:
            corrected_text = ", ".join(
                f"{wrong.title()} → {correct.title()}"
                for wrong, correct in suggestions.items()
            )
            st.info(f"Corrected skills: {corrected_text}")

        if ignored_skills:
            ignored_text = ", ".join(skill.title() for skill in ignored_skills)
            st.warning(f"Ignored inputs: {ignored_text}")

        validated_query = ", ".join(final_skills)

        with st.spinner("Analyzing your skills and finding matching jobs..."):
            recommended_jobs = search(
                query=validated_query,
                df=jobs_df,
                vectorizer=vectorizer,
                tfidf_matrix=tfidf_matrix,
                top_n=15
            )

        if not recommended_jobs:
            st.warning("No matching jobs were found.")
            st.stop()

        analyzed_jobs = analyze_recommended_jobs(
            user_skills=final_skills,
            recommended_jobs=recommended_jobs,
            next_skill_limit=3
        )

        # ── DEDUPLICATION ─────────────────────────────────────────────────────
        seen = set()
        unique_jobs = []
        for job in analyzed_jobs:
            key = (job['job_title'].lower().strip(), job['company_name'].lower().strip())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        analyzed_jobs = unique_jobs

        market_skill_frequency = get_market_skill_frequency(analyzed_jobs)

        market_missing_skills = get_common_missing_skills(
            skill_frequency=market_skill_frequency,
            user_skills=final_skills,
            limit=5
        )

        market_readiness = calculate_market_readiness(
            skill_frequency=market_skill_frequency,
            user_skills=final_skills
        )

        cleaned_user_skills = {
            str(skill).strip().lower()
            for skill in final_skills
            if str(skill).strip()
        }

        market_strong_skills = [
            skill
            for skill, count in market_skill_frequency.most_common()
            if skill in cleaned_user_skills
        ]

        career_report = generate_career_report(final_skills)
        recommended_career = career_report.get("recommended_career")

        if recommended_career:
            career_name = recommended_career.get("career", analyzed_jobs[0]["job_title"])
        else:
            career_name = analyzed_jobs[0]["job_title"]

        for job in analyzed_jobs:
            job["career_prediction"] = career_name

        display_jobs = analyzed_jobs[:3]

        st.markdown("## Recommended Jobs")

        job_columns = st.columns(len(display_jobs))
        for column, job in zip(job_columns, display_jobs):
            with column:
                render_job_card(job)

        best_job = display_jobs[0]
        next_priority = market_missing_skills[0] if market_missing_skills else "No major market skill gap"

        render_summary(
            best_match=f"{best_job['job_title']} at {best_job['company_name']}",
            strong_skills=market_strong_skills,
            missing_skills=market_missing_skills[:3],
            next_priority=next_priority
        )

        career_chart_data = career_report.get("chart_data", [])
        render_charts(skill_match=market_readiness, career_data=career_chart_data)

        roadmap_steps = generate_complete_roadmap(
            missing_skills=market_missing_skills,
            total_weeks=4
        )

        if roadmap_steps:
            render_roadmap(roadmap_steps)
        else:
            st.markdown("## Personalized Roadmap")
            st.success("You already possess the major skills required across the relevant job market.")

        # ── MARKET INSIGHTS ───────────────────────────────────────────────────
        st.markdown("## Market Insights")
        st.caption("Most demanded skills across your top matching jobs")

        # Use the already calculated market skill frequency
        # instead of splitting skills manually.
        freq = market_skill_frequency.most_common(10)

        if freq:
            max_count = freq[0][1]
            half = len(freq) // 2
            col_a, col_b = st.columns(2)

            for i, (skill, count) in enumerate(freq):
                bar_pct = int((count / max_count) * 100)
                col = col_a if i < half else col_b
                with col:
                    st.markdown(f"""
                    <div class="insight-row">
                        <span class="insight-skill">{skill.title()}</span>
                        <div class="insight-bar-wrap">
                            <div class="insight-bar" style="width:{bar_pct}%"></div>
                        </div>
                        <span class="insight-count">{count} jobs</span>
                    </div>
                    """, unsafe_allow_html=True)