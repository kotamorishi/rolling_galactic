# Serve text string for the UUID
from flask import Flask, request, redirect,url_for, render_template, jsonify
import urllib.parse

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
            content = f.readlines()[-1]
    except:
        return 'Not found :-( ' + sanitized_input, 404
    return content

@app.route('/update', methods=['GET'])
def redirect_to_index():
    return redirect(url_for('hello'))

@app.route('/update', methods=['POST'])
def submit_data():
    UUID = str(request.form.get('uuid'))  # Get uuid from the form
    message = str(request.form.get('message'))  # Get data from the form
    # print debug message
    print('UUID: ' + UUID)
    print('Message: ' + message)
    # Since uuid could have some special chars, sanitize uuid
    sanitized_input = urllib.parse.quote(UUID)
    print('sanitized_input: ' + sanitized_input)
    # write to file
    try:
        with open('uuid/' + sanitized_input, 'a') as f:
            f.write("\r\n" + message)
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
    return jsonify(data), 200

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=3999, debug=True)