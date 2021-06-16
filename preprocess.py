# importing important libraries.
import re
from nltk.stem.snowball import SnowballStemmer
import json
import requests
from keras.preprocessing import sequence

# importing important libraries.
import nltk
from nltk.corpus import stopwords

# keras load model.
from keras.models import load_model
import numpy as np
import joblib 

# contracted words list with their expanded form.    # can't to can not 
content = requests.get("https://github.com/JoeKifle/Toxic-Comment-Classification/blob/main/expandedContractions.json?raw=true")
cList = json.loads(content.content)

class cleanComment:
    def __init__(self) -> None:
        nltk.download('stopwords')
        self.stop = stopwords.words('english')
        self.stemmer = SnowballStemmer("english")

    def clean_comment(self,comment):
        '''
        This function will remove the following contents from the comment.
            * URLs.        * Emails.
            * Months.      * '\n' characters.
            * Digits.      * Non english characters.
        
        '''
    
        comment = comment.lower()
        comment = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', '', comment) # clean url
        comment = re.sub(r'(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)','',comment) # clean month
        comment = re.sub(r'\d+', '', comment)                           # clean numbers
        comment = re.sub(r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+','',comment) # clean email 
        comment = re.sub(r'\n', '', comment)                            # clean \n
        comment = re.sub(r'([^\x00-\x7F])+','',comment)                 # clean Non-English characters 
        return comment 
    
    def expandComment(self,comment):
        if type(comment) is str:
            for key in cList:
                value = cList[key]
                comment = comment.replace(key, value)
            return comment
        else:
            return comment
    
    def stemming(self,sentence):
        stemSentence = ""
        for word in sentence.split():
            stem = self.stemmer.stem(word)
            stemSentence += stem
            stemSentence += " "
        stemSentence = stemSentence.strip()
        return stemSentence
    
    def hello(self):
        print("Hello")

class Model:
    def __init__(self) -> None:
        pass

    def loadVectorizer(self,modelName):
        file_path = "models/{0}".format(modelName)
    # Open file and preprocessin object
        with open(file_path, 'rb') as f:
            object = joblib.load(f)
            return object  

    def loadModel(self,modelName):
        loadedModel = load_model('models/{0}'.format(modelName))
        return loadedModel
    def makePrediction(self,modelName):
        pass


#cc = cleanComment()
#clean_message = "All of my edits are good.  Cunts like you who revert good edits because you're too stupid to understand how to write well , and then revert other edits just because you've decided to bear a playground grudge, are the problem.  Maybe one day you'll realise the damage you did to a noble project.  201.215.187.159"

#pre-processing.
#clean_message = cc.clean_comment(clean_message)
#clean_message = cc.expandComment(clean_message)
#clean_message = cc.stemming(clean_message)

#Loading Model.
#models = Model()
#vctModel = models.loadVectorizer("vectorizer-model.pkl")
#clfModel = models.loadModel("cnnModel.h5")


# Test run.
#max_len = 200
#test = vctModel.texts_to_sequences(["you scumbag!"])
# padding the sequences
#test = sequence.pad_sequences(test, max_len)
#print(np.round(clfModel.predict(test)))
    



    