from modules.imp_funcs import firebaseConfig
from pyrebase import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
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
    def SetChild(cls , *args , data):
        child_location = FirebaseManager.Navigator(*args)
        child_location.set(data)
    
    @classmethod
    def GetChild(cls , *args ):
        child_location = FirebaseManager.Navigator(*args)
        return child_location.get().val()

    @classmethod
    def FilterChilds(cls , *args , property , filter_value ):
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
    
    
    @property
    def name(phone_number = None):
        return FirebaseManager.GetChild('General_User',str(phone_number) , 'name')

    @classmethod
    def isRegistered(cls , phone_number = None):
        return str(phone_number) in FirebaseManager.GetChild('General_User').keys()

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


class SHOP(FirebaseManager):
    @classmethod
    def GetProductById(cls , product_id = None ):
       return dict(FirebaseManager.GetChild('Products' , product_id))

    @classmethod
    def GetAllProducts(cls):
        return dict(FirebaseManager.GetChild('Products'))

    @classmethod
    def GetUserCart(cls , phone_number = None):
        return dict(FirebaseManager.GetChild('General_User' , phone_number)['cart'])

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


