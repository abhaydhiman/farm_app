from googletrans import Translator
import math, random 



# ***********************************************************************
'''
In this section firebase configuration is given in a dictationary
This helps us to connect firebase server 
'''
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

 


# *------------------------------------------------------------------------------------------------------------------*

'''
This function translates english to any other language using google translate api
'''
def translator(text , to_langg = 'hi'): 
    if to_langg.lower() != 'en':
        translator = Translator() 
        return translator.translate(text ,  src = 'en', dest = to_langg).text
    else:
        return text


# *------------------------------------------------------------------------------------------------------------------*

'''
OTP generator function returns a 6 digit OTP
This is useful during registering a new phone number and authenticating it
'''

def OTP_generator():
    # for nuemeric OTP 
    corpus= "0123456789"
    generate_OTP = "" 
    size = 6 # length of generated OTP
    length = len(corpus) 
    for i in range(size) : 
        generate_OTP += corpus[math.floor(random.random() * length)] 
    print("OOOOO" , generate_OTP)
    return int(generate_OTP)



# *------------------------------------------------------------------------------------------------------------------*


'''
This function is used to send OTP message for phone number confirmation during signup
[means for registering a new phone number]
'''
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
    'authorization': "G17OkTawBjvLS1opDfJKehQTZKeFguqGIc7cjvs277esW2QeakbpH0pZR7UN",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url , data = payload, headers = headers)

    print(response.text)


# *------------------------------------------------------------------------------------------------------------------*


'''
This particular function is used to generate context for different pages

    1 if-elif-else  ladder  used to select desired page context

        >>'signup_page'
        >>'submit_signup_details'
        >>'login_page'
        >>'check_login_details'



    NOTE -> Speciality of this particular function is that it has a option parameter 'texts_to_be_added' w
            which can be used to add values to desired value to context
            [ I had used it for adding warnings -> like phone_number already registered etc]
    

    2 if statment is used to add warning messages
'''

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

    elif for_page == 'set_password':
        context = {
                    'Enter_Password'     : translator('Enter Password' , to_langg = language_selected) , 
                    'password'           : translator('password' , to_langg = language_selected) , 
                    'confirm_password'   : translator('Confirm Password' , to_langg = language_selected) , 
                    'Set_Password'       : translator('Set Password' , to_langg = language_selected) , 
        }
                
            
    if texts_to_be_added is not None:
        for sub_list in texts_to_be_added:
            if sub_list[0] != 'generated_otp':
                context[sub_list[0]] = translator( sub_list[1] , to_langg = language_selected )
            else:
                context[sub_list[0]] = sub_list[1]
    
    return context


