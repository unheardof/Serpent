from flask import Flask, request
from multiprocessing import Process, Queue

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

def listen(listener_id, command_queue, response_queue, app_name, port):
    post_url_destination = '%s/post' % app_name
    get_url_destination = '%s/get' % app_name
    is_onetime_response = False
    get_function_response = None

    def handle_callback_post():
        response_queue.put({ 'listener_id': listener_id, 'response_values': request.values })
        return 'Received' # response to your request.

    def handle_callback_get():
        response = get_function_response
        if is_onetime_response:
            get_function_response = None
            is_onetime_response = False
            
        return response

    handle_callback_post.provide_automatic_options = False
    handle_callback_post.methods = ['POST']
        
    handle_callback_get.provide_automatic_options = False
    handle_callback_get.methods = ['GET']

    def start_app():
        app = Flask(app_name)
        app.add_url_rule('/', post_url_destination, handle_callback_post)
        app.add_url_rule('/', get_url_destination, handle_callback_get)
        app.run(host='0.0.0.0', port = port)

    while True:
        # Message structure: { 'message': '<message contents>', 'one-time-message': <True || False; defaults to False> }
        command_message = command_queue.get()
        if 'one-time-message' in command_message and command_message['one-time-message']:
            is_onetime_response = True

        get_function_response = command_message['message']

def start_listener(listener_id, command_queue, response_queue, app_name, port):
    listener_proc = Process(target=listen, args=(listener_id, command_queue, response_queue, app_name, port))
    listener_proc.start()

    return listener_proc
