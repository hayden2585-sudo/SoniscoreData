#!/usr/bin/env python3
"""
SoniscoreData Mini App Store
Simple web-based app store for distributing beta versions
"""

from flask import Flask, request, render_template, jsonify, send_file, abort
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

app = Flask(__name__, template_folder='templates')

# App store configuration
APP_STORE_CONFIG = {
    'app_name': 'SoniscoreData',
    'version': '1.0.0',
    'description': 'Data processing and scoring application with mobile support',
    'developer': 'Hayden Johnson',
    'category': 'Utilities',
    'tags': ['data', 'processing', 'scoring', 'mobile', 'android'],
    'screenshots': ['screenshot1.png', 'screenshot2.png'],
    'requirements': ['Python 3.8+', 'Flask', 'pandas', 'numpy'],
    'features': [
        'CSV/Excel/JSON data processing',
        'Composite score calculation',
        'Data visualization',
        'Mobile-friendly web interface',
        'Android-optimized version',
        'Command-line interface',
        'Unit tests included'
    ],
    'supported_platforms': ['Web', 'Android', 'iOS'],
    'download_count': 0,
    'rating': 0.0,
    'reviews': []
}

# Mock database for apps
APPS_DB = {
    'soniscoredata': APP_STORE_CONFIG.copy()
}

# Mock database for downloads
DOWNLOADS_DB = {}

# Mock database for reviews
REVIEWS_DB = {}


@app.route('/')
def app_store_index():
    """Main app store page."""
    return render_template('app_store/index.html', apps=APPS_DB)


@app.route('/app/<app_id>')
def app_detail(app_id):
    """App detail page."""
    app = APPS_DB.get(app_id)
    if not app:
        abort(404)
    
    # Get downloads and reviews
    downloads = DOWNLOADS_DB.get(app_id, [])
    reviews = REVIEWS_DB.get(app_id, [])
    
    # Calculate rating
    if reviews:
        app['rating'] = sum(r['rating'] for r in reviews) / len(reviews)
    else:
        app['rating'] = 0.0
    
    return render_template('app_store/detail.html', app=app, downloads=downloads, reviews=reviews)


@app.route('/download/<app_id>', methods=['POST'])
def download_app(app_id):
    """Handle app download."""
    app = APPS_DB.get(app_id)
    if not app:
        return jsonify({'error': 'App not found'}), 404
    
    # Increment download count
    app['download_count'] = app.get('download_count', 0) + 1
    
    # Record download
    download_record = {
        'timestamp': datetime.now().isoformat(),
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'ip_address': request.remote_addr,
        'platform': detect_platform()
    }
    
    if app_id not in DOWNLOADS_DB:
        DOWNLOADS_DB[app_id] = []
    DOWNLOADS_DB[app_id].append(download_record)
    
    # Return download link
    return jsonify({
        'success': True,
        'download_url': f"/api/download/{app_id}",
        'message': 'Download started!'
    })


@app.route('/api/download/<app_id>')
def api_download(app_id):
    """API endpoint for downloading app."""
    app = APPS_DB.get(app_id)
    if not app:
        return jsonify({'error': 'App not found'}), 404
    
    # Generate download link (in real app, this would be actual file)
    download_url = f"https://github.com/hayden2585-sudo/SoniscoreData/releases/download/v{app['version']}/{app_id}-v{app['version']}.zip"
    
    return jsonify({
        'success': True,
        'app_id': app_id,
        'version': app['version'],
        'download_url': download_url,
        'file_size': '2.5 MB',
        'checksum': hashlib.md5(app_id.encode()).hexdigest()
    })


@app.route('/review/<app_id>', methods=['POST'])
def add_review(app_id):
    """Add review for app."""
    app = APPS_DB.get(app_id)
    if not app:
        return jsonify({'error': 'App not found'}), 404
    
    data = request.get_json()
    if not data or 'rating' not in data or 'comment' not in data:
        return jsonify({'error': 'Rating and comment required'}), 400
    
    review = {
        'id': hashlib.md5(f"{app_id}{data['rating']}{data['comment']}".encode()).hexdigest(),
        'app_id': app_id,
        'rating': int(data['rating']),
        'comment': data['comment'],
        'timestamp': datetime.now().isoformat(),
        'user_id': request.remote_addr  # In real app, use proper user auth
    }
    
    if app_id not in REVIEWS_DB:
        REVIEWS_DB[app_id] = []
    REVIEWS_DB[app_id].append(review)
    
    return jsonify({'success': True, 'review': review})


@app.route('/search')
def search_apps():
    """Search for apps."""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'apps': list(APPS_DB.values())})
    
    # Simple search
    results = []
    for app_id, app in APPS_DB.items():
        if (query in app['app_name'].lower() or
            query in app['description'].lower() or
            any(query in tag.lower() for tag in app.get('tags', []))):
            results.append(app)
    
    return jsonify({'apps': results, 'total': len(results)})


@app.route('/stats')
def stats():
    """Get app store statistics."""
    total_downloads = sum(app.get('download_count', 0) for app in APPS_DB.values())
    total_reviews = sum(len(REVIEWS_DB.get(app_id, [])) for app_id in APPS_DB.keys())
    
    return jsonify({
        'total_apps': len(APPS_DB),
        'total_downloads': total_downloads,
        'total_reviews': total_reviews,
        'average_rating': sum(app.get('rating', 0) for app in APPS_DB.values()) / len(APPS_DB) if APPS_DB else 0
    })


def detect_platform():
    """Detect user platform."""
    ua = request.headers.get('User-Agent', '').lower()
    
    if 'android' in ua:
        return 'android'
    elif 'iphone' in ua or 'ipad' in ua or 'ios' in ua:
        return 'ios'
    elif 'windows' in ua:
        return 'windows'
    elif 'mac' in ua:
        return 'macos'
    elif 'linux' in ua:
        return 'linux'
    else:
        return 'unknown'


@app.route('/admin')
def admin_panel():
    """Admin panel for app store management."""
    return render_template('app_store/admin.html', apps=APPS_DB, downloads=DOWNLOADS_DB, reviews=REVIEWS_DB)


@app.route('/admin/app/<app_id>/update', methods=['POST'])
def update_app(app_id):
    """Update app information."""
    app = APPS_DB.get(app_id)
    if not app:
        return jsonify({'error': 'App not found'}), 404
    
    data = request.get_json()
    for key in ['description', 'features', 'tags', 'version']:
        if key in data:
            app[key] = data[key]
    
    return jsonify({'success': True, 'app': app})


@app.route('/admin/app/<app_id>/delete', methods=['POST'])
def delete_app(app_id):
    """Delete app from store."""
    if app_id in APPS_DB:
        del APPS_DB[app_id]
        if app_id in DOWNLOADS_DB:
            del DOWNLOADS_DB[app_id]
        if app_id in REVIEWS_DB:
            del REVIEWS_DB[app_id]
        return jsonify({'success': True})
    
    return jsonify({'error': 'App not found'}), 404


if __name__ == '__main__':
    print("=" * 50)
    print("🏪 SoniscoreData Mini App Store")
    print("=" * 50)
    print("🌐 App Store URL: http://localhost:8080")
    print("🔧 Admin Panel: http://localhost:8080/admin")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8080, debug=True)