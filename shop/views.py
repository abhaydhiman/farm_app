from django.shortcuts import render
from django.http import JsonResponse # For AJAX --> JSON response will be returned for all AJAX calls



# *********************connecting to firebase realtime database*********************************
from modules.imp_funcs import firebaseConfig
from pyrebase import pyrebase

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
# **********************************************************************************************


# Create your views here.

# *====================================================================================================================================================================*

def shop_now(request):
    product_dic = dict(db.child("Products").get().val()) # Getting all teh products from the database and Converting ordered dict to dict
    # Getting the cart of ( LOGGED IN user ) from firebase  of current user
    cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart']

    # *******************************************
    '''
    with this for loop i am adding a new bool variable to each product based on its presence or
    absence in cart --> for more clarity open 'shop_now.html' and search 'product.inCart'
    '''
    new_prod_lis = []

    for product_id , product in product_dic.items():
        # cart_prod_id = product['product_id']
        if  product_id in cart.keys() and cart[ product_id ] != 0:
            product['inCart'] = True
        else:
            product['inCart'] = False
        new_prod_lis.append(product)
    # *******************************************

    categories = db.child('categories').get().val() # Fetching all unique categories from firebase database
    context  = {'categories' : categories , 
                'products_lis': new_prod_lis , 
    }
    return render(request , 'shop/shop_now.html' , context)


# *====================================================================================================================================================================*

'''
This function is pure AJAX it is called from 'shop_now.html'
For more clarity go to shop_now.html and search "shop:add_to_cart"
'''
def add_to_cart(request):
    if request.is_ajax() and request.method == 'POST':
        product_id = request.POST['id_of_selected_prod']
        # Getting the cart from firebase  of current user
        cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart'] 

        #********************************************************************************************************************
        '''
        FLOW OF BELOW - if - else statement

         If product_id is not in cart , then we add item to cart
         else we will pop/remove the item from cart
        '''
        if product_id not in cart.keys():
            cart[product_id] = 1
            html_code_to_be_send = "<li  id="+ product_id + ' ' +'class="active cart_class"><a><i class="fa fa-shopping-cart"></i></a></li>'
        else:
            cart.pop(product_id)
            html_code_to_be_send = "<li  id="+ product_id + ' ' +'class="cart_class"><a><i class="fa fa-shopping-cart"></i></a></li>'
        #********************************************************************************************************************

        # Updating isEmpty variable of cart in firebaase database
        cart['isEmpty'] = True if len(cart) == 1 else False 

        # Updating the cart in firebase database
        db.child('General_User').child( request.session['loggedin_user_phone_number'] ).child('cart').set(cart)
       
       # This dict will be sended to AJAX functions as success response
        resp_data = {
            'c_html'              : html_code_to_be_send,
            'id_of_selected_prod' : product_id ,
            # more data
        }
        return JsonResponse(resp_data, status=200)


    

# *====================================================================================================================================================================*

'''
This function is called from 'product_details.html'
for more clarity just go product_details.html and search 'shop:product_details


This function works for both ajax and normal django requests --> Its outermost if-else decides wheteher the request is AJAX or not
structure

        if non AJAX request:

            if product selected for overview is already in cart of user then [+ quantity -] will be displayed
            else [Add to Cart] button is shown

        elif AJAX request:
            if    [Add to Cart button] is selected then product is added to user's cart
            elif  [+ quantity -] is selected then based upon (id which is either 'plus' or 'minus') product quantity is changed in user's cart

'''

def product_details(request):
    # Getting the cart from firebase  of current user
    cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart'] 
    cart_prod_id = request.POST['product_id'] #  cart_prodids are in form --> prod1 , prod2 , prod3 etc 

    if request.method == "POST" and not request.is_ajax():
                    if (cart_prod_id in cart.keys()) and  (cart[ cart_prod_id ] != 0) :
                        quantity = cart[ cart_prod_id ]
                        add_to_cart_button = 'inActive'
                    else:
                        quantity = 0
                        add_to_cart_button = 'Active'
                        
                    # Fetching the data of a product based on product_id      
                    product = db.child("Products").child(str(request.POST['product_id'])).get().val()

                    context = {'product' : product , 
                            'add_to_cart_button' : add_to_cart_button ,
                            'quantity' : quantity , 
                            }
                    return render(request , 'shop/product_details.html' , context)
    
    elif request.is_ajax() :
                    cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart'] 
                    if request.POST['AlreadyExistsInCart'] == 'True':
                                    id = request.POST['id'] # Either contains 'plus' and 'minus'
                                    if id == 'plus':
                                        cart[ cart_prod_id ] += 1 

                                    elif id == 'minus':
                                        cart[ cart_prod_id ] = max(0 , cart[ cart_prod_id ] - 1) # This prevents -ve value of quantity
                                        
                                    html_code_to_be_send = "<a id='quantity'>" + str(cart[ cart_prod_id ]) + "</a>"
                    elif request.POST['AlreadyExistsInCart'] == 'False':
                                    cart[ cart_prod_id ] = 1
                                    html_code_to_be_send = "<button id='plus' class='change_quantity btn btn-secondary'>+</button><a id='quantity'> 1 </a><button id='minus' class='change_quantity btn btn-secondary'>-</button>"

                    # Updating the cart in firebase database for AJAX request
                    db.child('General_User').child( request.session['loggedin_user_phone_number'] ).child('cart').set(cart)
                    
                    # This dict will be sended to AJAX functions as success response
                    resp_data = {
                        'c_html': html_code_to_be_send,
                    }
                    return JsonResponse(resp_data, status=200)


