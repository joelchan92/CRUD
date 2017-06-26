import subprocess
from flask import Flask, jsonify

#CHECK bridge exist(ovs-vsctl bridge command)
def check_br(bridge):
    check = subprocess.call(['sudo', 'ovs-vsctl', 'br-exists', bridge])
    return check

#READ bridge(ovs-vsctl bridge command)
def read_br(bridge):
	read_bridge = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'bridge', bridge])
	return read_bridge

#CREATE bridge name(ovs-vsctl bridge command)
def create_br(bridge):
	create_bridge = subprocess.call(['sudo', 'ovs-vsctl', 'add-br', bridge])
	return create_bridge

#DELETE bridge(ovs-vsctl bridge command)
def delete_br(bridge):
	delete_bridge = subprocess.call(['sudo', 'ovs-vsctl', 'del-br', bridge])
	return delete_bridge

#UPDATE bridge(ovs-vsctl bridge command)
def update_br(bridge_old, bridge_new):
	delete_br(bridge_old)
	create_br(bridge_new)
	return read_br(bridge_new) 

#UPDATE bridge openflow version(ovs-vsctl bridge command)
def update_br_protocol(bridge, protocol):
	update_protocol = subprocess.call(['sudo', 'ovs-vsctl', '--', 'set', 'bridge', bridge, protocol])
	return update_protocol

#READ all interfaces on bridge(ovs-vsctl interface command)
def read_interface_br(bridge):
	read_all_interface = subprocess.check_output(['sudo', 'ovs-vsctl', 'list-ifaces', bridge])
	return read_all_interface

#READ all bridges that contains interface(ovs-vsctl interface command)
def read_br_interface(interface):
	read_all_bridge = subprocess.check_output(['sudo', 'ovs-vsctl', 'ifaces-to-br', interface])
	return read_all_bridge

#READ netflow(ovs-vsctl netflow command)
def read_nf(bridge):
	read_netflow = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'netflow', bridge])
	return read_netflow

#CREATE netflow(ovs-vsctl netflow command)
def create_nf(bridge, target, timeout):
	create_netflow = subprocess.call(['sudo', 'ovs-vsctl', '--', 'set', 'Bridge', bridge, 'netflow=@nf', '--', '--id=@nf', 'create', 'Netflow', target, timeout])
	return create_netflow

#UPDATE netflow(ovs-vsctl netflow command)
def update_nf(bridge, options):
	update_netflow = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'NetFlow', bridge, options])
	return update_netflow

#DELETE netflow(ovs-vsctl netflow command)
def delete_nf(bridge):
	delete_netflow = subprocess.call(['sudo', 'ovs-vsctl', 'clear', 'Bridge', bridge, 'netflow'])
	return delete_netflow

#READ qos(ovs-vsctl qos command)
def read_qos(interface):
	readqos = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'interface', interface])
	return readqos

#CREATE qos(ovs-vsctl qos command)
def create_qos(interface, qos):
	createqos = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, qos])
	return createqos

#DELETE qos ingress_policing_rate(ovs-vsctl qos command)
def delete_qos_rate(interface):
	deleteqosrate = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, 'ingress_policing_rate=0'])
	return deleteqosrate

#DELETE qos ingress_policing_burst(ovs-vsctl qos command)
def delete_qos_burst(interface):
        deleteqosburst = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, 'ingress_policing_burst=0'])
        return deleteqosburst

#UPDATE qos(ovs-vsctl qos command)
def update_qos(interface, qos):
        updateqos = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, qos])
        return updateqos

