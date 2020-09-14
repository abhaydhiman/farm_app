// Importing Packages
import 'package:flutter/material.dart';
import 'button.dart';
import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'signup.dart';
import 'dart:async';

// main class for language selection
class SelectLanguage extends StatefulWidget {
  @override
  _SelectLanguageState createState() => _SelectLanguageState();
}

// extended class for select language
class _SelectLanguageState extends State<SelectLanguage> {
  // final GlobalKey<AnimatedListState> _listKey = GlobalKey();
  // List<String> _data = [];

  // url for flask api for language select
  String url = "http://192.168.43.45:5000/lang";
  String _queryController;
  List data;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          TyperAnimatedTextKit(
            text: ['FarmTech'],
            textStyle: TextStyle(
                fontSize: 60.0,
                fontWeight: FontWeight.w900,
                color: Colors.redAccent),
          ),
          SizedBox(
            height: 5.0,
          ),
          Text(
            'Made For Nature',
            style: TextStyle(
                color: Colors.blueGrey,
                fontSize: 25.0,
                fontWeight: FontWeight.bold),
          ),
          SizedBox(
            height: 50.0,
          ),
          Text(
            'Choose Language',
            style: TextStyle(
                color: Colors.deepOrange,
                fontSize: 30.0,
                fontWeight: FontWeight.bold),
          ),
          SizedBox(
            height: 10.0,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              RoundedButton(
                buttonColor: Colors.redAccent,
                onPressed: () async {
                  // setting variable to the selected language
                  _queryController = 'Hindi';
                  // calling function to send data to flask app
                  this._getResponse();
                  await new Future.delayed(const Duration(seconds: 1));
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => SignUp(data),
                    ),
                  );
                },
                text: 'हिन्दी',
              ),
              RoundedButton(
                buttonColor: Colors.amber,
                onPressed: () async {
                  // setting variable to the selected language
                  _queryController = 'English';
                  // calling function to send data to flask app
                  this._getResponse();
                  await new Future.delayed(const Duration(seconds: 1));
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => SignUp(data),
                    ),
                  );
                },
                text: 'English',
              )
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              RoundedButton(
                buttonColor: Colors.green,
                onPressed: () async {
                  // setting variable to the selected language
                  _queryController = 'Marathi';
                  // calling function to send data to flask app
                  this._getResponse();
                  await new Future.delayed(const Duration(seconds: 1));
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => SignUp(data),
                    ),
                  );
                },
                text: 'मराठी',
              ),
              RoundedButton(
                buttonColor: Colors.blueAccent,
                onPressed: () async {
                  // setting variable to the selected language
                  _queryController = 'Tamil';
                  // calling function to send data to flask app
                  this._getResponse();
                  await new Future.delayed(const Duration(seconds: 1));
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => SignUp(data),
                    ),
                  );
                },
                text: 'తెలుగు',
              )
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              RoundedButton(
                buttonColor: Colors.deepOrangeAccent,
                onPressed: () async {
                  // setting variable to the selected language
                  _queryController = 'Haryanvi';
                  // calling function to send data to flask app
                  this._getResponse();
                  await new Future.delayed(const Duration(seconds: 1));
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => SignUp(data),
                    ),
                  );
                },
                text: 'हरियाणवी',
              ),
              RoundedButton(
                buttonColor: Colors.pinkAccent,
                onPressed: () async {
                  // setting variable to the selected language
                  _queryController = 'Punjabi';
                  // calling function to send data to flask app
                  this._getResponse();
                  await new Future.delayed(const Duration(seconds: 1));
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => SignUp(data),
                    ),
                  );
                },
                text: 'ਪੰਜਾਬੀ',
              )
            ],
          ),
        ],
      ),
    );
  }

  // fuction for http client
  http.Client _getClient() {
    return http.Client();
  }

  // function for sending data to flask app
  void _getResponse() {
    Map<String, dynamic> data2;
    if (_queryController.length > 0) {
      var client = _getClient();
      try {
        client.post(
          url,
          body: {"query": _queryController},
        )..then((response) {
            data2 = jsonDecode(response.body);
            _passdata(data2["response"]);
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
