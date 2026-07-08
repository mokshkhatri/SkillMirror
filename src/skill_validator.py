import pandas as pd
import difflib
import re

# ----------------------------------
# Load Technical Skills Database
# ----------------------------------

technical_skills = pd.read_csv("data/technical_skills.csv")

VALID_SKILLS = set(
    technical_skills["skill"]
    .dropna()
    .str.lower()
    .str.strip()
)


# ----------------------------------
# Validate User Skills
# ----------------------------------

def validate_skills(user_input):
    """
    Takes user input as a string and returns:
    1. Accepted skills
    2. Suggested corrections
    3. Ignored skills
    """

    # Split by commas or new lines
    words = re.split(r"[,\n]+", user_input)

    accepted = []
    suggestions = {}
    ignored = []

    for word in words:

        skill = word.strip().lower()

        if skill == "":
            continue

        # Exact Match
        if skill in VALID_SKILLS:
            accepted.append(skill)
            continue

        # Closest Match
        close_match = difflib.get_close_matches(
            skill,
            VALID_SKILLS,
            n=1,
            cutoff=0.75
        )

        if len(close_match) > 0:
            suggestions[skill] = close_match[0]
        else:
            ignored.append(skill)

    return accepted, suggestions, ignored


# ----------------------------------
# Display Results
# ----------------------------------

def display_results(accepted, suggestions, ignored):

    print("\n==============================")
    print("      SKILL VALIDATION")
    print("==============================\n")

    print("Accepted Skills")
    print("----------------")

    if accepted:
        for skill in accepted:
            print("✔", skill.title())
    else:
        print("None")

    print("\nSuggested Corrections")
    print("----------------------")

    if suggestions:
        for wrong, correct in suggestions.items():
            print(f"{wrong.title()}  -->  {correct.title()}")
    else:
        print("None")

    print("\nIgnored Skills")
    print("----------------")

    if ignored:
        for skill in ignored:
            print("✘", skill.title())
    else:
        print("None")


# ----------------------------------
# Main
# ----------------------------------

if __name__ == "__main__":

    print("\n========== Skill Validator ==========\n")

    print("Enter your skills.")
    print("Separate them using commas.")
    print("\nExample:")
    print("Python, SQL, Excell, Tensor Flow, Football\n")

    user_input = input("Enter Skills: ")

    accepted, suggestions, ignored = validate_skills(user_input)

    display_results(
        accepted,
        suggestions,
        ignored
    )