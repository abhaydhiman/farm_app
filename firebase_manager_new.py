from modules.imp_funcs import firebaseConfig
from pyrebase import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
from modules.imp_funcs import translator
import sys




# ***********************firebase_admin_sdk*********************
from firebase_admin import auth as authh # ? VERY VERY IMPORTANT
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('..\\firebase_admin_sdk.json')
firebase_admin.initialize_app(cred , {
    'databaseURL' : 'https://testing-54b5b.firebaseio.com/'
})
# ***********************firebase_admin_sdk*********************


class FirebaseManager:

    """
    NOTE -> Importing firebaseConfig dictationary from { modules/imp_func.py }

    >>> firebase class is a well structured class which
    >>> helps us to use CRUD operations in a super easy way
    >>> LIMITATION --> FilterChilds method can only be used to filter different dictatioinarties not lists
    """


    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()

    @classmethod
    def create_user_with_email_and_password(cls , email , password):
        auth.create_user_with_email_and_password(email , password)
    
    @classmethod
    def sign_in_with_email_and_password(cls , email , password):
        auth.sign_in_with_email_and_password(email , password)


    @classmethod
    def Navigator(cls , *args):
        child_location = FirebaseManager.db.child( args[0] )
        for val in args[1:len(args)]:
            child_location = child_location.child(val)
        return child_location

    @classmethod
    def SetChild(cls , *args , data ):
        child_location = FirebaseManager.Navigator(*args)
        child_location.set(data)
    
    @classmethod
    def GetChild(cls , *args ):
        child_location = FirebaseManager.Navigator(*args)
        return child_location.get().val()

    @classmethod
    def FilterChilds(cls , *args , property  , filter_value):
        child_location = FirebaseManager.Navigator(*args) 
        childs = dict( child_location.get().val() ) 
        selected_childs = { key:value for key , value in childs.items() if value[property] == filter_value } # Filtering the required categorical products
        return selected_childs

    @classmethod
    def ImageUploader(cls , *args , image_name):
        child_location = FirebaseManager.Navigator(*args) 
        storage = firebase.storage()  # Connecting to firebase stroage
        path_on_cloud = "omg/" + str(image_name) + ".jpg"
        path_on_local = sys.path[0] + "\pro_farm\static\images\\featured\\" + "feature-" + str(image_name) + ".jpg"
        storage.child(path_on_cloud).put(path_on_local) 
        return storage.child('prod_imgs/' + str(image_name) + '.jpg').get_url(None) # Returning the URL of stored image in firebase storage

    def __str__(self): # Helps to print objects of firebase and its child classes
        return str(vars(self))


class User(FirebaseManager):
    """
    >>> User class is used to user objects
    >>> This class is a child class of FirebaseManager class present inside same file
    """
    


    # Overriding (sign_in_with_email_and_password) function of parent class
    def create_user_with_email_and_password(self  , email , password):
        FirebaseManager.create_user_with_email_and_password(email , password)
        # Pushing the User object data to firebase realtime database
        print(self.phone_number)
        FirebaseManager.SetChild( 'General_User', self.phone_number , data = vars(self) )
    
    def UpdateUserData(self):
        FirebaseManager.SetChild('General_User' , self.phone_number , data = vars(self) )

    def __init__( self , language = None , phone_number = None , isSeller = False , isFarmer = True):
        self.name         = None
        self.phone_number = phone_number
        self.state        = None
        self.city         = None
        self.language     = language
        self.cart         = None
        self.isSeller     = isSeller
        self.isFarmer     = isFarmer
        FirebaseManager.__init__(self) # Calling the constructor of parent class ---> call parent constructor if and only if there are instance members to be created 

    def DeleteUserAccount(self):


        # *************************************firebase_admin_skd*************************************
        user =  firebase_admin.auth.get_user_by_email( str(self.phone_number) + "@farmapp.com" ) 
        firebase_admin.auth.delete_user(user.uid)
        # *************************************firebase_admin_skd*************************************

    def ResetPassword(self):
        """
        >>>    new_user = User(phone_number = 9306219945)
        >>>    new_user.ResetPassword()

        >>>    otp_given_by_user = int(input("Enter OTP sent"))

        >>>    if otp_given_by_user == new_user.otp_generated:
        >>>        new_password = int(input("Enter new password of atleast 6 digits"))
        >>>        new_user.DeleteUserAccount()
        >>>        new_user.create_user_with_email_and_password(str(new_user.phone_number) + "@farmapp.com" , new_password)

        >>>    else:
        >>>        print("OTP eneterd is incorrect")
        """

 
        from modules.imp_funcs import OTP_generator , msg_sender
        generated_otp        = OTP_generator()
        phone_number_of_user = self.phone_number

        # *msg_sender(given_phone_number=self.phone_number , given_message=str(generated_otp))

        print("oooo" , generated_otp)        
        self.otp_generated = generated_otp

    def isRegistered(self):
        print(str(self.phone_number))
        return str(self.phone_number) in FirebaseManager.GetChild('General_User').keys()


