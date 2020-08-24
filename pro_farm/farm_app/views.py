# from django.shortcuts import render

# # Create your views here.

# def home_page(request):
#     context = {}
#     return render(request , 'home.html' , context)


from django.shortcuts import render
from modules.imp_funcs import *

# Create your views here.

def home_page(request):
    context = {
        'var_1' : translator("Hello") ,
        'var_2' : OTP_generator()
        }
    return render(request , 'home.html' , context)