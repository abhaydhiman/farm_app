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
def text_translator(language):
    text_ls = []
    if language == 'en':
        text_ls = ["Farm Tech", "Made For Nature", "Sign Up", "Enter Name", "Enter Phone Number", "Submit", "Login"]
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'साइन अप करें', 'नाम दर्ज', 'फोन नंबर दर्ज', 'प्रस्तुत', 'लॉग इन करें']
    elif language == 'pa':
        text_ls = ['ਫਾਰਮ ਟੈਕ', 'ਕੁਦਰਤ ਲਈ ਬਣਾਇਆ ਗਿਆ', 'ਸਾਇਨ ਅਪ', 'ਨਾਮ ਦਰਜ ਕਰੋ', 'ਫੋਨ ਨੰਬਰ ਦਰਜ ਕਰੋ', 'ਜਮ੍ਹਾਂ ਕਰੋ', 'ਲਾਗਿਨ']
    elif language == 'mr':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'साइन अप करा', 'नाव प्रविष्ट करा', 'फोन नंबर प्रविष्ट करा', 'प्रस्तुत करणे', 'लॉगिन']
    elif language == 'ta':
        text_ls = ['பண்ணை தொழில்நுட்பம்', 'இயற்கைக்காக தயாரிக்கப்பட்டது', 'பதிவுபெறுக', 'பெயரை உள்ளிடுக', 'தொலைபேசி எண்ணை உள்ளிடவும்', 'சமர்ப்பிக்கவும்', 'உள்நுழைய']
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'साइन अप करें', 'नाम दर्ज', 'फोन नंबर दर्ज', 'प्रस्तुत', 'लॉग इन करें']
    return text_ls


# Function for translating text to a given language
def text_translator2(language):
    text_ls = []
    if language == 'en':
        text_ls = ["Farm Tech", "Made For Nature", "Enter OTP", "Enter OTP", "Submit", language]
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'ओटीपी दर्ज करें', 'ओटीपी दर्ज करें', 'प्रस्तुत', language]
    elif language == 'pa':
        text_ls = ['ਫਾਰਮ ਟੈਕ', 'ਕੁਦਰਤ ਲਈ ਬਣਾਇਆ ਗਿਆ', 'ਓਟੀਪੀ ਦਰਜ ਕਰੋ', 'ਓਟੀਪੀ ਦਰਜ ਕਰੋ', 'ਜਮ੍ਹਾਂ ਕਰੋ', language]
    elif language == 'mr':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'ओटीपी प्रविष्ट करा', 'ओटीपी प्रविष्ट करा', 'प्रस्तुत करणे', language]
    elif language == 'ta':
        text_ls = ['பண்ணை தொழில்நுட்பம்', 'இயற்கைக்காக தயாரிக்கப்பட்டது', 'otp ఎంటర్', 'otp ఎంటర్', 'சமர்ப்பிக்கவும்', language]
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'ओटीपी दर्ज करें', 'ओटीपी दर्ज करें', 'प्रस्तुत', language]
    return text_ls


# Function for translating text to a given language
def text_translator3(language):
    text_ls = []
    if language == 'en':
        text_ls = ["Farm Tech", "Made For Nature", "Create Password", "Enter Password", "confirm Password", "Submit", language]
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'पासवर्ड बनाएं', 'पासवर्ड दर्ज करें', 'पासवर्ड की पुष्टि कीजिये', "प्रस्तुत", language]
    elif language == 'pa':
        text_ls = ['ਫਾਰਮ ਟੈਕ', 'ਕੁਦਰਤ ਲਈ ਬਣਾਇਆ ਗਿਆ', 'ਪਾਸਵਰਡ ਬਣਾਓ', 'ਪਾਸਵਰਡ ਦਰਜ ਕਰੋ', 'ਪਾਸਵਰਡ ਪੱਕਾ ਕਰੋ', "ਜਮ੍ਹਾਂ ਕਰੋ", language]
    elif language == 'mr':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'पासवर्ड तयार करा', 'पासवर्ड टाका', 'पासवर्डची पुष्टी करा', "प्रस्तुत करणे", language]
    elif language == 'ta':
        text_ls = ['பண்ணை தொழில்நுட்பம்', 'இயற்கைக்காக தயாரிக்கப்பட்டது', 'పాస్వర్డ్ సృష్టించండి', 'రహస్య సంకేతం తెలపండి', 'పాస్వర్డ్ను నిర్ధారించండి', "సమర్పించండి", language]
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'पासवर्ड बनाएं', 'पासवर्ड दर्ज करें', 'पासवर्ड की पुष्टि कीजिये', "प्रस्तुत", language]
    return text_ls


# Function for translating text to a given language
def text_translator4(language):
    text_ls = []
    if language == 'en':
        text_ls = ["Farm Tech", "Made For Nature", "Login", "Enter Phone Number", "Enter Password", "Submit", "Signup",language]
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'लॉग इन करें', 'फोन नंबर दर्ज', 'पासवर्ड दर्ज करें', "प्रस्तुत", "साइन अप करें", language]
    elif language == 'pa':
        text_ls = ['ਫਾਰਮ ਟੈਕ', 'ਕੁਦਰਤ ਲਈ ਬਣਾਇਆ ਗਿਆ', 'ਲਾਗਿਨ', 'ਫੋਨ ਨੰਬਰ ਦਰਜ ਕਰੋ', 'ਪਾਸਵਰਡ ਦਰਜ ਕਰੋ',  "ਜਮ੍ਹਾਂ ਕਰੋ", "ਸਾਇਨ ਅਪ", language]
    elif language == 'mr':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'लॉगिन' , 'फोन नंबर प्रविष्ट करा', 'पासवर्ड टाका',  "प्रस्तुत करणे", "साइन अप", language]
    elif language == 'ta':
        text_ls = ['பண்ணை தொழில்நுட்பம்', 'இயற்கைக்காக தயாரிக்கப்பட்டது', 'ప్రవేశించండి', 'ఫోన్ నంబర్‌ను నమోదు చేయండి', 'రహస్య సంకేతం తెలపండి',  "సమర్పించండి", "చేరడం", language]
    elif language == 'hi':
        text_ls = ['फार्म टेक', 'मेड फॉर नेचर', 'लॉग इन करें', 'फोन नंबर दर्ज', 'पासवर्ड दर्ज करें',  "प्रस्तुत", "साइन अप करें", language]
    return text_ls


# # Function for translating User Home Text to the language selected by user
# def user_home_text_translator(lang, name, city, state):
#     text_ls = user_home_text()
#     translated_ls = []
#     for text in text_ls:
#         translated = trans.translate(text, src='en', dest=lang)
#         translated_ls.append(translated.text)
#     name = trans.translate(name, src='en', dest=lang)
#     city = trans.translate(city, src='en', dest=lang)
#     state = trans.translate(state, src='en', dest=lang)
#     return translated_ls, name.text, city.text, state.text


# # Function for translating Weather page text to the language selected by user
# def weather_text_translator(lang, city, state):
#     text_ls = weather_text()
#     translated_ls = []
#     for text in text_ls:
#         translated = trans.translate(text, src='en', dest=lang)
#         translated_ls.append(translated.text)
#     city = trans.translate(city, src='en', dest=lang)
#     state = trans.translate(state, src='en', dest=lang)
#     return translated_ls, city.text, state.text

# def english_translator(text):
#     translated = trans.translate(text, dest='en')
#     return translated.text
