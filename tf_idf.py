from sklearn.feature_extraction.text import TfidfVectorizer


def do_tfidf(token):
    tfidf = TfidfVectorizer(max_df=0.05, min_df=0.002) 
    words = tfidf.fit_transform(token)
    sentence = " ".join(tfidf.get_feature_names())
    return sentence

"""
def do_tfidf(token):
    tfidf = TfidfVectorizer(max_df=0.7, min_df= 0.01,use_idf=True,ngram_range=(1,2)) 
    words = tfidf.fit_transform(token)
    sentence = " ".join(tfidf.get_feature_names())
    return sentence
"""