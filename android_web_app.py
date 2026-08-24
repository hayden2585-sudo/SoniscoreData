#!/usr/bin/env python3
"""
SoniscoreData - Android-Compatible Web Application
Lightweight Flask app for mobile beta testing
No heavy dependencies required on Android device
"""

from flask import Flask, request, render_template, jsonify
import csv
import json
import io
import os
import tempfile
from pathlib import Path

app = Flask(__name__, template_folder='templates')

# Configuration
UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'csv', 'txt'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_csv_data(file_content):
    """Parse CSV data without pandas for Android compatibility."""
    try:
        # Decode bytes to string
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')
        
        # Parse CSV
        reader = csv.DictReader(io.StringIO(file_content))
        data = list(reader)
        
        if not data:
            return None, "No data found in CSV"
        
        # Convert numeric columns
        numeric_columns = []
        for key in data[0].keys():
            try:
                float(data[0][key])
                numeric_columns.append(key)
            except (ValueError, TypeError):
                pass
        
        # Calculate scores (simple normalization)
        for row in data:
            # Calculate composite score (average of numeric columns)
            numeric_values = []
            for col in numeric_columns:
                try:
                    value = float(row[col])
                    numeric_values.append(value)
                except (ValueError, TypeError):
                    pass
            
            if numeric_values:
                row['composite_score'] = sum(numeric_values) / len(numeric_values)
            else:
                row['composite_score'] = 0.0
        
        return data, None
    
    except Exception as e:
        return None, f"Error parsing CSV: {str(e)}"


def parse_json_data(file_content):
    """Parse JSON data without heavy dependencies."""
    try:
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')
        
        data = json.loads(file_content)
        
        # Handle different JSON formats
        if isinstance(data, dict):
            if 'data' in data:
                data = data['data']
            elif 'records' in data:
                data = data['records']
            else:
                data = [data]
        
        if not isinstance(data, list):
            return None, "Invalid JSON format"
        
        # Calculate scores
        numeric_columns = []
        for row in data:
            for key in row.keys():
                if isinstance(row[key], (int, float)):
                    if key not in numeric_columns:
                        numeric_columns.append(key)
        
        for row in data:
            numeric_values = []
            for col in numeric_columns:
                if col in row:
                    try:
                        numeric_values.append(float(row[col]))
                    except (ValueError, TypeError):
                        pass
            
            if numeric_values:
                row['composite_score'] = sum(numeric_values) / len(numeric_values)
            else:
                row['composite_score'] = 0.0
        
        return data, None
    
    except Exception as e:
        return None, f"Error parsing JSON: {str(e)}"


@app.route('/')
def index():
    """Main page for Android testing."""
    return render_template('android_index.html')


@app.route('/process', methods=['POST'])
def process_data():
    """Process uploaded data file (Android-compatible)."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: CSV, TXT, JSON'}), 400
    
    try:
        # Read file content
        file_content = file.read()
        
        # Parse based on file type
        if file.filename.endswith('.json'):
            data, error = parse_json_data(file_content)
        else:
            # Assume CSV for .csv and .txt
            data, error = parse_csv_data(file_content)
        
        if error:
            return jsonify({'error': error}), 400
        
        if not data:
            return jsonify({'error': 'No data found'}), 400
        
        # Calculate statistics
        scores = [row.get('composite_score', 0) for row in data]
        
        response = {
            'success': True,
            'rows_processed': len(data),
            'columns': list(data[0].keys()) if data else [],
            'summary': {
                'mean_score': sum(scores) / len(scores) if scores else 0,
                'max_score': max(scores) if scores else 0,
                'min_score': min(scores) if scores else 0,
                'median_score': sorted(scores)[len(scores)//2] if scores else 0,
            },
            'top_scores': [],
            'bottom_scores': []
        }
        
        # Get top and bottom scores if name column exists
        if 'name' in data[0] and data:
            sorted_data = sorted(data, key=lambda x: x.get('composite_score', 0), reverse=True)
            response['top_scores'] = sorted_data[:5]
            response['bottom_scores'] = sorted_data[-5:][::-1]
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/process_inline', methods=['POST'])
def process_inline():
    """Process inline JSON data (Android-compatible)."""
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Parse and process data
        processed_data, error = parse_json_data(data['data'])
        
        if error:
            return jsonify({'error': error}), 400
        
        if not processed_data:
            return jsonify({'error': 'No data found'}), 400
        
        # Calculate statistics
        scores = [row.get('composite_score', 0) for row in processed_data]
        
        response = {
            'success': True,
            'rows_processed': len(processed_data),
            'columns': list(processed_data[0].keys()) if processed_data else [],
            'summary': {
                'mean_score': sum(scores) / len(scores) if scores else 0,
                'max_score': max(scores) if scores else 0,
                'min_score': min(scores) if scores else 0,
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'SoniscoreData (Android-compatible)',
        'version': '1.0.0-android'
    })


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    return jsonify({
        'service': 'SoniscoreData API',
        'version': '1.0.0-android',
        'endpoints': ['/process', '/process_inline', '/health'],
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'notes': [
            'Android-compatible version',
            'No pandas/numpy required',
            'Lightweight CSV/JSON processing',
            'Works on all mobile devices'
        ]
    })


@app.route('/android-test')
def android_test():
    """Android-specific test page."""
    return render_template('android_test.html')


if __name__ == '__main__':
    print("=" * 50)
    print("🤖 SoniscoreData - Android-Compatible Web App")
    print("=" * 50)
    print("✅ No pandas/numpy required")
    print("✅ Lightweight CSV/JSON processing")
    print("✅ Works on all Android devices")
    print("🌐 Server starting...")
    print()
    print("To test on Android:")
    print("1. Find your IP: ifconfig | grep 'inet ' | grep -v 127.0.0.1")
    print("2. Run: python3 android_web_app.py")
    print("3. Access from Android: http://YOUR_IP:5000")
    print()
    print("Or use ngrok for public URL:")
    print("  ngrok http 5000")
    print()
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)