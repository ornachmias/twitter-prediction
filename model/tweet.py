from tweepy import Status


class Tweet(object):

    def __init__(self):
        """
        Initialize an internal representation of the Status object from Tweepy
        """
        self.id = None
        self.create_date = None
        self.hashtags = None
        self.urls = None
        self.retweet_count = None
        self.favorite_count = None
        self.text = None
        self.user_mentions = None
        self.party = None
        self.full_text = None
        self.language = None

    def load_from_status(self, status_object: Status, party):
        """
        Convert Tweepy's Status object to internal Tweet object
        :param status_object: Status object received from iterating over Tweepy query
        :param party: The current status label
        """
        self.party = party
        self.id = status_object.id_str
        self.create_date = status_object.created_at
        self.retweet_count = status_object.retweet_count
        self.favorite_count = status_object.favorite_count

        # full_text and text are different properties and only one could be initialized
        # We prefer the full text and the queries always request it, but just in case we won't get it
        if hasattr(status_object, 'full_text'):
            self.text = status_object.full_text
        elif hasattr(status_object, 'text'):
            self.text = status_object.text

        self.language = status_object.lang

        self.hashtags = []
        self.urls = []
        self.user_mentions = []

        if hasattr(status_object, 'entities'):
            entities = status_object.entities
            if 'hashtags' in entities:
                for ent in entities['hashtags']:
                    if ent is not None:
                        if 'text' in ent:
                            hashtag = ent['text']
                            if hashtag is not None:
                                self.hashtags.append(hashtag)
            if 'user_mentions' in entities:
                for ent in entities['user_mentions']:
                    if ent is not None:
                        if 'screen_name' in ent:
                            name = ent['screen_name']
                            if name is not None:
                                self.user_mentions.append(name)
            if 'urls' in entities:
                for ent in entities['urls']:
                    if ent is not None:
                        if 'url' in ent:
                            url = ent['url']
                            if url is not None:
                                self.urls.append(url)