# print(FirebaseManager.GetChild('General_User'))
# user_1 = User(phone_number = 9306219945)
# print("Registration status : " , user_1.isRegistered())
# print(FirebaseManager.ImageUploader(image_name=2))
# print("Image uploaded successfully!!")
# user_1.ResetPasssword()
# User.ResetPassword()



#************************************nya--kaam*****************************************************
class USER(FirebaseManager):

    @classmethod
    def isRegistered(cls , phone_number = None):
        list_of_general_users = FirebaseManager.GetChild('General_User') # Getting the list of all general users if they have any otherwise we get None
        if list_of_general_users is None: # If value is None means its the first user --> means nobody isRegistered so we can return Fasle
           return False 
        else:
           return str(phone_number) in FirebaseManager.GetChild('General_User') # Returing True if phone_number is already registered else False

    @classmethod
    def SetUserData(cls , phone_number = None , data = None):
        FirebaseManager.SetChild('General_User' , phone_number , data = data)

    @classmethod
    def ResetPassword(cls , phone_number = None):
        """
                
        >>> generated_otp = USER.ResetPassword(phone_number = 9306219945)


        >>> otp_given_by_user = int(input("Enter OTP sent"))
        >>> if otp_given_by_user == generated_otp:
        >>>    new_password = int(input("Enter new password of atleast 6 digits"))
        >>>    USER.DeleteUserAccount(phone_number = 9306219945)
        >>>    FirebaseManager.create_user_with_email_and_password(str(9306219945) + "@farmapp.com" , new_password)
        >>> else:
        >>>    print("OTP eneterd is incorrect")

        """
        from modules.imp_funcs import OTP_generator , msg_sender
        generated_otp        = OTP_generator()
        phone_number_of_user = phone_number
        # * msg_sender(given_phone_number = phone_number , given_message=str(generated_otp))
        print("oooo" , generated_otp)
        return  generated_otp
        
    @classmethod
    def DeleteUserAccount(cls , phone_number = None ):
        # *************************************firebase_admin_skd*************************************
        user =  firebase_admin.auth.get_user_by_email( str(phone_number) + "@farmapp.com" ) 
        firebase_admin.auth.delete_user(user.uid)
        # *************************************firebase_admin_skd*************************************

    @classmethod
    def UpdateUserCart(cls , phone_number = None , Cart = None):
        FirebaseManager.SetChild('General_User' , phone_number  , data = Cart )

    @classmethod
    def GetLangOfUser(cls , phone_number = None):
        return FirebaseManager.GetChild('General_User' , phone_number , 'language')

    @classmethod
    def GetTranslatedTexts(cls , phone_number = None , for_page = None):
        language = USER.GetLangOfUser(phone_number = phone_number)
        return dict(FirebaseManager.GetChild('pages_text' , for_page , language))

    @classmethod
    def submit_loan_form(cls , phone_number = None , data = None):
        if data is not None:
            loans = FirebaseManager.GetChild('General_User' , phone_number , 'loan_data')
            if loans is not None:
                new_loan_index = len(loans)
            else:
                new_loan_index = 1
            FirebaseManager.SetChild('General_User' , phone_number , 'loan_data' , 'LoanForm ' + str(new_loan_index) , data=data )

    @classmethod
    def submit_insurance_form(cls , phone_number = None , data = None):
        if data is not None:
            insurances = FirebaseManager.GetChild('General_User' , phone_number , 'insurance_data')
            if insurances is not None:
                new_insurance_index = len(insurances)
            else:
                new_insurance_index = 1
            FirebaseManager.SetChild('General_User' , phone_number , 'insurance_data' , 'InsuranceForm ' + str(new_insurance_index) , data=data )

    @classmethod
    def translate_dic(cls , dic = None , to_langg = None):
        return {key:translator(text , to_langg = to_langg) for key , text in dic.items()}

    @classmethod
    def GetProfilePageData(cls , phone_number = None):
        user_data = dict(FirebaseManager.GetChild('General_User' , phone_number))

        language = user_data['language']

        profile_data = {}
        profile_data['name']         = user_data['name']
        profile_data['phone_number'] = user_data['phone_number']
        profile_data['status']       = user_data['status']
        profile_data['location']     = user_data['state'] + ','  + user_data['city']
        profile_data['dp']           = user_data['dp']

        profile_data = USER.translate_dic(dic=profile_data , to_langg=language)

        loan_and_insurance_lis = []

        if 'loan_data' in user_data.keys():
            for data in user_data['loan_data'].values():
                data = {key:value for key , value in data.items() if key  in ('date' , 'time' , 'STATUS')}
                data['form_type'] = 'loan'
                data['form_type'] = translator( data['form_type'] , to_langg = language)
                data['STATUS'] = translator( data['STATUS'] , to_langg = language)
                loan_and_insurance_lis.append(data)

        
        if 'insurance_data' in user_data.keys():
            for data in user_data['insurance_data'].values():
                data = {key:value for key , value in data.items() if key  in ('date' , 'time' , 'STATUS')}
                data['form_type'] = 'insurance'
                data['form_type'] = translator( data['form_type'] , to_langg = language)
                data['STATUS'] = translator( data['STATUS'] , to_langg = language)
                loan_and_insurance_lis.append(data)


        profile_data['loan_and_insurance_data'] = loan_and_insurance_lis
        return profile_data

    @classmethod
    def Base64ImageDecoder(cls , base_64_encoded_image = None):
        import base64

        base_64_encoded_image = base_64_encoded_image.split(',')[1]

        pad = len(base_64_encoded_image)%4
        base_64_encoded_image += "="*pad

        data =  base_64_encoded_image.replace(' ', '+')
        imgdata = base64.b64decode(data)
        filename = 'new_dp.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)

    @classmethod
    def SimpleImageUploader(cls , path_on_local = None , path_on_storage = None , phone_number=None):
        # Connecting to the firebase storage
        storage = firebase.storage()
        storage.child(path_on_storage).put(path_on_local)
        return storage.child('profile_pics/' + str(phone_number) + '.png').get_url(None) # Returning the URL of uploaded product image


    @classmethod
    def Base64ImageUploader(cls , base_64_encoded_image = None , phone_number = None):
        import sys
        USER.Base64ImageDecoder(base_64_encoded_image = base_64_encoded_image)

        path_on_local   = sys.path[0] + '\\new_dp.png'
        path_on_storage = 'profile_pics/' + str(phone_number) + '.png'

        return USER.SimpleImageUploader(path_on_local = path_on_local , path_on_storage = path_on_storage , phone_number=phone_number) # Returning the URL of uploaded product image

    @classmethod
    def update_dp(cls , phone_number = None , image = None):
        new_dp = USER.Base64ImageUploader(base_64_encoded_image=image , phone_number = phone_number)
        FirebaseManager.SetChild('General_User' , phone_number , 'dp' , data = new_dp)

    def UpdateProductData(cls , product_id = None , data = None):
        if data['image'] != "https://ohram.org/image/utilities/empty_product.svg":
            data['image'] = SHOP.Base64ImageUploader(base_64_encoded_image = data['image'] , product_id = product_id)

        FirebaseManager.SetChild('Products' , product_id , data = data)

