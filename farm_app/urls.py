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
from django.urls import path
from farm_app import views

urlpatterns = [
    # path('', views.home_page , name = 'home_page'),

    path('' , views.lang_select , name = 'lang_select'),

    path('signup' , views.signup_page , name = 'signup_page'),

    path('submit_signup_data' , views.submit_signup_data , name = 'submit_signup_data_page'),

    path('user_home' , views.user_home , name = 'user_home_page'),
]
