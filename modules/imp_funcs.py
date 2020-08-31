from googletrans import Translator
import math, random 

# ***********************************************************************
firebaseConfig = {
    'apiKey': "AIzaSyA7pwCBjWgP73LA4j5XfuOoOTYsuADxbmU",
    'authDomain': "testing-54b5b.firebaseapp.com",
    'databaseURL': "https://testing-54b5b.firebaseio.com",
    'projectId': "testing-54b5b",
    'storageBucket': "testing-54b5b.appspot.com",
    'messagingSenderId': "294631472490",
    'appId': "1:294631472490:web:db7cd1423e921fbc75b913",
    'measurementId': "G-40WJHR7Z7F"
  }
# ***********************************************************************

# ________________________________________________________________________________________________________________________


# This function translates english to any other language
def translator(text , to_langg = 'hi'): 
    if to_langg.lower() != 'en':
        translator = Translator() 
        return translator.translate(text ,  src = 'en', dest = to_langg).text
    else:
        return text


# *------------------------------------------------------------------------------------------------------------------*


def OTP_generator():
    # for nuemeric OTP 
    corpus= "0123456789"
    generate_OTP = "" 
    size = 6 # length of generated OTP
    length = len(corpus) 
    for i in range(size) : 
        generate_OTP += corpus[math.floor(random.random() * length)] 
    return generate_OTP


# *------------------------------------------------------------------------------------------------------------------*


def msg_sender( given_phone_number = None , given_message = None ):
    import requests
    url = "https://www.fast2sms.com/dev/bulk"

    #______________________________________________
    # Message will be send to given number
    phone_number = given_phone_number

    # Message text
    message = given_message
    #______________________________________________


    payload = "sender_id=FSTSMS&message=" + message + "&language=english&route=p&numbers=" + str(phone_number)

    headers = {
    'authorization': "9GytnwpSjMzNY2UixTHmVBJaL6b5IrKZWq1eu30gf8dvohXc74miIxFjDcCJLp513tSEkVofz0QrOAY6",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url , data = payload, headers = headers)

    print(response.text)


# *------------------------------------------------------------------------------------------------------------------*


def context_generator(for_page , language_selected ,  texts_to_be_added = None ):


    if for_page == 'signup_page':
        context = {
                    'Enter_Credentials' : translator('Enter Credentials' , to_langg = language_selected) , 
                    'Phone_Number'      : translator('Phone Number' , to_langg = language_selected) , 
                    'Full_Name'         : translator('Full Name' , to_langg = language_selected) , 
                    'Generate_OTP'      : translator('Generate OTP' , to_langg = language_selected) , 
                    'Already_a_user'    : translator('Already a user , Log in ' , to_langg = language_selected) , 
                    'confirmation_state' : 1 , 
        }



    elif for_page == 'submit_signup_details':
        context = {
                    'Verify_OTP'            : translator('Enter OTP' , to_langg = language_selected) , 
                    'OTP'                   : translator('OTP' , to_langg = language_selected) , 
                    'Confirm'               : translator('Confirm' , to_langg = language_selected) , 
                    'confirmation_state'    : 2 , 
        }



    elif for_page == 'login_page':
        context = {
                    'Enter_Credentials'  : translator('Enter Credentials' , to_langg = language_selected) , 
                    'Phone_Number'       : translator('Phone Number' , to_langg = language_selected) , 
                    'Password'           : translator('Password' , to_langg = language_selected) , 
                    'login'              : translator('Log in' , to_langg = language_selected) , 
        }
    
    elif for_page == 'check_login_details':
        context = {
                    'Enter_Credentials'  : translator('Enter Credentials' , to_langg = language_selected) , 
                    'Phone_Number'       : translator('Phone Number' , to_langg = language_selected) , 
                    'Password'           : translator('Password' , to_langg = language_selected) , 
                    'login'              : translator('Log in' , to_langg = language_selected) , 
                    'warning_msg'        : "Either phone number or password is incorrect" , 
                
            }
    if texts_to_be_added is not None:
        for sub_list in texts_to_be_added:
            context[sub_list[0]] = sub_list[1]
    
    return context
