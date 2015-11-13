import os
import string
from flask import Flask, Response, request, abort, redirect

app = Flask(__name__)

def rotate():
    lookup_table = {}
    for coll in (string.ascii_lowercase, string.ascii_uppercase):
        for index, letter in enumerate(coll):
            if index < 13:
                lookup_table[letter] = coll[index+13]
            else:
                lookup_table[letter] = coll[index-13]
    return lookup_table

letter_map = rotate()

slack_command_token = os.environ['SLACK_COMMAND_TOKEN']
slash_command = '/rot13'

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/rot13', methods=['POST'])
def rot13():
    token = request.form['token']
    command = request.form['command']
    text = request.form['text']
    if token != slack_command_token or command != slash_command:
        abort(403)
    rotated_text_list = [letter_map.get(x, x) for x in text]
    return Response(''.join(rotated_text_list), content_type='text/plain')




if __name__ == '__main__':
    app.run()
