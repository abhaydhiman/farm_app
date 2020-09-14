from flask import Flask, jsonify, request, session
from translator import language_checker, text_translator, text_translator2, text_translator3, text_translator4
from modules import opt_generator, msg_sender, firebase_user_checker, firebase_user_registerer, firebase_user_loger, firebase_data_fetcher

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route("/lang", methods=["POST","GET"])
def lang():
    query = dict(request.form)['query']
    lang = language_checker(query)
    lis = text_translator(lang)
    return jsonify({"response": [lis,lang]})


@app.route("/signup", methods=["POST","GET"])
def signup():
    query1 = dict(request.form)['query1']
    query2 = dict(request.form)['query2']
    lang =   dict(request.form)['lang']
    lis = ''
    msg = 0
    otp = ''
    flag = firebase_user_checker(query2)
    if flag == 0:
        otp = opt_generator()
        #msg_sender( given_phone_number = query2 , given_message = otp)
        lis = text_translator2(lang)
    else:
        msg = 1
    print(otp)
    return jsonify({"response": [msg, lis, otp, query1, query2]})


@app.route("/signup2", methods=["POST","GET"])
def signup2():
    lang = dict(request.form)['lang']
    lis = text_translator4(lang)
    return jsonify({"response": lis})


@app.route("/otp", methods=["POST","GET"])
def otp():
    query1 = dict(request.form)['query1']
    query2 = dict(request.form)['query2']
    lang = dict(request.form)['lang']
    name = dict(request.form)['name']
    phone = dict(request.form)['phone']
    msg = 0
    lis = ''
    if query1 != query2:
        msg = 1
    else:
        lis = text_translator3(lang)
    return jsonify({"response": [msg, lis, name, phone]})


@app.route("/password", methods=["POST","GET"])
def password():
    query1 = dict(request.form)['query1']
    query2 = dict(request.form)['query2']
    lang =   dict(request.form)['lang']
    name = dict(request.form)['name']
    phone = dict(request.form)['phone']
    msg = 0
    if (query1 != query2) or (len(query1) < 6):
        msg = 1
    else:
        msg = 0
        firebase_user_registerer(phone, query1, name, lang)
    return jsonify({"response": [msg]})



@app.route("/login", methods=["POST","GET"])
def login():
    query1 = dict(request.form)['query1']
    query2 = dict(request.form)['query2']
    lang =   dict(request.form)['lang']
    msg = 0
    pa = firebase_user_loger(query1, query2)
    if pa == 1:
        msg = 1
        name = firebase_data_fetcher(query1)
    else:
        msg = 0
    return jsonify({"response": [msg]})


@app.route("/login2", methods=["POST","GET"])
def login2():
    lang =   dict(request.form)['lang']
    lis = text_translator(lang)
    return jsonify({"response": [lis, lang]})



if __name__ == '__main__':
    app.run(debug=False, host="192.168.43.45", port=5000)
