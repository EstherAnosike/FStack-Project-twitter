""" 
User.py - The main user interaction file.
The file is supposed to allow for all user interaction including sending their messages,
sending tweets and hashing the passwords.
I guess we shall have to create a Tweeter class that instantiates everything.
"""


import smtplib                              #for sending an email
import re                                   #for email and username verification
import os                                   #for file and persistent storage
from email.mime.text import MIMEText        #helper for email
from datetime import datetime               #dates
from passlib.hash import pbkdf2_sha256      #password hash and verify
from os import path                         #path and file manipulation

class User:
    """
    @Class User - Generic class representing the user in the tweeter application
    The class holds all the properties and methods required to fully manipulate a user inside the class.
    """

    def __init__(self):
        self.user_name =""
        self.__email = ""
        self.__password = ""
        self.fullname = ""
        self.__profile_url = ""
        self.__messages = []
        self.__followers = []
        self.__following = []
        self.__bio_data = ""
        self.__phone_number = ""
        self.__date_of_birth = None
        self.__creation_date = datetime.now()
        self.__tweets = []
        self.__is_logged_in = False
        self.__hash = ""

    #verify that the email is really an email.
    #helper function - should be working on the user object but not inside the user object
    def __email_verify(self, email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else: return False

    #verify that the email is an alphanumerical name with the allowed characters.
    #I got this online
    #this one too
    def __username_verify(self, username):
        if re.match(r'^(?=(?![0-9])?[A-Za-z0-9]?[._-]?[A-Za-z0-9]+).{3,20}', username):
            return True
        else: return False


    #private hash_password to hash the incoming password so that it doesn't store as plain text
    def __hash_password(self, raw_password):
         return pbkdf2_sha256.hash(raw_password.strip(' '))

    #verify the password provided is really what is stored in the object.
    #used during login
    def __pwd_verify(self, password):
        if pbkdf2_sha256.verify(password, self.__password):
            return True
        else: return False

    #login function. Takes email and password
    #verify the password and email and then set up the users environment.
    #probably fetch the user environ from the user file stored at path.curdir+user_name+.csv
    #this should actually set up the user object
    def login(self, email, password):
        if self.__email == email and self.__pwd_verify(password):
            if self.__account_verify(self.__hash):
                pass
        else:
            print("Invalid username or password!")

    #used to check whether the user is really logged in
    #important to maintain a flag that keeps the state when a person is logged in so that you avoid
    #inconsisenc
    def is_logged_in(self):
        return (self.__is_logged_in == True)

    def logout(self):
        if self.__is_logged_in:
            pass #log the user out
        else:
            return None

    #take the hash and verify it against username.
    def __account_verify(self, hash):
        if pbkdf2_sha256.verify(hash, self.user_name):
            return True
        else:return False

    #create a new user instance.. should be a tool_function.
    def signup(self, username, email, password):
        if self.__username_verify(username) and self.__email_verify(email):
            self.__password = pbkdf2_sha256.hash(password.strip(' '))
            self.user_name = username
            self.__email = email
            self.__hash = pbkdf2_sha256.hash(username.strip(' '))
            #creted, go forth and define the save the document
            with open(path.curdir+self.user_name+".csv") as user_handle:
                user_handle.write(self.__dict__)
                #saved, close the file now
            user_handle.close()
            self.send_mail(email)
            #thats all. Wait for user to verify account before logging them in

        else:
            print("Invalid values provided!")


    def __reset_password(self, new_password):
        self.__password = pbkdf2_sha256.hash(new_password.strip(' '))

    def forgot_password(self, email, new_password):
        if self.__email == email:
            self.__reset_password(new_password)
        else:
            print("Cannot verify account")

    def send_mail(self, email):
        msg_body = """
            Thank you for signing up to tweeter. You can be free to browse the application.
            Verify your account by entering the code below.
            You can send tweets to friends, invite friends and follow those whom you like to follow.
            
            Keep in touch.
            Code: {}
        """.format(self.__hash)

        from_user = "ourtweeter@meltwater.org"
        subject = "Thank you for signing up!"
        if self.__email_verify(email):
            to_mail = email
            #..
            #sending mechanisms here
            #..
        else:
            return ("Unknown email!")




