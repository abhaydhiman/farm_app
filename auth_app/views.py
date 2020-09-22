from django.shortcuts import render
from modules.imp_funcs import *



# ***********************************************************************
# import pyrebase
from pyrebase import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
# ***********************************************************************



# *? All the auth_app views are defined below in order of flow

# *------------------------------------------------------------------------------------------------------------------*


def lang_select(request):

    context = {}
    return render(request , 'lang_select.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


def signup_page(request):

    if request.method == 'POST': 

        request.session['language_selected']  = request.POST['language_selected'] 

        language_selected = request.session['language_selected']

        context = context_generator(for_page = 'signup_page' ,language_selected =  language_selected , texts_to_be_added = None)

        return render(request , 'signup.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


def submit_signup_details(request):

    if request.method == 'POST' and ( str(request.POST['Phone_number']) not in db.child('General_User').get().val() ) :

        language_selected                       = request.session['language_selected']

        request.session['phone_number_of_user'] = request.POST['Phone_number']
        request.session['name_of_user']         = request.POST['name']

        

        context = context_generator(for_page = 'submit_signup_details'  , language_selected = language_selected , texts_to_be_added = [['generated_otp' , OTP_generator()]] )

        print(context['generated_otp'])

        msg_sender( given_phone_number = request.POST['Phone_number'] , given_message = str(context['generated_otp']) )

        return render(request , 'signup.html' , context)
    else:
        language_selected       = request.session['language_selected']

        context = context_generator(for_page = 'signup_page' ,language_selected =   language_selected ,
                                    texts_to_be_added = [['warning_msg' ,"Phone Number already registered"]])
        
        return render(request , 'signup.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


def verify_signup_details(request):
    context = {}

    if request.POST['generated_otp'] == request.POST['otp_given_by_user']:

        phone_number_of_user = request.session['phone_number_of_user']
        name_of_user         = request.session['name_of_user']
        language_selected    = request.session['language_selected']

        email = str(phone_number_of_user) + "@farmapp.com"
        password = request.POST['otp_given_by_user']

        user = auth.create_user_with_email_and_password(email , password)

        data = {'Phone Number' : phone_number_of_user ,
                'language'     : language_selected ,
                'name'         : name_of_user , 
        }

        db.child('General_User').child(str(phone_number_of_user)).set(data)



        return render(request , 'user_home.html' , context)
    else:
        language_selected       = request.session['language_selected']

        context = context_generator(for_page = 'submit_signup_details' ,language_selected =   language_selected ,
                                texts_to_be_added =  [['warning_msg' ,"OTP entered is incorrect"] , ['generated_otp' , request.POST['generated_otp']] ])
    
        return render(request , 'signup.html' , context)
            

# *------------------------------------------------------------------------------------------------------------------*


def login_page(request):
    if request.method == 'POST' :
        language_selected  = request.session['language_selected']

        context = context_generator(for_page = 'login_page', language_selected =   language_selected , texts_to_be_added =  None)

        return render(request , 'login_page.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


def check_login_details(request):
    context = {}
    if request.method == 'POST' :

        phone_number  = request.POST['Phone_number']
        email         = str(phone_number) + "@farmapp.com"
        password      = request.POST['password']

        try:

            user = auth.sign_in_with_email_and_password(email , password)

            return render(request , 'user_home.html' , context)

        except:

            language_selected  = request.session['language_selected']

            context = context_generator(for_page = 'check_login_details'  ,language_selected =  language_selected ,
                                        texts_to_be_added = [[' warning_msg' ,"Either phone number or password is incorrect" ]])
            return render(request , 'login_page.html' , context)


## *------------------------------------------------------------------------------------------------------------------*


def user_home(request):
    context = {}
    return render(request , 'user_home.html' , context)


## *------------------------------------------------------------------------------------------------------------------*
