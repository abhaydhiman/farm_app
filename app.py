# Importing Necessary Libraries
from flask import Flask, render_template,request
from modules import opt_generator, msg_sender, firebase_user_checker, firebase_user_registerer, firebase_user_loger
from translator import text_translator, language_checker



# Init flask app
app = Flask(__name__)



# Route for home page i.e. Language Selection Page
@app.route('/')
def home(): 
    return render_template('lang_select.html')



# Route for Sign Up page i.e. Page For Authentication
@app.route('/sign_up', methods=['POST'])
def sign_up(): 
    if request.method == 'POST':
        language = request.form['submit_button']

        # Checking Selected language
        lang = language_checker(language)

        # Translating Text
        text_ls = ['Enter Credentials', 'Submit', 'Already Registerd']
        sign_up_list = text_translator(text_ls, lang)
        return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message="")



# Route for OTP Verification Page i.e. Page For Submitting OTP
@app.route('/submit_otp', methods=['POST'])
def submit_otp():
    if request.method == 'POST':
        lang = request.form['lang']

        # To Go to Confirm OTP Page
        if request.form['sign-in-button'] == 'sign-in':
            phone_number = request.form['phone-number']
            name = request.form['name']
            flag = firebase_user_checker(phone_number)

            # If User is New
            if flag == 0:
                otp = opt_generator()
                text_ls = ['OTP For Your Farm App : ', 'Enter OTP', 'Verify Code', 'Cancel']
                otp_list = text_translator(text_ls, lang)
                msg_sender( given_phone_number = phone_number , given_message = otp_list[0] + str(otp))
                return render_template('confirm_otp.html', otp_list = otp_list, lang=lang, phone=phone_number, name=name, otp=otp)
            
            # If USer is Already Registered
            else:
                text_ls = ['Enter Credentials', 'Submit', 'Already Registerd', 'You are already Registered']
                sign_up_list = text_translator(text_ls, lang)
                return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message=sign_up_list[3])

        # To Go To Login Page            
        if request.form['sign-in-button'] == 'log-in':
            text_ls = ['Login', 'Submit', 'Cancel']
            log_list = text_translator(text_ls, lang)
            return render_template('log_in.html', log_list = log_list, lang=lang, mm="")



# Route for going to Set Password Page 
@app.route('/set_password', methods=['POST'])
def set_password():
    if request.method == 'POST':
        lang = request.form['lang']

        # To Go to Set Password Page
        if request.form['code-button'] == 'verify-code-button':
            otp_user = request.form['verification-code']
            phone_number = request.form['phone']
            name = request.form['name']
            otp = request.form['otp']

            # check if Otp Is Correct
            if otp == otp_user:
                text_ls = ['Submit Password', 'Enter Password', 'Confirm Password', 'Confirm']
                password_list = text_translator(text_ls, lang)
                return render_template('set_password.html', password_list=password_list , lang=lang, phone=phone_number, name=name, message="")

            # If OTP is Wrong Go to Sig UP Page                
            else:
                text_ls = ['Enter Credentials', 'Submit', 'Already Registerd', 'OTP Entered Was Wrong']
                sign_up_list = text_translator(text_ls, lang)
                return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message=sign_up_list[3])
        
        # If User Wants To Go back to Signup Page
        if request.form['code-button'] == 'cancel-button':
            text_ls = ['Enter Credentials', 'Submit', 'Already Registerd']
            sign_up_list = text_translator(text_ls, lang)
            return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message="")



# TO Go To Home Page If User Follows the Step to Register 
@app.route('/user_home', methods=['POST'])
def user_home():
    if request.method == 'POST':
        lang = request.form['lang']
        phone_number = request.form['phone']
        name = request.form['name']
        password1 = request.form['password']
        password2 = request.form['password-confirm']

        # If Both Password Match then register user and redirect to home page
        if password1 == password2 and len(password1)>=6:
            firebase_user_registerer(phone_number, password1, name, lang)
            return render_template('user_home.html')
        
        # If condition not matched then show error
        else:
            text_ls = ['Submit Password', 'Enter Password', 'Confirm Password', 'Confirm', 'Both Password Do not match  or password must be greater then 6 digits']
            password_list = text_translator(text_ls, lang)
            return render_template('set_password.html', password_list=password_list , lang=lang, phone=phone_number, name=name, message=password_list[4])


# TO Go To Home Page If User Follows the Step to Login 
@app.route('/user_home_2', methods=['POST'])
def user_home_2():
    if request.method == 'POST':
        lang = request.form['lang']

        # If user Wants to go to home page by logining
        if request.form['log-button'] == 'log-in':
            phone_number = request.form['phone-number']
            password = request.form['password']
            checker = firebase_user_loger(phone_number, password)

            # If Password matches with phone number then Redirect to home page
            if checker == 1:
                return render_template('user_home.html')

            # Otherwise Then error is shown 
            else:
                text_ls = ['Login', 'Submit', 'Cancel', 'Password Or Phone Number Did not match']
                log_list = text_translator(text_ls, lang)
                return render_template('log_in.html', log_list = log_list, lang=lang, mm=log_list[3])

        # If user wnats to go back to signup Page 
        if request.form['log-button'] == 'back':
            text_ls = ['Enter Credentials', 'Submit', 'Already Registerd']
            sign_up_list = text_translator(text_ls, lang)
            return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message="")



# Running the Flask App
if __name__ == "__main__":
    app.run(debug=True)