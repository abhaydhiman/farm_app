# from django.shortcuts import render

# # Create your views here.

# def home_page(request):
#     context = {}
#     return render(request , 'home.html' , context)


from django.shortcuts import render
from modules.imp_funcs import *
from firebase import firebase

#____________________________________________________________________________________________


def lang_select(request):
    context = {}
    return render(request , 'lang_select.html' , context)
    
#____________________________________________________________________________________________


def signup_page(request):

    if request.method == 'POST': 
        language_selected  = request.POST['language_selected'] 
        context = {
             'Enter_Credentials' : translator('Enter Credentials' , to_langg = language_selected) , 
             'Phone_Number'      : translator('Phone Number' , to_langg = language_selected) , 
             'Full_Name'         : translator('Full Name' , to_langg = language_selected) , 
             'Generate_OTP'      : translator('Generate OTP' , to_langg = language_selected) , 
             'language_selected' : language_selected , 
        }

        return render(request , 'signup.html' , context)

#____________________________________________________________________________________________


def submit_signup_data(request):
    phone_number = request.POST['Phone_number']
    name         = request.POST['name']
    Language     = request.POST["sign-in-button"]

    context = {
        'Enter_OTP' : translator('Enter OTP' , to_langg = 'English'),
        'Confirm'   : translator('Confirm'   , to_langg = 'English')
        }

    if request.POST['verify-code-button'] == "True":
        firebase = firebase.FirebaseApplication("https://python-project-f6272.firebaseio.com/", None)
        Data = {
            'Name' : name,
            'Phone_Number' :  phone_number,
            'Language' : Language
        }

        result = firebase.post('/python-project-f6272/User:', Data)
        print(result)

    return render(request , 'signup.html' , context)

    
#____________________________________________________________________________________________


def user_home(request):
    context = {}
    return render(request , 'user_home.html' , context)

#____________________________________________________________________________________________
