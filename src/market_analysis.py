from collections import Counter


# ---------------------------------
# Count Market Skill Frequency
# ---------------------------------

def get_market_skill_frequency(recommended_jobs):
    """
    Counts how frequently each skill appears
    across the recommended jobs.

    Parameters
    ----------
    recommended_jobs : list
        List of job dictionaries returned by the
        recommendation engine.

    Returns
    -------
    Counter
        Example:

        {
            "python": 14,
            "sql": 12,
            "docker": 9
        }
    """

    skill_counter = Counter()

    for job in recommended_jobs:

        skills = job.get(
            "required_skills",
            []
        )

        for skill in skills:

            skill = str(skill).strip().lower()

            if skill:
                skill_counter[skill] += 1

    return skill_counter


# ---------------------------------
# Find Common Missing Skills
# ---------------------------------

def get_common_missing_skills(
    skill_frequency,
    user_skills,
    limit=5
):
    """
    Returns the most frequently required market skills
    that the user does not already possess.

    Parameters
    ----------
    skill_frequency : Counter
        Skill counts returned by
        get_market_skill_frequency().

    user_skills : list, set or tuple
        Validated user skills.

    limit : int
        Maximum number of missing skills to return.

    Returns
    -------
    list

    Example:

    Market:
        Python -> 14
        SQL -> 13
        Docker -> 9
        Git -> 8

    User:
        Python
        SQL

    Output:
        ["docker", "git"]
    """

    if limit <= 0:
        return []

    cleaned_user_skills = {
        str(skill).strip().lower()
        for skill in user_skills
        if str(skill).strip()
    }

    missing_skills = []

    for skill, count in skill_frequency.most_common():

        if skill not in cleaned_user_skills:
            missing_skills.append(skill)

        if len(missing_skills) == limit:
            break

    return missing_skills


# ---------------------------------
# Calculate Market Readiness
# ---------------------------------

def calculate_market_readiness(
    skill_frequency,
    user_skills
):
    """
    Calculates how ready the user is for the relevant
    market represented by the recommended jobs.

    Frequently required skills contribute more to the
    readiness score than rarely required skills.

    Formula:

        total frequency of user-owned market skills
        ------------------------------------------- x 100
        total frequency of all market skills

    Returns
    -------
    float
        Market readiness percentage between 0 and 100.
    """

    if not skill_frequency:
        return 0.0

    cleaned_user_skills = {
        str(skill).strip().lower()
        for skill in user_skills
        if str(skill).strip()
    }

    total_market_demand = sum(
        skill_frequency.values()
    )

    if total_market_demand == 0:
        return 0.0

    matched_market_demand = sum(
        count
        for skill, count in skill_frequency.items()
        if skill in cleaned_user_skills
    )

    market_readiness = (
        matched_market_demand
        / total_market_demand
    ) * 100

    return round(
        market_readiness,
        2
    )