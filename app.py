# Importing Flask Libraries
from flask import Flask, render_template,request,session, jsonify


# Importing Functions from modules.py
from modules import opt_generator, msg_sender, firebase_user_checker, firebase_user_registerer,\
firebase_user_loger, firebase_data_fetcher, weather_fetcher, day_fetcher, loan_data, get_current_time,\
loan_data_fetcher, insu_data, insu_data_fetcher, update_status, product_data_sender,product_data_fetcher,\
product_data_fetcher2, product_data_updater, product_remover, user_image_sender, user_image_fetcher,\
all_product_fetcher, buy_product_data, user_cart_data_sender, user_cart_data_fetcher


# Importing Functions For translation from translator.py
from translator import text_translator, language_checker, user_home_text_translator, weather_text_translator,\
english_translator, financial_translator, loan_text_translator, insu_text_translator



# Init flask app
app = Flask(__name__)
app.secret_key = 'any random string'



# Route for home page i.e. Language Selection Page
@app.route('/')
def home():
    return render_template('new_lang_select.html')



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





# Route for going to Set Password Page For Farmer
@app.route('/set_password', methods=['POST'])
def set_password():
    if request.method == 'POST':
        lang = request.form['lang']

        # To Go to Set Password Page For farmer
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

            # If OTP is Wrong Go to Farmer Sign UP Page                
            else:
                text_ls = ['Enter Credentials', 'Phone Number', 'Full Name', 'Submit', 'Already Registerd, Login', 'OTP Entered Was Wrong']
                sign_up_list = text_translator(text_ls, lang)
                return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message=sign_up_list[5])
        
        # If User Wants To Go back to Farmer Signup Page
        if request.form['code-button'] == 'cancel-button':
            text_ls = ['Enter Credentials', 'Phone Number', 'Full Name', 'Submit', 'Already Registerd, Login']
            sign_up_list = text_translator(text_ls, lang)
            return render_template('signup.html', sign_up_list = sign_up_list, lang=lang, message="")





# TO Go To Home Page If Farmer Follows the Step to Register
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
        status = request.form['status']

        # If Both Password Match then register user and redirect to home page
        if password1 == password2 and len(password1)>=6:
            firebase_user_registerer(phone_number, password1, name, lang, state, city, status)
            translated_list, name,city, state , status= user_home_text_translator(lang, name, city, state, status)
            session['name'] = name
            session['lang'] = lang
            session['phone_number'] = phone_number
            session['state'] = state
            session['city'] = city
            session['status'] = status
            image = user_image_fetcher(phone_number)
            return render_template('user_home.html', t_lis = translated_list, phone_number = phone_number, name = name, city=city, state = state, status=status, image=image)

        # If condition not matched then show error
        else:
            text_ls = ['Submit Password', 'Enter Password', 'Confirm Password', 'Confirm', 'Both Password Do not match / password must be greater then 6 digits']
            password_list = text_translator(text_ls, lang)
            return render_template('set_password.html', password_list=password_list , lang=lang, phone=phone_number, name=name, message=password_list[4])





# TO Go To Home Page If Farmer Follows the Step to Login
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
                name, state, city, status = firebase_data_fetcher(phone_number)
                translated_list, name,city, state, status = user_home_text_translator(lang, name, city, state, status)
                session['name'] = name
                session['lang'] = lang
                session['phone_number'] = phone_number
                session['state'] = state
                session['city'] = city
                session['status'] = status
                image = user_image_fetcher(phone_number)
                return render_template('user_home.html', t_lis = translated_list, phone_number = phone_number, name = name,city = city, state = state, status=status,image=image)

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




# TO Go To Home Page If User Clicks on Home LINK on any Page
@app.route('/user_home_3', methods=['POST','GET'])
def user_home_3():
    name = session['name']
    lang = session['lang']
    phone_number = session['phone_number']
    state = session['state']
    city = session['city']
    status = session['status']
    image = user_image_fetcher(phone_number)
    translated_list, name, city, state, status = user_home_text_translator(lang, name, city, state,status)
    return render_template('user_home.html', t_lis = translated_list, phone_number = phone_number, name = name, city = city, state = state, status=status,image=image)




