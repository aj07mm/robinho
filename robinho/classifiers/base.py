import pandas as pd
import pickle
from imblearn.under_sampling import RandomUnderSampler


class BaseClassifier():
    RANDOM_SEED = 123

    def __init__(self):
        try:
            with open('output/' + self.name + '.pkl', "rb") as f:
                self.clf = pickle.load(f)
        except FileNotFoundError:
            self.train()

    def features_labels(self):
        raise NotImplementedError

    def undersample_data(self, X, y):
        columns = X.columns.values.tolist()

        X, y = RandomUnderSampler(random_state=BaseClassifier.RANDOM_SEED, ratio='all').fit_sample(
            X.values.tolist(), y.values.tolist())
        X = pd.DataFrame(X, columns=columns)

        return X, y

    def extract_title(self, X):
        return X['title']

    def extract_content(self, X):
        return X['content']

    def join_text_and_content(self, X):
        return X['title'] + ' ' + X['content']

    def classifier(self):
        raise NotImplementedError

    def load_links(self):
        try:
            df = pd.read_csv("links.csv")
        except FileNotFoundError:
            print("Downloading links data...")
            df = pd.read_json(
                "https://api.fakenewsdetector.org/links/all")
            df.to_csv("links.csv")

        df.dropna(subset=["title", "content"], inplace=True, how="all")
        df = df.fillna('')

        return df

    def train(self):
        X, y = self.features_labels()

        clf = self.classifier()
        clf = clf.fit(X, y)

        self.save_model(clf)

    def save_model(self, clf):
        with open('output/' + self.name + '.pkl', "wb") as f:
            pickle.dump(clf, f)

        self.clf = clf

    def predict(self, title, content):
        df = pd.DataFrame()
        df['title'] = [title]
        df['content'] = [content]
        return self.clf.predict_proba(df)[0][1]
