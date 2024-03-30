from functools import wraps

from flask import Flask, jsonify, request
import os

app = Flask(__name__)

def get_key(key_env_name):
    API_KEY = os.getenv(key_env_name)
    if not API_KEY:
        raise ValueError('API_KEY environment variable is not set')
    return API_KEY

def require_api_key(api_key_name: str = "main"):
    def _require_api_key(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            KEY_DICT = {
                "main": os.getenv("API_KEY"),
            }
            if request.headers.get('x-api-key') and request.headers.get('x-api-key') == KEY_DICT[api_key_name]:
                return fn(*args, **kwargs)
            else:
                return jsonify(error="API key is missing or incorrect"), 403
        return decorated_function
    return _require_api_key

@app.route('/health', methods=['POST'])
@require_api_key()
def health():
    request_data = request.get_json()
    return jsonify(message='Data received and processed successfully')

if __name__ == '__main__':
    app.run(debug=True)