# TO Go To Weather Page If User Clicks on Weather LINK on any page
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



# To Go to profile page if user clicks on more info link on cliking on Profile crousel
@app.route('/profile', methods=['POST','GET'])
def profile():
    phone_number = session['phone_number']
    name = session['name']
    lang = session['lang']
    state = session['state']
    city = session['city']
    tstatus = session['status']
    image = user_image_fetcher(phone_number)
    date,time, status = loan_data_fetcher(phone_number)
    date2,time2,status2 = insu_data_fetcher(phone_number)
    ls = text_translator([city, state, name, 'Profile','Upload Photo', 'Loan', 'Insurance', tstatus], lang)
    return render_template('profile.html',loan=ls[5],insu=ls[6],text = ls[3],text2 = ls[4],name = ls[2],phone_number = phone_number,city = ls[0],state = ls[1], date = date, time = time, length=len(date), status = status,date2 = date2, time2 = time2, length2=len(date2), status2 = status2, tstatus=tstatus, image=image)



# To Send User Image Data to Database
@app.route('/user_image', methods=['POST','GET'])
def user_image():
    phone_number = session['phone_number']
    image = request.files.get('image')
    user_image_sender(phone_number,image)
    return jsonify({'name':image})



# To Go to financial page if user clicks Financial link On Financial Card
@app.route('/financial', methods=['POST','GET'])
def financial():
    lang = session['lang']
    ls = financial_translator(lang)
    return render_template('financial.html', ls = ls, msg = '')



# To Go to Loan Form page if user clicks on Form Card Link
@app.route('/loan', methods=['POST','GET'])
def loan():
    lang = session['lang']
    ls, t1,t2,t3 = loan_text_translator(lang, t1="Submit", t2="Reset", t3="Cancel")
    return render_template('loan.html', ls = ls, t1=t1,t2=t2,t3=t3)



# This is the Route for going bck to financial page if user clicks on submit button on loan form
@app.route('/loan_submit', methods=['POST','GET'])
def loan_submit():
    # Getting all the required information
    if request.method == 'POST':
        name = request.form['name']
        name2 = request.form['name2']
        dob = request.form['dob']
        number = request.form['number']
        email = request.form['email']
        gender = request.form['gender']
        maritial = request.form['maritial']
        income = request.form['income']
        address = request.form['address']
        loan_type = request.form['type']
        area = request.form['area']
        total_area = request.form['totalarea']
        my_loan = request.form['myloan']
        amount = request.form['amount']
        des = request.form['text']
        c_record = 'False'
        c_record2 = 'False'
        blacklist = 'False'
        sign = 'False'
        if request.form.get('c1'):
            c_record = 'True'
        if request.form.get('c2'):
            c_record2 = 'True'
        if request.form.get('c3'):
            blacklist = 'True'
        if request.form.get('c4'):
            sign = 'True'
        amount_blacklist = request.form['amount2']
        lang = session['lang']
        phone_number = session['phone_number']
        ls = financial_translator(lang)
        time, date = get_current_time()
        status = 'Pending'
        loan_data(name,name2 ,dob ,number ,email ,gender ,maritial, income ,address ,loan_type,area ,total_area ,my_loan ,amount ,des,c_record ,c_record2 ,blacklist ,sign ,amount_blacklist ,phone_number, time, date, status=status)
        msg = text_translator(['Form for loan has been Submited'], lang)
        return render_template('financial.html', ls = ls, msg = msg[0])




# To Go to insurance page if user clicks on Insurance Card
@app.route('/insu', methods=['POST','GET'])
def insu():
    lang = session['lang']
    ls, t1,t2,t3 = insu_text_translator(lang, t1="Submit", t2="Reset", t3="Cancel")
    return render_template('insurance.html', ls = ls, t1=t1,t2=t2,t3=t3)




