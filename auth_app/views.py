from django.shortcuts import render , redirect
from firebase_manager_new import USER

# from modules.imp_funcs import *

# ***********************************************************************


'''
All the given function are imported from { modules/imp_func.py }
'''
# from modules.imp_funcs  import  translator       # Translator translates the context texts
from modules.imp_funcs  import  OTP_generator     # This function is used to generate OTP
from modules.imp_funcs  import  msg_sender        # This function is used to send OTP for signup 
from modules.imp_funcs  import  context_generator # All functions of auth_app uses this function to generate context


# ***********************************************************************


'''
NOTE -> Importing firebaseConfig dictationary from { modules/imp_func.py }
'''
from modules.imp_funcs import firebaseConfig
from pyrebase import pyrebase

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


# ***********************************************************************








# *?-----------------------------------FLOW OF VIEW FUNCTIONS--start------------------------------|
'''
NOTE -> All the functions that are mentioned below are defined in in order of flow


# * lang_select --->  shifts control to {signup_page}

# * signup_page --->  it has two buttons , **Only allows unregistered numbers for signup**
                                        >> 1 Generate OTP button for [signup]             --> shifts control to {submit_signup_details}
                                        >> 2 Already a user , Log in button for [login]   --> shifts control to {Login_page}

# * submit_signup_details  

# * verify_signup_details

# * login_page

# * check_login_details

# * user_home


'''
# *?-----------------------------------FLOW OF VIEW FUNCTIONS--end------------------------------|




# *? All the auth_app views are defined below in order of flow

# *------------------------------------------------------------------------------------------------------------------*


def lang_select(request):
    # request.session.flush()
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key] # Deleting all previous session variables

    context = {}
    return render(request , 'auth_app/lang_select.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


def signup_page(request):

    if request.method == 'POST': 

        request.session['language_selected']  = request.POST['language_selected'] 

        language_selected = request.session['language_selected']

        context = context_generator(for_page = 'signup_page' ,
                                    language_selected =  language_selected ,
                                    texts_to_be_added = None)

        return render(request , 'auth_app/signup.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


# **USE OF IF-ELSE here --> Here user is allowed to generate an OTP if its number is not registered in our firebase** else user recieves an error message

def submit_signup_details(request):
    if request.method == 'POST' and not USER.isRegistered(phone_number = request.POST['Phone_number']) :
        phone_number                            = request.POST['Phone_number']
        language_selected                       = request.session['language_selected']
        request.session['phone_number_of_user'] = request.POST['Phone_number']
        request.session['name_of_user']         = request.POST['name']
        request.session['STATUS']               = request.POST['status']

        context = context_generator(for_page = 'submit_signup_details'  , 
                                    language_selected = language_selected , 
                                    texts_to_be_added = [['generated_otp' , OTP_generator()]] )

        # msg_sender( given_phone_number = request.POST['Phone_number'] , given_message = str(context['generated_otp']) )

        return render(request , 'auth_app/signup.html' , context)
    else:
        language_selected       = request.session['language_selected']
        context = context_generator(for_page = 'signup_page' ,
                                    language_selected =   language_selected ,
                                    texts_to_be_added = [['warning_msg' ,"Phone Number already registered"]])
        
        return render(request , 'auth_app/signup.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


# **USE OF IF-ELSE here --> Here user is only registered in our firebase if OTP  by user is correct**

def verify_signup_details(request):
    context = {}

    if request.POST['generated_otp'] == request.POST['otp_given_by_user']:
        phone_number_of_user = request.session['phone_number_of_user']
        name_of_user         = request.session['name_of_user']
        language_selected    = request.session['language_selected']

        context = context_generator(for_page = 'set_password' ,
                                    language_selected = language_selected)
        return render(request , 'auth_app/set_password.html' , context)

    else:
        language_selected       = request.session['language_selected']
        context = context_generator(for_page = 'submit_signup_details' ,
                                    language_selected =   language_selected ,
                                    texts_to_be_added =  [['warning_msg' ,"OTP entered is incorrect"] , 
                                    ['generated_otp' , request.POST['generated_otp']] ])
        return render(request , 'auth_app/signup.html' , context)


# *------------------------------------------------------------------------------------------------------------------*
# Firebase me password 6 digit ka hona hi chahiye
# ?dono password equal na ho to error msg else statement me 
def check_password(request):

    phone_number_of_user = request.session['phone_number_of_user']
    name_of_user         = request.session['name_of_user']
    language_selected    = request.session['language_selected']

    if request.POST['password_1'] == request.POST['password_2'] :
        email = str(phone_number_of_user) + "@farmapp.com"
        user = auth.create_user_with_email_and_password(email , request.POST['password_1'])
        data = {'phone_number' : phone_number_of_user ,
                'language'     : language_selected ,
                'name'         : name_of_user , 
                'state'        : request.POST['state'] , 
                'city'         : request.POST['city'] , 
                'cart'         : {'isEmpty' : True } , 
                'status'       : request.session['STATUS'],
        }

        # STATUS includes seller than it has a special cart named as SellerCart
        if "Seller" in  request.session['STATUS']:
            data['SellerCart'] = {'isEmpty':True}



        USER.SetUserData(phone_number = phone_number_of_user , data = data)
        context = {}
        request.session['loggedin_user_phone_number'] = phone_number_of_user
        return redirect('user_home:home_page')
    else:
        phone_number_of_user = request.session['phone_number_of_user']
        name_of_user         = request.session['name_of_user']
        language_selected    = request.session['language_selected']
        context = context_generator(for_page = 'set_password' ,
                                    language_selected = language_selected ,
                                    texts_to_be_added = [['warning_msg' ,"Entered passwords doesn't match!!" ]])
        return render(request , 'auth_app/set_password.html' , context)
    

# *------------------------------------------------------------------------------------------------------------------*


def login_page(request):
    if request.method == 'POST' :
        language_selected  = request.session['language_selected']
        context = context_generator(for_page = 'login_page', 
                                    language_selected =   language_selected ,
                                    texts_to_be_added =  None)
        return render(request , 'auth_app/login_page.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


# **USE OF TRY-EXCEPT here --> If user enters correct phone number and password , then he is allowed to login**

def check_login_details(request):
    if request.method == 'POST' :
        context = {}
        phone_number  = request.POST['Phone_number']
        email         = str(phone_number) + "@farmapp.com"
        password      = request.POST['password']

        try:
            user = auth.sign_in_with_email_and_password(email , password)
            request.session['loggedin_user_phone_number'] = phone_number
            return redirect('user_home:home_page')

        except:
            language_selected  = request.session['language_selected']
            context = context_generator(for_page = 'check_login_details'  ,
                                        language_selected =  language_selected ,
                                        texts_to_be_added = [[' warning_msg' ,"Either phone number or password is incorrect" ]])
            return render(request , 'auth_app/login_page.html' , context)


# *------------------------------------------------------------------------------------------------------------------*


# def user_home(request):
#     return redirect('user_home:home_page') # for redirecting to urls of user_home app of this project
    
    
# # *------------------------------------------------------------------------------------------------------------------*


# def weather(request):
    context = {}
    return render(request , 'auth_app/weather.html' , context)