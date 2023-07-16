from nltk.corpus import stopwords
import joblib
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
nltk.data.path.append('./nltk_data')


model = joblib.load('pac_classify.pkl')
tfidfvect = joblib.load('tfidfvectorizer.pkl')


class PredictionModel:
    output = {}

    # constructor
    def __init__(self, original_text):
        self.output['original'] = original_text


    # predict
    def predict(self):
        review = self.preprocess()
        text_vect = tfidfvect.transform([review]).toarray()
        self.output['prediction'] = 'FAKE' if model.predict(text_vect) == 1 else 'REAL'
        return self.output


    # Helper methods
    def preprocess(self):
        review = re.sub('[^a-zA-Z]', ' ', self.output['original'])
        review = review.lower()
        review = review.split()
        review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
        review = ' '.join(review)
        self.output['preprocessed'] = review
        return review