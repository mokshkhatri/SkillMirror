import os
import re
import pandas as pd


# ---------------------------------
# Career Skill Requirements
# ---------------------------------

career_paths = {
    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "statistics",
        "data visualization",
        "data analysis"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "machine learning",
        "deep learning",
        "tensorflow",
        "scikit-learn",
        "statistics",
        "matplotlib"
    ],

    "Machine Learning Engineer": [
        "python",
        "tensorflow",
        "pytorch",
        "deep learning",
        "machine learning",
        "docker",
        "git",
        "scikit-learn",
        "numpy",
        "opencv"
    ],

    "AI Engineer": [
        "python",
        "tensorflow",
        "pytorch",
        "transformers",
        "hugging face",
        "nlp",
        "llm",
        "generative ai",
        "langchain",
        "rag"
    ],

    "Backend Developer": [
        "python",
        "django",
        "flask",
        "fastapi",
        "sql",
        "mysql",
        "postgresql",
        "git",
        "docker",
        "rest api"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "next.js",
        "bootstrap",
        "tailwind css",
        "git",
        "figma"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "express.js",
        "mongodb",
        "sql",
        "git",
        "docker"
    ],

    "Android Developer": [
        "java",
        "kotlin",
        "android",
        "android studio",
        "firebase",
        "git",
        "sqlite",
        "rest api",
        "xml",
        "flutter"
    ],

    "Cloud Engineer": [
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "terraform",
        "linux",
        "git",
        "jenkins",
        "cloudformation"
    ],

    "DevOps Engineer": [
        "docker",
        "kubernetes",
        "jenkins",
        "terraform",
        "ansible",
        "linux",
        "aws",
        "git",
        "github actions",
        "nginx"
    ],

    "Cybersecurity Analyst": [
        "network security",
        "ethical hacking",
        "penetration testing",
        "wireshark",
        "linux",
        "python",
        "firewall",
        "cryptography",
        "security",
        "kali linux"
    ],

    "Network Engineer": [
        "networking",
        "ccna",
        "routing",
        "switching",
        "tcp/ip",
        "dns",
        "dhcp",
        "firewall",
        "linux",
        "windows server"
    ],

    "Software Tester": [
        "manual testing",
        "selenium",
        "java",
        "python",
        "testng",
        "jira",
        "automation testing",
        "bug tracking",
        "api testing",
        "postman"
    ],

    "Data Engineer": [
        "python",
        "sql",
        "spark",
        "hadoop",
        "airflow",
        "aws",
        "etl",
        "data warehouse",
        "docker",
        "kafka"
    ],

    "Business Intelligence Analyst": [
        "power bi",
        "tableau",
        "sql",
        "excel",
        "data visualization",
        "statistics",
        "python",
        "dashboard",
        "business analysis",
        "reporting"
    ],

    "Database Administrator": [
        "mysql",
        "postgresql",
        "oracle",
        "sql",
        "database",
        "backup",
        "performance tuning",
        "linux",
        "mongodb",
        "database security"
    ],

    "Embedded Systems Engineer": [
        "c",
        "c++",
        "embedded c",
        "microcontroller",
        "arduino",
        "raspberry pi",
        "stm32",
        "electronics",
        "iot",
        "pcb"
    ],

    "IoT Developer": [
        "arduino",
        "raspberry pi",
        "embedded c",
        "mqtt",
        "iot",
        "python",
        "esp32",
        "sensors",
        "wifi",
        "cloud"
    ],

    "Blockchain Developer": [
        "solidity",
        "ethereum",
        "web3",
        "smart contracts",
        "javascript",
        "node.js",
        "git",
        "blockchain",
        "cryptography",
        "metamask"
    ],

    "UI/UX Designer": [
        "figma",
        "adobe xd",
        "photoshop",
        "illustrator",
        "wireframing",
        "prototyping",
        "user research",
        "design thinking",
        "ui design",
        "ux design"
    ]
}


# ---------------------------------
# Parse Student Skills
# ---------------------------------

def parse_skills(skills):
    """
    Accepts either:

    String:
        "Python, SQL, Power BI"

    List:
        ["Python", "SQL", "Power BI"]

    Returns:
        {"python", "sql", "power bi"}
    """

    if skills is None:
        return set()

    if isinstance(skills, str):
        raw_skills = re.split(
            r"[,;|\n/]+",
            skills
        )
    else:
        raw_skills = skills

    cleaned_skills = set()

    for skill in raw_skills:
        skill = str(skill).strip().lower()
        skill = skill.strip("[]'\" ")

        if skill and skill not in {
            "nan",
            "none",
            "not available"
        }:
            cleaned_skills.add(skill)

    return cleaned_skills


