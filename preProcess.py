import random
import re


class PreProcess(object):
    def pre_process(self, tweets):
        """
        Run the entire sub methods of the pre process step
        Note that although it is bit ineffective, each method get array of tweets and returned
        array of tweets to make the reading of this method much simpler.
        I'll note the technical usage of each method in code, but the explanation for the step will be in the report.
        :param tweets: Array of tweets
        :return: Array of tweets
        """
        tweets = self._remove_duplicates(tweets)
        tweets = self._decapitalize_tweets(tweets)
        tweets = self._remove_numbers_and_punctuations(tweets)
        tweets = self._remove_useless_words(tweets)
        tweets = self._remove_urls(tweets)
        tweets = self._shuffle_data(tweets)
        return tweets

    def split_to_batches(self, tweets, batch_size):
        """
        Split an array of tweets to batches
        :param tweets: Array of tweets
        :param batch_size: Number of tweets in each batch
        :return: Array of sub arrays of tweets
        """
        result = []
        l = len(tweets)
        for i in range(0, l, batch_size):
            result.append(tweets[i:i+batch_size])
        return result

    def merge_tweets_text(self, tweets):
        """
        Merge several tweets' text into a single long text
        :param tweets: Array of tweets to merge
        :return: String of the merged tweets' text
        """
        result = ''
        for t in tweets:
            result += t.text

        return result

    def split_by_party(self, training_set):
        """
        Split an array of labeled tweets into a dictionary by the party
        :param training_set: Array of labeled tweets
        :return: Dictionary from party to array of tweets
        """
        result = {}
        for t in training_set:
            if t.party not in result:
                result[t.party] = []

            result[t.party].append(t)

        return result

    def split_by_language(self, tweets):
        """
        Split an array of tweets by the language set by Twitter in each tweet
        :param tweets: Array of tweets
        :return: Dictionary from language code to array of tweets
        """
        result = {}
        for t in tweets:
            if t.language not in result:
                result[t.language] = []

            result[t.language].append(t)

        return result

    def _remove_urls(self, tweets):
        """
        Using a basic regular expression, replace instances of links in text with an empty string
        :param tweets: Array of tweets
        :return: Array of tweets
        """
        for t in tweets:
            t.text = re.sub(r'https?:?\/\/.*[\r\n]*', '', t.text, flags=re.MULTILINE)

        return tweets

    def _remove_duplicates(self, tweets):
        """
        Based on the tweet ID, remove duplicate tweets
        :param tweets: Array of tweets
        :return: Array of tweets
        """
        result = []
        existing_ids = set()

        for t in tweets:
            if t.id not in existing_ids:
                result.append(t)
                existing_ids.add(t.id)

        return result

    # Although most tweets are in Hebrew, I did query the data in english as well, so just to be safe
    def _decapitalize_tweets(self, tweets):
        """
        Decapitalize all text in the tweet
        :param tweets: Array of tweets
        :return: Array of tweets
        """
        for t in tweets:
            t.text = t.text.lower()

        return tweets

    def _remove_numbers_and_punctuations(self, tweets):
        """
        Remove all instances of numbers and punctuations from the text since they are mostly irrelevant
        :param tweets: Array of tweets
        :return: Array of tweets
        """
        ignore_letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':', ',', '.', '(', ')', '"']
        for t in tweets:
            for i in ignore_letters:
                t.text = t.text.replace(i, '')

        return tweets

    def _remove_useless_words(self, tweets):
        """
        Well this one is a bit tricky and will be explained in the report, but note that it's hard coded to avoid
        playing with this parameter too much
        :param tweets: Array of tweets
        :return: Array of tweets
        """
        ignore_words = ['בנימין', 'נתניהו', 'ביבי']
        for t in tweets:
            for i in ignore_words:
                t.text = t.text.replace(i, '')

        return tweets

    def _shuffle_data(self, tweets):
        """
        Shuffle an array of tweets
        :param tweets: Array of tweets
        :return: Array of tweets
        """
        random.shuffle(tweets)
        return tweets

