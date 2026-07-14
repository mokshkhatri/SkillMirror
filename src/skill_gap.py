import os
import re

import pandas as pd


# ---------------------------------
# Technical Skills File
# ---------------------------------

TECHNICAL_SKILLS_PATH = "data/technical_skills.csv"


# ---------------------------------
# Normalize Text
# ---------------------------------

def normalize_text(text):
    """
    Converts text to lowercase and cleans unnecessary
    spacing while preserving useful characters such as:

    c++
    c#
    node.js
    tcp/ip
    """

    if text is None:
        return ""

    text = str(text).lower().strip()

    # Replace common separators and brackets with spaces.
    # Forward slash is preserved for skills such as tcp/ip.
    text = re.sub(r"[,;|()\[\]{}\n\r\t]+", " ", text)

    # Replace repeated spaces with one space.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------
# Load Valid Technical Skills
# ---------------------------------

def load_valid_skills():
    """
    Loads the master list of valid technical skills from
    data/technical_skills.csv.

    The CSV must contain a column named 'skill'.
    """

    if not os.path.exists(TECHNICAL_SKILLS_PATH):
        raise FileNotFoundError(
            f"Technical skills file not found: "
            f"{TECHNICAL_SKILLS_PATH}"
        )

    technical_skills = pd.read_csv(
        TECHNICAL_SKILLS_PATH
    )

    if "skill" not in technical_skills.columns:
        raise ValueError(
            "technical_skills.csv must contain "
            "a column named 'skill'."
        )

    valid_skills = set()

    for skill in technical_skills["skill"].dropna():

        cleaned_skill = normalize_text(skill)

        if cleaned_skill:
            valid_skills.add(cleaned_skill)

    return valid_skills


VALID_SKILLS = load_valid_skills()


# Check longer and multiword skills first.
# Example:
# "machine learning" should be detected before
# shorter overlapping terms.
SORTED_VALID_SKILLS = sorted(
    VALID_SKILLS,
    key=lambda skill: (
        len(skill.split()),
        len(skill)
    ),
    reverse=True
)


# ---------------------------------
# Check Span Overlap
# ---------------------------------

def spans_overlap(
    start,
    end,
    occupied_spans
):
    """
    Checks whether a newly detected skill overlaps with
    another skill already selected from the same text.
    """

    for occupied_start, occupied_end in occupied_spans:

        if (
            start < occupied_end
            and end > occupied_start
        ):
            return True

    return False


# ---------------------------------
# Extract Skills from Free Text
# ---------------------------------

def extract_skills_from_text(text):
    """
    Finds complete technical skills inside raw,
    space-separated job text.

    Example input:

        python sql machine learning
        data visualization power bi

    Example output:

        [
            "python",
            "sql",
            "machine learning",
            "data visualization",
            "power bi"
        ]
    """

    cleaned_text = normalize_text(text)

    if not cleaned_text:
        return []

    detected_matches = []
    occupied_spans = []

    for skill in SORTED_VALID_SKILLS:

        escaped_skill = re.escape(skill)

        # Prevent small skills such as "r" or "c" from
        # matching inside larger ordinary words.
        pattern = (
            rf"(?<![a-z0-9])"
            rf"{escaped_skill}"
            rf"(?![a-z0-9])"
        )

        for match in re.finditer(
            pattern,
            cleaned_text
        ):
            start, end = match.span()

            if spans_overlap(
                start,
                end,
                occupied_spans
            ):
                continue

            detected_matches.append(
                {
                    "skill": skill,
                    "start": start,
                    "end": end
                }
            )

            occupied_spans.append(
                (start, end)
            )

    # Restore the original order in which skills
    # appeared inside the job text.
    detected_matches.sort(
        key=lambda item: item["start"]
    )

    detected_skills = []

    for item in detected_matches:

        skill = item["skill"]

        if skill not in detected_skills:
            detected_skills.append(skill)

    return detected_skills


# ---------------------------------
# Parse User or Job Skills
# ---------------------------------

