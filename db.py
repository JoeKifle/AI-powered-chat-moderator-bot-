import telebot as tb
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta


#define connection
class DB_helper:
    def __init__(self, bot):
        self.bot = bot
        cred = credentials.Certificate("creds/hlt-toxic-comment-project-firebase-adminsdk-d89k0-bc4e6d8246.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://hlt-toxic-comment-project-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        # The two dbs.
        self.user_ref = db.reference("users")
        self.comm_ref = db.reference("comments")
        
    def saveuser(self, message):
        '''
          Registers new users who wrote offensive commments.

        '''

        tgId = message.from_user.id
        fname = message.from_user.first_name
        lname = message.from_user.last_name
        warningCount = 1
        
        if not self.isUserNew(message):
                self.user_ref.push({
                'tgId' : tgId,
                'fname': fname,
                'lname': lname,
                'warningCount': warningCount,
                })
    
    def isUserNew(self, message):
        ''''
        Return: 
           True -> If the user is a new user.
           False -> If he/she has not been registered yet.
        '''
        # check if the user is already registered
        result = self.user_ref.order_by_child('tgId').equal_to(message.from_user.id).get()
        if len(result) == 1:
            return True
        else:
            return False
    def get_post_mention(self,userID,userFname):
        '''
        Prepare the mention links.
        '''
        user_id = userID
        mention = "["+userFname+"](tg://user?id="+str(user_id)+")"
        return mention
    
    def getWarningCount(self,message):
        '''
        Return: Type -> int
          -? number of warnings he recieved yet.
        '''
        result = self.user_ref.order_by_child('tgId').equal_to(message.from_user.id).get()
        if(len(result)>0):
            for key, val in result.items():
                values = val
            return values["warningCount"]
        else:
            return 0 

    def saveComment(self, message, tags):
        '''
          save comment in the database.
        '''
        
        

        self.comm_ref.push({
                'comTags:' : tags,
                'comment':  message.text,
                'userID': message.from_user.id,
                'messageID': message.id 
            })

    def reportWarning(self, message, tags):
        
        chat_id = message.chat.id
        userID = message.from_user.id
        userFname = message.from_user.first_name+" "+message.from_user.last_name
        mention = self.get_post_mention(userID,userFname)
        
        # saving message.
        self.saveComment(message, tags)

        if not self.isUserNew(message):
            # The user is registered.
            self.saveuser(message)
            self.bot.send_message(chat_id,"Hey {0}❗️, Your message has been removed.\n\nReason: {1} contents!.\n\n ⚠️ Your FIRST Warning 😠.⚠️".format(mention,tags),parse_mode="Markdown")

        else:
            warningCount = self.getWarningCount(message)
            warningCount+=1
            if(warningCount > 2):
                # restrict user from a group for 48 hour
                #print("restricting the user for 48 hours")
                
                #self.restrictUser(userID,message)
                self.bot.send_message(chat_id,"Hey {0}❗️, You're restricted for 24 hours 👿.".format(mention),parse_mode="Markdown")
                
                # reset the user warning count to 0.
                result = self.user_ref.order_by_child('tgId').equal_to(message.from_user.id).get()
                for key, val in result.items():
                    user_key = key
                user_ref = self.user_ref.child(user_key)
                user_ref.update({
                    'warningCount': 0,
                })

                # Restric user for 24 hours.
                hours_24_from_now = datetime.now() + timedelta(hours=24)
                try:
                    self.bot.restrict_chat_member(message.chat.id,message.from_user.id, can_send_messages=False,until_date=hours_24_from_now)
                except:
                    print("[Error code: 0] - Error occured restricting user")

                return 1  # 1 - for blocking the user.
       
            else:
                # update the warning count.
                result = self.user_ref.order_by_child('tgId').equal_to(message.from_user.id).get()
                for key, val in result.items():
                    user_key = key
                user_ref = self.user_ref.child(user_key)
                user_ref.update({
                    'warningCount': warningCount,
                })
                warning = ["","FIRST","LAST"]
                warningText = warning[warningCount]
                self.bot.send_message(chat_id,"Hey {0}❗️, Your message has been removed.\n\nReason: {2} contents.\n\n ⚠️ Your {1} Warning. ⚠️".format(mention, warningText,tags),parse_mode="Markdown")

                return 0  # 0 - Just another warning.
 
       





