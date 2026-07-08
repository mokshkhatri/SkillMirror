import pandas as pd

from skill_gap import generate_report
from career_predictor import display_results


# ==========================================
# Enter User Learning Logs
# ==========================================

def enter_logs():

    print("\n==========================================")
    print("      ENTER YOUR LEARNING LOGS")
    print("==========================================")
    print("Enter one learning activity per line.")
    print("Type END when finished.\n")

    logs = []

    while True:

        log = input("> ")

        if log.upper() == "END":
            break

        if log.strip() != "":
            logs.append(log)

    if len(logs) == 0:
        print("\n❌ No logs entered!\n")
        return False

    df = pd.DataFrame({
        "Date": ["2026-07-05"] * len(logs),
        "Log": logs
    })

    df.to_csv("data/user_logs.csv", index=False)

    print("\n✅ Learning Logs Saved Successfully!\n")

    return True


# ==========================================
# Analyze Complete Profile
# ==========================================

def analyze_profile():

    print("\n==========================================")
    print("         ANALYZING PROFILE")
    print("==========================================\n")

    print("Generating Skill Gap Report...\n")

    generate_report()

    print("\n==========================================")
    print("        CAREER PREDICTION")
    print("==========================================\n")

    display_results()

    print("\n==========================================")
    print("    INTERNSHIP RECOMMENDATION")
    print("==========================================")

    print("\nComing Soon...")
    print("This module will use similarity.py\n")


# ==========================================
# Main Application
# ==========================================

def main():

    while True:

        print("\n==========================================")
        print("            SKILL MIRROR")
        print("==========================================")
        print("1. Analyze My Profile")
        print("2. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            success = enter_logs()

            if success:
                analyze_profile()

        elif choice == "2":

            print("\nThank you for using SkillMirror!")
            break

        else:

            print("\n❌ Invalid Choice! Please try again.\n")


# ==========================================
# Start Application
# ==========================================

if __name__ == "__main__":
    main()