# This is the Route for going bck to financial page if user clicks on submit button on Insurance form
@app.route('/insu_submit', methods=['POST','GET'])
def insu_submit():
    # Getting all the required information
    if request.method == 'POST':
        name = request.form['name']
        name2 = request.form['name2']
        dob = request.form['dob']
        number = request.form['number']
        email = request.form['email']
        gender = request.form['gender']
        maritial = request.form['maritial']
        income = request.form['income']
        address = request.form['address']
        insu_type = request.form['type']
        area = request.form['area']
        total_area = request.form['totalarea']
        des = request.form['text']
        c_record = 'False'
        c_record2 = 'False'
        blacklist = 'False'
        sign = 'False'
        if request.form.get('c1'):
            c_record = 'True'
        if request.form.get('c2'):
            c_record2 = 'True'
        if request.form.get('c3'):
            blacklist = 'True'
        if request.form.get('c4'):
            sign = 'True'
        amount_blacklist = request.form['amount2']
        lang = session['lang']
        phone_number = session['phone_number']
        ls = financial_translator(lang)
        time, date = get_current_time()
        status = 'Pending'
        insu_data(name,name2 ,dob ,number ,email ,gender ,maritial, income ,address ,insu_type,area ,total_area,des,c_record ,c_record2 ,blacklist ,sign ,amount_blacklist ,phone_number, time, date, status=status)
        msg = text_translator(['Form for insurance has been Submited'], lang)
        return render_template('financial.html', ls = ls, msg = msg[0])




# To Go to shop page if user clicks on more info link
@app.route('/shop', methods=['POST','GET'])
def shop():
    lang = session['lang']
    phone_number = session['phone_number']
    status = session['status']
    pname,pdes,price,stock,cat,image, buyers, unique_cat = all_product_fetcher()
    if status == 'Farmer':
        b_text = 'Become Seller'
    else:
        b_text = 'Sell Products'
    return render_template('shop_now.html', b_text = b_text, pname = pname, price=price, image = image, cat = cat, unique_cat = unique_cat, length = len(pname))




# To  Make a Farmer to Seller + Farmer
@app.route('/become_seller',methods=['POST','GET'])
def become_seller():
    lang = session['lang']
    phone_number = session['phone_number']
    status = update_status(phone_number)
    session['status'] = status
    b_text = 'Sell Products'
    return jsonify({'b_text' : b_text})




# To Go to Sell Product Page
@app.route('/seller',methods=['POST','GET'])
def seller():
    lang = session['lang']
    phone_number = session['phone_number']
    status = session['status']
    pname,pdes,price,stock,cat,image,buyers = product_data_fetcher(phone_number)
    return render_template('seller.html',pname=pname,pdes=pdes,price=price,stock=stock,cat=cat,image=image, buyers=buyers, length=len(pname))




# To Rgister a product on Seller Page
@app.route('/product',methods=['POST','GET'])
def product():
    lang = session['lang']
    phone_number = session['phone_number']
    status = session['status']
    name = request.form['name']
    price = request.form['price']
    cat = request.form['cat']
    des = request.form['des']
    stock = request.form['stock']
    image = request.form['image']
    cat = cat.replace(' ','-')
    flag = product_data_sender(phone_number=phone_number,name=name,price=price,category=cat,des=des,in_Stock=stock,image=image)

    html = '<tbody><tr onclick="show_hide_row({});"><td class="shoping__cart__item">\<img id="{}_image" src="{}" alt="">\
            <h5 id="{}_name">{}</h5></td><td id="{}_cat" class="shoping__cart__price">{}</td>\
            <td id="{}_price" class="shoping__cart__price">{}</td><td id="{}_stock" class="shoping__cart__price">{}\
            </td><td id="{}_buy" class="shoping__cart__price">{}</td><td class="shoping__cart__item__close">\
            <span class="fa fa-close"></span></td></tr>\<tr id="{}" class="shoping__cart__price hidden_row ftco-animated">\
            <td colspan=4 id="{}_des">{}</td><td class="shoping__cart__item__price"><a href="#hidden_row12" onclick="show_hide_row({});">\
            <button class="primary-btn cart-btn bedit" value="{}" type="submit" name="wow">Edit</button>\
            </a></td></tr></tbody>\
            <tbody id="new_product_row"></tbody>'.format("'" + name + "'",name,image,name,name,name,cat,name,price,name,stock,name,0,name,name,des,"'" + "hidden_row12" + "'",name)

    return jsonify({'flag':flag,'html':html})