# *====================================================================================================================================================================*
'''
This function is used to display all the products of a selected category
'''

def category_preview(request):
    if request.method == 'POST':
        cat_selected = request.POST['cat_selected'] # Recieving the category selected by user
        products = dict(db.child('Products').get().val()) # Fetching all products from firebase database
        selected_cat_prods = [ product for product_id , product in products.items() if product['category'] == cat_selected ] # Filtering the required categorical products
        context = {'selected_prods' : selected_cat_prods}
        return render(request , 'shop/shop_grid.html' , context)
                    
# *====================================================================================================================================================================*


def shop_grid(request):
    context = {}
    return render(request , 'shop/shop_grid.html')


# *====================================================================================================================================================================*
def get_cart_of_user(phone_number):
    cart = db.child('General_User').child(phone_number).get().val()['cart']
    return cart

def cart(request):

    if  not request.is_ajax():
                    phone_number = request.session['loggedin_user_phone_number'] #Getting the phone number of current logged in user
                    cart = get_cart_of_user(phone_number)
                    
                    # Here in cart we have product_id and its quantity , but we want each product details so we will fetch each data of each product in cart and appends it to our new dictationary

                    Products = []
                    
                    for item_id , quantity in cart.items() :
                        if item_id != 'isEmpty':
                            product_data_dic = dict(db.child('Products').child(item_id).get().val())

                        
                            product_data_dic['quantity']    = quantity

                            # Next line is to get total price of one product by formula = ( quantity of a product) X (price of that product)
                            product_data_dic['total_price'] = quantity * product_data_dic['price'] 
                            Products.append(product_data_dic)

                    # Getting the total bill 
                    total_bill = 0
                    for product in Products:
                        total_bill += product['total_price']

                    context = {
                        'Products' : Products ,
                        'total_bill' : total_bill ,
                    }
                    return render(request , 'shop/cart.html' , context)

    elif request.is_ajax():
                    print()
                    print()
                    print()
                    print(request.POST)
                    print()
                    print()
                    print()

                    # Getting the values sended through ajax request
                    product_id   = request.POST['product_id']
                    new_quantity = request.POST['new_quantity']

                    phone_number = request.session['loggedin_user_phone_number'] #Getting the phone number of current logged in user
                    cart = get_cart_of_user(phone_number)
                    cart[product_id] = int(new_quantity) # Updating the quanttiy of a item

                    # Getting the updated bill
                    new_total_bill = 0
                    for item_id , quantity in cart.items():
                        if item_id != 'isEmpty':
                            product_data_dic = dict(db.child('Products').child(item_id).get().val())
                            new_total_bill += product_data_dic['price']*quantity

                    resp_data = {
                        'product_id':product_id ,
                        'new_price' :int(new_quantity) * dict(db.child('Products').child(product_id).get().val())['price'],
                        'new_total_bill' : new_total_bill ,
                        }                    
                    # Updating the cart in firebase database for AJAX request
                    db.child('General_User').child( request.session['loggedin_user_phone_number'] ).child('cart').set(cart)
                    return JsonResponse(resp_data, status=200)
                    
               

# *====================================================================================================================================================================*

# ? Bakwaas h ye dono htaunga isse baad me 😂
def show_cart_items(request):
     if request.is_ajax() and request.method == 'POST':

        # Getting the cart from firebase  of current user
        cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart']

        texts = []

        for item in cart.keys():
            texts.append("<h5>" + cart[item] + "</h5>")


        resp_data = {'cart_items_texts' : texts}
        return JsonResponse(resp_data , status=200)
def testing(request):
    return render(request , "shop/shoping_cart.html")

         
# *====================================================================================================================================================================*
