import streamlit as st


def render_navbar():
    st.markdown(
        """
        <style>
        .brand-title {
            font-size: 30px;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
        }

        .brand-title span {
            color: #6366F1;
        }

        .brand-subtitle {
            color: #94A3B8;
            font-size: 13px;
            margin-top: 6px;
        }

        .nav-item {
            color: #94A3B8;
            font-size: 14px;
            font-weight: 500;
            text-align: center;
            padding-bottom: 8px;
        }

        .nav-active {
            color: #ffffff;
            font-weight: 700;
            border-bottom: 2px solid #6366F1;
        }

        .nav-line {
            border-bottom: 1px solid #1F2937;
            margin-top: 18px;
            margin-bottom: 28px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.7, 1.3])

    with left:
        st.markdown(
            """
            <div class="brand-title">Skill<span>Mirror</span></div>
            <div class="brand-subtitle">Compare your skills with real industry requirements</div>
            """,
            unsafe_allow_html=True
        )

    with right:
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown('<div class="nav-item nav-active">Dashboard</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="nav-item">Jobs</div>', unsafe_allow_html=True)

        with c3:
            st.markdown('<div class="nav-item">Roadmap</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="nav-item">Analytics</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-line"></div>', unsafe_allow_html=True)