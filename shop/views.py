from django.shortcuts import render
from django.http import JsonResponse # For AJAX --> JSON response will be returned for all AJAX calls
from firebase_manager_new import USER , SHOP


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
    # product_dic = dict(db.child("Products").get().val()) # Getting all teh products from the database and Converting ordered dict to dict
    # Getting the cart of ( LOGGED IN user ) from firebase  of current user
    # cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart']

    # *******************************************
    '''
    with this for loop i am adding a new bool variable to each product based on its presence or
    absence in cart --> for more clarity open 'shop_now.html' and search 'product.inCart'
    '''
    # new_prod_lis = []

    # for product_id , product in product_dic.items():
    #     # cart_prod_id = product['product_id']
    #     if  product_id in cart.keys() and cart[ product_id ] != 0:
    #         product['inCart'] = True
    #     else:
    #         product['inCart'] = False
    #     new_prod_lis.append(product)
    # *******************************************
    products_lis = SHOP.GetAllProducts().values()
    # categories = db.child('categories').get().val() # Fetching all unique categories from firebase database
    context  = {'categories' : SHOP.GetListOfCategories() ,
                'products_lis': products_lis ,
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



# def product_details(request):

#     '''
#     This function is called from 'product_details.html'
#     for more clarity just go product_details.html and search 'shop:product_details


#     This function works for both ajax and normal django requests --> Its outermost if-else decides wheteher the request is AJAX or not
#     structure

#             if non AJAX request:

#                 if product selected for overview is already in cart of user then [+ quantity -] will be displayed
#                 else [Add to Cart] button is shown

#             elif AJAX request:
#                 if    [Add to Cart button] is selected then product is added to user's cart
#                 elif  [+ quantity -] is selected then based upon (id which is either 'plus' or 'minus') product quantity is changed in user's cart

#     '''

    # # Getting the cart from firebase  of current user
    # cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart'] 
    # cart_prod_id = request.POST['product_id'] #  cart_prodids are in form --> prod1 , prod2 , prod3 etc 

    # if  not request.is_ajax():
    #                 if (cart_prod_id in cart.keys()) and  (cart[ cart_prod_id ] != 0) :
    #                     quantity = cart[ cart_prod_id ]
    #                     add_to_cart_button = 'inActive'
    #                 else:
    #                     quantity = 0
    #                     add_to_cart_button = 'Active'
                        
    #                 # Fetching the data of a product based on product_id      
    #                 product = db.child("Products").child(str(request.POST['product_id'])).get().val()
    #                 product['quantity'] = quantity

    #                 context = {'product' : product , 
    #                         'add_to_cart_button' : add_to_cart_button ,
    #                         # 'quantity' : quantity , 
    #                         }
    #                 return render(request , 'shop/product_details.html' , context)
    
    # elif request.is_ajax() :
#                     cart = db.child('General_User').child( request.session['loggedin_user_phone_number'] ).get().val()['cart'] 
#                     if request.POST['AlreadyExistsInCart'] == 'True':
#                                     id = request.POST['id'] # Either contains 'plus' and 'minus'
#                                     if id == 'plus':
#                                         cart[ cart_prod_id ] += 1 

#                                     elif id == 'minus':
#                                         cart[ cart_prod_id ] = max(0 , cart[ cart_prod_id ] - 1) # This prevents -ve value of quantity
                                        
#                                     html_code_to_be_send = "<a id='quantity'>" + str(cart[ cart_prod_id ]) + "</a>"
#                     elif request.POST['AlreadyExistsInCart'] == 'False':
#                                     cart[ cart_prod_id ] = 1
#                                     html_code_to_be_send = "<button id='plus' class='change_quantity btn btn-secondary'>+</button><a id='quantity'> 1 </a><button id='minus' class='change_quantity btn btn-secondary'>-</button>"

#                     # Updating the cart in firebase database for AJAX request
#                     db.child('General_User').child( request.session['loggedin_user_phone_number'] ).child('cart').set(cart)
                    
#                     # This dict will be sended to AJAX functions as success response
#                     resp_data = {
#                         'c_html': html_code_to_be_send,
#                     }
#                     return JsonResponse(resp_data, status=200)

def product_details(request):
 
    # Getting the cart from firebase  of current user
    phone_number = request.session['loggedin_user_phone_number']
    cart = SHOP.GetUserCart(phone_number = phone_number)
    cart_prod_id = request.POST['product_id'] #  cart_prodids are in form --> prod1 , prod2 , prod3 etc 

    if  not request.is_ajax():
                        if (cart_prod_id in cart.keys()) and  (cart[ cart_prod_id ] != 0) :
                            quantity = cart[ cart_prod_id ]
                            add_to_cart_button = 'inActive'
                        else:
                            quantity = 0
                            add_to_cart_button = 'Active'
                            
                        # Fetching the data of a product based on product_id      
                        product = SHOP.GetProductById(product_id = cart_prod_id)
                        product['quantity'] = quantity

                        context = {'product' : product , 
                                'add_to_cart_button' : add_to_cart_button ,
                                # 'quantity' : quantity , 
                                }
                        return render(request , 'shop/product_details.html' , context)
                        
    elif request.is_ajax():
                        # Getting the values sended through ajax request
                        product_id   = request.POST['product_id']
                        new_quantity = int(request.POST['new_quantity'])

                        cart[product_id] = int(new_quantity)                           # Updating the quanttiy of a item
                        SHOP.UpdateUserCart(phone_number = phone_number , cart = cart) # Updating the cart in firebase database for AJAX request

                        resp_data = {}
                        return JsonResponse(resp_data, status=200)



# *====================================================================================================================================================================*
'''
This function is used to display all the products of a selected category
'''

def category_preview(request):
    if request.method == 'POST':
        cat_selected = request.POST['cat_selected'] # Recieving the category selected by user
        selected_cat_prods = SHOP.FilterProductsByCategory(cat_req = cat_selected) # Filtering the required categorical products
        context = {'selected_prods' : selected_cat_prods}
        print(context['selected_prods'])
        return render(request , 'shop/shop_grid.html' , context)

# *====================================================================================================================================================================*


def shop_grid(request):
    context = {}
    return render(request , 'shop/shop_grid.html')


# *====================================================================================================================================================================*

def cart(request):
    """
    >>> This particular function runs for (shop/cart.html) template
    >>> if request is not ajax then we fetch complete data of all products present in user's cart using SHOP.GetUserProductCompleteData()`
    >>> if request is ajax then we have to change quantity of a product of user's cart also we have to update 'new_price'(changed by changing quantity) and 'new_total_bill
    """ 
    phone_number = request.session['loggedin_user_phone_number'] #Getting the phone number of current logged in user

    if  not request.is_ajax():
                    cart = SHOP.GetUserCart(phone_number = phone_number)
                    total_bill , Products_list = SHOP.GetUserCartProductsCompleteData(phone_number = phone_number)
                    context = {
                        'total_bill' : total_bill ,
                        'Products' : Products_list ,
                    }
                    return render(request , 'shop/cart.html' , context)

    elif request.method == 'POST' and request.is_ajax():
                    # Getting the values sended through ajax request
                    product_id   = request.POST['product_id']
                    new_quantity = request.POST['new_quantity']

                    # Updating the User Cart
                    cart = SHOP.GetUserCart(phone_number)
                    cart[product_id] = int(new_quantity)                           # Updating the quanttiy of a item
                    SHOP.UpdateUserCart(phone_number = phone_number , cart = cart) # Updating the cart in firebase database for AJAX request

                    # Getting the updated bill
                    new_total_bill = SHOP.GetTotalBillOfUser(phone_number = phone_number)
                    resp_data = {
                        'product_id'     : product_id ,
                        'new_price'      : int(new_quantity) * SHOP.GetProductById(product_id = product_id)['price'],
                        'new_total_bill' : new_total_bill ,
                        }                    
                    return JsonResponse(resp_data, status=200)
                    













# *====================================================================================================================================================================*

def sell_something(request):
    """
    >>> This particualar function runs for (shop/seller.html) template
    >>> if request is not AJAX then we fetch all the products which are from SellerCart and display them
    >>> if requst is AJAX [menas seller added a new product]
                        >Firslty we fetch newly added product data and add 'buyers' and 'ratings' initially to 0
                        >Then we call SHOP.SellerAddsNewProduct() to add product data to Products and also to SellerCart[note SellerCart only stores little info about product]
                        >After that we prepare new_html_str  =  (row element + one empty hidden) , this new_html_str replaces the hidden element 
    """
    phone_number = request.session['loggedin_user_phone_number']
    if not request.is_ajax():
        SellerCartProdsLis = SHOP.GetSellerCartProductsDetails(phone_number = phone_number)
        context = {
            'Products' : SellerCartProdsLis ,
        }
        return render(request , 'shop/seller.html', context)
    elif request.is_ajax() and request.method == 'POST':

        data = dict() # Fetching the data sended through ajax request
        data['product_name'] = request.POST['product_name']
        data['price'] = int(request.POST['price'])
        data['stock'] = request.POST['stock']
        data['category'] = request.POST['category']
        data['desc'] = request.POST['desc']

        try:
            data['image'] = request.POST['image']
        except:
            data['image'] = "https://ohram.org/image/utilities/empty_product.svg"

        
        # *Adding rating and buyers initially 0 for newly added product
        data['buyers'] = 0
        data['rating'] = 0


        new_prod_id , image_URL = SHOP.SellerAddsNewProduct(phone_number = phone_number , prod_data = data) # Getting product_id for newly added product

        data['product_id'] = new_prod_id
        data['image']      = image_URL
        
        # new_html_str replace an hiddend element and also add it so that more and more products can be furter added
        # new_html_str = '<tbody><tr onclick="show_hide_row({});"><td class="shoping__cart__item"><img src="{}" alt=""><h5>{}</h5></td><td class="shoping__cart__price">${}</td><td class="shoping__cart__price">{}</td><td class="shoping__cart__price">{}</td><td class="shoping__cart__item__close"><a href="#" name="wow"><span class="fa fa-close"></span></a></td></tr><tr id="desc_of_{}" class="shoping__cart__price hidden_row ftco-animated"><td colspan=4>{}</td><td class="shoping__cart__item__price"><button class="primary-btn cart-btn" type="submit" name="wow">Edit</button></td></tr></tbody><tbody id="item_to_be_replaced"></tbody>'.format("'" + 'desc_of_' +  'prod' + str(data['product_id']) + "'" , data['image']  , data['product_name'], data['price'] ,data['stock'] ,0 , 'prod' + str( data['product_id']) ,  data['desc'])
        new_html_str = '<tbody><tr onclick="show_hide_row({});"><td class="shoping__cart__item"><img src="{}" alt=""><h5>{}</h5></td><td class="shoping__cart__price">${}</td><td id="category_of_{{product.product_id}}" class="shoping__cart__price">{}</td><td class="shoping__cart__price">{}</td><td class="shoping__cart__price">{}</td><td class="shoping__cart__item__close"><a href="#" name="wow"><span class="fa fa-close"></span></a></td></tr><tr id="desc_of_{}" class="shoping__cart__price hidden_row ftco-animated"><td colspan=4>{}</td><td class="shoping__cart__item__price"><button class="primary-btn cart-btn" type="submit" name="wow">Edit</button></td></tr></tbody><tbody id="item_to_be_replaced"></tbody>'.format("'" + 'desc_of_' +  'prod' + str(data['product_id']) + "'" , data['image']  , data['product_name'], data['price'] ,data['stock'] , data['category']  , 0 , 'prod' + str( data['product_id']) ,  data['desc'])
        
        resp_data = {
            'c_html' : new_html_str ,
        }                    
        return JsonResponse(resp_data, status=200)


def update_product_data(request):
    """
    >>> Used by seller.html page via AJAX request
    >>> This function is used to update existing product data 
    """
    if request.is_ajax():
            data = dict() # Fetching the data sended through ajax request
            data['product_name'] = request.POST['product_name']
            data['price'] = int(request.POST['price'])
            data['stock'] = request.POST['stock']
            data['category'] = request.POST['category']
            data['desc'] = request.POST['desc']
            data['product_id'] = request.POST['product_id']

            try:
                print("Try chal ra hai")
                print("Try chal ra hai")
                print("Try chal ra hai")
                print("Try chal ra hai")
                data['image'] = request.POST['image']
            except:
                print("Except chal ra hai")
                print("Except chal ra hai")
                print("Except chal ra hai")
                print("Except chal ra hai")
                data['image'] = SHOP.GetProductById(product_id = data['product_id'])['image']

            SHOP.UpdateProductData(product_id = data['product_id'],
                                data = data,
            )

            return JsonResponse(data, status=200)

def remove_product(request):
    """
    >>> This function is used to remove a specific product from SellerCart as well as Products
    """
    if request.is_ajax():
        print("AJAX zindabad")
        print("AJAX zindabad")
        print("AJAX zindabad")
        print("AJAX zindabad")
        print("AJAX zindabad")
        print("AJAX zindabad")
        product_id = request.POST['product_id']
        phone_number = request.session['loggedin_user_phone_number']
        SHOP.RemoveProduct(phone_number = phone_number , product_id = product_id)
        return JsonResponse(status = 200)

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
