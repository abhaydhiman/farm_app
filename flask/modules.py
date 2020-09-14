# Importing All Necessary Libraries
import random
import math
import requests
import json
import datetime
import calendar
import pyrebase
from firebase import firebase
from translator import text_translator


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



# This function fetches name from database for registerd user
def firebase_data_fetcher(phone_number):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Farmer:']:
        if data_list['Farmer:'][data]['Phone Number'] == str(phone_number):
            name = data_list['Farmer:'][data]['Name']
            break
    return name



# This function fetches all the weather information according to the given location
def weather_fetcher(city_name = None, state_name = None, lang = None):
    
    #type your API KEY Here.
    api_key = ""
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"
    #complete_url variable to store the complete_url address
    complete_url= base_url + "appid=" + api_key + "&q=" + city_name + "," + state_name + '&units=metric'
    response = requests.get(complete_url)


    #json method of response object convert json format data into python format data
    x = response.json()

    current_time = datetime.date.today() 
    dt = []
    temp = []
    ma = []
    mi = []
    hum = []
    des = []
    speed = []
    visi = []
    day = []
    code = []
    for val in x['list']:
        if val['dt_txt'][0:10] == str(current_time):
            temp.append(val['main']['temp'])
            dt.append(val['dt_txt'][0:10])
            day.append(calendar.day_name[current_time.weekday()])
            ma.append(val['main']['temp_max'])
            mi.append(val['main']['temp_min'])
            hum.append(val['main']['humidity'])
            des.append(val['weather'][0]['description'])
            speed.append(round((val['wind']['speed'] * 3.6),2))
            visi.append(val['visibility']/1000)
            code.append(val['weather'][0]['id'])
            current_time = current_time + datetime.timedelta(days=1)
    des = text_translator(des, lang)
    day = text_translator(day, lang)
    return dt, temp, ma, mi, hum, des, speed, visi, day, code



# This fuction fetches the current day condition ,i.e., morning, evening or night
def day_fetcher():
    currentTime = datetime.datetime.now()
    currentTime = currentTime.hour
    if currentTime < 12:
        return('mor')
    elif 12 <= currentTime < 18:
        return('aft')
    else:
        return('eve')


