from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def search(query, df, vectorizer, tfidf_matrix, top_n=5):
    query_tokens = query.lower().replace(',', ' ').split()
    query_tokens = [t for t in query_tokens if t not in stop_words]
    query_tokens = [lemmatizer.lemmatize(t, pos='n') for t in query_tokens]
    query_string = ' '.join(query_tokens)

    query_vector = vectorizer.transform([query_string])
    scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    top_indices = scores.argsort()[::-1][:top_n]

    results = []
    for idx in top_indices:
        results.append({
            'job_title':      df.iloc[idx]['job_title'],
            'company_name':   df.iloc[idx]['company_name'],
            'location':       df.iloc[idx]['location'],
            'experience_raw': df.iloc[idx]['experience_raw'],
            'work_mode':      df.iloc[idx]['work_mode'],
            'company_rating': df.iloc[idx]['company_rating'],
            'score':          round(float(scores[idx]) * 100, 2),
            'job_url':        df.iloc[idx]['job_url'],
            'skills_required': df.iloc[idx]['skills_required']
        })

    return results