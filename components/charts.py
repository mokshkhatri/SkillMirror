import streamlit as st
import plotly.graph_objects as go


def render_charts(skill_match, career_data):
    st.markdown("## Analytics")

    left, right = st.columns(2, gap="medium")

    # --------------------------------
    # Left: Overall Skill Match Gauge
    # --------------------------------
    with left:
        with st.container(border=True):
            st.markdown("### Market Readiness")

            gauge_value = float(skill_match or 0)

            gauge_chart = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=gauge_value,
                    number={
                        "suffix": "%",
                        "font": {
                            "size": 42,
                            "color": "#FFFFFF"
                        }
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100],
                            "tickwidth": 1,
                            "tickcolor": "#94A3B8"
                        },
                        "bar": {
                            "color": "#6366F1",
                            "thickness": 0.28
                        },
                        "bgcolor": "rgba(0,0,0,0)",
                        "borderwidth": 0,
                        "steps": [
                            {
                                "range": [0, 50],
                                "color": "#3F1D1D"
                            },
                            {
                                "range": [50, 75],
                                "color": "#3F3518"
                            },
                            {
                                "range": [75, 100],
                                "color": "#064E3B"
                            }
                        ]
                    }
                )
            )

            gauge_chart.update_layout(
                height=245,
                margin=dict(
                    l=25,
                    r=25,
                    t=10,
                    b=5
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FFFFFF")
            )

            st.plotly_chart(
                gauge_chart,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

    # --------------------------------
    # Right: Career Prediction Donut
    # --------------------------------
    with right:
        with st.container(border=True):
            st.markdown("### Career Prediction")

            if career_data:
                career_labels = [
                    item["career"]
                    for item in career_data
                ]

                career_values = [
                    item["percentage"]
                    for item in career_data
                ]

                career_chart = go.Figure(
                    data=[
                        go.Pie(
                            labels=career_labels,
                            values=career_values,
                            hole=0.68,
                            textinfo="percent",
                            textfont={
                                "size": 12
                            },
                            marker={
                                "colors": [
                                    "#6366F1",
                                    "#3B82F6",
                                    "#94A3B8"
                                ]
                            }
                        )
                    ]
                )

                career_chart.update_layout(
                    height=245,
                    margin=dict(
                        l=20,
                        r=20,
                        t=5,
                        b=10
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#FFFFFF"),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        x=0.5,
                        xanchor="center",
                        y=-0.05,
                        yanchor="top"
                    )
                )

                st.plotly_chart(
                    career_chart,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    }
                )

            else:
                st.info(
                    "Career prediction data is not available."
                )