# ---------------------------------
# Load Student Skills
# ---------------------------------

def load_student_skills(user_skills=None):
    """
    Uses Streamlit input when user_skills is supplied.

    If no input is supplied, user_logs.csv is used
    for terminal testing.
    """

    if user_skills is not None:
        return parse_skills(user_skills)

    logs_path = "data/user_logs.csv"

    if not os.path.exists(logs_path):
        return set()

    logs = pd.read_csv(logs_path)

    if "Log" not in logs.columns:
        return set()

    skills = set()

    for log in logs["Log"]:
        if pd.isna(log):
            continue

        skills.update(
            parse_skills(str(log))
        )

    return skills


# ---------------------------------
# Predict Career Matches
# ---------------------------------

def predict_career(user_skills=None):
    """
    Calculates how well the student's skills match
    each predefined career path.
    """

    student_skills = load_student_skills(
        user_skills
    )

    predictions = []

    for career, required_skills in career_paths.items():

        required_skill_set = set(required_skills)

        matched_skills = sorted(
            student_skills.intersection(
                required_skill_set
            )
        )

        missing_skills = sorted(
            required_skill_set.difference(
                student_skills
            )
        )

        if len(required_skill_set) == 0:
            match_score = 0.0
        else:
            match_score = round(
                (
                    len(matched_skills)
                    / len(required_skill_set)
                ) * 100,
                2
            )

        predictions.append(
            {
                "career": career,
                "match_score": match_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "matched_count": len(
                    matched_skills
                ),
                "total_skills": len(
                    required_skill_set
                )
            }
        )

    predictions.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return predictions


# ---------------------------------
# Create Career Chart Percentages
# ---------------------------------

def calculate_chart_percentages(top_matches):
    """
    Converts the top three career match scores into
    percentages whose total is 100.

    These values are suitable for the Streamlit
    career prediction donut chart.
    """

    if not top_matches:
        return []

    total_score = sum(
        item["match_score"]
        for item in top_matches
    )

    if total_score == 0:
        equal_share = round(
            100 / len(top_matches),
            2
        )

        chart_data = []

        for item in top_matches:
            chart_data.append(
                {
                    "career": item["career"],
                    "percentage": equal_share
                }
            )

        return chart_data

    chart_data = []

    running_total = 0.0

    for index, item in enumerate(top_matches):

        if index == len(top_matches) - 1:
            percentage = round(
                100 - running_total,
                2
            )
        else:
            percentage = round(
                (
                    item["match_score"]
                    / total_score
                ) * 100,
                2
            )

            running_total += percentage

        chart_data.append(
            {
                "career": item["career"],
                "percentage": percentage
            }
        )

    return chart_data


# ---------------------------------
# Generate Career Report
# ---------------------------------

def generate_report(user_skills=None):
    """
    Returns the best career, top three matches and
    chart-ready percentage values.
    """

    predictions = predict_career(
        user_skills
    )

    if not predictions:
        return {
            "recommended_career": None,
            "top_matches": [],
            "chart_data": []
        }

    top_matches = predictions[:3]

    return {
        "recommended_career": top_matches[0],
        "top_matches": top_matches,
        "chart_data": calculate_chart_percentages(
            top_matches
        )
    }


# ---------------------------------
# Terminal Display for Testing
# ---------------------------------

def display_report(user_skills=None):

    report = generate_report(user_skills)

    best = report["recommended_career"]

    if best is None:
        print("No career prediction available.")
        return

    print("\n========== CAREER PREDICTION ==========\n")

    print(best["career"])
    print(
        f"Match Score : "
        f"{best['match_score']}%"
    )

    print("\nMatched Skills")

    if best["matched_skills"]:
        for skill in best["matched_skills"]:
            print(skill.title())
    else:
        print("None")

    print("\nMissing Skills")

    if best["missing_skills"]:
        for skill in best["missing_skills"]:
            print(skill.title())
    else:
        print("None")

    print("\nTop Career Matches")

    for career in report["top_matches"]:
        print(
            f"{career['career']} "
            f"({career['match_score']}%)"
        )


# ---------------------------------
# Main: Terminal Testing
# ---------------------------------

if __name__ == "__main__":

    display_report(
        "Python, SQL, Excel, Power BI"
    )