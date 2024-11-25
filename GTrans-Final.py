import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import mysql.connector as bridge
import os
import pyttsx3
import datetime


conn = bridge.connect(host = 'localhost',user = 'root',passwd = 'admin',database='GTrans')
xo = conn.cursor()


dic = ('afrikaans', 'af', 'albanian', 'sq',
       'amharic', 'am', 'arabic', 'ar',
       'armenian', 'hy', 'azerbaijani', 'az',
       'basque', 'eu', 'belarusian', 'be',
       'bengali', 'bn', 'bosnian', 'bs', 'bulgarian',
       'bg', 'catalan', 'ca', 'cebuano',
       'ceb', 'chichewa', 'ny', 'chinese (simplified)',
       'zh-cn', 'chinese (traditional)',
       'zh-tw', 'corsican', 'co', 'croatian', 'hr',
       'czech', 'cs', 'danish', 'da', 'dutch',
       'nl', 'english', 'en', 'esperanto', 'eo',
       'estonian', 'et', 'filipino', 'tl', 'finnish',
       'fi', 'french', 'fr', 'frisian', 'fy', 'galician',
       'gl', 'georgian', 'ka', 'german',
       'de', 'greek', 'el', 'gujarati', 'gu',
       'haitian creole', 'ht', 'hausa', 'ha',
       'hawaiian', 'haw', 'hebrew', 'he', 'hindi',
       'hi', 'hmong', 'hmn', 'hungarian',
       'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian',
       'id', 'irish', 'ga', 'italian',
       'it', 'japanese', 'ja', 'javanese', 'jw',
       'kannada', 'kn', 'kazakh', 'kk', 'khmer',
       'km', 'korean', 'ko', 'kurdish (kurmanji)',
       'ku', 'kyrgyz', 'ky', 'lao', 'lo',
       'latin', 'la', 'latvian', 'lv', 'lithuanian',
       'lt', 'luxembourgish', 'lb',
       'macedonian', 'mk', 'malagasy', 'mg', 'malay',
       'ms', 'malayalam', 'ml', 'maltese',
       'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian',
       'mn', 'myanmar (burmese)', 'my',
       'nepali', 'ne', 'norwegian', 'no', 'odia', 'or',
       'pashto', 'ps', 'persian', 'fa',
       'polish', 'pl', 'portuguese', 'pt', 'punjabi',
       'pa', 'romanian', 'ro', 'russian',
       'ru', 'samoan', 'sm', 'scots gaelic', 'gd',
       'serbian', 'sr', 'sesotho', 'st',
       'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si',
       'slovak', 'sk', 'slovenian', 'sl',
       'somali', 'so', 'spanish', 'es', 'sundanese',
       'su', 'swahili', 'sw', 'swedish',
       'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu',
       'te', 'thai', 'th', 'turkish',
       'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur',
       'ug', 'uzbek', 'uz',
       'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
       'yiddish', 'yi', 'yoruba',
       'yo', 'zulu', 'zu')


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.runAndWait()


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wish():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    elif hour >= 18 and hour < 24:
        speak("Good Evening Sir!")
    else:
        speak("Hello Sir")

    speak("I am your Translating Assistant")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"You have said {query}\n")
        record.append(query)
    



    except Exception as e:
        speak("Can not recognize you")
        print("WARNING:It may also occur due to poor internet connection.")
        return "None"
    return query


wish()

record = []

speak("Say something to translate \n")
query = takecommand()
while (query == "None"):
    query = takecommand()


def destination_language():
    speak("Language in which you want to convert?")
    print("Ex. Tamil, Hindi , English , etc.")

    to_lang = takecommand()
    while (to_lang == "None"):
        to_lang = takecommand()
    to_lang = to_lang.lower()
    return to_lang


to_lang = destination_language()


while (to_lang not in dic):
    print("Language is currently not available, please say some other language")
    print("Please check the supported languages")
    print(dic)
    to_lang = destination_language()


to_lang = dic[dic.index(to_lang) + 1]


translator = Translator()
text_to_translate = translator.translate(query, dest=to_lang)
text = text_to_translate.text
speak = gTTS(text=text, lang=to_lang, slow=False)

speak.save("captured_voice.mp3")

os.system('captured_voice.mp3')
os.remove('captured_voice.mp3')

record.append(text)

print("The Translated word is",text)

xo.execute("insert into translation(From_Word,To_Word,Req_Lang) values (%s,%s,%s)",(record[0],record[2],record[1]))

conn.commit()
conn.close()
