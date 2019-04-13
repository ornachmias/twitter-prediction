from configurations import Configurations
from dataAccess.fileSystemDataAccess import FileSystemDataAccess
from dataAccess.twitterDataAccess import TwitterDataAccess
from model.parties import categorized_twitter_accounts


class DataLoader(object):
    def __init__(self):
        # Initialize the TwitterDataAccess and FileSystemDataAccess classes
        self._twitterDataAccess = TwitterDataAccess(Configurations.api_key, Configurations.api_secret_key,
                                                    Configurations.access_token, Configurations.access_token_secret)
        self._fileSystemDataAccess = FileSystemDataAccess(Configurations.data_root)

    def get_categorized_tweets(self):
        """
        Generate an array of tweets with a known party to be used as training set
        :return: A tweets array
        """
        tweets = []

        # Note that out way of getting the labeled tweets is getting tweets from the 4 most
        # important people in each party
        for p in categorized_twitter_accounts:
            # If the tweets are already saved in the file system, simply load them instead of accessing Twitter
            current_tweets = []
            if not self._fileSystemDataAccess.is_tweets_exists(p, self._fileSystemDataAccess.categorized_tweets_path):
                current_tweets = self._twitterDataAccess.get_user_tweets(p, Configurations.historical_days_extraction, categorized_twitter_accounts[p])
                self._fileSystemDataAccess.save_tweets(p, current_tweets, self._fileSystemDataAccess.categorized_tweets_path)
            else:
                current_tweets = self._fileSystemDataAccess.get_tweets(p, self._fileSystemDataAccess.categorized_tweets_path)

            tweets.extend(current_tweets)

        return tweets

    def get_uncategorized_tweets(self):
        """
        Generate an array of tweets with a unknown party to be used as test set
        :return:
        """

        # If configured, limit the search queries to a specific country
        country_id = None
        if Configurations.search_country != '':
            country_id = self._twitterDataAccess.get_country_id(Configurations.search_country)
        tweets = []

        # We limit the test data to a specific search queries in twitter
        for q in Configurations.search_keywords:
            # If the tweets are already saved in the file system, simply load them instead of accessing Twitter
            current_tweets = []
            if not self._fileSystemDataAccess.is_tweets_exists(q, self._fileSystemDataAccess.queries_tweets_path):
                current_tweets = self._twitterDataAccess.get_search_tweets(country_id,
                                                                           Configurations.historical_days_extraction, q)
                self._fileSystemDataAccess.save_tweets(q, current_tweets, self._fileSystemDataAccess.queries_tweets_path)
            else:
                current_tweets = self._fileSystemDataAccess.get_tweets(q, self._fileSystemDataAccess.queries_tweets_path)

            tweets.extend(current_tweets)

        return tweets




