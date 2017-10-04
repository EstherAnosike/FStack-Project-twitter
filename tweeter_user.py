from datetime import datetime
import re
import csv
from hashlib import sha256
import os

USER_DETAILS = "details.csv"
tweets = []


class User:

    """
    @Class User - Generic class representing the user in the tweeter application
    The class holds all the properties and methods required to fully manipulate a user inside the class.
    """

    def __init__(self, **kwargs):
        self.user_name = kwargs.get('user_name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.fullname = kwargs.get("fullname")
        self.profile_url = kwargs.get("profile_url")
        self.messages = []
        self.messages.append(kwargs.get('messages', []))

        self.followers = []
        self.following = []
        self.following.append(kwargs.get("following"))
        self.followers.append(kwargs.get("followers"))
        self.bio_data = kwargs.get("bio_data")
        self.phone_number = kwargs.get("phone_number")
        self.date_of_birth = kwargs.get('date_of_birth', None)
        self.creation_date = kwargs.get("creation_date", datetime.now())
        self.tweets = kwargs.get("tweets")
        self.is_logged_in = kwargs.get("is_logged_in", False)
        self.last_login_time = datetime.now()




    def tweet(self, my_tweet):
        tweet = Tweet(self, my_tweet[:280])
        self.tweets.append(tweet)

    def retweet(self, tweet):
        if tweet in self.tweets:
            tweet.retweet -= 1
        else:
            self.tweets.append(tweet)

    def like(self, tweet):
        if tweet in self.tweets:
            tweet.likes += 1

    def __del_obj(self, obj):
        if isinstance(obj, Tweet):
            if obj in self.tweets:
                self.tweets.remove(obj)
        elif isinstance(obj, Message):
            if obj in self.messages:
                self.messages.remove(obj)

    def del_tweet(self, tweet):
        self.__del_obj(tweet)
    def del_message(self, msg):
        self.__del_obj(msg)

    def message(self, msg_txt, to):
        if isinstance(to, User):
            msg = Message(msg_txt, self, to)
            self.messages.append(msg)
            print("Sent message to {} at {} time".format(to.user_name, msg.creation_date))
        else:
            print("Invalid recipient!")


    def follow(self, user_name=""):
        users_dict = Tweeter.load(USER_DETAILS)

        for user in users_dict:
            user_obj = User.create_user(**user)
            if user_obj.user_name == self.user_name:
                users_dict.remove(user)

        for user in users_dict:

            user_obj = User.create_user(**user)
            temp_self = self
            if user_obj.user_name == self.user_name:
                users_dict.remove(user)
            if user_obj.user_name == user_name:
                temp_user_obj = user_obj
                users_dict.remove(user)
                temp_user_obj.followers.append(self)  # adding current user the persons followers
                temp_self.following.append(temp_user_obj)  # Adding the person to current users following
                users_dict.append(temp_user_obj.__dict__)
                users_dict.append(temp_self.__dict__)

                print('''
                                        {} now following {}
                                        Currently following {}
                                    '''.format(self.user_name, temp_user_obj.user_name, len(self.following)-1))
                os.remove(USER_DETAILS)
                for i in users_dict:
                    Tweeter.save(i)
                return

    def un_follow(self, user_name):
        for user in Tweeter.load(USER_DETAILS):
            if user.user_name == user_name:
                user.followers.remove(self)
                self.following.remove(user)

                print('done')

    @classmethod
    def create_user(cls, **datadict):
        return cls(**datadict)

    def __repr__(self):
        return("""
        Account Information:
        Name: {}       Created on: {}
        Tweets: {}    Messages: {}     Followers: {}    Following: {}   
        Email: {}
        Logged in: {} Since: {}
        """.format(self.user_name.capitalize(), self.creation_date, len(self.tweets), len(self.messages), \
                   len(self.followers), len(self.following), self.email, self.is_logged_in, self.last_login_time))


class Tweet:

    """
    @Tweet creates the tweet object
    Takes the username of the person tweeting and the message
    Returns the tweet object
    """
    def __init__(self, user, message):
        self.user = user
        self.message = message
        self.like = 0
        self.retweets = 0
        self.creation_date = datetime.now()

class Message:

    def __init__(self,msg, fr, to):
        self.msg = msg
        self.creation_date = datetime.now()
        self.to = to
        self.fr = fr

    def __repr__(self):
        return"{} at this {}".format(self.msg, self.datetime)


class Tweeter:

    @staticmethod
    def save(info_dict):
        headers = ['following', 'date_of_birth', 'user_name', 'bio_data', 'email', 'password', 'is_logged_in', 'creation_date', 'messages', 'tweets', 'fullname', 'last_login_time', 'phone_number', 'followers', 'profile_url']
        try:
            with open(USER_DETAILS, 'a+') as fh:
                csv_w = csv.DictWriter(fh, headers)
                if os.stat(USER_DETAILS).st_size == 0:
                    csv_w.writeheader()
                csv_w.writerow(info_dict)
        except Exception as e:
            raise e

    @staticmethod
    def is_email_valid(email):
        return re.match(r'\b[\w.-]+?@\w+?\.\w+?\b', email)

    @staticmethod
    def register(username, email, password):
        if Tweeter.is_email_valid(email):
            dict_r = dict(user_name=username, email=email, password=sha256(password).hexdigest())
            user = User(**dict_r)
            Tweeter.save(user.__dict__)
            # todo send mail later..
        else:
            print("Invalid email address!")

    @staticmethod
    def load(filename):
        user_list = []
        try:
            with open(filename, 'r') as fh:
                fh_dict = csv.DictReader(fh)
                for i in fh_dict:
                    user_list.append(i)
                return user_list
        except Exception as e:
            raise e

    @staticmethod
    def verify_password(user, password):
        return user.get('password') == sha256(password).hexdigest()

    @staticmethod
    def user_exist(email):
        user_list = Tweeter.load(USER_DETAILS)
        for user in user_list:
            if user.get("email") == email:
                return True
        return False

    @staticmethod
    def login(email,password):
        user_list = Tweeter.load("details.csv")
        user_obj = None

        for user in user_list:
            if user.get('email') == email and Tweeter.verify_password(user, password):
                user['is_logged_in'] = True
                user_obj = User.create_user(**user )
        return user_obj

    @staticmethod
    def logout(self):
        if self.is_logged_in:
            self.is_logged_in = False
            del self
            print("Logged out!")



def main():
    #Tweeter.register("George", "george@gmail.com", b"asdfghjkl")
    # Tweeter.register("Ib", "ibra@gmail.com", b'1234567890')

    george = Tweeter.login("george@gmail.com", b"asdfghjkl")
    #
    Ib = Tweeter.login("ibra@gmail.com", b'1234567890')    # george.follow("Ib")
    if Ib is not None:
         Ib.follow("George")
         Ib.message("Hi man", george)

    # else:
    #     print("Invalid credentials!")


if __name__ == '__main__':
    main()



