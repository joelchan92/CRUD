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

#Custom error handler instead of abusing abort()
def error(status_code, message, check):
    response = jsonify({
        'Status': status_code,
        'Error': message,
        'Fix': check
    })
    response.status_code = status_code
    return response

#READ bridge netflow(GET)
@call.route('/flask/<string:bridge>', methods=['GET'])
@auth.login_required
def read_ovsnf(bridge):
	check = process.check_br(bridge)
	if check == 0:
		return jsonify({'Netflow': process.read_nf(bridge)
							})
	else:
                return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#CREATE bridge netflow(POST)
@call.route('/flask', methods=['POST'])
@auth.login_required
def create_ovsnf():
	bridge = request.json['bridge']
	target = request.json['target']
	timeout = request.json['timeout']
	check = process.check_br(bridge)
	if check == 0:
		process.create_nf(bridge, target, timeout)
		return jsonify({'bridge': bridge,
				'target': target,
				'timeout': timeout
						})
	else:
		return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#DELETE bridge netflow(DELETE)
@call.route('/flask/<string:bridge>', methods=['DELETE'])
@auth.login_required
def delete_ovsnf(bridge):
	check = process.check_br(bridge)
	if check == 0:
		process.delete_nf(bridge)
		return jsonify({'result': True
				'bridge netflow deleted': bridge})
	else:
		return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges') 

#UPDATE bridge netflow(UPDATE)
@call.route('/flask', methods=['PUT'])
@auth.login_required
def update_ovsnf():
	bridge = request.json['bridge']
	options = request.json['options']
	check = process.check_br(bridge)
	if check == 0:
		process.update_nf(bridge, options)
		return jsonify({'bridge': bridge,
				'options': options
						})
	else:
		return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

if __name__ == '__main__':
	call.run(debug=True)
