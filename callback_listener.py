from flask import Flask, request

# Setup instructions:
#
# $ pip install Flask
# $ FLASK_APP=callback_listener.py flask run
#
# See http://flask.pocoo.org/ for more details

# How to send test request:
#  curl -i -X POST -H 'Content-Type: application/{"key":"posted value"}' http://127.0.0.1:5000
#
# Taken from https://stackoverflow.com/questions/4797534/how-do-i-manually-fire-http-post-requests-with-firefox-or-chrome

app = Flask(__name__)
@app.route('/', methods=['POST'])
def result():
    print(request.values)
    return 'Received' # response to your request.
