from datetime import datetime

class Tweet:
    """
    @class: Tweet
    @:param text - text is an expected string of input from the user representing a tweet message
                    However, the limit of a text for a certain tweet is 140 characters.
    @:param user_id - this is the user object that posted a tweet.

    @:property retweet - it initializes to 0 and it is the number of retweets for this tweet.
    @:property likes - it initializes to 0 and it is the number of likes for a tweet.


    """

    def __init__(self,text):
        if len(text) <= 280:
            self.text = text
            self.retweet = 0
            self.likes = 0
            self.comment = 0
            self.time = datetime.now()
        else:
            raise ("Can only create a tweet from a user")

    def __repr__(self):
        return ("tweeted {} at {} \nComments: {} \t Likes: {} \t Retweets: {}.".format(self.text, self.time, self.comment,self.likes,                self.retweet))


