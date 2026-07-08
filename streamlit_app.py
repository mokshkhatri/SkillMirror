import streamlit as st
import pandas as pd

from src.skill_validator import validate_skills
from src.skill_gap import generate_report as skill_gap_report
from src.career_predictor import generate_report as career_report
from src.roadmap import generate_roadmap

st.set_page_config(page_title="SkillMirror", page_icon="🎯", layout="wide")

st.title("🎯 SkillMirror")
st.markdown("### Compare your skills with industry demands")
st.divider()

st.sidebar.title("🎯 SkillMirror")

skills = st.sidebar.text_area(
    "Enter Technical Skills",
    placeholder="Python, SQL, Excel"
)

analyze = st.sidebar.button("🚀 Analyze")

if analyze:

    accepted, corrected, ignored = validate_skills(skills)
    report = skill_gap_report(accepted)
    career = career_report(accepted)
    best = career["recommended_career"]
    roadmap = generate_roadmap(best["missing_skills"])

    st.success("Profile analyzed successfully!")

    c1,c2,c3 = st.columns(3)
    with c1:
        st.subheader("✅ Accepted")
        if accepted:
            for s in accepted:
                st.success(s.title())
        else:
            st.warning("None")

    with c2:
        st.subheader("✏ Corrections")
        if corrected:
            for w,c in corrected.items():
                st.info(f"{w.title()} → {c.title()}")
        else:
            st.write("No corrections")

    with c3:
        st.subheader("❌ Ignored")
        if ignored:
            for s in ignored:
                st.error(s.title())
        else:
            st.write("None")

    st.divider()
    st.header("📊 Skill Mirror Report")
    summary=report["summary"]
    m1,m2,m3=st.columns(3)
    m1.metric("Accepted Skills", len(accepted))
    m2.metric("Career Match", f"{best['match_score']}%")
    m3.metric("Skill Match", f"{summary['skill_match']}%")
    st.info(f"Your current profile matches approximately **{summary['skill_match']}%** of the required skills.")
    st.progress(summary["skill_match"]/100)

    with st.expander("📚 Learned Skills", expanded=True):
        if report["learned"]:
            cols=st.columns(3)
            for i,s in enumerate(report["learned"]):
                cols[i%3].success(s.title())
        else:
            st.warning("No learned skills yet.")

    st.divider()
    st.header("🎯 Recommended Career")
    a,b=st.columns([2,1])
    with a:
        st.success(best["career"])
        st.markdown(f"## {best['stars']}")
    with b:
        st.metric("Career Match",f'{best["match_score"]}%')

    with st.expander("✅ Matched Skills", expanded=True):
        if best["matched_skills"]:
            cols=st.columns(3)
            for i,s in enumerate(best["matched_skills"]):
                cols[i%3].success(s.title())
        else:
            st.warning("None")

    with st.expander("❌ Skills to Learn", expanded=True):
        if best["missing_skills"]:
           cols=st.columns(3)
           for i,s in enumerate(best["missing_skills"][:9]):
               cols[i%3].error(s.title())

        else:   
            st.success("No additional skills required.")   

    st.divider()
    st.header("🏆 Top Career Matches")

    df = pd.DataFrame(career["top_matches"])[["career", "match_score"]]
    df.columns = ["Career", "Match %"]

    st.dataframe(df, use_container_width=True)

    st.divider()
    with st.expander("🗺️ Learning Roadmap", expanded=True):
        if roadmap:
            cols=st.columns(2)
            for i,item in enumerate(roadmap):
                with cols[i%2]:
                    st.info(f"**{item['week']}**\n\n{item['skill']}")

    st.divider()
    st.header("📋 Overall Summary")
    st.success(f"Recommended Career: {best['career']}")
    c1, c2, c3 = st.columns(3)

    c1.metric("Career", best["career"])

    c2.metric("Career Match", f"{best['match_score']}%")

    c3.metric("Skill Match", f"{summary['skill_match']}%")