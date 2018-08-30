class FeatureExtractor:

    def __init__(self, tweets):
        self.tweets = tweets

    def get_hashtag_features(self):
        self.__get_hashtags()
        


    def __get_hashtags(self):
        """
            Private method used to extract hashtags from the given tweets.
            hashtags list form: [{'text': 'documentation', 'indices': [211, 225]}, {'text': 'parsingJSON', 'indices': [226, 238]}]
        """

        hashtags = []
        for tweet in self.tweets:
            #simple tweet
            first_level_potential_hashtags = tweet["entities"]["hashtags"]
            if len(first_level_potential_hashtags) > 0:
                hashtags.extend(first_level_potential_hashtags)

            #extended_tweet
            if "extended_tweet" in tweet:
                extended_potential_hashtags = tweet["extended_tweet"]["entities"]["hashtags"]
                if len(extended_potential_hashtags) > 0:
                    hashtags.extend(extended_potential_hashtags)

            #retweet
            if "retweeted_status" in tweet:
                retweeted_potential_hashtags = tweet["retweeted_status"]["entities"]["hashtags"]
                if len(retweeted_potential_hashtags) > 0:
                    hashtags.extend(retweeted_potential_hashtags)
        
        self.hashtags = hashtags

        
        
                