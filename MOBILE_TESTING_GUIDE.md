# SoniscoreData - Mobile Beta Testing Guide

## 📱 Beta Tester Distribution Options

### Option 1: Web App (Easiest - No Install Required)
**Best for**: Quick feedback, no setup required
**Platform**: iOS Safari, Android Chrome

**Steps to Create Web Version:**
1. **Create simple web interface**:
   ```bash
   cd SoniscoreData
   mkdir -p static/templates
   ```

2. **Create HTML interface** (`static/templates/index.html`):
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>SoniscoreData</title>
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <style>
           body { font-family: Arial, sans-serif; margin: 20px; }
           .container { max-width: 600px; margin: 0 auto; }
           .upload-area { border: 2px dashed #ccc; padding: 20px; text-align: center; }
           .result { margin-top: 20px; padding: 15px; background: #f5f5f5; }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>📊 SoniscoreData</h1>
           <p>Upload your data file to calculate scores</p>
           
           <div class="upload-area">
               <input type="file" id="fileInput" accept=".csv,.xlsx,.json">
               <p>Supported: CSV, Excel, JSON</p>
           </div>
           
           <button id="processBtn" style="margin-top: 20px; padding: 10px 20px;">
               Process Data
           </button>
           
           <div id="results" class="result" style="display: none;">
               <h3>Results:</h3>
               <p id="output"></p>
           </div>
       </div>
       
       <script>
           document.getElementById('processBtn').addEventListener('click', async () => {
               const file = document.getElementById('fileInput').files[0];
               if (!file) {
                   alert('Please select a file first');
                   return;
               }
               
               const formData = new FormData();
               formData.append('file', file);
               
               try {
                   const response = await fetch('/process', { method: 'POST', body: formData });
                   const result = await response.json();
                   document.getElementById('output').textContent = JSON.stringify(result, null, 2);
                   document.getElementById('results').style.display = 'block';
               } catch (error) {
                   alert('Error processing file: ' + error.message);
               }
           });
       </script>
   </body>
   </html>
   ```

3. **Create Flask web app** (`web_app.py`):
   ```python
   from flask import Flask, request, render_template, jsonify
   from data_processor import DataProcessor
   import os
   
   app = Flask(__name__, template_folder='static/templates')
   processor = DataProcessor()
   
   @app.route('/')
   def index():
       return render_template('index.html')
   
   @app.route('/process', methods=['POST'])
   def process():
       if 'file' not in request.files:
           return jsonify({'error': 'No file provided'}), 400
       
       file = request.files['file']
       if file.filename == '':
           return jsonify({'error': 'No file selected'}), 400
       
       try:
           # Save uploaded file temporarily
           temp_path = f'/tmp/{file.filename}'
           file.save(temp_path)
           
           # Process data
           df = processor.load_data(temp_path)
           df_clean = processor.clean_data(df)
           df_scored = processor.calculate_scores(df_clean)
           
           # Return results
           return jsonify({
               'rows': len(df_scored),
               'columns': list(df_scored.columns),
               'top_scores': df_scored.nlargest(5, 'composite_score')[['name', 'composite_score', 'rank']].to_dict('records') if 'name' in df_scored.columns else [],
               'summary': {
                   'mean_score': float(df_scored['composite_score'].mean()),
                   'max_score': float(df_scored['composite_score'].max()),
                   'min_score': float(df_scored['composite_score'].min())
               }
           })
       except Exception as e:
           return jsonify({'error': str(e)}), 500
       finally:
           # Clean up temp file
           if os.path.exists(temp_path):
               os.remove(temp_path)
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000, debug=True)
   ```

4. **Run web app**:
   ```bash
   pip install flask
   python web_app.py
   ```

5. **Share with testers**:
   - **Local network**: `http://YOUR_IP_ADDRESS:5000`
   - **ngrok** (temporary public URL):
     ```bash
     # Install ngrok
     brew install ngrok
     
     # Run ngrok
     ngrok http 5000
     
     # Share the https://*.ngrok.io URL with testers
     ```

### Option 2: Progressive Web App (PWA)
**Best for**: Native-like experience, offline capability

**Steps to Convert to PWA:**
1. **Add manifest.json** (`static/manifest.json`):
   ```json
   {
     "name": "SoniscoreData",
     "short_name": "Soniscore",
     "description": "Data processing and scoring application",
     "start_url": "/",
     "display": "standalone",
     "background_color": "#ffffff",
     "theme_color": "#2c3e50",
     "icons": [
       {
         "src": "/static/icons/icon-192x192.png",
         "sizes": "192x192",
         "type": "image/png"
       },
       {
         "src": "/static/icons/icon-512x512.png",
         "sizes": "512x512",
         "type": "image/png"
       }
     ]
   }
   ```

2. **Add service worker** (`static/service-worker.js`):
   ```javascript
   self.addEventListener('install', event => {
     event.waitUntil(
       caches.open('soniscore-v1').then(cache => {
         return cache.addAll([
           '/',
           '/static/js/main.js',
           '/static/css/style.css'
         ]);
       })
     );
   });
   
   self.addEventListener('fetch', event => {
     event.respondWith(
       caches.match(event.request).then(response => {
         return response || fetch(event.request);
       })
     );
   });
   ```

3. **Add to index.html**:
   ```html
   <link rel="manifest" href="/static/manifest.json">
   <meta name="theme-color" content="#2c3e50">
   <meta name="apple-mobile-web-app-capable" content="yes">
   <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
   ```

4. **Test on mobile**:
   - iOS: Safari → Share → "Add to Home Screen"
   - Android: Chrome → Menu → "Install app"

### Option 3: Native Mobile App (Most Comprehensive)
**Best for**: Full native experience, app store distribution

**Option A: React Native**
1. **Create React Native project**:
   ```bash
   npx react-native init SoniscoreApp
   ```

2. **Install dependencies**:
   ```bash
   cd SoniscoreApp
   npm install axios react-native-fs
   ```

3. **Create main component** (`App.js`):
   ```javascript
   import React, { useState } from 'react';
   import { View, Text, Button, Alert, TextInput } from 'react-native';
   import RNFS from 'react-native-fs';
   import axios from 'axios';
   
   export default function App() {
     const [data, setData] = useState(null);
     const [inputText, setInputText] = useState('');
     
     const processData = async () => {
       try {
         const response = await axios.post('http://YOUR_IP:5000/process', {
           data: inputText
         });
         setData(response.data);
       } catch (error) {
         Alert.alert('Error', 'Failed to process data');
       }
     };
     
     return (
       <View style={{ padding: 20 }}>
         <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 20 }}>
           SoniscoreData
         </Text>
         <TextInput
           style={{ borderWidth: 1, padding: 10, marginBottom: 10 }}
           placeholder="Enter data (JSON format)"
           value={inputText}
           onChangeText={setInputText}
           multiline
         />
         <Button title="Process Data" onPress={processData} />
         {data && (
           <Text style={{ marginTop: 20 }}>
             Results: {JSON.stringify(data, null, 2)}
           </Text>
         )}
       </View>
     );
   }
   ```

4. **Build for testing**:
   ```bash
   # iOS
   npx react-native run-ios
   # Android
   npx react-native run-android
   ```

**Option B: Flutter**
1. **Create Flutter project**:
   ```bash
   flutter create soniscore_app
   ```

2. **Add dependencies** (`pubspec.yaml`):
   ```yaml
   dependencies:
     flutter:
       sdk: flutter
     http: ^1.1.0
     path_provider: ^2.1.0
   ```

3. **Create main widget** (`lib/main.dart`):
   ```dart
   import 'package:flutter/material.dart';
   import 'package:http/http.dart' as http;
   import 'dart:convert';
   
   void main() => runApp(SoniscoreApp());
   
   class SoniscoreApp extends StatelessWidget {
     @override
     Widget build(BuildContext context) {
       return MaterialApp(
         title: 'SoniscoreData',
         home: SoniscoreHome(),
       );
     }
   }
   
   class SoniscoreHome extends StatefulWidget {
     @override
     _SoniscoreHomeState createState() => _SoniscoreHomeState();
   }
   
   class _SoniscoreHomeState extends State<SoniscoreHome> {
     final TextEditingController _controller = TextEditingController();
     String _result = '';
     
     Future<void> _processData() async {
       try {
         final response = await http.post(
           Uri.parse('http://YOUR_IP:5000/process'),
           headers: {'Content-Type': 'application/json'},
           body: jsonEncode({'data': _controller.text}),
         );
         
         if (response.statusCode == 200) {
           setState(() {
             _result = jsonEncode(jsonDecode(response.body), indent: 2);
           });
         } else {
           setState(() {
             _result = 'Error: ${response.statusCode}';
           });
         }
       } catch (e) {
         setState(() {
           _result = 'Error: $e';
         });
       }
     }
     
     @override
     Widget build(BuildContext context) {
       return Scaffold(
         appBar: AppBar(title: Text('SoniscoreData')),
         body: Padding(
           padding: EdgeInsets.all(16.0),
           child: Column(
             children: [
               TextField(
                 controller: _controller,
                 decoration: InputDecoration(
                   labelText: 'Enter data (CSV format)',
                   border: OutlineInputBorder(),
                 ),
                 maxLines: 5,
               ),
               SizedBox(height: 16),
               ElevatedButton(
                 onPressed: _processData,
                 child: Text('Process Data'),
               ),
               SizedBox(height: 16),
               if (_result.isNotEmpty)
                 Text(
                   _result,
                   style: TextStyle(fontSize: 12),
                 ),
             ],
           ),
         ),
       );
     }
   }
   ```

### Option 4: QR Code Distribution (Most Secure)
**Best for**: Controlled access, enterprise testing

**Steps:**
1. **Create web app** (Option 1)
2. **Generate QR code**:
   ```bash
   # Install qrencode
   brew install qrencode
   
   # Generate QR code for your app URL
   qrencode -o soniscore_qr.png "https://your-app.ngrok.io"
   ```

3. **Share QR code** with testers:
   - Print QR codes on cards
   - Email QR codes
   - Display at testing locations

### Option 5: TestFlight (iOS Only)
**Best for**: iOS beta testing

**Steps:**
1. **Create iOS app** (React Native or Flutter)
2. **Archive for TestFlight**:
   ```bash
   # Using Xcode
   Product → Archive
   Distribute App → TestFlight
   ```

3. **Add testers**:
   - Go to App Store Connect
   - Users and Access → TestFlight
   - Add tester emails

4. **Share invitation** with testers

### Option 6: Google Play Beta (Android Only)
**Best for**: Android beta testing

**Steps:**
1. **Create Android app** (React Native or Flutter)
2. **Create alpha/beta track**:
   ```bash
   # Build APK for testing
   flutter build apk --release
   # or
   npx react-native build-android --variant=release
   ```

3. **Upload to Play Console**:
   - Go to Google Play Console
   - Create Internal testing track
   - Upload APK
   - Add tester emails

4. **Share invitation** with testers

## 📋 **Quick Comparison Table**

| Option | Complexity | Platform | Best For | Time to Setup |
|--------|------------|----------|----------|---------------|
| **Web App** | ⭐ Easy | All | Quick feedback, no install | 10 min |
| **PWA** | ⭐⭐ Medium | All | Native-like experience | 30 min |
| **React Native** | ⭐⭐⭐ Hard | iOS/Android | Full native app | 2 hours |
| **Flutter** | ⭐⭐⭐ Hard | iOS/Android | Cross-platform native | 2 hours |
| **QR Code** | ⭐ Easy | All | Secure distribution | 5 min |
| **TestFlight** | ⭐⭐⭐ Hard | iOS | iOS beta testing | 1 hour |
| **Play Console** | ⭐⭐⭐ Hard | Android | Android beta testing | 1 hour |

## 🎯 **Recommended Approach for Beta Testing**

### **Phase 1: Web App (Today)**
1. Create simple web interface
2. Deploy with ngrok for public URL
3. Share with testers immediately
4. Collect feedback

### **Phase 2: PWA (This Week)**
1. Add PWA capabilities
2. Test offline functionality
3. Gather user experience feedback

### **Phase 3: Native App (Next Month)**
1. Choose React Native or Flutter
2. Build native app
3. TestFlight/Play Console distribution
4. Full feature set

## 🔧 **Quick Web App Setup**

**Want to start testing today?** Run this:

```bash
# 1. Navigate to your project
cd /Users/haydenjohnson/.agnes/temporary/2026-08-24/20260824_1/work/SoniscoreData

# 2. Install Flask
pip install flask

# 3. Create web app files
mkdir -p static/templates
```

**Then create these files:**
- `web_app.py` (server)
- `static/templates/index.html` (interface)
- `static/manifest.json` (PWA)

**Start testing:**
```bash
# Run web app
python web_app.py

# In another terminal, start ngrok
ngrok http 5000

# Share the https://*.ngrok.io URL with testers!
```

## 📱 **Tester Instructions**

**For web app testers:**
1. Open the shared URL on their mobile device
2. Upload a CSV/Excel file
3. Click "Process Data"
4. View results and provide feedback

**What testers should evaluate:**
- [ ] Interface usability
- [ ] Load time
- [ ] Processing accuracy
- [ ] Error handling
- [ ] Mobile responsiveness
- [ ] Feature completeness

**Ready to create the web app?** I can generate all the necessary files right now!