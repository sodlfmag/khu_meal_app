import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'firebase_options.dart'; // flutterfire configure로 생성된 파일

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '경희대 학식 알리미',
      home: HomeScreen(),
    );
  }
}


class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // 기본 선택 탭: 서울캠 청운관 (Firestore 필드: seoul_chungwoon)
  String selectedField = "seoul_chungwoon";

  // Drawer에 표시할 메뉴와 Firestore 필드 매핑
  final Map<String, String> tabMapping = {
    "서울캠 청운관": "seoul_chungwoon",
    "서울캠 푸른솔": "seoul_puruensol",
    "국제캠 학생회관": "global_studentunion",
    "국제캠 제2기숙사": "global_dorm2",
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('경희대 학식 알리미'),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            // Drawer 헤더
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
              child: Text(
                '식당 선택',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            // 각 ListTile 생성
            for (String displayName in tabMapping.keys)
              ListTile(
                title: Text(displayName),
                onTap: () {
                  setState(() {
                    selectedField = tabMapping[displayName]!;
                  });
                  Navigator.pop(context);
                },
              ),
          ],
        ),
      ),
      body: Center(
        child: FutureBuilder<DocumentSnapshot<Map<String, dynamic>>>(
  future: FirebaseFirestore.instance
      .collection("menu_links")
      .doc("latest")
      .get(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return CircularProgressIndicator();
    } else if (snapshot.hasError) {
      return Text("데이터 로드 중 에러 발생: ${snapshot.error}");
    } else if (!snapshot.hasData || !snapshot.data!.exists) {
      if (selectedField == "global_dorm2") {
        return Image.network(
            "https://via.placeholder.com/300?text=국제캠+제2기숙사");
      }
      return Text("데이터를 찾을 수 없습니다.");
    } else {
      var data = snapshot.data!.data()!;
      String? imageUrl = data[selectedField];
      if (selectedField == "global_dorm2" &&
          (imageUrl == null || imageUrl.isEmpty)) {
        imageUrl =
            "https://via.placeholder.com/300?text=국제캠+제2기숙사";
      }
      if (imageUrl == null || imageUrl.isEmpty) {
        return Text("이미지 URL이 없습니다.");
      }
      return Image.network(imageUrl);
    }
  },
),
      ),
    );
  }
}
