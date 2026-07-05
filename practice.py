import pandas as pd
import sys
sys.path.append('src')

from tokenizer import tokenize_dataframe
from tfidf_model import build_tfidf_matrix
from similarity import search
from recommend_jobs import recommend, get_market_skills

df = pd.read_csv("data/cleaned_jobs.csv")

df = tokenize_dataframe(df)

vectorizer, tfidf_matrix = build_tfidf_matrix(df)

results = search("python machine learning data science", df, vectorizer, tfidf_matrix)

recommend(results)

print("\nTop Market Skills:")
print(get_market_skills(results))