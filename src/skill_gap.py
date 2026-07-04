import pandas as pd
import re


# -------------------------------
# Load datasets
# -------------------------------

jobs = pd.read_csv("data/skills_ready_jobs.csv")
logs = pd.read_csv("data/user_logs.csv")
technical_skills = pd.read_csv("data/technical_skills.csv")

# -------------------------------
# Get all market skills
# -------------------------------
def load_market_skills():
    """
    Load only valid technical skills from the jobs dataset.
    Any word not present in technical_skills.csv is ignored.
    """

    market_skills = set()

    # Load approved technical skills
    valid_skills = set(
        technical_skills["skill"]
        .dropna()
        .str.lower()
        .str.strip()
    )

    # Read every job's skills
    for row in jobs["skills_required"]:

        if pd.isna(row):
            continue

        text = str(row).lower()

        # Split on commas and spaces
        words = re.split(r"[,/;|()\n]+|\s+", text)

        for word in words:

            word = word.strip()

            if word in valid_skills:
                market_skills.add(word)

    return market_skills
# -------------------------------
# Extract skills learned by user
# -------------------------------

def load_student_skills(market_skills):
    """
    Find technical skills present in the student's learning logs.
    """

    student_skills = set()

    # Read every log
    for log in logs["Log"]:

        if pd.isna(log):
            continue

        text = str(log).lower()

        # Check every market skill
        for skill in market_skills:

            if skill.lower() in text:
                student_skills.add(skill)

    return student_skills


# -------------------------------
# Find Missing Skills
# -------------------------------

def calculate_skill_gap(market_skills, student_skills):

    learned = market_skills.intersection(student_skills)

    missing = market_skills.difference(student_skills)

    return learned, missing


# -------------------------------
# Skill Match %
# -------------------------------

def calculate_alignment(market_skills, student_skills):

    if len(market_skills) == 0:
        return 0

    return round(
        len(student_skills) / len(market_skills) * 100,
        2
    )


# -------------------------------
# Display Report
# -------------------------------

def generate_report():

    market_skills = load_market_skills()

    student_skills = load_student_skills(market_skills)

    learned, missing = calculate_skill_gap(
        market_skills,
        student_skills
    )

    score = calculate_alignment(
        market_skills,
        student_skills
    )

    print("\n========== SKILL MIRROR REPORT ==========\n")

    print(f"Total Market Skills : {len(market_skills)}")
    print(f"Skills Learned      : {len(learned)}")
    print(f"Missing Skills      : {len(missing)}")
    print(f"Skill Match         : {score}%")

    print("\nTop Learned Skills\n")
    
    show_next_skills(student_skills, market_skills)

    for skill in sorted(list(learned))[:20]:
        print("✔", skill)

    print("\nTop Missing Skills\n")

    for skill in sorted(list(missing))[:20]:
        print("✘", skill)


# -------------------------------
# Main
# -------------------------------
# -----------------------------------
# Show match increase after learning
# -----------------------------------

def show_next_skills(student_skills, market_skills):

    missing = list(market_skills - student_skills)

    print("\n========== NEXT SKILLS TO LEARN ==========\n")

    for skill in missing[:5]:

        new_match = ((len(student_skills) + 1) / len(market_skills)) * 100

        print(f"Learn: {skill}")
        print(f"Estimated Skill Match: {new_match:.2f}%\n")

if __name__ == "__main__":
    generate_report()
