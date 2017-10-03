from datetime import datetime

class User:
    """
    @Class User - Generic class representing the user in the tweeter application
    The class holds all the properties and methods required to fully manipulate a user inside the class.
    """
    registered_users=[] #add all user objects to list

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
        User.registered_users.append(self)



    def follow(self,user_name=None):
        for list_user in User.registered_users:
            if list_user.user_name ==user_name :
                list_user.__followers.append(self.user_name) # adding current user the persons followers
                self.__following.append(user_name) #dding the person to current users following

                print('''
                        {} now following {}
                        Currently following {}
                
                
                     
                     '''.format(self.user_name,list_user.user_name,len(self.__following)))

    def unfollow(self,user_name):
        for useradd in User.registered_users:
            if useradd.user_name == user_name:
                useradd.__followers.remove(user_name)
                self.__following.remove(user_name)

                print('done')




andrew = User ('andrew','qwertyu','qwertyrety')
Francis = User('frank','ghana','wertyui')
print(andrew.follow('frank'))
print(andrew.unfollow('frank'))


 # print(andrew.follow('adrsrs'))