# *------------------------------------------------------------------------------------------------------------------*
''' 
This particular function is used to fetch weather forecast for a given distt + state
'''
def weather_fetcher(distt_and_state = None):
    import requests,json
    import _datetime as datetime
    from statistics import mode
    from statistics import mean
    from collections import OrderedDict 


    #type your API KEY Here.
    api_key = "a0b9cc010f855a1e70a2b59ea96b931f"
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"
    # https://samples.openweathermap.org/data/2.5/forecast/daily?id=524901&appid=b1b15e88fa797225412429c1c50c122a1
    #complete_url variable to store the complete_url address
    complete_url= base_url + "appid=" + api_key + "&q=" + distt_and_state + '&units=metric'

    #get methods of requests module retruns respons object
    response = requests.get(complete_url)


    #json method of response object convert json format data into python format data
    x = response.json()


    # *=====================================================================================================================* #
    # main_lis will be returned by this function --> 
    main_lis = []
    current_date = datetime.date.today()

    lis_of_dates = []
    for val in x['list']:
        lis_of_dates.append(val['dt_txt'][:10:])

    # Getting unique values with order maintained
    unique_lis_of_dates = list(OrderedDict.fromkeys(lis_of_dates))
    # *=====================================================================================================================* #

    for current_date in unique_lis_of_dates:
        dic = {}
        dic['temp']         = []
        dic['temp_min']     = []
        dic['temp_max']     = []
        dic['humidity']     = []
        dic['weather_desc'] = []
        dic['wind_speed']   = []
        dic['visibility']   = []
        dic['id']           = []

        for val in x['list']:

            if str(current_date) == val['dt_txt'][:10:] :

                dic['temp'].append(val['main']['temp'])
                dic['temp_min'].append(val['main']['temp_min'])
                dic['temp_max'].append(val['main']['temp_max'])
                dic['humidity'].append(val['main']['humidity'])
                dic['weather_desc'].append(val['weather'][0]['description'])
                dic['wind_speed'].append(val['wind']['speed'] * 3.6)
                dic['visibility'].append(val['visibility'] / 1000)
                dic['id'].append(val['weather'][0]['id'])


        dic['temp']         = int( mean(dic['temp']) )          # Taking mean temperature for a particular dau
        dic['temp_min']     = int( min(dic['temp_min']) )       # Taking minimum temperature for a particualar day
        dic['temp_max']     = int( max(dic['temp_max']) )       # Taking maximum temperature for a particualar day
        dic['humidity']     = int( mean(dic['humidity']) )      # Takin mean humidity for a particular day
        
        try :
            dic['weather_desc'] = mode(dic['weather_desc'])[0]  # Taking mode of weathe_disc list as the final weather description for that particular day
        except : 
            dic['weather_desc'] = [dic['weather_desc'][0]]

        dic['wind_speed']   = int( mean(dic['wind_speed']) )    # Taking mean wind speed as final speed for that particular day
        dic['visibility']   = int( mean(dic['visibility']) )    # Taking mean  visibility as final visibility for that particular day
        dic['day_of_week']  = datetime.datetime.strptime(current_date, "%Y-%m-%d" ).strftime("%A") # Finding out the day of weak from date object
        dic['date']         = str( current_date )[ 8 : 10 : ] + '/' + str( current_date )[ 5 : 7 : ] + '/' + str( current_date )[ 0 : 4 : ] # Just changing the format of date from yyyy-mm-dd to dd/mm/yyyy 😂

        main_lis.append(dic) # Adding data to main_lis which will be finally returned
        


        # **========================Icon + BG img Decider -> START==========================**
        dic['id'] = mode(dic['id'])

        # ? 200 - 232 -> thunderstorm
        # ? 300 - 321 -> drizzle
        # ? 500 - 531 -> heavy rain
        # ? 600 - 622 -> snow
        # ? 800       -> clear
        # ? 801 - 804 -> clouds
        # If day_time is True then it's day time and if it is False then it is night time
        if datetime.datetime.now().hour in range(5 , 19): # 
            day_time = True
        else:
            day_time = False

        
        if   dic['id'] in range(200 , 233):
            dic['icon']   = 'fas fa-bolt'
            dic['bg_img'] = 'thunderstorm.jpg'

        elif dic['id'] in range(300 , 322):
            dic['icon']   = 'fas fa-cloud-sun-rain' if day_time else 'fas fa-cloud-moon-rain'
            dic['bg_img'] = 'cloudy_day.jpg' if day_time else 'cloudy_night.jpg'

        elif dic['id'] in range(500 , 532):
            dic['icon']   = 'fas fa-cloud-rain'
            dic['bg_img'] = 'cloudy_rainy.jpg'
        
        elif dic['id'] in range(600 , 622):
            dic['icon']   = 'fa fa-snowflake-o'
            dic['bg_img'] = 'snowy.jpg'

        elif dic['id'] == 800:
            dic['icon']   = 'fa fa-sun-o' if day_time else 'fa fa-moon-o'
            dic['bg_img'] = 'clear_image.png' if day_time else 'night_image4.jpg'

        elif dic['id'] in range(801 , 805):
            dic['icon']   = 'fas fa-cloud-sun' if day_time else 'fas fa-cloud-moon'
            dic['bg_img'] = 'sunny_cloudy.jpg' if day_time else 'night_cloudy.jpg'


                
    
    # **========================Icon + BG img Decider -> END==========================**

    return main_lis


    



 