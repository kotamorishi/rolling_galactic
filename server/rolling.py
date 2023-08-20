# Serve text string for the UUID
from flask import Flask, request, redirect,url_for, render_template, jsonify, make_response
import urllib.parse
import json

app = Flask(__name__)

@app.route('/<uuid>')
def get_uuid_string(uuid):
    # Since uuid could have some special chars, sanitize uuid
    sanitized_input = urllib.parse.quote(uuid)
    # read from file and return the content of file
    content = ''
    # try catch block to handle file not found
    try:
        with open('uuid/' + sanitized_input, 'r') as f:
            # read the last line of the file
            content = f.read();
    except:
        data = {
        'status': 'Not Found',
        'message': 'Requested uuid not found on this server.'
        }
        return jsonify(data), 404
    # respond with the content of the file in json format
    response = make_response(content)
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200

    return response

@app.route('/update', methods=['GET'])
def redirect_to_index():
    return redirect(url_for('hello'))

@app.route('/update', methods=['POST'])
def submit_data():
    UUID = str(request.form.get('uuid'))  # Get uuid from the form
    message = str(request.form.get('message'))  # Get data from the form
    color = str(request.form.get('colorpicker'))  # Get color from the form
    # print debug message
    # print('UUID: ' + UUID)
    # print('Message: ' + message)
    # print('Color: ' + color)

    #  Since uuid could have some special chars, sanitize uuid
    sanitized_input = urllib.parse.quote(UUID)

    data = {
        "color": color,
        "message": message,
        "city": "New York"
    }

    try:
        with open('uuid/' + sanitized_input, 'w') as json_file:
            json.dump(data, json_file)
    except:
        data = {
            'status': 'error',
            'message': 'something went wrong'
        }
        return jsonify(data), 500
    
    data = {
        'status': 'success',
        'message': 'data updated'
    }
    # log to 
    return jsonify(data), 200

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=3999, debug=True)