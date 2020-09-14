import 'login.dart';
import 'package:flutter/material.dart';
import 'button.dart';
import 'package:animated_text_kit/animated_text_kit.dart';
import 'constants.dart';
import 'otp.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignUp extends StatefulWidget {
  List data2;
  SignUp(List data) {
    this.data2 = data;
  }
  @override
  _SignUpState createState() => _SignUpState(data2);
}

class _SignUpState extends State<SignUp> {
  List data3;
  _SignUpState(List data2) {
    this.data3 = data2;
  }
  String name;
  String phone;
  // url for flask api for Signup
  String url = "http://192.168.43.45:5000/signup";
  String url2 = "http://192.168.43.45:5000/signup2";
  List data;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(0.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Flexible(
              child: TyperAnimatedTextKit(
                text: [data3[0][0]],
                textStyle: TextStyle(
                    fontSize: 60.0,
                    fontWeight: FontWeight.w900,
                    color: Colors.redAccent),
              ),
            ),
            SizedBox(
              height: 5.0,
            ),
            Text(
              data3[0][1],
              style: TextStyle(
                  color: Colors.blueGrey,
                  fontSize: 25.0,
                  fontWeight: FontWeight.bold),
            ),
            SizedBox(
              height: 50.0,
            ),
            Text(
              data3[0][2],
              style: TextStyle(
                  color: Colors.brown,
                  fontSize: 30.0,
                  fontWeight: FontWeight.bold),
            ),
            SizedBox(
              height: 25.0,
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25.0),
              child: TextField(
                onChanged: (value) {
                  name = value;
                },
                decoration: kTextFieldDecoration.copyWith(
                  hintText: data3[0][3],
                ),
              ),
            ),
            SizedBox(
              height: 10.0,
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25.0),
              child: TextField(
                onChanged: (value) {
                  phone = value;
                },
                decoration: kTextFieldDecoration.copyWith(
                  hintText: data3[0][4],
                ),
              ),
            ),
            SizedBox(
              height: 10.0,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                RoundedButton(
                  buttonColor: Colors.green,
                  onPressed: () async {
                    // calling function to send data to flask app
                    this._getResponse();
                    await new Future.delayed(const Duration(seconds: 3));
                    if (data[0] == 0) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => OTP(data),
                        ),
                      );
                    }
                  },
                  text: data3[0][5],
                ),
                RoundedButton(
                  buttonColor: Colors.blue,
                  onPressed: () async {
                    this._getResponse2();
                    await new Future.delayed(const Duration(seconds: 3));
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => LoginScreen(data),
                      ),
                    );
                  },
                  text: data3[0][6],
                )
              ],
            ),
          ],
        ),
      ),
    );
  }

  http.Client _getClient() {
    return http.Client();
  }

  // function for sending data to flask app
  void _getResponse() {
    Map<String, dynamic> data7;
    if (name.length > 0 && phone.length > 0) {
      var client = _getClient();
      try {
        client.post(
          url,
          body: {"query1": name, "query2": phone, "lang": data3[1]},
        )..then((response) {
            data7 = jsonDecode(response.body);
            _passdata(data7["response"]);
          });
      } catch (e) {
        print("Failed -> $e");
      } finally {
        client.close();
      }
    }
  }

  // function for sending data to flask app
  void _getResponse2() {
    Map<String, dynamic> data7;
    var client = _getClient();
    try {
      client.post(
        url2,
        body: {"lang": data3[1]},
      )..then((response) {
          data7 = jsonDecode(response.body);
          _passdata(data7["response"]);
        });
    } catch (e) {
      print("Failed -> $e");
    } finally {
      client.close();
    }
  }

  void _passdata(List list) {
    data = list;
  }
}
