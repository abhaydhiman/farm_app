# Importing Necessary Libraries
from flask import Flask, render_template,request,session
from modules import opt_generator, msg_sender, firebase_user_checker, firebase_user_registerer, firebase_user_loger, firebase_data_fetcher, weather_fetcher, day_fetcher
from translator import text_translator, language_checker, user_home_text_translator, weather_text_translator, english_translator



# Init flask app
app = Flask(__name__)
app.secret_key = 'any random string'



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
        text_ls = ['Enter Credentials', 'Phone Number', 'Full Name', 'Submit', 'Already Registerd, Login']
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
                text_ls = ['Enter Credentials', 'Phone Number', 'Full Name', 'Submit', 'Already Registerd, Login', 'You are already Registered']
                sign_up_list = text_translator(text_ls, lang)
                return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message=sign_up_list[5])

        # To Go To Login Page            
        if request.form['sign-in-button'] == 'log-in':
            text_ls = ['Login', 'Phone Number', 'Password', 'Submit', 'Cancel']
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

            # If OTP is Wrong Go to Sign UP Page                
            else:
                text_ls = ['Enter Credentials', 'Phone Number', 'Full Name', 'Submit', 'Already Registerd, Login', 'OTP Entered Was Wrong']
                sign_up_list = text_translator(text_ls, lang)
                return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message=sign_up_list[5])
        
        # If User Wants To Go back to Signup Page
        if request.form['code-button'] == 'cancel-button':
            text_ls = ['Enter Credentials', 'Phone Number', 'Full Name', 'Submit', 'Already Registerd, Login']
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
        state = request.form['stt']
        city = request.form['city']
        # If Both Password Match then register user and redirect to home page
        if password1 == password2 and len(password1)>=6:
            firebase_user_registerer(phone_number, password1, name, lang, state, city)
            translated_list, name,city, state = user_home_text_translator(lang, name, city, state)
            session['name'] = name
            session['lang'] = lang
            session['phone_number'] = phone_number
            session['state'] = state
            session['city'] = city
            return render_template('user_home.html', t_lis = translated_list, phone_number = phone_number, name = name, city=city, state = state)
        
        # If condition not matched then show error
        else:
            text_ls = ['Submit Password', 'Enter Password', 'Confirm Password', 'Confirm', 'Both Password Do not match / password must be greater then 6 digits']
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
                name, state, city = firebase_data_fetcher(phone_number)
                translated_list, name,city, state = user_home_text_translator(lang, name, city, state)
                session['name'] = name
                session['lang'] = lang
                session['phone_number'] = phone_number
                session['state'] = state
                session['city'] = city
                return render_template('user_home.html', t_lis = translated_list, phone_number = phone_number, name = name,city = city, state = state)

            # Otherwise Then error is shown 
            else:
                text_ls = ['Login', 'Phone Number', 'Password', 'Submit', 'Cancel', 'Password Or Phone Number Did not match']
                log_list = text_translator(text_ls, lang)
                return render_template('log_in.html', log_list = log_list, lang=lang, mm=log_list[5])

        # If user wnats to go back to signup Page 
        if request.form['log-button'] == 'back':
            text_ls = ['Enter Credentials', 'Phone Number', 'Full Name', 'Submit', 'Already Registerd, Login']
            sign_up_list = text_translator(text_ls, lang)
            return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message="")





# TO Go To Home Page If User Clicks on Home LINK on user home 
@app.route('/user_home_3', methods=['POST','GET'])
def user_home_3():
    name = session['name']
    lang = session['lang']
    phone_number = session['phone_number']
    state = session['state']
    city = session['city']
    translated_list, name, city, state = user_home_text_translator(lang, name, city, state)
    return render_template('user_home.html', t_lis = translated_list, phone_number = phone_number, name = name, city = city, state = state)




# TO Go To Weather Page If User Clicks on Weather LINK 
@app.route('/weather', methods=['POST','GET'])
def weather():
    name = session['name']
    lang = session['lang']
    state = session['state']
    city = session['city']
    city = english_translator(city)
    state = english_translator(state)
    dt, temp, ma, mi, hum, des, speed, visi, day, code = weather_fetcher(city_name = city, state_name = state, lang = lang)
    translated_list, city, state = weather_text_translator(lang, city, state)
    phone_number = session['phone_number']
    cond = day_fetcher()
    return render_template('wheather.html', t_lis = translated_list, city = city, state = state, dt = dt, temp = temp,ma = ma,mi = mi,hum = hum,des = des,speed = speed,visi = visi, day = day, cond = cond, code = code)



# Running the Flask App
if __name__ == "__main__":
    app.run(debug=True)