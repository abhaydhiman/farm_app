"""pro_farm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path , include
from user_home import views

app_name = 'user_home'

urlpatterns = [
    path('' , views.home_page , name = 'home_page') ,
    path('weather' , views.weather , name = 'weather') ,
    path('shop_now' , views.shop_now , name = 'shop_now') ,
    path('financial' , views.financial , name = 'financial'),
    path('profile' , views.profile , name = 'profile') ,
    path('change_dp' , views.profile , name = 'change_dp'),
    path('loan' , views.loan , name = 'loan'),
    path('submit_loan_form' , views.submit_loan_form , name = 'submit_loan_form'),
    path('insurance' , views.insurance , name = 'insurance'),
    path('submit_insurance_form' , views.submit_insurance_form , name = 'submit_insurance_form'),
]
