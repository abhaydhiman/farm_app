# Importing Google Translator Python Library
from googletrans import Translator

# Importing Functions From pages_text.py File
from pages_text import user_home_text, weather_text, user_home_text2, user_home_text3, user_home_text4,\
user_home_text5, financial_text,loan_text,loan_text2,loan_text3,loan_text4,loan_text5,insu_text,insu_text2,\
insu_text3,insu_text4,insu_text5


# Init For GoogleTrans
trans = Translator()


#_____________________________________________________________________
# Fuction for checking the language selected by user
def language_checker(language):

    lang = '' 

    if language == 'English':
        lang = 'en'
    elif language == 'Hindi':
        lang = 'hi'
    elif language == 'Punjabi':
        lang = 'pa'
    elif language == 'Marathi':
        lang = 'mr'
    elif language == 'Tamil':
        lang = 'ta'
    elif language == 'Haryanvi':
        lang = 'hi'

    return lang


#_____________________________________________________________________
# Function for translating text to a given language
def text_translator(text_ls, lang):
    translated_ls = []
    for text in text_ls:
        translated = trans.translate(text, src='en', dest=lang)
        translated_ls.append(translated.text)
    return translated_ls



#___________________________________________________________________________
# Function for translating User Home Text to the language selected by user
def user_home_text_translator(lang, name, city, state):
    translated_ls = []
    if lang == 'en':
        translated_ls = user_home_text()
    elif lang == 'hi':
        translated_ls = user_home_text2()
    elif lang == 'pa':
        translated_ls = user_home_text3()
    elif lang == 'mr':
        translated_ls = user_home_text4()
    elif lang == 'ta':
        translated_ls = user_home_text5()
    elif lang == 'hi':
        translated_ls = user_home_text2()
    name = trans.translate(name, src='en', dest=lang)
    city = trans.translate(city, src='en', dest=lang)
    state = trans.translate(state, src='en', dest=lang)
    return translated_ls, name.text, city.text, state.text



#_____________________________________________________________________________
# Function for translating Weather page text to the language selected by user
def weather_text_translator(lang, city, state):
    text_ls = weather_text()
    translated_ls = []
    for text in text_ls:
        translated = trans.translate(text, src='en', dest=lang)
        translated_ls.append(translated.text)
    city = trans.translate(city, src='en', dest=lang)
    state = trans.translate(state, src='en', dest=lang)
    return translated_ls, city.text, state.text



#_____________________________________________________________________
# Function for translating given text of any language to english
def english_translator(text):
    translated = trans.translate(text, dest='en')
    return translated.text



#_____________________________________________________________________
# Function for translating Financial Page Text
def financial_translator(lang):
    text_ls = financial_text()
    translated_ls = []
    for text in text_ls:
        translated = trans.translate(text, src='en', dest=lang)
        translated_ls.append(translated.text)
    return translated_ls



#____________________________________________________________________________
# Function for translating Loan Form Text to the language selected by user
def loan_text_translator(lang, t1, t2, t3):
    translated_ls = []
    if lang == 'en':
        translated_ls = loan_text()
    elif lang == 'hi':
        translated_ls = loan_text2()
    elif lang == 'pa':
        translated_ls = loan_text3()
    elif lang == 'mr':
        translated_ls = loan_text4()
    elif lang == 'ta':
        translated_ls = loan_text5()
    elif lang == 'hi':
        translated_ls = loan_text2()
    t1 = trans.translate(t1, src='en', dest=lang)
    t2 = trans.translate(t2, src='en', dest=lang)
    t3 = trans.translate(t3, src='en', dest=lang)
    return translated_ls, t1.text, t2.text, t3.text



#__________________________________________________________________________
# Function for translating Insurance Form Text to the language selected by user
def insu_text_translator(lang, t1, t2, t3):
    translated_ls = []
    if lang == 'en':
        translated_ls = insu_text()
    elif lang == 'hi':
        translated_ls = insu_text2()
    elif lang == 'pa':
        translated_ls = insu_text3()
    elif lang == 'mr':
        translated_ls = insu_text4()
    elif lang == 'ta':
        translated_ls = insu_text5()
    elif lang == 'hi':
        translated_ls = insu_text2()
    t1 = trans.translate(t1, src='en', dest=lang)
    t2 = trans.translate(t2, src='en', dest=lang)
    t3 = trans.translate(t3, src='en', dest=lang)
    return translated_ls, t1.text, t2.text, t3.text

