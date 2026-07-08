# ---------------------------------
# Generate Learning Roadmap
# ---------------------------------

def generate_roadmap(missing_skills):

    roadmap = []

    weeks = [
        "Week 1",
        "Week 2",
        "Week 3",
        "Week 4",
        "Week 5",
        "Week 6",
        "Week 7",
        "Week 8"
    ]

    for i, skill in enumerate(missing_skills):

        if i >= len(weeks):
            break

        roadmap.append({

            "week": weeks[i],

            "skill": skill.title()

        })

    return roadmap


# ---------------------------------
# Display Roadmap (Testing)
# ---------------------------------

def display_roadmap(roadmap):

    print("\n========== LEARNING ROADMAP ==========\n")

    for item in roadmap:

        print(item["week"])
        print("-" * len(item["week"]))
        print(item["skill"])
        print()


# ---------------------------------
# Main (Testing)
# ---------------------------------

if __name__ == "__main__":

    sample_missing = [

        "power bi",

        "tableau",

        "docker",

        "machine learning",

        "tensorflow",

        "aws"

    ]

    roadmap = generate_roadmap(sample_missing)

    display_roadmap(roadmap)