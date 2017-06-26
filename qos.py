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

#READ qos interface(GET)
@call.route('/flask/<string:interface>', methods=['GET'])
@auth.login_required
def read_ovsqos(interface):
	check = process.check_br(interface)
	if check == 0:
		return jsonify({'qos': process.read_qos(interface)
							})
	else:
		return error(500, 'The QOS interface specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#CREATE qos interface(POST)
@call.route('/flask', methods=['POST'])
@auth.login_required
def create_ovsqos():
	interface = request.json['interface']
	qos = request.json['qos']
	check = process.check_br(interface)
	if check == 0:
		process.create_qos(interface, qos)
		return jsonify({'interface': interface,
				'qos': qos
						})
	else:
		return error(500, 'The QOS interface specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#DELETE qos interface ingress_policing_rate/ingress_policing_burst(DELETE)
@call.route('/flask/<string:interface>', methods=['DELETE'])
@auth.login_required
def delete_ovsqosrate(interface):
	check = process.check_br(interface)
	if check == 0:
		process.delete_qos_rate(interface)
		process.delete_qos_burst(interface)
		return jsonify({'result': True,
				'interface resetted back to 0': interface
								})
	else:
		return error(500, 'The QOS interface specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

#UPDATE qos interface(UPDATE)
@call.route('/flask', methods=['PUT'])
@auth.login_required
def update_ovsqos():
        interface = request.json['interface']
        qos = request.json['qos']
	check = process.check_br(interface)
	if check == 0:
        	process.create_qos(interface, qos)
        	return jsonify({'interface': interface,
                	        'qos': qos
                        	                })
	else:
		return error(500, 'The QOS interface specified does not match or does not exist', 'Use (ovs-vsctl show) for list of bridges')

if __name__ == '__main__':
	call.run(debug=True)
