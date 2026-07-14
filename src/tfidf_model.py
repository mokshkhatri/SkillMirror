from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

def build_tfidf_matrix(df):
    tfidf_matrix = vectorizer.fit_transform(df['token_string'])
    return vectorizer, tfidf_matrix