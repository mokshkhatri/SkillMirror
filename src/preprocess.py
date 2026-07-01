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

# Clean extra spaces from text columns
jobs["Company"] = jobs["Company"].str.strip()
jobs["Job_Titles"] = jobs["Job_Titles"].str.strip()
jobs["Location"] = jobs["Location"].str.strip()
jobs["Skills"] = jobs["Skills"].str.strip()

print("\nDataset Shape After Cleaning:")
print(jobs.shape)

print("\nMissing Values After Cleaning:")
print(jobs.isnull().sum())

print("\nDuplicate Rows After Cleaning:")
print(jobs.duplicated().sum())

# Save cleaned dataset
jobs.to_csv("data/cleaned_jobs.csv", index=False)

print("\nCleaned dataset saved as data/cleaned_jobs.csv")