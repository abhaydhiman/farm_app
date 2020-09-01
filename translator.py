# Importing Required Libraries
from googletrans import Translator


# Init For GoogleTrans
trans = Translator()


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

# Function for translating text to a given language
def text_translator(text_ls, lang):
    translated_ls = []
    for text in text_ls:
        translated = trans.translate(text, src='en', dest=lang)
        translated_ls.append(translated.text)
    return translated_ls