#!flask/bin/python
import process
from flask import Flask, jsonify, abort, make_response, request, url_for
import json
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

call = Flask(__name__)

#Get Password
@auth.get_password
def get_password(username):
        if username == 'miguel':
                return 'python'
        return None

@auth.error_handler
def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)

#Error Handler
@call.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

#READ all interfaces on bridge(GET)
@call.route('/flask/<string:bridge>', methods=['GET'])
@auth.login_required
def read_interface_ovsbr(bridge):
        return process.read_interface_br(bridge)

#READ all bridges that contains interface(GET)
@call.route('/flask/<string:interface>', methods=['GET'])
@auth.login_required
def read_ovsbr_interface(interface):
        return process.read_br_interface(interface)

if __name__ == '__main__':
        call.run(debug=True)
