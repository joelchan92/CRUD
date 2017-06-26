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

#READ bridge name(GET)
@call.route('/flask/<string:bridge>', methods=['GET'])
@auth.login_required
def read_ovsbr(bridge):
	check = process.check_br(bridge)
	if check == 0:
		process.read_br(bridge)
		return jsonify({'bridge': process.read_br(bridge)
					})
	else:
		return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#CREATE bridge name(POST)
@call.route('/flask', methods=['POST'])
@auth.login_required
def create_ovsbr():
	bridge = request.json['bridge']
	check = process.check_br(bridge)
	if check == 0:
		return error(500, 'The bridge specified exists', 'Please choose another bridge name')
	else:
		process.create_br(bridge)
                return jsonify({'bridge': bridge
                                         })

#DELETE bridge name(DELETE)
@call.route('/flask/<string:bridge>', methods=['DELETE'])
@auth.login_required
def delete_ovsbr(bridge):
	check = process.check_br(bridge)
	if check == 0:
		process.delete_br(bridge)
		return jsonify({'result': True,
				'bridge deleted': bridge
						})
        else:
                return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#UPDATE bridge name(UPDATE)
@call.route('/flask', methods=['PUT'])
@auth.login_required
def update_ovsbr():
	bridge_old = request.json['bridge_old']
	bridge_new = request.json['bridge_new']
	check = process.check_br(bridge_old)
	if check == 0:
		process.update_br(bridge_old, bridge_new)
		return jsonify({'old bridge': bridge_old,
				'new bridge': bridge_new
						})
	else:
		return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#UPDATE bridge openflow version(UPDATE)
@call.route('/flask/<string:bridge>/<string:protocol>', methods=['PUT'])
@auth.login_required
def update_ovsbr_protocol(bridge, protocol):
	check = process.check_br(bridge)
	if check == 0:
		process.update_br_protocol(bridge, protocol)
		return jsonify({'bridge': bridge,
				'openflow version': protocol
							})
	else:
                return error(500, 'The bridge specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

if __name__ == '__main__':
	call.run(debug=True)
