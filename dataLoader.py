from configurations import Configurations
from dataAccess.fileSystemDataAccess import FileSystemDataAccess
from dataAccess.twitterDataAccess import TwitterDataAccess
from model.parties import categorized_twitter_accounts


class DataLoader(object):
    def __init__(self):
        self._twitterDataAccess = TwitterDataAccess(Configurations.api_key, Configurations.api_secret_key,
                                                    Configurations.access_token, Configurations.access_token_secret)
        self._fileSystemDataAccess = FileSystemDataAccess(Configurations.data_root)

    def get_categorized_tweets(self):
        tweets = []
        for p in categorized_twitter_accounts:
            current_tweets = []
            if not self._fileSystemDataAccess.is_tweets_exists(p, self._fileSystemDataAccess.categorized_tweets_path):
                current_tweets = self._twitterDataAccess.get_user_tweets(p, Configurations.historical_days_extraction, categorized_twitter_accounts[p])
                self._fileSystemDataAccess.save_tweets(p, current_tweets, self._fileSystemDataAccess.categorized_tweets_path)
            else:
                current_tweets = self._fileSystemDataAccess.get_tweets(p, self._fileSystemDataAccess.categorized_tweets_path)

            tweets.extend(current_tweets)

        return tweets

    def get_uncategorized_tweets(self):
        country_id = None
        if Configurations.search_country != '':
            country_id = self._twitterDataAccess.get_country_id(Configurations.search_country)
        tweets = []
        for q in Configurations.search_keywords:
            current_tweets = []
            if not self._fileSystemDataAccess.is_tweets_exists(q, self._fileSystemDataAccess.queries_tweets_path):
                current_tweets = self._twitterDataAccess.get_search_tweets(country_id,
                                                                           Configurations.historical_days_extraction, q)
                self._fileSystemDataAccess.save_tweets(q, current_tweets, self._fileSystemDataAccess.queries_tweets_path)
            else:
                current_tweets = self._fileSystemDataAccess.get_tweets(q, self._fileSystemDataAccess.queries_tweets_path)

            tweets.extend(current_tweets)

        return tweets




