import telebot
from db import DB_helper
from keras.preprocessing import sequence
from preprocess import cleanComment, Model

import numpy as np
API_TOKEN = '#######'

bot = telebot.TeleBot(API_TOKEN)
#server = Flask(__name__)

db = DB_helper(bot)

# clean comment object.
cc = cleanComment()

max_len = 200

#Loading Model.
models = Model()
vctModel = models.loadVectorizer("vectorizer-model.pkl")
clfModel = models.loadModel("cnnModel.h5")


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I will be watching toxic messages in a chat.\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    
    # identify the source of the message.
    print(message.chat.type)
    
    tags = isToxic(message.text)
    if(not len(tags)==0):
        print(tags)
        
        # res: 1-> The user has to be banned for 24 hour, 0-> Just another warning.
        res = db.reportWarning(message, tags)
       
        # delete message.
        bot.delete_message(message.chat.id, message.message_id)

        
            

def isToxic(chatText):
    #pre-processing.
    cleanChat = cc.clean_comment(chatText)
    cleanChat = cc.expandComment(chatText)
    cleanChat = cc.stemming(chatText)

    # vectorizing.    
    cvtChat = vctModel.texts_to_sequences([cleanChat])
    cvtChat = sequence.pad_sequences(cvtChat, max_len)

    result = []

    comments = ["Toxic","Severe toxic","Obscene","Threat","Insult","Identity hate"]
    predictionRes = np.round(clfModel.predict(cvtChat))[0]
    print(predictionRes)
    for i in range(len(predictionRes)):
        if(predictionRes[i]==1):
            result.append(comments[i])
    
    return result



bot.polling()


'''
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://boiling-retreat-81374.herokuapp.com/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

'''
