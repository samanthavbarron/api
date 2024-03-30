from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify(message='Hello, World!')

@app.route('/api/data', methods=['GET'])
def get_data():
    # Logic to retrieve data from database or other sources
    data = {'key': 'value'}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    # Logic to handle POST request data
    request_data = request.get_json()
    # Logic to process the data and store it
    # Return a response
    return jsonify(message='Data received and processed successfully')

if __name__ == '__main__':
    app.run(debug=True)
