import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

SCRIPT_DIR = Path(__file__).parent.absolute()
API_COLLECTION_PATH = SCRIPT_DIR / "webex_api_collection.json"
CONFIG_PATH = SCRIPT_DIR / "enabled_features.json"

def load_api_data():
    with open(API_COLLECTION_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_enabled_features():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_enabled_features(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

@app.route('/')
def index():
    return render_template('config.html')

@app.route('/api/features')
def get_features():
    api_data = load_api_data()
    enabled = load_enabled_features()
    
    features = []
    for feature_name, endpoints in api_data['endpoints'].items():
        features.append({
            'name': feature_name,
            'count': len(endpoints),
            'enabled': enabled.get(feature_name, False),
            'endpoints': [{'title': ep['title'], 'method': ep['method'], 'path': ep['path']} 
                         for ep in endpoints]
        })
    
    return jsonify(features)

@app.route('/api/save', methods=['POST'])
def save_config():
    config = request.json
    save_enabled_features(config)
    return jsonify({'success': True})

@app.route('/api/stats')
def get_stats():
    api_data = load_api_data()
    enabled = load_enabled_features()
    
    total = sum(len(eps) for eps in api_data['endpoints'].values())
    enabled_count = sum(len(api_data['endpoints'][f]) for f in enabled if enabled[f])
    
    return jsonify({
        'total': total,
        'enabled': enabled_count,
        'features_total': len(api_data['endpoints']),
        'features_enabled': sum(1 for v in enabled.values() if v)
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Webex MCP Configuration Server")
    print("="*60)
    print("\nOpen in browser: http://localhost:5000")
    print("\nPress Ctrl+C to stop\n")
    app.run(debug=True, port=5000)
