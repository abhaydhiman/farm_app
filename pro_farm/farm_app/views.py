# from django.shortcuts import render

# # Create your views here.

# def home_page(request):
#     context = {}
#     return render(request , 'home.html' , context)


from django.shortcuts import render
from modules.imp_funcs import *

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
        }

        return render(request , 'signup.html' , context)

#____________________________________________________________________________________________


def submit_signup_data(request):
    phone_number = request.POST['Phone_number']
    name         = request.POST['name']
    context = {
        'Enter_OTP' : translator('Enter OTP' , to_langg = 'English'),
        'Confirm'   : translator('Confirm'   , to_langg = 'English')
        }
    return render(request , 'confirm_OTP.html' , context)

    
#____________________________________________________________________________________________


def user_home(request):
    context = {}
    return render(request , 'user_home.html' , context)

#____________________________________________________________________________________________
