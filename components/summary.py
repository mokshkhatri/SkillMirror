import streamlit as st


def render_summary(
    best_match,
    strong_skills,
    missing_skills,
    next_priority
):
    st.markdown("## Overall Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.markdown("**Best Match**")
            st.markdown(f":violet[{best_match}]")

    with col2:
        with st.container(border=True):
            st.markdown("**Strong Skills**")

            if strong_skills:
                st.markdown(f":green[{' · '.join(strong_skills)}]")
            else:
                st.caption("No strong skills identified")

    with col3:
        with st.container(border=True):
            st.markdown("**Important Missing Skills**")

            if missing_skills:
                st.markdown(f":red[{' · '.join(missing_skills)}]")
            else:
                st.caption("No missing skills identified")

    with col4:
        with st.container(border=True):
            st.markdown("**Next Learning Priority**")
            st.markdown(f":blue[{next_priority}]")