import pandas as pd
import difflib
import re


# ----------------------------------
# Load Technical Skills Database
# ----------------------------------

technical_skills = pd.read_csv(
    "data/technical_skills.csv"
)

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
    Returns

    accepted skills
    suggested corrections
    ignored skills
    """

    if user_input is None:
        return [], {}, []

    words = re.split(
        r"[,\n;|/]+",
        str(user_input)
    )

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

        if close_match:

            suggestions[skill] = close_match[0]

        else:

            ignored.append(skill)

    return (
        sorted(accepted),
        suggestions,
        sorted(ignored)
    )


# ----------------------------------
# Auto Accept Suggestions
# ----------------------------------

def get_final_skills(user_input):
    """
    Returns the final skill list.

    Example

    Input:
    Python, Excell, SQL

    Output:
    Python
    Excel
    SQL
    """

    accepted, suggestions, ignored = validate_skills(
        user_input
    )

    final_skills = accepted.copy()

    for corrected_skill in suggestions.values():

        if corrected_skill not in final_skills:

            final_skills.append(corrected_skill)

    final_skills.sort()

    return final_skills


# ----------------------------------
# Display Results
# ----------------------------------

def display_results(
    accepted,
    suggestions,
    ignored
):

    print("\n")
    print("=" * 45)
    print("        SKILL VALIDATION")
    print("=" * 45)

    print("\nAccepted Skills")

    if accepted:

        for skill in accepted:

            print("✔", skill.title())

    else:

        print("None")

    print("\nSuggested Corrections")

    if suggestions:

        for wrong, correct in suggestions.items():

            print(
                f"{wrong.title()} → {correct.title()}"
            )

    else:

        print("None")

    print("\nIgnored Skills")

    if ignored:

        for skill in ignored:

            print("✘", skill.title())

    else:

        print("None")


# ----------------------------------
# Main
# ----------------------------------

if __name__ == "__main__":

    user_input = input(
        "Enter Skills: "
    )

    accepted, suggestions, ignored = validate_skills(
        user_input
    )

    display_results(
        accepted,
        suggestions,
        ignored
    )

    print("\nFinal Skills")

    print(
        get_final_skills(user_input)
    )