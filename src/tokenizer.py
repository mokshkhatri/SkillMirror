from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def tokenize(text):
    text = text.replace(',', ' ')
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    tokens = [lemmatizer.lemmatize(t, pos='n') for t in tokens]
    return tokens

def tokenize_dataframe(df):
    df['cleaned_skills'] = df['skills_required'].apply(lambda x: str(x).lower())
    df['tokens'] = df['cleaned_skills'].apply(tokenize)
    df['token_string'] = df['tokens'].apply(lambda x: ' '.join(x))
    return df