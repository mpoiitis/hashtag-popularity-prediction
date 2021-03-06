from pymongo import MongoClient
import pymongo

class DbHandler:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["Test_db"]

        collection = self.db["plastic"]
        collection.create_index([('user', pymongo.TEXT)])

    def getTweets(self, db="plastic"):
        tweets = self.db[db].find({}) #use curly brackets to bypass default return limit
        return list(tweets)

    def getTweetsByNum(self, num, skip=None, db="plastic"):
        if skip != None:
            tweets = self.db[db].find({}).skip(skip).limit(num)
        else:
            tweets = self.db[db].find({}).limit(num)
        return list(tweets)

    def getTweetTexts(self, num, skip=None, db="plastic"):
        if skip != None:
            texts = list(self.db[db].find({}, {"text":1, "_id":0}).skip(skip).limit(num))
        else:
            texts = list(self.db[db].find({}, {"text":1, "_id":0}).limit(num))

        texts = [item["text"] for item in texts]
        text = " ".join(texts)

        return text

    def getTweetAuthors(self, num, skip=None, db="plastic"):

        if skip != None:
            authors = list(self.db[db].find({}, {"user.id_str":1, "_id":0}).skip(skip).limit(num))
        else:
            authors = list(self.db[db].find({}, {"user.id_str":1, "_id":0}).limit(num))

        authors = [item["user"]["id_str"] for item in authors]
        return authors

    def getRetweetsNum(self, num, skip=None, db="plastic"):
        if skip != None:
            retweets = list(self.db[db].find({"retweeted_status": {"$exists": "true"}}).skip(skip).limit(num))
        else:
            retweets = list(self.db[db].find({"retweeted_status": {"$exists": "true"}}).limit(num))

        return len(retweets)

    def getTweetById(self, id, db="plastic"):
        tweet = self.db[db].find_one({"id_str": id})
        return tweet

    # def getTweetsFromTopK(self):
    #     tweets = self.db["topK"].find({})
    #     return list(tweets)
    #
    # def storeTopKTweets(self, tweets):
    #     collection = self.db["topK"]
    #     collection.insert_many(tweets)

    def getTweetsForHashtag(self, hashtag="India", db="plastic"):
        collection = self.db[db]
        exp1 = {"entities.hashtags.text" : "{}".format(hashtag)}
        exp2 = {"extended_tweet.entities.hashtags.text" : "{}".format(hashtag)}
        exp3 = {"retweeted_status.entities.hashtags.text": "{}".format(hashtag)}
        exp4 = {"retweeted_status.extended_tweet.entities.hashtags.text": "{}".format(hashtag)}
        tweets = list(collection.find({"$or": [exp1, exp2, exp3, exp4]}))
        return tweets

    def getNumOfTweets(self, db="plastic"):
        return self.db[db].count()