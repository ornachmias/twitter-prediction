from datetime import timedelta, datetime

import tweepy
from tweepy import Cursor

from model.parties import Parties
from model.tweet import Tweet


class TwitterDataAccess(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Initialization of the wrapper class for Tweepy library
        :param consumer_key: Tweepy's consumer key
        :param consumer_secret: Tweepy's consumer secret
        :param access_token: Tweepy's access token
        :param access_token_secret: Tweepy's token secret
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # We set wait_on_rate_limit as true to avoid exceptions when we reached limit and just wait instead
        self._api = tweepy.API(auth, wait_on_rate_limit=True)

    def print_user_data(self, target):
        """
        Print user's data received from Tweepy.
        This method isn't really used except for testing purposes.
        :param target: Person's or page name
        """
        print("Getting data for {}".format(target))
        item = self._api.get_user(target)
        print("Name: {}".format(item.name))
        print("Screen Name: {}".format(item.screen_name))
        print("Description: {}".format(item.description))
        print("Statuses Count: {}".format(str(item.statuses_count)))
        print("Friends Count: {}".format(str(item.friends_count)))
        print("Followers Count: {}".format(str(item.followers_count)))

    def get_user_tweets(self, target, days, party):
        """
        Get a specific user's tweets from the last X number of days, and associate the tweets with specific paryy
        :param target: Target name
        :param days: Number of days to query back
        :param party: The party associated with the person queried
        :return: Array of tweets for the specific person
        """
        tweets = []
        end_date = datetime.utcnow() - timedelta(days=days)
        for status in Cursor(self._api.user_timeline, id=target, count=1000, tweet_mode='extended').items():
            tweet = Tweet()
            tweet.load_from_status(status, party)
            tweets.append(tweet)

            if status.created_at < end_date:
                break

        return tweets

    def get_country_id(self, country_query):
        """
        Get the country id to be used as part of queries
        :param country_query: Name of the country we want to get Id for
        :return: Twitter internal ID for the specific country
        """
        places = self._api.geo_search(query=country_query, granularity="country")
        return places[0].id

    def get_search_tweets(self, country_code, days, target):
        """
        Free text tweets search
        :param country_code: (Optional) Twitter's internal ID for the country, set None if we don't want this filter
        :param days: Number of days to query back from Twitter
        :param target: The search query we want to invoke against Twitter
        :return: Array of tweets with party set to Unknown
        """
        tweets = []
        end_date = datetime.utcnow() - timedelta(days=days)
        query = target
        if country_code is not None:
            query = 'place:{} AND {}'.format(country_code, target)
        for status in Cursor(self._api.search, q=query, count=1000, tweet_mode='extended').items():
            if status.created_at > end_date:
                tweet = Tweet()
                tweet.load_from_status(status, Parties.Unknown)
                tweets.append(tweet)

        return tweets


