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
from shop import views

app_name = 'shop'

urlpatterns = [
    
    path('' , views.shop_now , name = 'shop_now') , # Temporarily addded only for testing
    

    path('shop_now'         , views.shop_now         , name = 'shop_now') , 
    path('shop_grid'        , views.shop_grid        , name = 'shop_grid') , 
    path('product_details'  , views.product_details  , name = 'product_details') , # This url is used with AJAX and normal django requests
    path('category_preview' , views.category_preview , name = 'category_preview') , 
    


    # ================================AJAX URLS=====================================

    path('add_to_cart'      , views.add_to_cart     , name = 'add_to_cart' ) ,
    path('show_cart_items'  , views.show_cart_items , name = 'show_cart_items' ) ,
    path('add_item_to_cart' , views.product_details , name = 'add_item_to_cart') ,


    #-----testing url
    path('testing' , views.testing , name = 'testing')
]
