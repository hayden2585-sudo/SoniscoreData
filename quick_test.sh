#!/bin/bash
# Quick Test Script for SoniscoreData Mobile Beta

echo "======================================"
echo "SoniscoreData - Quick Test Setup"
echo "======================================"
echo ""

# Check if Flask is installed
if ! command -v flask &> /dev/null; then
    echo "Installing Flask..."
    pip install flask
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "ngrok not found. Installing..."
    brew install ngrok
fi

echo ""
echo "📱 Starting web server..."
echo "1. Server will start on port 5000"
echo "2. ngrok will create public URL"
echo "3. Test on mobile devices"
echo ""

# Start ngrok in background
echo "🚀 Starting ngrok..."
ngrok http 5000 &
NGROK_PID=$!
sleep 3

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)

if [ -z "$NGROK_URL" ]; then
    echo "Could not get ngrok URL. Check ngrok status."
    echo "You can find it at: http://localhost:4040"
else
    echo ""
    echo "✅ Web app ready!"
    echo ""
    echo "📱 Share this URL with beta testers:"
    echo "   $NGROK_URL"
    echo ""
    echo "📊 Test the app:"
    echo "   1. Open URL on mobile device"
    echo "   2. Upload example_data.csv"
    echo "   3. Click 'Process Data'"
    echo "   4. View results"
    echo ""
    echo "🔧 Local access:"
    echo "   http://localhost:5000"
    echo ""
    echo "⏹️  To stop: Ctrl+C"
fi

echo ""
echo "Starting web server..."
python web_app.py

# Cleanup
kill $NGROK_PID 2>/dev/null