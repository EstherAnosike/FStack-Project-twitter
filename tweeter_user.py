from datetime import datetime
import re
import csv
from hashlib import sha256
import os

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
        self.messages = kwargs.get('messages')
        self.followers = kwargs.get("followers" )
        self.following = kwargs.get("following")
        self.bio_data = kwargs.get("bio_data")
        self.phone_number = kwargs.get("phone_number")
        self.date_of_birth = kwargs.get('date_of_birth', None)
        self.creation_date = kwargs.get("creation_date",datetime.now())
        self.tweets = kwargs.get("tweets")
        self.is_logged_in = kwargs.get("is_logged_in", False)
        self.last_login_time = datetime.now()


    @classmethod
    def create_user(cls, **datadict):
        return cls(**datadict)

    def __repr__(self):
        return("""
        Account Information:
        {}         Created on: {}
        Tweets: {}    Messages: {}     Followers: {}    Following: {}   
        Email: {}
        Logged in: {} Since: {}
        """.format(self.user_name.capitalize(), self.creation_date, len(self.tweets), len(self.messages), \
                   len(self.followers), len(self.following), self.email, self.is_logged_in, self.last_login_time))




class Tweeter:

    @staticmethod
    def save(info_dict):
        filename = "details.csv"

        try:
            with open(filename, 'a+') as fh:
                csv_w = csv.DictWriter(fh,info_dict.keys())
                if os.stat(filename).st_size == 0:
                    csv_w.writeheader()
                csv_w.writerow(info_dict)
            fh.close()
        except Exception as e:
            raise e

    @staticmethod
    def is_email_valid(email):
        return (re.match(r'\b[\w.-]+?@\w+?\.\w+?\b', email))

    @staticmethod
    def register(username, email, password):
        if Tweeter.is_email_valid(email):
            dict_r = dict(username=username, email=email, password=sha256(password).hexdigest())
            user = User(**dict_r)
            Tweeter.save(user.__dict__)
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
                return (user_list)
        except Exception as e:
            raise e

    @staticmethod
    def verify_password(user, password):
        return (user.get('password') == sha256(password).hexdigest())

    @staticmethod
    def user_exist(email):
        user_list = Tweeter.load("details.csv")
        for user in user_list:
            if user.get("email") == email:
                return True

        return False

    @staticmethod
    def login(email,password):
         user_list = Tweeter.load("details.csv")
         for user in user_list:
             if user.get('email') == email and Tweeter.verify_password(user, password):
                user['is_logged_in'] = True
                user_obj = User.create_user(**user )
                print(user_obj)
Tweeter.login("esthesr@gmail.com", b"whatever")

