from translate import Translator
import math, random
#________________________________________________________________________________________________________________________

def translator(text , to_langg = 'hindi'):
    translator= Translator(to_lang = to_langg)
    translated_text = translator.translate(text)
    return translated_text
#_______________________________________________________________________________________________________________________
def OTP_generator():
    # for alpha nuemeric OTP 
    corpus= "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    generate_OTP = "" 
    size = 5 # length of generated OTP
    length = len(corpus) 
    for i in range(size) : 
        generate_OTP += corpus[math.floor(random.random() * length)] 
    return generate_OTP
#_______________________________________________________________________________________________________________________
