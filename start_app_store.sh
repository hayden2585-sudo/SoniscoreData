#!/bin/bash
# Start SoniscoreData Mini App Store

echo "🏪 Starting SoniscoreData Mini App Store..."
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    pip3 install flask
fi

# Get local IP
LOCAL_IP=$(ifconfig | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo "📱 App Store URLs:"
echo "   • Main:     http://localhost:8080"
echo "   • Network:  http://$LOCAL_IP:8080"
echo "   • Admin:    http://localhost:8080/admin"
echo ""
echo "🤖 Android Test URLs:"
echo "   • Main:     http://localhost:5000/android-test"
echo "   • Network:  http://$LOCAL_IP:5000/android-test"
echo ""
echo "🔧 To create public URLs:"
echo "   App Store:  ngrok http 8080"
echo "   Android:    ngrok http 5000"
echo ""
echo "⏹️  Press Ctrl+C to stop"
echo ""

# Start app store in background
echo "🚀 Starting App Store on port 8080..."
python3 app_store.py &
APP_STORE_PID=$!

# Wait a moment
sleep 2

# Start Android app if not already running
if ! lsof -i :5000 >/dev/null 2>&1; then
    echo "🚀 Starting Android app on port 5000..."
    python3 android_web_app.py &
    ANDROID_PID=$!
    echo "Android app PID: $ANDROID_PID"
else
    echo "✅ Android app already running on port 5000"
fi

echo "App Store PID: $APP_STORE_PID"
echo ""
echo "🎉 App Store and Android app are running!"
echo "   Open http://localhost:8080 in your browser"
echo ""
echo "To stop: kill $APP_STORE_PID"
echo "         kill $ANDROID_PID (if started)"