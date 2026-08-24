#!/usr/bin/env python3
"""
SoniscoreData - Web Application for Mobile Beta Testing
Simple Flask web app for mobile-friendly data processing
"""

from flask import Flask, request, render_template, jsonify, send_file
from data_processor import DataProcessor
import os
import tempfile
from pathlib import Path

app = Flask(__name__, template_folder='templates')
processor = DataProcessor()

# Configuration
UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_data():
    """Process uploaded data file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: CSV, Excel, JSON'}), 400
    
    try:
        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Process data
        df = processor.load_data(file_path)
        df_clean = processor.clean_data(df)
        df_scored = processor.calculate_scores(df_clean)
        
        # Prepare response
        response = {
            'success': True,
            'rows_processed': len(df_scored),
            'columns': list(df_scored.columns),
            'summary': {
                'mean_score': float(df_scored['composite_score'].mean()) if 'composite_score' in df_scored.columns else None,
                'max_score': float(df_scored['composite_score'].max()) if 'composite_score' in df_scored.columns else None,
                'min_score': float(df_scored['composite_score'].min()) if 'composite_score' in df_scored.columns else None,
                'median_score': float(df_scored['composite_score'].median()) if 'composite_score' in df_scored.columns else None,
            },
            'top_scores': [],
            'bottom_scores': []
        }
        
        # Get top and bottom scores if 'name' column exists
        if 'name' in df_scored.columns and 'composite_score' in df_scored.columns:
            top_5 = df_scored.nlargest(5, 'composite_score')[['name', 'composite_score', 'rank']]
            bottom_5 = df_scored.nsmallest(5, 'composite_score')[['name', 'composite_score', 'rank']]
            response['top_scores'] = top_5.to_dict('records')
            response['bottom_scores'] = bottom_5.to_dict('records')
        
        # Clean up
        os.remove(file_path)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/process_inline', methods=['POST'])
def process_inline():
    """Process inline JSON data."""
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Convert to DataFrame
        df = processor.load_data(pd.DataFrame(data['data']))
        df_clean = processor.clean_data(df)
        df_scored = processor.calculate_scores(df_clean)
        
        # Prepare response
        response = {
            'success': True,
            'rows_processed': len(df_scored),
            'columns': list(df_scored.columns),
            'summary': {
                'mean_score': float(df_scored['composite_score'].mean()) if 'composite_score' in df_scored.columns else None,
                'max_score': float(df_scored['composite_score'].max()) if 'composite_score' in df_scored.columns else None,
                'min_score': float(df_scored['composite_score'].min()) if 'composite_score' in df_scored.columns else None,
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'SoniscoreData'})


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    return jsonify({
        'service': 'SoniscoreData API',
        'version': '1.0.0',
        'endpoints': ['/process', '/process_inline', '/health'],
        'supported_formats': list(ALLOWED_EXTENSIONS)
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 SoniscoreData Web App")
    print("=" * 50)
    print(f"📱 Mobile-friendly interface")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"🌐 Server starting...")
    print()
    print("To test on mobile:")
    print("1. Find your IP: ifconfig | grep 'inet ' | grep -v 127.0.0.1")
    print("2. Run: python web_app.py")
    print("3. Access from mobile: http://YOUR_IP:5000")
    print()
    print("Or use ngrok for public URL:")
    print("  ngrok http 5000")
    print()
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)