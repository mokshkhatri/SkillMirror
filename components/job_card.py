import streamlit as st


def render_skills(skills, color="blue"):
    if not skills:
        st.caption("None")
        return

    text = " · ".join(skills)

    if color == "green":
        st.markdown(f":green[{text}]")
    elif color == "red":
        st.markdown(f":red[{text}]")
    elif color == "violet":
        st.markdown(f":violet[{text}]")
    else:
        st.markdown(f":blue[{text}]")


def render_job_card(job):
    with st.container(border=True):

        top_left, top_right = st.columns([2.3, 1])

        with top_left:
            st.markdown(f"### {job['job_title']}")
            st.caption(job["company_name"])

        with top_right:
            st.success(f"{job['score']}% \nRelevance")

        st.caption(
            f"{job['location']} • "
            f"{job['experience_raw']} • "
            f"{job['work_mode']} • "
            f"Rating {job['company_rating']}"
        )

        st.markdown("**Required Skills**")
        render_skills(job["required_skills"], "blue")

        st.markdown("**Your Skills**")
        render_skills(job["learned_skills"], "green")

        st.markdown("**Missing Skills**")
        render_skills(job["missing_skills"], "red")

        st.markdown("**Suggested Next Skills**")
        render_skills(job["next_skills"], "red")

        st.markdown("**Career Prediction**")
        render_skills([job["career_prediction"]], "violet")

        st.link_button(
            "View Details",
            job["job_url"],
            use_container_width=True
        )