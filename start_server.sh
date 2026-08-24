#!/bin/bash
# Start SoniscoreData Web Server

echo "🚀 Starting SoniscoreData Web Server..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check dependencies
echo "📦 Checking dependencies..."
python3 -c "import flask, pandas, numpy" 2>/dev/null || {
    echo "Installing missing dependencies..."
    pip3 install flask pandas numpy matplotlib seaborn scikit-learn
}

# Get local IP
LOCAL_IP=$(ifconfig | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo ""
echo "✅ Dependencies ready!"
echo ""
echo "📱 Starting web server..."
echo ""
echo "🌐 Server will be available at:"
echo "   • Local:    http://localhost:5000"
echo "   • Network:  http://$LOCAL_IP:5000"
echo ""
echo "📋 To test on mobile:"
echo "   1. Connect phone to same WiFi as computer"
echo "   2. Open browser on phone"
echo "   3. Go to: http://$LOCAL_IP:5000"
echo ""
echo "🔗 Or use ngrok for public URL:"
echo "   1. Install ngrok: brew install ngrok"
echo "   2. Run: ngrok http 5000"
echo "   3. Share the https://*.ngrok.io URL"
echo ""
echo "⏹️  Press Ctrl+C to stop server"
echo ""
echo "======================================"
echo "Starting server now..."
echo "======================================"
echo ""

# Start the server
cd "$(dirname "$0")"
python3 web_app.py