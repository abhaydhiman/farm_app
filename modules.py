# Importing All Necessary Libraries for different modules
import random
import math
import requests
import json
import datetime
import calendar
import time
import pyrebase
from firebase import firebase
import os
import cv2
from io import BytesIO
import base64
import numpy as np
from PIL import Image
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from matplotlib import pyplot as plt
from translator import text_translator, english_translator


#__________________________________________________________________________________
# Configuration Key Of firebase
firebaseConfig = {
   
}

# Init of Pyrebase
pirebase = pyrebase.initialize_app(firebaseConfig)
auth = pirebase.auth()

# Init of Firebase
firebase = firebase.FirebaseApplication("https://the-farm-app-4015b.firebaseio.com/", None)


# Loading the Model for disease prediction
json_file = open('model_num.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# Loading the weights
loaded_model.load_weights("model_num.h5")



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
def firebase_user_registerer(phone_number, password, name, lang, state, city, status):

    email = str(phone_number)+"@farmapp.com"
    user = auth.create_user_with_email_and_password(email, password)
    Data = {
        'Phone Number' : phone_number,
        'Name' :  name,
        'Language' : lang,
        'State' : state,
        'City' : city,
        'Status': status,
        'Image': 'Null'
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



#___________________________________________________________________________________________
# This function fetches name from database for registerd user
def firebase_data_fetcher(phone_number):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Farmer:']:
        if data_list['Farmer:'][data]['Phone Number'] == str(phone_number):
            name = data_list['Farmer:'][data]['Name']
            state = data_list['Farmer:'][data]['State']
            city = data_list['Farmer:'][data]['City']
            status = data_list['Farmer:'][data]['Status']
            break
    return name, state, city,status




#___________________________________________________________________________________________
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



#___________________________________________________________________________________________
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



#___________________________________________________________________________________________
# This function sends the the data of Loan form to firebase of that particular user
def loan_data(name,name2 ,dob ,number ,email ,gender ,maritial, income ,address ,loan_type,area ,total_area ,my_loan ,amount ,des,c_record ,c_record2 ,blacklist ,sign ,amount_blacklist ,phone_number, time, date, status):
    loan_type = english_translator(loan_type)
    Data = {
        'Registered Number' : phone_number,
        'First-Name' :  name,
        'Last-Name' : name2,
        'Date-of-Birth' : dob,
        'Phone Number' : number,
        'Email' : email,
        'Gender' : gender,
        'Maritial Status' : maritial,
        'Income' : income,
        'Address' : address,
        'Loan-Type' : loan_type,
        'Area' : area,
        'Total Area' : total_area,
        'Already Have Loan' : my_loan,
        'Amount of Loan' : amount,
        'Loan Description' : des,
        'Criminal Record' : c_record,
        'Criminal Case Pending' : c_record2,
        'Blacklisted' : blacklist,
        'Blacklist Amount' : amount_blacklist,
        'Signed Gurantee' : sign,
        'Time' : time,
        'Date' : date,
        'Status': status
    }

    result = firebase.post('/the-farm-app-4015b/Loan:', Data)



#___________________________________________________________________________________________
# This function gets the current time and date and used for Form and Insurance Data
def get_current_time():
    from datetime import datetime
    from datetime import date
    now = datetime.now() #get a datetime object containing current date and time
    current_time = now.strftime("%H:%M") #created a string representing current time
    t = time.strptime(current_time, "%H:%M")
    timevalue_12hour = time.strftime( "%I:%M %p", t )
    today = date.today()
    return timevalue_12hour, today



#___________________________________________________________________________________________
# This Function Fetches the loan data from firebase as per registered number given
def loan_data_fetcher(phone_number):
    date_ls = []
    time_ls = []
    status_ls = []
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Loan:']:
        if data_list['Loan:'][data]['Registered Number'] == str(phone_number):
            date = data_list['Loan:'][data]['Date']
            time = data_list['Loan:'][data]['Time']
            status = data_list['Loan:'][data]['Status']
            date_ls.append(date)
            time_ls.append(time)
            status_ls.append(status)

    return date_ls, time_ls, status_ls



#___________________________________________________________________________________________
# This Function sends Insurance form data to the firebase as per registered User
def insu_data(name,name2 ,dob ,number ,email ,gender ,maritial, income ,address ,insu_type,area ,total_area,des,c_record ,c_record2 ,blacklist ,sign ,amount_blacklist ,phone_number, time, date, status):
    loan_type = english_translator(insu_type)
    Data = {
        'Registered Number' : phone_number,
        'First-Name' :  name,
        'Last-Name' : name2,
        'Date-of-Birth' : dob,
        'Phone Number' : number,
        'Email' : email,
        'Gender' : gender,
        'Maritial Status' : maritial,
        'Income' : income,
        'Address' : address,
        'Insurance-Type' : loan_type,
        'Area' : area,
        'Total Area' : total_area,
        'Insurance Description' : des,
        'Criminal Record' : c_record,
        'Criminal Case Pending' : c_record2,
        'Blacklisted' : blacklist,
        'Blacklist Amount' : amount_blacklist,
        'Signed Gurantee' : sign,
        'Time' : time,
        'Date' : date,
        'Status': status
    }

    result = firebase.post('/the-farm-app-4015b/Insurance:', Data)



#_____________________________________________________________________________________________
# This function fetches the insurance data from firebase as per given registered Phone number
def insu_data_fetcher(phone_number):
    date_ls = []
    time_ls = []
    status_ls = []
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Insurance:']:
        if data_list['Insurance:'][data]['Registered Number'] == str(phone_number):
            date = data_list['Insurance:'][data]['Date']
            time = data_list['Insurance:'][data]['Time']
            status = data_list['Insurance:'][data]['Status']
            date_ls.append(date)
            time_ls.append(time)
            status_ls.append(status)

    return date_ls, time_ls, status_ls



#_____________________________________________________________________________________________
# This function  updates the status of the user from farmer to farmer+seller
def update_status(phone_number):
    data_list = firebase.get('the-farm-app-4015b/',None)
    status = 'Farmer + Seller'
    for data in data_list['Farmer:']:
        if data_list['Farmer:'][data]['Phone Number'] == str(phone_number):
            firebase.put('the-farm-app-4015b/Farmer:/'+data,'Status',status)
            break
    return status



#_____________________________________________________________________________________________
# This function sends the product data to the firebase
def product_data_sender(phone_number,name,des,price,in_Stock, category, image):
    flag = 0
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Products:']:
        if data_list['Products:'][data]['Registered Number'] == str(phone_number):
            if name == data_list['Products:'][data]['Product Name']:
                flag = 1
                break
    if flag == 0:
        Data = {
        'Registered Number': phone_number,
        'Product Name' : name,
        'Description' : des,
        'Price' : price,
        'In Stock': in_Stock,
        'Category' : category,
        'Buyers':'0',
        'Image':image
        }
        result = firebase.post('/the-farm-app-4015b/Products:', Data)
    return flag



#__________________________________________________________________________________________________________________________
# This function fetches the product data fors eller page for a particular seller, the products he is currently selleing
def product_data_fetcher(phone_number):
    data_list = firebase.get('the-farm-app-4015b/',None)
    pname = []
    pdes = []
    price = []
    stock = []
    cat = []
    image = []
    buyers = []
    for data in data_list['Products:']:
        if data_list['Products:'][data]['Registered Number'] == str(phone_number):
            name = data_list['Products:'][data]['Product Name']
            price1 = data_list['Products:'][data]['Price']
            des = data_list['Products:'][data]['Description']
            stock1 = data_list['Products:'][data]['In Stock']
            cat1 = data_list['Products:'][data]['Category']
            buy = data_list['Products:'][data]['Buyers']
            img = data_list['Products:'][data]['Image']
            pname.append(name)
            pdes.append(des)
            price.append(price1)
            stock.append(stock1)
            cat.append(cat1)
            buyers.append(buy)
            image.append(img)
    return pname,pdes,price,stock,cat,image, buyers




#_____________________________________________________________________________________________
# This function fetches the product data of a particular product for editing
def  product_data_fetcher2(phone_number,name):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Products:']:
        if data_list['Products:'][data]['Registered Number'] == str(phone_number):
            if str(name) == data_list['Products:'][data]['Product Name']:
                price1 = data_list['Products:'][data]['Price']
                des = data_list['Products:'][data]['Description']
                stock1 = data_list['Products:'][data]['In Stock']
                cat1 = data_list['Products:'][data]['Category']
                buy = data_list['Products:'][data]['Buyers']
                img = data_list['Products:'][data]['Image']
                break
    return price1,des,stock1,cat1,buy,img




#_____________________________________________________________________________________________
# This function updates the data for a product if user changes the data
def product_data_updater(phone_number,name,price,category,des,in_Stock,image):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Products:']:
        if data_list['Products:'][data]['Registered Number'] == str(phone_number):
            if str(name) == data_list['Products:'][data]['Product Name']:
                firebase.put('the-farm-app-4015b/Products:/'+data,'Price',price)
                firebase.put('the-farm-app-4015b/Products:/'+data,'Description',des)
                firebase.put('the-farm-app-4015b/Products:/'+data,'In Stock',in_Stock)
                firebase.put('the-farm-app-4015b/Products:/'+data,'Category',category)
                firebase.put('the-farm-app-4015b/Products:/'+data,'Image',image)
                break




#_____________________________________________________________________________________________
# This function removes aparticular product from the firebase
def product_remover(phone_number, name):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Products:']:
        if data_list['Products:'][data]['Registered Number'] == str(phone_number):
            if str(name) == data_list['Products:'][data]['Product Name']:
                firebase.delete('the-farm-app-4015b/Products:/',data)
                break



#_____________________________________________________________________________________________
# This function fetches all the products from firebase
def all_product_fetcher():
    data_list = firebase.get('the-farm-app-4015b/',None)
    pname = []
    pdes = []
    price = []
    stock = []
    cat = []
    image = []
    buyers = []
    for data in data_list['Products:']:
        name = data_list['Products:'][data]['Product Name']
        price1 = data_list['Products:'][data]['Price']
        des = data_list['Products:'][data]['Description']
        stock1 = data_list['Products:'][data]['In Stock']
        cat1 = data_list['Products:'][data]['Category']
        buy = data_list['Products:'][data]['Buyers']
        img = data_list['Products:'][data]['Image']
        pname.append(name)
        pdes.append(des)
        price.append(price1)
        stock.append(stock1)
        cat.append(cat1)
        buyers.append(buy)
        image.append(img)
    unique_cat = set(cat)
    return pname,pdes,price,stock,cat,image, buyers, unique_cat





#_____________________________________________________________________________________________
# This function fetches the data from firebase for the product the user wants to buy
def buy_product_data(pname):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Products:']:
        if str(pname) == data_list['Products:'][data]['Product Name']:
            name = data_list['Products:'][data]['Product Name']
            price1 = data_list['Products:'][data]['Price']
            des = data_list['Products:'][data]['Description']
            stock1 = data_list['Products:'][data]['In Stock']
            cat1 = data_list['Products:'][data]['Category']
            buy = data_list['Products:'][data]['Buyers']
            img = data_list['Products:'][data]['Image']
    return price1,des,stock1,cat1,buy,img




#_____________________________________________________________________________________________
# This function sends the user image to the firebase
def user_image_sender(phone_number,image):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Farmer:']:
        if data_list['Farmer:'][data]['Phone Number'] == str(phone_number):
            firebase.put('the-farm-app-4015b/Farmer:/'+data,'Image',image)
            break



#_____________________________________________________________________________________________
# This function fetches the image of the user
def user_image_fetcher(phone_number):
    data_list = firebase.get('the-farm-app-4015b/',None)
    for data in data_list['Farmer:']:
        if data_list['Farmer:'][data]['Phone Number'] == str(phone_number):
            image = data_list['Farmer:'][data]['Image']
            break

    return image



#_____________________________________________________________________________________________
# To send the data of the product to user cart
def user_cart_data_sender(phone_number, pname, amount):
    data = {
    'Phone Number': phone_number,
    'Product Name': pname,
    'Amount' : amount
    }

    result = firebase.post('/the-farm-app-4015b/Cart:', data)



#_____________________________________________________________________________________________
# To Fetch the user cart data
def user_cart_data_fetcher(phone_number):
    data_list = firebase.get('the-farm-app-4015b/',None)
    pname = []
    amount_lis = []
    for data in data_list['Cart:']:
        if data_list['Cart:'][data]['Phone Number'] == str(phone_number):
            name = data_list['Cart:'][data]['Product Name']
            amount = data_list['Cart:'][data]['Amount']
            pname.append(name)
            amount_lis.append(amount)
    return pname, amount_lis





#_____________________________________________________________________________________________
# This function is used to convert base64 to image.
def image_decoder(image):
    encoded_data = image.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img



#_____________________________________________________________________________________________
# This function is used to classify the disease for a leaf for image uploaded by user
def leaf_disease_predictor(img):
    # Reading the image
    # Converting image to array
    img = cv2.resize(img, (224, 224)).astype(np.float32)
    img = np.expand_dims(img, axis=0)
    # making the prediction
    prediction = loaded_model.predict(img)
    if np.argmax(prediction) == 0:
        result = "Bacterial_spot"
    elif np.argmax(prediction) == 1:
        result = "Early_Blight"
    elif np.argmax(prediction) == 2:
        result = "Late Blight"
    elif np.argmax(prediction) == 3:
        result = "Leaf Mold"
    elif np.argmax(prediction) == 4:
        result = "Septoria Leaf Mold"
    elif np.argmax(prediction) == 5:
        result = "Spider mites"
    elif np.argmax(prediction) == 6:
        result = "Target Spot"
    elif np.argmax(prediction) == 7:
        result = "Yellow Leaf Curl Virus"
    elif np.argmax(prediction) == 8:
        result = "Mosaic Virus"
    else:
        result = "Healthy"
    return result


