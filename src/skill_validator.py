import pandas as pd
import difflib
import re

technical_skills = pd.read_csv("data/technical_skills.csv")

VALID_SKILLS = set(
    technical_skills["skill"]
    .dropna()
    .str.lower()
    .str.strip()
)

NON_TECH_WORDS = {
    "chess", "cricket", "football", "basketball", "tennis",
    "hockey", "volleyball", "badminton", "swimming", "running",
    "gaming", "cooking", "dancing", "singing", "reading",
    "cycling", "hiking", "fishing", "painting", "drawing"
}

MULTI_WORD_SKILLS = {
    "machine learning", "artificial intelligence", "deep learning",
    "natural language processing", "computer vision", "data science",
    "data analysis", "data visualization", "web development",
    "software development", "software engineering", "spring boot",
    "power bi", "ms excel", "ms office", "react native",
    "node js", "next js", "generative ai", "cloud computing",
    "cyber security", "network security", "operating systems",
    "data structures", "object oriented programming",
    "version control", "restful api", "rest api"
}


def validate_skills(user_input):

    if user_input is None:
        return [], {}, []

    accepted = []
    suggestions = {}
    ignored = []

    remaining = str(user_input).lower()

    for phrase in sorted(MULTI_WORD_SKILLS, key=len, reverse=True):
        if phrase in remaining:
            if phrase in VALID_SKILLS:
                accepted.append(phrase)
            else:
                accepted.append(phrase)
            remaining = remaining.replace(phrase, ",")

    words = re.split(r"[,\n;|/]+", remaining)

    for word in words:

        skill = word.strip().lower()

        if skill == "" or skill in accepted:
            continue

        if skill in NON_TECH_WORDS:
            ignored.append(skill)
            continue

        if skill in VALID_SKILLS:
            accepted.append(skill)
            continue

        close_match = difflib.get_close_matches(
            skill,
            VALID_SKILLS,
            n=1,
            cutoff=0.85
        )

        if close_match:
            suggestions[skill] = close_match[0]
        else:
            if len(skill) > 2:
                ignored.append(skill)

    return (
        sorted(set(accepted)),
        suggestions,
        sorted(ignored)
    )


def get_final_skills(user_input):

    accepted, suggestions, ignored = validate_skills(user_input)

    final_skills = accepted.copy()

    for corrected_skill in suggestions.values():
        if corrected_skill not in final_skills:
            final_skills.append(corrected_skill)

    final_skills.sort()

    return final_skills


def display_results(accepted, suggestions, ignored):

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
            print(f"{wrong.title()} → {correct.title()}")
    else:
        print("None")

    print("\nIgnored Skills")
    if ignored:
        for skill in ignored:
            print("✘", skill.title())
    else:
        print("None")


if __name__ == "__main__":

    user_input = input("Enter Skills: ")
    accepted, suggestions, ignored = validate_skills(user_input)
    display_results(accepted, suggestions, ignored)
    print("\nFinal Skills")
    print(get_final_skills(user_input))