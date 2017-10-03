from datetime import datetime
import re
import csv
from hashlib import sha256
import os

USER_DETAILS = "details.csv"

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

    def follow(self,user_name=""):
        for user in Tweeter.load(USER_DETAILS):
            user_obj = User.create_user(**user)
            if user_obj.user_name ==user_name :
                user_obj.followers.append(self) # asedding current user the persons followers
                self.following.append(user_obj) #dding the person to current users following
                print('''
                        {} now following {}
                        Currently following {}
                
                
                     
                     '''.format(self.user_name,user_obj.user_name,len(self.following)))

    def unfollow(self,user_name):
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




class Tweeter:

    @staticmethod
    def save(info_dict):

        try:
            with open(USER_DETAILS, 'a+') as fh:
                csv_w = csv.DictWriter(fh,info_dict.keys())
                if os.stat(USER_DETAILS).st_size == 0:
                    csv_w.writeheader()
                csv_w.writerow(info_dict)
        except Exception as e:
            raise e

    @staticmethod
    def is_email_valid(email):
        return (re.match(r'\b[\w.-]+?@\w+?\.\w+?\b', email))

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
                return (user_list)
        except Exception as e:
            raise e

    @staticmethod
    def verify_password(user, password):
        return (user.get('password') == sha256(password).hexdigest())

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

def main():

    Tweeter.register("George", "george@gmail.com", b"asdfghjkl")
    Tweeter.register("Ib", "ibra@gmail.com", b'1234567890')

    george = Tweeter.login("george@gmail.com", b"asdfghjkl")
    george.follow("Ib")
    print(george)



if __name__ == '__main__':
    main()