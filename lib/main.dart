import 'package:flutter/material.dart';
import 'package:kisan_tech/select_language.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FARM-TECH',
      home: SelectLanguage(),
    );
  }
}
