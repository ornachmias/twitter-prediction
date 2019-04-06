import os
import pickle


class FileSystemDataAccess(object):
    def __init__(self, root_path):
        self._root_path = root_path
        self.categorized_tweets_path = os.path.join(root_path, 'categorized_tweets')
        self.queries_tweets_path = os.path.join(root_path, 'queries_tweets')
        if not os.path.exists(self.categorized_tweets_path):
            os.makedirs(self.categorized_tweets_path)

        if not os.path.exists(self.queries_tweets_path):
            os.makedirs(self.queries_tweets_path)

    def save_tweets(self, tag, tweets, path):
        file_path = os.path.join(path, tag + '.pickle')
        with open(file_path, 'wb') as wfp:
            pickle.dump(tweets, wfp)

    def is_tweets_exists(self, tag, path):
        file_path = os.path.join(path, tag + '.pickle')
        return os.path.exists(file_path)

    def get_tweets(self, tag, path):
        file_path = os.path.join(path, tag + '.pickle')
        with open(file_path, 'rb') as rfp:
            return pickle.load(rfp)


