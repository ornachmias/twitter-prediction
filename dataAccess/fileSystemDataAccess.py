import os
import pickle


class FileSystemDataAccess(object):
    def __init__(self, root_path):
        """
        Initialization for the file system's data access
        :param root_path: Directory in which all of the actions in the class are performed
        """
        self._root_path = root_path
        self.categorized_tweets_path = os.path.join(root_path, 'categorized_tweets')
        self.queries_tweets_path = os.path.join(root_path, 'queries_tweets')
        if not os.path.exists(self.categorized_tweets_path):
            os.makedirs(self.categorized_tweets_path)

        if not os.path.exists(self.queries_tweets_path):
            os.makedirs(self.queries_tweets_path)

    def save_tweets(self, tag, tweets, path):
        """
        Save array of tagged tweets into the local file system
        :param tag: A keyword for the array of tweets that will be set as the file name
        :param tweets: Array of tweets
        :param path: The directory path to save the data into
        """
        file_path = os.path.join(path, tag + '.pickle')
        with open(file_path, 'wb') as wfp:
            pickle.dump(tweets, wfp)

    def is_tweets_exists(self, tag, path):
        """
        Check if a set of tweets was already saved or not
        :param tag: A keyword for the array of tweets that will be set as the file name
        :param path: The directory path to save the data into
        :return: True in case the path exists, False if not
        """
        file_path = os.path.join(path, tag + '.pickle')
        return os.path.exists(file_path)

    def get_tweets(self, tag, path):
        """
        Load an array of tweets from existing path
        :param tag: A keyword for the array of tweets that will be set as the file name
        :param path: The directory path to save the data into
        :return: Array of tweets loaded from file system
        """
        file_path = os.path.join(path, tag + '.pickle')
        with open(file_path, 'rb') as rfp:
            return pickle.load(rfp)


