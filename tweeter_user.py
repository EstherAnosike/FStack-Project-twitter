from datetime import datetime

class User:
    """
    @Class User - Generic class representing the user in the tweeter application
    The class holds all the properties and methods required to fully manipulate a user inside the class.
    """

    def __init__(self, username, password, email):
        self.user_name =username
        self.__email = email
        self.__password = password
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


