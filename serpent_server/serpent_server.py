from flask import Flask, request
import db

#
# To run locally:
#
# FLASK_APP=ip_assignment_tool.py flask run --host=0.0.0.0
#

app = Flask(__name__)
application = app # Needed for ElasticBeanstalk

# TODO: Integrate encryption

@app.route('/index.html', methods=['GET'])
def fetch():
    token = request.args.get('uuid', None)

    # TODO: Also return an empty response if the token fails validation /
    # does not match an active op token
    if token == None:
        return ''

    # TODO: Integrate encrypted / mac'ed tokens and payloads
    # TODO: Lookup current payload based on the token
    return 'ACK'

@app.route('/submit', methods=['POST'])
def post():
    pass

@app.route('/save', methods=['POST'])
def stage():
    pass

@app.route('/info.html', methods=['GET'])
def reset():
    pass

# TODO: Add configuration (post and get)
@app.route('/config', methods=['GET', 'POST'])
def configure():
    pass
