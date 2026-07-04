import pandas as pd

# Read the jobs dataset
jobs = pd.read_csv("data/jobs.csv")

print("Original Dataset Shape:")
print(jobs.shape)

print("\nMissing Values Before Cleaning:")
print(jobs.isnull().sum())

print("\nDuplicate Rows Before Cleaning:")
print(jobs.duplicated().sum())

# Remove duplicate rows
jobs = jobs.drop_duplicates()

# Remove rows where important columns are actually empty
jobs = jobs.dropna(subset=[
    "job_title",
    "company_name",
    "location",
    "skills_required",
    "job_url"
])

# Clean extra spaces from text columns
jobs["job_title"] = jobs["job_title"].astype(str).str.strip()
jobs["company_name"] = jobs["company_name"].astype(str).str.strip()
jobs["location"] = jobs["location"].astype(str).str.strip()
jobs["skills_required"] = jobs["skills_required"].astype(str).str.strip()
jobs["experience_raw"] = jobs["experience_raw"].astype(str).str.strip()
jobs["work_mode"] = jobs["work_mode"].astype(str).str.strip()

# Remove rows where skills are written as "Not Available"
jobs = jobs[jobs["skills_required"].str.lower() != "not available"]

# Remove rows where job URL is written as "Not Available"
jobs = jobs[jobs["job_url"].str.lower() != "not available"]

print("\nDataset Shape After Cleaning:")
print(jobs.shape)

print("\nMissing Values After Cleaning:")
print(jobs.isnull().sum())

print("\nDuplicate Rows After Cleaning:")
print(jobs.duplicated().sum())

# Reset row numbers
jobs = jobs.reset_index(drop=True)

# Save cleaned dataset
jobs.to_csv("data/cleaned_jobs.csv", index=False)

print("\nCleaned dataset saved as data/cleaned_jobs.csv")