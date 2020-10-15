from django.shortcuts import render , redirect
from modules.diff_langs_texts import *
from firebase_manager_new import *
from django.http import HttpResponse
from pyrebase import pyrebase
from modules.imp_funcs import firebaseConfig
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
import datetime
from django.http import JsonResponse # For AJAX --> JSON response will be returned for all AJAX calls

# Create your views here.


def home_page(request):

    try :
        if request.session['loggedin_user_phone_number'] :
            phone_number_of_user = request.session['loggedin_user_phone_number']
    except:
        return HttpResponse("Hraami manuus , na password na signup sidha home page pe jaana chahte ho , boht tez ho re ho 😂, ha ha ha. jhlla number one")


    dic = {
    'hi' : 'hindi' ,
    'en' : 'English' ,
    'mr' : 'marathi' ,
    'pa' : 'punjabi' ,
    'ta' : 'tamil' ,
    }



    data_of_user = db.child('General_User').child(str(phone_number_of_user)).get().val()

    request.session['phone_number_of_logged_in_user'] = data_of_user['phone_number']

    data_of_user['language_for_filter'] = data_of_user['language']

    data_of_user['language'] = dic[ data_of_user['language'] ]

    data_of_user['dp'] = data_of_user['dp']

    # request.session['language_of_logged_in_user'] = data_of_user['language']

    context = {'image_lis' : ['D' , 'as' , 'b3'] , 'context' : data_of_user}
    return render(request , 'user_home/user_home.html' , context)




def weather(request):

    data_of_user = db.child('General_User').child(str(request.session['phone_number_of_logged_in_user'])).get().val()

    # Getting the city,state and language of user from firebase data
    city = data_of_user['city'] 
    state = data_of_user['state']
    language_of_user = data_of_user['language']

    from modules.imp_funcs import weather_fetcher
    import _datetime as datetime

    # This dict contains all texts of weather.html page
    text_dic = {
    "Weather"       : "Weather",
    "Home"          : "Home",
    "Weather"       : "Weather",
    "Work"          : "Work" ,
    "Blog"          : "Blog",
    "Contact"       : "Contact",
    "Weather"       : "Weather",
    "Max"           : "Max",
    "Min"           : "Min",
    "Visibility"    : "Visibility",
    "Wind"          : "Wind",
    "Humidity"      : "Humidity" ,
    }

    date_data_lis = weather_fetcher( city + ',' + state )

    current_date_data = date_data_lis[0]




    context = { 
                'date_data_lis'     : date_data_lis ,
                'current_date_data' : current_date_data ,
                'city'              : city ,
                'state'             : state ,
                'text_dic'          : text_dic ,
                'language_of_user'  : language_of_user ,
                # 'icons_lis'         : icons_lis ,
            }
    # weather_fetcher(state_name , city_name)
    return render(request , 'user_home/weather.html' , context )


def shop_now(request):
    return redirect('shop:shop_page') 


def profile(request):

    if request.method == 'POST':
        new_dp = request.POST['new_dp']
        USER.update_dp(phone_number = request.session['loggedin_user_phone_number'] ,image =  new_dp)
        return JsonResponse(status=200)
    else:
        profile_data = USER.GetProfilePageData(phone_number = request.session['loggedin_user_phone_number'] )
        print()
        print()
        print()
        print()
        print()
        print(profile_data)
        print()
        print()
        print()
        print()
        print()
        return render(request , 'user_home/profile.html' , profile_data)

def financial(request):
    print()
    print()
    print()
    print("financial PaGe")
    print()
    print()
    print()
    translated_texts = USER.GetTranslatedTexts(phone_number = request.session['loggedin_user_phone_number'] ,  for_page = 'for_financial_page')
    context = {
        # 'ls' : text_lis ,
        'texts' : translated_texts ,
    }
    return render(request , 'user_home/financial.html' , context)

def loan(request):
    translated_texts = USER.GetTranslatedTexts(phone_number = request.session['loggedin_user_phone_number'] ,  for_page = 'for_loan_page')
    context = {
        'texts' : translated_texts ,
        # 'ls'    : text_lis ,
    }
    return render(request , 'user_home/loan.html' , context)

def submit_loan_form(request):
    if request.method == 'POST':
        data = dict(request.POST)
        data = {key:value[0] for key , value in data.items() if key not in ['csrfmiddlewaretoken' , 'confirm1' , 'confirm2']}
        data['date']   = str(datetime.date.today())
        data['time']   = str(datetime.datetime.now().time())
        data['STATUS'] = 'pending'
        USER.submit_loan_form(phone_number = request.session['loggedin_user_phone_number'] , data = data)
        print()
        print()
        print()
        print()
        print()
        print()
        print()

        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print(data)
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        return render(request , 'user_home/financial.html')

def insurance(request):
    translated_texts = USER.GetTranslatedTexts(phone_number = request.session['loggedin_user_phone_number'] ,  for_page = 'for_insurance_page')
    context = {
        'texts' : translated_texts ,
        # 'ls'    : text_lis ,
    }
    return render(request , 'user_home/insurance.html' , context)

def submit_insurance_form(request):
    if request.method == 'POST':
        data = dict(request.POST)
        data = {key:value[0] for key , value in data.items() if key not in ['csrfmiddlewaretoken' , 'confirm1' , 'confirm2']}
        data['date']   = str(datetime.date.today())
        data['time']   = str(datetime.datetime.now().time())
        data['STATUS'] = 'pending'
        USER.submit_insurance_form(phone_number = request.session['loggedin_user_phone_number'] , data = data)
        return render(request , 'user_home/financial.html')