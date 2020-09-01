# Importing All Necessary Libraries
import random
import math
import requests
import pyrebase
from firebase import firebase


#__________________________________________________________________________________
# Configuration Key Of firebase
firebaseConfig = {

}

# Init of Pyrebase
pirebase = pyrebase.initialize_app(firebaseConfig)
auth = pirebase.auth()

# Init of Firebase
firebase = firebase.FirebaseApplication("https://the-farm-app-4015b.firebaseio.com/", None)


#___________________________________________________________________________________________
# Function For Generating OTP. It returns a OTP Of length 6
def opt_generator():

    # for nuemeric OTP 
    corpus= "0123456789"
    generate_OTP = "" 

    size = 6 # length of generated OTP

    length = len(corpus) 

    for i in range(size) : 
        generate_OTP += corpus[math.floor(random.random() * length)] 

    return generate_OTP


#___________________________________________________________________________________________
# Function For Sending OTP To the Given Number.
def msg_sender( given_phone_number = None , given_message = None ):

    url = "https://www.fast2sms.com/dev/bulk"

    #______________________________________________
    # Message will be send to given number
    phone_number = given_phone_number

    # Message text
    message = given_message
    #______________________________________________

    payload = "sender_id=FSTSMS&message=" + message + "&language=english&route=p&numbers=" + str(phone_number)
    headers = {
    'authorization': "",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url , data = payload, headers = headers)


#___________________________________________________________________________________________
# Function for authenticating user in firebase if already registered or not
def firebase_user_checker(phone_number):

    # Check if user is Already Registered Or Not
    data_list = firebase.get('the-farm-app-4015b/',None)
    flag = 0
    for data in data_list['Farmer:']:
        if data_list['Farmer:'][data]['Phone Number'] == str(phone_number):
            flag = 1
    return flag


#___________________________________________________________________________________________
# Function For registering New user To Firebase and Adding His Data To Realtime Database
def firebase_user_registerer(phone_number, password, name, lang):

    email = str(phone_number)+"@farmapp.com"
    user = auth.create_user_with_email_and_password(email, password)
    Data = {
        'Phone Number' : phone_number,
        'Name' :  name,
        'Language' : lang
    }

    result = firebase.post('/the-farm-app-4015b/Farmer:', Data)


#___________________________________________________________________________________________
# Function for Login User, check if Credentials were correct or not
def firebase_user_loger(phone_number, password):
    email = str(phone_number)+"@farmapp.com"
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        return 1
    except:
        return 0
