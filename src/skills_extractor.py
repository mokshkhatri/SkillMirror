import pandas as pd

# Read the cleaned jobs dataset
jobs = pd.read_csv("data/cleaned_jobs.csv")

# Extract the Skills column
skills = jobs["Skills"]

print("Original Skills Column:")
print(skills.head())

# Convert skills text to lowercase
skills = skills.str.lower()

# Remove unnecessary characters
skills = skills.str.replace("[", "", regex=False)
skills = skills.str.replace("]", "", regex=False)
skills = skills.str.replace("'", "", regex=False)
skills = skills.str.replace(",", "", regex=False)

print("\nCleaned Skills Column:")
print(skills.head())

# Store cleaned skills in a new column
jobs["Skills"] = skills

# Save the updated dataset
jobs.to_csv("data/skills_ready_jobs.csv", index=False)

print("\nSkills-ready dataset saved as data/skills_ready_jobs.csv")