class SHOP(FirebaseManager):
    @classmethod
    def GetProductById(cls , product_id = None ):
       return dict(FirebaseManager.GetChild('Products' , product_id))


    @classmethod
    def UpdateProductData(cls , product_id = None , data = None):
        if data['image'] != "https://ohram.org/image/utilities/empty_product.svg":
            data['image'] = SHOP.Base64ImageUploader(base_64_encoded_image = data['image'] , product_id = product_id)
        
        FirebaseManager.SetChild('Products' , product_id , data = data)


    @classmethod
    def GetAllProducts(cls):
        Products = dict(FirebaseManager.GetChild('Products'))
        Products = {product_id:data for product_id , data in Products.items() if not isinstance(data , int)}
        return Products

    @classmethod
    def GetUserCart(cls , phone_number = None):
        return dict(FirebaseManager.GetChild('General_User' , phone_number)['cart'])

    @classmethod
    def GetSellerCart(cls , phone_number = None):
        return dict(FirebaseManager.GetChild('General_User' , phone_number)['SellerCart'])

    @classmethod
    def GetListOfCategories(cls):
        return FirebaseManager.GetChild('categories') # Returns a list of all categories 
        

    @classmethod
    def UpdateUserCart(cls , phone_number = None ,  cart = None):
        FirebaseManager.SetChild('General_User' , phone_number , 'cart' , data = cart)

    @classmethod
    def GetTotalBillOfUser(cls , Products_list = None , phone_number = None):
        total_bill = 0
        
        if Products_list is not None:#If you provides Products_list then if block runs
            for product in Products_list:
                total_bill += product['total_price']
        elif phone_number is not None:# If you don't provide Products_list and provides phone_number of user then elif block runs
            cart = SHOP.GetUserCart(phone_number = phone_number)
            for product_id , quantity in cart.items():
                if product_id != 'isEmpty':
                    product_data_dic = SHOP.GetProductById(product_id = product_id)
                    total_bill += quantity * product_data_dic['price']
        return total_bill

    @classmethod
    def GetUserCartProductsCompleteData(cls , phone_number = None):
        """
        >>> This function return a total_bill and list of dictationaries[each representing a product from cart of user]
        >>> All the dictationaries contain extra parameter such as quantity , total_price of each product based on its quantity
        """
        cart = SHOP.GetUserCart(phone_number = phone_number)
        Products_list = []

        for product_id , quantity in cart.items():
            if product_id != 'isEmpty':
                product_data_dic                = SHOP.GetProductById(product_id = product_id)
                product_data_dic['quantity']    = quantity
                # Getting the product's total price based on its quantity
                product_data_dic['total_price'] = quantity * product_data_dic['price']
                Products_list.append(product_data_dic)

        total_bill = SHOP.GetTotalBillOfUser(Products_list = Products_list)
        return total_bill , Products_list

    @classmethod 
    def GetSellerCartProductsDetails(cls , phone_number = None):
        SellerCart = SHOP.GetSellerCart(phone_number = phone_number)
        Products_list = []

        for product_id in SellerCart.keys():
            if product_id != 'isEmpty':
                product_data_dic                = SHOP.GetProductById(product_id = product_id)
                product_data_dic['Details']     = SellerCart[product_id]
                Products_list.append(product_data_dic)

        return Products_list



    @classmethod
    def UpdateCategories(cls , new_cat = None):
        if new_cat is not None:
            categories_present = SHOP.GetListOfCategories() 
            if new_cat not in categories_present:
                categories_present.append(new_cat)
            FirebaseManager.SetChild('categories' , data = categories_present)
        else:
            Products = SHOP.GetAllProducts()
            updated_categories = {data['category'] for product_id , data in Products.items()}
            FirebaseManager.SetChild('categories' , data = list(updated_categories))




    @classmethod
    def Base64ImageDecoder(cls , base_64_encoded_image = None):
        import base64

        base_64_encoded_image = base_64_encoded_image.split(',')[1]

        pad = len(base_64_encoded_image)%4
        base_64_encoded_image += "="*pad

        data =  base_64_encoded_image.replace(' ', '+')
        imgdata = base64.b64decode(data)
        filename = 'DECODED.png'  
        with open(filename, 'wb') as f:
            f.write(imgdata)
    
    @classmethod
    def SimpleImageUploader(cls , path_on_local = None , path_on_storage = None , product_id = None):
        # Connecting to the firebase storage
        storage = firebase.storage()  
        storage.child(path_on_storage).put(path_on_local)
        return storage.child('prod_imgs/' + str(product_id) + '.png').get_url(None) # Returning the URL of uploaded product image


    @classmethod
    def Base64ImageUploader(cls , base_64_encoded_image = None , product_id = None):
        import sys
        SHOP.Base64ImageDecoder(base_64_encoded_image = base_64_encoded_image)
        
        path_on_local   = sys.path[0] + '\DECODED.png'
        path_on_storage = 'prod_imgs/' + str(product_id) + '.png'

        return SHOP.SimpleImageUploader(path_on_local = path_on_local , path_on_storage = path_on_storage , product_id = product_id) # Returning the URL of uploaded product image
   

    @classmethod
    def SellerAddsNewProduct(cls , phone_number = None , prod_data = None):
        """
        >>> Whenever seller adds new product from seller.html , there is an AJAX request generate and it will trigger this particular function from shop/views.py/sell_something
        >>> The major task of this function is to take prod_data provided by seller and add that product to Firebase realtime db and storage[for image]
        >>> This function accepts product data and RETURNS (product_id given to new product and image_URL)
        >>>  WORKFLOW :
        >>> This function firstly decides product_id of new product based on the total number of products already present in database
        >>> After we call Base64ImageUploader which will firslty convert b64 format string to a image named (DECODED.png) and then push that particular image to db
        """
        
        total_prods = len( FirebaseManager.GetChild('Products') ) # We fetch total_number of products here because it helps us to decide the product_id of new product just added by SELLER
        product_id = total_prods + 1

        if prod_data['image'] != "https://ohram.org/image/utilities/empty_product.svg":
            prod_data['image'] = SHOP.Base64ImageUploader(base_64_encoded_image = prod_data['image'] , product_id = product_id)
        

        prod_data['product_id'] = 'prod' + str(product_id)
        FirebaseManager.SetChild('Products' , 'prod'+str(product_id) , data=prod_data ) # Adding the product to Products section of database

        filtered_prod_data = { key:prod_data[key] for key in prod_data.keys() and ['buyers' , 'rating' , 'stock'] } # Getting only 'buyers' , 'rating' nad 'stock' value for dic_for_seller [for more clarification see the realtime database table and also print the prod_data dictationary]
        FirebaseManager.SetChild('General_User' , phone_number , 'SellerCart' , 'prod'+str(product_id) , data = filtered_prod_data) #Adding the product to SellerCart of 

        #If seller adds new product then we then we have to also update categories (VERY VERY IMPORTANT)
        SHOP.UpdateCategories(new_cat = prod_data['category'])
        
        return product_id , prod_data['image']  # Here (total_prod + 1) actually represent product_id of newly added product

    @classmethod
    def RemoveProduct(cls , phone_number = None ,  product_id = None):
        FirebaseManager.SetChild('Products' , product_id , data = 0) # Setting the product details to 0 
        FirebaseManager.SetChild('General_User' , phone_number , 'SellerCart' , product_id , data = [] ) # Removing the product form seller cart

    @classmethod
    def FilterProductsByCategory(cls , cat_req = None):
        Products = SHOP.GetAllProducts()
        Products = [ data for product_id , data in Products.items() ]
        return [product for product in Products if product['category'] == cat_req]

