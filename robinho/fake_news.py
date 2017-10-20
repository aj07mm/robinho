from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import robinho.common as common


def features_labels():
    df = common.load_links()

    df["is_fake_news"] = [
        category_id == 2 for category_id in df["category_id"]
    ]

    X = df["title"]
    y = df["is_fake_news"]

    return X, y


def classifier():
    return Pipeline([
        ('vect', CountVectorizer(ngram_range=(1, 2))),
        ('tfidf', TfidfTransformer()),
        ('sampling', RandomUnderSampler()),
        ('clf', MultinomialNB()),
    ])


def train():
    X, y = features_labels()

    clf = classifier()
    clf = clf.fit(X, y)

    common.save(clf, 'fake_news')


def predict(title):
    return common.predict('fake_news', title)