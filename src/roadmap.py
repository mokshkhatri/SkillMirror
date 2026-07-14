import re


# ---------------------------------
# Clean Missing Skills
# ---------------------------------

def parse_missing_skills(missing_skills):
    """
    Accepts either:

    String:
        "Power BI, Tableau, Docker"

    List:
        ["Power BI", "Tableau", "Docker"]

    Returns:
        ["power bi", "tableau", "docker"]
    """

    if missing_skills is None:
        return []

    if isinstance(missing_skills, str):
        raw_skills = re.split(
            r"[,;|\n/]+",
            missing_skills
        )
    else:
        raw_skills = missing_skills

    cleaned_skills = []

    for skill in raw_skills:
        skill = str(skill).strip().lower()
        skill = skill.strip("[]'\" ")

        if (
            skill
            and skill not in {
                "nan",
                "none",
                "not available"
            }
            and skill not in cleaned_skills
        ):
            cleaned_skills.append(skill)

    return cleaned_skills


# ---------------------------------
# Create Tasks for One Skill
# ---------------------------------

def create_skill_tasks(skill):
    """
    Generates simple learning tasks for one missing skill.
    """

    skill_title = skill.title()

    return [
        f"Learn the basics of {skill_title}",
        f"Practice {skill_title} with examples",
        f"Build one small project using {skill_title}"
    ]


# ---------------------------------
# Generate Four-Week Roadmap
# ---------------------------------

def generate_roadmap(
    missing_skills,
    max_weeks=4
):
    """
    Creates a personalized roadmap from missing skills.

    Each missing skill is assigned to one week.
    The Streamlit dashboard currently displays four weeks.
    """

    skills = parse_missing_skills(
        missing_skills
    )

    if max_weeks <= 0:
        return []

    selected_skills = skills[:max_weeks]

    roadmap = []

    for index, skill in enumerate(
        selected_skills,
        start=1
    ):
        roadmap.append(
            {
                "week": f"Week {index}",
                "title": f"Learn {skill.title()}",
                "skill": skill,
                "tasks": create_skill_tasks(skill)
            }
        )

    return roadmap


# ---------------------------------
# Add Final Project Week
# ---------------------------------

def generate_complete_roadmap(
    missing_skills,
    total_weeks=4
):
    """
    Creates up to three skill-learning weeks and uses
    the final week for a practical project.

    This matches the current SkillMirror UI better.
    """

    skills = parse_missing_skills(
        missing_skills
    )

    if total_weeks <= 0:
        return []

    skill_week_limit = max(
        total_weeks - 1,
        0
    )

    selected_skills = skills[:skill_week_limit]

    roadmap = []

    for index, skill in enumerate(
        selected_skills,
        start=1
    ):
        roadmap.append(
            {
                "week": f"Week {index}",
                "title": f"Learn {skill.title()}",
                "skill": skill,
                "tasks": create_skill_tasks(skill)
            }
        )

    if selected_skills:
        project_skills = ", ".join(
            skill.title()
            for skill in selected_skills
        )

        roadmap.append(
            {
                "week": f"Week {len(roadmap) + 1}",
                "title": "Build a Practical Project",
                "skill": "project",
                "tasks": [
                    f"Use {project_skills} in one project",
                    "Upload the project to GitHub",
                    "Add the project to your resume"
                ]
            }
        )

    return roadmap


# ---------------------------------
# Display Roadmap for Testing
# ---------------------------------

def display_roadmap(roadmap):

    print(
        "\n========== LEARNING ROADMAP ==========\n"
    )

    if not roadmap:
        print("No roadmap required.")
        return

    for item in roadmap:
        print(item["week"])
        print("-" * len(item["week"]))
        print(item["title"])

        for task in item["tasks"]:
            print(f"- {task}")

        print()


# ---------------------------------
# Main: Terminal Testing
# ---------------------------------

if __name__ == "__main__":

    sample_missing_skills = [
        "power bi",
        "tableau",
        "docker"
    ]

    roadmap = generate_complete_roadmap(
        sample_missing_skills
    )

    display_roadmap(roadmap)