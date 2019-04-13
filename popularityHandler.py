from model.parties import categorized_twitter_accounts


class PopularityHandler(object):
    def get_popularity_score(self, tweets):
        """
        Count the number of retweets on each party's tweet, and set a score to each party.
        This score will be used as the popularity score.
        :param tweets: Array of labeled tweets
        :return: Dictionary of party to probability score
        """
        party_retweets_count = {}
        party_tweets_count = {}
        parties = set()

        for t in tweets:
            if t.party not in party_tweets_count:
                party_tweets_count[t.party] = 0
            if t.party not in party_retweets_count:
                party_retweets_count[t.party] = 0

            parties.add(t.party)
            party_tweets_count[t.party] += 1
            party_retweets_count[t.party] += t.retweet_count

        absolute_popularity = {}
        absolute_popularity_sum = 0
        for p in parties:
            c = party_retweets_count[p] / party_tweets_count[p]
            absolute_popularity[p] = c
            absolute_popularity_sum += c

        relative_popularity = {}
        for p in parties:
            relative_popularity[p] = absolute_popularity[p] / absolute_popularity_sum

        return relative_popularity

    def count_hashtags(self, tweets):
        """
        Count the number of user's tweets hashtags to a specific politician,
        and set a score for this count for each party.
        :param tweets: Labeled or unlabeled tweets
        :return: Dictionary of party to hashtags count score
        """
        results = {}
        for t in tweets:
            if t.user_mentions is not None and len(t.user_mentions) > 0:
                for u in t.user_mentions:
                    if u in categorized_twitter_accounts:
                        if categorized_twitter_accounts[u] not in results:
                            results[categorized_twitter_accounts[u]] = 0
                        results[categorized_twitter_accounts[u]] += 1

        total_hashtags = sum(results.values())
        for p in results:
            results[p] = results[p] / total_hashtags

        return results
