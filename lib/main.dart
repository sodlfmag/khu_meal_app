import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:photo_view/photo_view.dart';
import 'package:photo_view/photo_view_gallery.dart';
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
  String selectedField = "seoul_chungwoon";

  final Map<String, String> tabMapping = {
    "서울캠 청운관": "seoul_chungwoon",
    "서울캠 푸른솔": "seoul_puruensol",
    "국제캠 학생회관": "global_studentunion",
    "국제캠 제2기숙사": "global_dorm2",
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('경희대 학식 알리미')),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(color: Colors.blue),
              child: Text('식당 선택', style: TextStyle(color: Colors.white, fontSize: 24)),
            ),
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
          future: FirebaseFirestore.instance.collection("menu_links").doc("latest").get(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return CircularProgressIndicator();
            } else if (snapshot.hasError) {
              return Text("데이터 로드 중 에러 발생: ${snapshot.error}");
            } else if (!snapshot.hasData || !snapshot.data!.exists) {
              if (selectedField == "global_dorm2") {
                return _buildImageWidget(
                  context,
                  "https://via.placeholder.com/300?text=국제캠+제2기숙사",
                );
              }
              return Text("데이터를 찾을 수 없습니다.");
            } else {
              var data = snapshot.data!.data()!;
              String? imageUrl = data[selectedField];

              if (selectedField == "global_dorm2" && (imageUrl == null || imageUrl.isEmpty)) {
                imageUrl = "https://via.placeholder.com/300?text=국제캠+제2기숙사";
              }

              if (imageUrl == null || imageUrl.isEmpty) {
                return Text("이미지 URL이 없습니다.");
              }

              return _buildImageWidget(context, imageUrl);
            }
          },
        ),
      ),
    );
  }

  Widget _buildImageWidget(BuildContext context, String imageUrl) {
    return InkWell(
      onTap: () => _showImageDialog(context, imageUrl),
      child: Image.network(
        imageUrl,
        fit: BoxFit.cover,
        loadingBuilder: (context, child, loadingProgress) {
          if (loadingProgress == null) return child;
          return Center(child: CircularProgressIndicator());
        },
        errorBuilder: (context, error, stackTrace) {
          return Icon(Icons.error, size: 50, color: Colors.red);
        },
      ),
    );
  }

void _showImageDialog(BuildContext context, String imageUrl) {
  showDialog(
    context: context,
    builder: (context) {
      return Container(
        width: MediaQuery.of(context).size.width, // 전체 너비로 설정
        height: MediaQuery.of(context).size.height, // 전체 높이로 설정
        color: Colors.black87, // 배경색 설정
        child: Stack(
          children: [
            PhotoView(
              imageProvider: NetworkImage(imageUrl),
              backgroundDecoration: BoxDecoration(color: Colors.black87),
              minScale: PhotoViewComputedScale.contained,
              maxScale: PhotoViewComputedScale.covered * 2.5,
            ),
            Positioned(
              top: 20,
              right: 20,
              child: IconButton(
                icon: Icon(Icons.close, color: Colors.white, size: 30),
                onPressed: () => Navigator.pop(context), // 닫기 버튼 클릭 시 다이얼로그 닫기
              ),
            ),
          ],
        ),
      );
    },
  );
}
}
