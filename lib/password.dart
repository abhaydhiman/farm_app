import 'package:flutter/material.dart';
import 'button.dart';
import 'package:animated_text_kit/animated_text_kit.dart';
import 'constants.dart';
import 'home.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Password extends StatefulWidget {
  List data2;
  Password(List data) {
    this.data2 = data;
  }
  @override
  _PasswordState createState() => _PasswordState(data2);
}

class _PasswordState extends State<Password> {
  List data3;
  _PasswordState(List data2) {
    this.data3 = data2;
  }
  // url for flask api for Login
  String url = "http://192.168.43.45:5000/password";
  List data;
  String p1;
  String p2;
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
                text: [data3[1][0]],
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
              data3[1][1],
              style: TextStyle(
                  color: Colors.blueGrey,
                  fontSize: 25.0,
                  fontWeight: FontWeight.bold),
            ),
            SizedBox(
              height: 50.0,
            ),
            Text(
              data3[1][2],
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
                  p1 = value;
                },
                decoration: kTextFieldDecoration.copyWith(
                  hintText: data3[1][3],
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
                  p2 = value;
                },
                decoration: kTextFieldDecoration.copyWith(
                  hintText: data3[1][4],
                ),
              ),
            ),
            SizedBox(
              height: 10.0,
            ),
            RoundedButton(
              buttonColor: Colors.green,
              onPressed: () async {
                this._getResponse();
                await new Future.delayed(const Duration(seconds: 3));
                if (data[0] == 0) {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => HomeScreen(),
                    ),
                  );
                }
              },
              text: data3[1][5],
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
    if (p1.length > 0 && p2.length > 0) {
      var client = _getClient();
      try {
        client.post(
          url,
          body: {
            "query1": p1,
            "query2": p2,
            "lang": data3[1][6],
            "name": data3[2],
            "phone": data3[3]
          },
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

  void _passdata(List list) {
    data = list;
  }
}