def parse_skills(skills):
    """
    Accepts strings, lists, sets, or tuples.

    It supports:

    Comma-separated input:
        "Python, SQL, Power BI"

    Space-separated job text:
        "python sql machine learning power bi"

    List input:
        ["Python", "SQL", "Power BI"]
    """

    if skills is None:
        return []

    if isinstance(
        skills,
        (list, set, tuple)
    ):
        detected_skills = []

        for item in skills:

            item_text = normalize_text(item)

            if not item_text:
                continue

            # Use an exact valid skill when possible.
            if item_text in VALID_SKILLS:

                if item_text not in detected_skills:
                    detected_skills.append(item_text)

            else:
                # Also supports list items containing
                # multiple space-separated skills.
                extracted = extract_skills_from_text(
                    item_text
                )

                for skill in extracted:

                    if skill not in detected_skills:
                        detected_skills.append(skill)

        return detected_skills

    text = str(skills).strip()

    if not text:
        return []

    # Phrase matching works for both comma-separated
    # and space-separated text after normalization.
    return extract_skills_from_text(text)


# ---------------------------------
# Find Ignored User Input
# ---------------------------------

def find_ignored_user_skills(
    user_skills,
    cleaned_user_skills
):
    """
    Finds user-entered comma-separated values that were
    not recognised as valid technical skills.

    Example:

        Input:
            "Python, SQL, Football"

        Ignored:
            ["football"]
    """

    if user_skills is None:
        return []

    if isinstance(
        user_skills,
        (list, set, tuple)
    ):
        raw_parts = list(user_skills)

    else:
        raw_parts = re.split(
            r"[,;|\n]+",
            str(user_skills)
        )

    ignored = []

    for part in raw_parts:

        cleaned_part = normalize_text(part)

        if not cleaned_part:
            continue

        extracted = extract_skills_from_text(
            cleaned_part
        )

        if not extracted:
            ignored.append(cleaned_part)

    return sorted(set(ignored))


# ---------------------------------
# Compare Student with One Job
# ---------------------------------

def calculate_skill_gap(
    user_skills,
    required_skills
):
    """
    Compares the student with one recommended job.

    Returns:
        learned_skills
        missing_skills
    """

    student_skill_set = set(
        parse_skills(user_skills)
    )

    required_skill_set = set(
        parse_skills(required_skills)
    )

    learned_skills = sorted(
        required_skill_set.intersection(
            student_skill_set
        )
    )

    missing_skills = sorted(
        required_skill_set.difference(
            student_skill_set
        )
    )

    return learned_skills, missing_skills


# ---------------------------------
# Calculate Job-Specific Match
# ---------------------------------

def calculate_alignment(
    learned_skills,
    required_skills
):
    """
    Calculates:

    learned required skills
    ----------------------- x 100
    total required skills
    """

    job_skills = parse_skills(
        required_skills
    )

    if len(job_skills) == 0:
        return 0.0

    match_score = (
        len(learned_skills)
        / len(job_skills)
    ) * 100

    return round(match_score, 2)


# ---------------------------------
# Suggested Next Skills
# ---------------------------------

def get_next_skills(
    missing_skills,
    limit=3
):
    """
    Returns the first few missing skills that the
    student should learn next.
    """

    if limit <= 0:
        return []

    return list(missing_skills)[:limit]


# ---------------------------------
# Estimated Improvement
# ---------------------------------

def calculate_estimated_match(
    learned_skills,
    required_skills,
    skill_number=1
):
    """
    Estimates the match percentage after learning
    additional missing skills.
    """

    job_skills = parse_skills(
        required_skills
    )

    if len(job_skills) == 0:
        return 0.0

    improved_skill_count = min(
        len(learned_skills) + skill_number,
        len(job_skills)
    )

    estimated_match = (
        improved_skill_count
        / len(job_skills)
    ) * 100

    return round(estimated_match, 2)


# ---------------------------------
# Analyze One Recommended Job
# ---------------------------------