phone_number = 9306219945
# SHOP.ellerAddsNewProduct(phone_number = phone_number , prod_data = {'naam' : 'kam hi h' , 'wow' : 'cool'})
# new = SHOP.GetSellerCartProductsDetails(phone_number=phone_number)

# for p in new:
#     print(p)
#     print()
#     print()
#     print()
#     print()
#     print()
# print(len(FirebaseManager.GetChild('Products')))
# print()
# print()
# print(FirebaseManager.GetChild('Products'))
# SHOP.UpdateCategories(new_cat = 'yank')


# print(SHOP.FilterProductsByCategory('ooterikiii'))

# translated_texts = USER.GetTranslatedTexts(phone_number = phone_number , for_page = 'for_loan_page')
# new__dic = {'csrfmiddlewaretoken': ['sZ5XGkGvs2VqAl8LK99EneHr7TARFAq53YCwpMjtAJ9oAMF5tMleMbVsqWkmJhEq'], 'first_name': ['ayush'], 'last_name': ['Malik'], 'DOB': ['2001-10-04'], 'phone_number': ['9306219945'], 'email': ['ayushmalik779@gmail.com'], 'gender': ['Male'], 'maritial_status': ['Single'], 'annual_income': ['1'], 'permanent_address': ['111'], 'insurance_type': ['type3'], 'land_area': ['1'], 'total_land_area': ['1'], 'insurance_required_for': ['okiee'], 'is_there_a_criminal_record_on_you': ['Yes'], 'Is_there_pending_criminal_case_on_you': ['Yes'], 'have_you_been_blacklisted': ['Yes'], 'if_yes__amount': ['10'], 'Have_you_signed_a_guarantee_or_surety_for_an_entity': ['Yes']}
# USER.submit_loan_form(phone_number = phone_number , data=new__dic)

# print(USER.GetProfilePageData(phone_number = phone_number))
# print(USER.translate_dic({'Ayush':'Ayush' , 'Malik': 'Malik'} , to_langg='hi'))