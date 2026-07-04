import pandas as pd

# Read the cleaned jobs dataset
jobs = pd.read_csv("data/cleaned_jobs.csv")

# Extract the skills_required column
skills = jobs["skills_required"]

print("Original Skills Column:")
print(skills.head())

# Convert skills text to lowercase
skills = skills.str.lower()

# Remove unnecessary characters
skills = skills.str.replace("[", "", regex=False)
skills = skills.str.replace("]", "", regex=False)
skills = skills.str.replace("'", "", regex=False)
skills = skills.str.replace('"', "", regex=False)
skills = skills.str.replace(",", " ", regex=False)
skills = skills.str.replace("|", " ", regex=False)
skills = skills.str.replace(";", " ", regex=False)

# Remove extra spaces
skills = skills.str.split().str.join(" ")

print("\nCleaned Skills Column:")
print(skills.head())

# Store cleaned skills back in the same column
jobs["skills_required"] = skills

# Save the updated dataset
jobs.to_csv("data/skills_ready_jobs.csv", index=False)

print("\nSkills-ready dataset saved as data/skills_ready_jobs.csv")