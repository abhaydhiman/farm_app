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
from auth_app import views
import shop as shop

urlpatterns = [
    path(''                      , views.lang_select           , name = 'lang_select_page'),
    path('signup'                , views.signup_page           , name = 'signup_page'),
    path('login_page'            , views.login_page            , name = 'login_page') ,
    path('check_login_details'   , views.check_login_details   , name = 'check_login_details') ,
    path('submit_signup_details' , views.submit_signup_details , name = 'submit_signup_details') ,
    path('verify_signup_details' , views.verify_signup_details , name = 'verify_signup_details') ,
    path('check_password'        , views.check_password        , name = 'check_password_details') ,


    # ? Including the URLS of apps(user_home and shop_home)
    path('user_home/' , include('user_home.urls')) , # for using urls of user_home app [very very important] 
    path('shop_home/' , include('shop.urls')) ,     # for using urls of shop app [very very important]

    # path('shop_home/add_item_to_cart' , shop.views.product_details),

    

]