def analyze_job_skill_gap(
    user_skills,
    required_skills,
    next_skill_limit=3
):
    """
    Generates the complete skill-gap report for one
    recommended job.

    This is the main function Streamlit should use.
    """

    cleaned_user_skills = parse_skills(
        user_skills
    )

    cleaned_required_skills = parse_skills(
        required_skills
    )

    learned_skills, missing_skills = calculate_skill_gap(
        cleaned_user_skills,
        cleaned_required_skills
    )

    skill_match = calculate_alignment(
        learned_skills,
        cleaned_required_skills
    )

    next_skills = get_next_skills(
        missing_skills,
        next_skill_limit
    )

    next_skill_details = []

    for index, skill in enumerate(
        next_skills,
        start=1
    ):
        estimated_match = calculate_estimated_match(
            learned_skills,
            cleaned_required_skills,
            skill_number=index
        )

        next_skill_details.append(
            {
                "skill": skill,
                "estimated_match": estimated_match
            }
        )

    ignored_user_skills = find_ignored_user_skills(
        user_skills,
        cleaned_user_skills
    )

    report = {
        "required_skills": cleaned_required_skills,
        "learned_skills": learned_skills,
        "missing_skills": missing_skills,
        "next_skills": next_skills,
        "next_skill_details": next_skill_details,
        "skill_match": skill_match,

        "total_required_skills": len(
            cleaned_required_skills
        ),

        "total_learned_skills": len(
            learned_skills
        ),

        "total_missing_skills": len(
            missing_skills
        ),

        "ignored_user_skills": ignored_user_skills
    }

    return report


# ---------------------------------
# Add Skill Gap to Recommended Jobs
# ---------------------------------

def analyze_recommended_jobs(
    user_skills,
    recommended_jobs,
    next_skill_limit=3
):
    """
    Adds job-specific skill-gap information to every
    job returned by Mahi's recommendation engine.
    """

    analyzed_jobs = []

    for job in recommended_jobs:

        job_copy = job.copy()

        required_skills = job_copy.get(
            "skills_required",
            ""
        )

        gap_report = analyze_job_skill_gap(
            user_skills=user_skills,
            required_skills=required_skills,
            next_skill_limit=next_skill_limit
        )

        job_copy.update(
            gap_report
        )

        analyzed_jobs.append(
            job_copy
        )

    return analyzed_jobs


# ---------------------------------
# Terminal Display for Testing
# ---------------------------------

def display_report(report):
    """
    Displays one job-specific skill-gap report
    in the terminal for testing.
    """

    print("\n" + "=" * 50)
    print("          JOB-SPECIFIC SKILL GAP")
    print("=" * 50)

    print(
        f"\nTotal Required Skills : "
        f"{report['total_required_skills']}"
    )

    print(
        f"Skills Learned        : "
        f"{report['total_learned_skills']}"
    )

    print(
        f"Missing Skills        : "
        f"{report['total_missing_skills']}"
    )

    print(
        f"Skill Match           : "
        f"{report['skill_match']}%"
    )

    print("\nRequired Skills")
    print("-" * 30)

    if report["required_skills"]:

        for skill in report["required_skills"]:
            print(skill.title())

    else:
        print("None")

    print("\nLearned Skills")
    print("-" * 30)

    if report["learned_skills"]:

        for skill in report["learned_skills"]:
            print(skill.title())

    else:
        print("None")

    print("\nMissing Skills")
    print("-" * 30)

    if report["missing_skills"]:

        for skill in report["missing_skills"]:
            print(skill.title())

    else:
        print("None")

    print("\nSuggested Next Skills")
    print("-" * 30)

    if report["next_skill_details"]:

        for item in report["next_skill_details"]:

            print(
                f"{item['skill'].title()} "
                f"-> Estimated match: "
                f"{item['estimated_match']}%"
            )

    else:
        print("No missing skills.")

    if report["ignored_user_skills"]:

        print("\nIgnored User Skills")
        print("-" * 30)

        for skill in report["ignored_user_skills"]:
            print(skill.title())


# ---------------------------------
# Main: Terminal Testing
# ---------------------------------

if __name__ == "__main__":

    sample_user_skills = (
        "Python, SQL, Excel, Football"
    )

    # This deliberately matches the actual format
    # of skills_ready_jobs.csv: no commas required.
    sample_required_skills = (
        "python sql excel power bi "
        "machine learning data visualization tableau"
    )

    skill_gap_report = analyze_job_skill_gap(
        user_skills=sample_user_skills,
        required_skills=sample_required_skills
    )

    display_report(
        skill_gap_report
    )