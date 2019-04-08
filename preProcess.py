import random
import re


class PreProcess(object):
    def pre_process(self, tweets):
        tweets = self._remove_duplicates(tweets)
        tweets = self._decapitalize_tweets(tweets)
        tweets = self._remove_numbers_and_punctuations(tweets)
        tweets = self._remove_urls(tweets)
        tweets = self._shuffle_data(tweets)
        return tweets

    def split_to_batches(self, tweets, batch_size):
        result = []
        l = len(tweets)
        for i in range(0, l, batch_size):
            result.append(tweets[i:i+batch_size])
        return result

    def merge_tweets_text(self, tweets):
        result = ''
        for t in tweets:
            result += t.text

        return result

    def split_by_party(self, training_set):
        result = {}
        for t in training_set:
            if t.party not in result:
                result[t.party] = []

            result[t.party].append(t)

        return result

    def split_by_language(self, tweets):
        result = {}
        for t in tweets:
            if t.language not in result:
                result[t.language] = []

            result[t.language].append(t)

        return result

    def _remove_urls(self, tweets):
        for t in tweets:
            t.text = re.sub(r'https?:?\/\/.*[\r\n]*', '', t.text, flags=re.MULTILINE)

        return tweets

    def _remove_duplicates(self, tweets):
        result = []
        existing_ids = set()

        for t in tweets:
            if t.id not in existing_ids:
                result.append(t)
                existing_ids.add(t.id)

        return result

    # Although most tweets are in Hebrew, I did query the data in english as well, so just to be safe
    def _decapitalize_tweets(self, tweets):
        for t in tweets:
            t.text = t.text.lower()

        return tweets

    def _remove_numbers_and_punctuations(self, tweets):
        ignore_letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':', ',', '.', '(', ')', '"']
        for t in tweets:
            for i in ignore_letters:
                t.text = t.text.replace(i, '')

        return tweets

    def _shuffle_data(self, tweets):
        random.shuffle(tweets)
        return tweets