# To Send Updated product Data on Seller Page As per Given Name
@app.route('/pedit',methods=['POST','GET'])
def pedit():
    name = request.form['name']
    phone_number = session['phone_number']
    price,des,stock,cat,buyers,img = product_data_fetcher2(phone_number,name)
    return jsonify({'name':name,'price':price,'des':des,'stock':stock,'cat':cat,'buy':buyers,'img':img})




# To Send Updated product Data on Seller Page And to database
@app.route('/update_product',methods=['POST','GET'])
def update_product():
    phone_number = session['phone_number']
    name = request.form['name']
    price = request.form['price']
    cat = request.form['cat']
    des = request.form['des']
    stock = request.form['stock']
    image = request.form['image']
    product_data_updater(phone_number=phone_number,name=name,price=price,category=cat,des=des,in_Stock=stock,image=image)
    return jsonify({'name':name,'price':price,'des':des,'stock':stock,'cat':cat,'img':image})




# To delete product Data on Seller Page And from database
@app.route('/product_remove',methods=['POST','GET'])
def product_remove():
    phone_number = session['phone_number']
    name = request.form['name']
    product_remover(phone_number, name)
    return jsonify({'name':name})




# To go to shop_details page to buy the selected product
@app.route('/buy_product',methods=['POST','GET'])
def buy_product():
    phone_number = session['phone_number']
    pname = request.form['product_buy']
    price1,des,stock1,cat1,buy,img = buy_product_data(pname)
    return render_template('shop_details.html', pname = pname, price = price1, des = des, stock = stock1, cat = cat1, buy = buy, img = img)




# To go to sho grid page if user clicks on different categories card.
@app.route('/product_grid', methods=['POST','GET'])
def product_grid():
    phone_number = session['phone_number']
    product_cat = request.form['product_cat']
    return render_template('shop_grid.html')




# To go to checkout page or cart page if user clicks on buy now or add to cart button
@app.route('/buy_now', methods=['POST','GET'])
def buy_now():
    phone_number = session['phone_number']
    pname = request.form['name']
    amount = request.form['amount']
    buy2 = request.form['buy']
    price1,des,stock1,cat1,buy,img = buy_product_data(pname)
    price1 = int(price1)
    price1 = price1*int(amount)
    if price1 > 400:
        price12= price1 + 20
    else:
        price12 = price1 + (price1*(20/100))
    if buy2 == 'buy':
        return render_template('checkout.html', pname = pname, price = price1, price12 = price12, des = des, stock = stock1, cat = cat1, buy = buy, img = img, amount = amount)
    else:
        user_cart_data_sender(phone_number, pname, amount)
        name_lis, amount_lis = user_cart_data_fetcher(phone_number)
        price_lis = []
        des_lis = []
        img_lis = []
        for nam in name_lis:
            price1,des,stock1,cat1,buy,img = buy_product_data(nam)
            price_lis.append(price1)
            img_lis.append(img)
        price12 = []
        for i in range(len(price_lis)):
            prices = int(price_lis[i])*int(amount_lis[i])
            price12.append(prices)
        sum_price = sum(price12)
        totp_price = sum_price + (sum_price*(20/100))
        return render_template('shoping_cart.html', name_lis = name_lis,price_lis=price_lis,img_lis = img_lis, amount_lis=amount_lis, price12 = price12,length = len(name_lis), sum_price=sum_price, totp_price = totp_price)




# To Go to disease Prediction Page if the user clicks on the disease prediction card.
@app.route('/disease_prediction', methods=['POST','GET'])
def disease_prediction():
    phone_number = session['phone_number']
    return render_template('disease_prediction.html')




# To Show the Different categories of Disease Cards based on the Main Card Clicked
@app.route('/disease', methods=['POST','GET'])
def disease():
    phone_number = session['phone_number']
    name = request.form['name']
    print(name)
    return jsonify({'name':name})





# Running the Flask App
if __name__ == "__main__":
    app.run(debug=True)
