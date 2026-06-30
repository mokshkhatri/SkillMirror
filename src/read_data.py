import pandas as pd

# Read datasets
jobs = pd.read_csv("data/jobs.csv")
logs = pd.read_csv("data/user_logs.csv")

# Display first 5 rows
print("Jobs Dataset Preview:")
print(jobs.head())

print("\nUser Logs Dataset Preview:")
print(logs.head())

# Display dataset dimensions
print("\nJobs Dataset Shape:")
print(jobs.shape)

print("\nUser Logs Dataset Shape:")
print(logs.shape)

# Display column names
print("\nJobs Dataset Columns:")
print(jobs.columns)

print("\nUser Logs Dataset Columns:")
print(logs.columns)

# Display dataset information
print("\nJobs Dataset Info:")
jobs.info()

print("\nUser Logs Dataset Info:")
logs.info()