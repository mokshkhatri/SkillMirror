import streamlit as st


def render_roadmap(roadmap_steps):
    st.markdown("## Personalized Roadmap")

    columns = st.columns(len(roadmap_steps))

    for index, step in enumerate(roadmap_steps):
        with columns[index]:
            with st.container(border=True):
                st.markdown(f"### Week {index + 1}")
                st.markdown(f"**{step['title']}**")

                for task in step["tasks"]:
                    st.markdown(f"- {task}")