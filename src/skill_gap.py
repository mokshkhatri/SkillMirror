import pandas as pd
import re

# ---------------------------------
# Load Datasets
# ---------------------------------

jobs = pd.read_csv("data/skills_ready_jobs.csv")
logs = pd.read_csv("data/user_logs.csv")
technical_skills = pd.read_csv("data/technical_skills.csv")


# ---------------------------------
# Load Market Skills
# ---------------------------------

def load_market_skills():

    market_skills = set()

    valid_skills = set(
        technical_skills["skill"]
        .dropna()
        .str.lower()
        .str.strip()
    )

    for row in jobs["skills_required"]:

        if pd.isna(row):
            continue

        text = str(row).lower()

        words = re.split(
            r"[,/;|()\n]+|\s+",
            text
        )

        for word in words:

            word = word.strip()

            if word in valid_skills:

                market_skills.add(word)

    return market_skills


# ---------------------------------
# Load Student Skills
# ---------------------------------

def load_student_skills(
        market_skills,
        user_skills=None
):

    student_skills = set()

    # Streamlit Mode

    if user_skills is not None:

        for skill in user_skills:

            skill = skill.lower().strip()

            if skill in market_skills:

                student_skills.add(skill)

        return student_skills

    # CSV Mode (Testing)

    for log in logs["Log"]:

        if pd.isna(log):
            continue

        skill = str(log).lower().strip()

        if skill in market_skills:

            student_skills.add(skill)

    return student_skills


# ---------------------------------
# Calculate Skill Gap
# ---------------------------------

def calculate_skill_gap(
        market_skills,
        student_skills
):

    learned = market_skills.intersection(
        student_skills
    )

    missing = market_skills.difference(
        student_skills
    )

    return learned, missing


# ---------------------------------
# Calculate Skill Match
# ---------------------------------

def calculate_alignment(
        market_skills,
        student_skills
):

    if len(market_skills) == 0:

        return 0

    return round(

        (
            len(student_skills)
            / len(market_skills)
        ) * 100,

        2

    )


# ---------------------------------
# Suggested Next Skills
# ---------------------------------

def show_next_skills(
        student_skills,
        market_skills
):

    next_skills = []

    missing = sorted(

        list(

            market_skills
            - student_skills

        )

    )

    for skill in missing[:5]:

        estimated_match = round(

            (

                (
                    len(student_skills)
                    + 1

                )

                / len(market_skills)

            ) * 100,

            2

        )

        next_skills.append({

            "skill": skill,

            "estimated_match":
                estimated_match

        })

    return next_skills

# ---------------------------------
# Generate Report
# ---------------------------------

def generate_report(user_skills=None):

    market_skills = load_market_skills()

    student_skills = load_student_skills(
        market_skills,
        user_skills
    )

    learned, missing = calculate_skill_gap(
        market_skills,
        student_skills
    )

    match_score = calculate_alignment(
        market_skills,
        student_skills
    )

    next_skills = show_next_skills(
        student_skills,
        market_skills
    )

    report = {

    "summary": {

        "total_market_skills": len(market_skills),

        "skills_learned": len(learned),

        "skill_match": match_score

    },

    "learned": sorted(list(learned))

}

    return report


# ---------------------------------
# Display Report (Terminal Testing)
# ---------------------------------

def display_report(report):

    print("\n")
    print("=" * 50)
    print("          SKILL MIRROR REPORT")
    print("=" * 50)

    print(f"\nTotal Market Skills : {report['summary']['total_market_skills']}")
    print(f"Skills Learned      : {report['summary']['skills_learned']}")
    print(f"Skill Match         : {report['summary']['skill_match']}%")

    print("\n" + "=" * 50)
    print("YOUR LEARNED SKILLS")
    print("=" * 50)

    if len(report["learned"]) == 0:

        print("No matching technical skills found.")

    else:

        for skill in report["learned"]:

            print(f"✔ {skill.title()}")

# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    report = generate_report()

    display_report(report)