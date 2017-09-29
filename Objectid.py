import re


class ObjectId:
    """"
    Class ObjectId enables userid to be either email,phone number or user name
    static fields:
        email
        username
        p_number
    class instances:
        userid
    regex module imported - validate inputs
    """

    email = ""
    username = ""
    p_number = 0

    def __init__(self, userid):

        if re.match(r'[\w.-]+@[\w.-]+.\w+', userid):
            self.email = userid
        elif re.match(r'[0-9]', userid):
            self.p_number = userid
        elif re.match(r'[a-zA-Z0-9]', userid):
            self.username = userid
        else:
            print("Unknown format!")


ObjectId(userid=input("Input login(email,phone number or username):"))

