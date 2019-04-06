from datetime import timedelta, datetime

import tweepy
from tweepy import Cursor

from model.parties import Parties
from model.tweet import Tweet


class TwitterDataAccess(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(auth, wait_on_rate_limit=True)

    def print_user_data(self, target):
        print("Getting data for {}".format(target))
        item = self._api.get_user(target)
        print("Name: {}".format(item.name))
        print("Screen Name: {}".format(item.screen_name))
        print("Description: {}".format(item.description))
        print("Statuses Count: {}".format(str(item.statuses_count)))
        print("Friends Count: {}".format(str(item.friends_count)))
        print("Followers Count: {}".format(str(item.followers_count)))

    def get_user_tweets(self, target, days, party):
        tweets = []
        end_date = datetime.utcnow() - timedelta(days=days)
        for status in Cursor(self._api.user_timeline, id=target, count=1000).items():
            tweet = Tweet()
            tweet.load_from_status(status, party)
            tweets.append(tweet)

            if status.created_at < end_date:
                break

        return tweets

    def get_country_id(self, country_query):
        places = self._api.geo_search(query=country_query, granularity="country")
        return places[0].id

    def get_search_tweets(self, country_code, days, target):
        tweets = []
        end_date = datetime.utcnow() - timedelta(days=days)
        query = target
        if country_code is not None:
            query = 'place:{} AND {}'.format(country_code, target)
        for status in Cursor(self._api.search, q=query, count=1000).items():
            if status.created_at > end_date:
                tweet = Tweet()
                tweet.load_from_status(status, Parties.Unknown)
                tweets.append(tweet)

        return tweets


