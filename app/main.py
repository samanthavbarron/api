"""Main API code"""

from dataclasses import dataclass
from functools import wraps
import logging
import os

from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

@dataclass
class AppConfig:
    host: str
    port: int
    debug: bool

host = os.getenv("API_HOST")
port = os.getenv("API_PORT")
if port:
    port = int(port)


app_config = AppConfig(
    host = host if host else "0.0.0.0",
    port = port if port else 5000,
    debug = False,
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1000 * 100

@dataclass
class QRCode:
    url: str
    mode: str | None = None

qr_code = QRCode(
    url = os.getenv("API_QR_DEFAULT", "https://google.com"),
    mode = None,
)

def get_key(key_env_name):
    API_KEY = os.getenv(key_env_name)
    if not API_KEY:
        raise ValueError('API_KEY environment variable is not set')
    return API_KEY

def check_api_key(request, key_name: str = "main"):
    KEY_DICT = {
        "main": os.getenv("API_KEY"),
    }

    provided_key = request.headers.get('x-api-key')

    if provided_key and provided_key == KEY_DICT[key_name]:
        return True
    
    logger.error(f"Invalid key received: {provided_key}")
    return False


def require_api_key(api_key_name: str = "main"):
    def _require_api_key(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if check_api_key(request, key_name=api_key_name):
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

@app.route("/qr", methods=["GET", "POST"])
def qr():
    if request.method == "GET":
        return redirect(qr_code.url, code=302)

    elif request.method == "POST":
        if not check_api_key(request):
            return jsonify(error="API key is missing or incorrect"), 403

        request_data = request.get_json()
        if "url" not in request_data:
            return jsonify(error="URL is missing"), 400
        else:
            qr_code.url = request_data["url"]
            return jsonify(
                message="URL updated successfully",
                new_url=qr_code.url,
            ), 200
    else:
        return jsonify(error="Method not allowed"), 405


if __name__ == '__main__':
    logging.basicConfig(filename="api.log", level=logging.DEBUG)
    logging.info("Starting app...")
    app.run(
        host=app_config.host,
        port=app_config.port,
        debug=app_config.debug
    )
