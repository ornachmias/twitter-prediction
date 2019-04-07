class PopularityHandler(object):
    def get_popularity_score(self, tweets):
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
