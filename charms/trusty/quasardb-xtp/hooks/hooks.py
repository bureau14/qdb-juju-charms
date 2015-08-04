#!/usr/bin/env python

from charmhelpers.core import hookenv
from utils import set_peer

import sys

hooks = hookenv.Hooks()

def restart_qdbd():
    hookenv.log('now restarting qdbd node')
    from charmhelpers.core.services.base import service_restart
    service_restart('qdbd')

# should we sanitize the address?
def get_this_hostname():
    return hookenv.unit_get('private-address')

def get_this_port(port_name):
    return hookenv.config(port_name)

def get_leader_hostname():
    return hookenv.leader_get('leader_hostname')

def get_leader_port():
    return hookenv.leader_get('leader_port')

def return_information(info_type, hostname, port):
    return { 'hostname': hostname, 'port': port, 'type': info_type }

# we peer to a singled elected leader node, otherwise we will spend our time restarting qdb nodes

def peer_to_leader():
    host = get_leader_hostname()
    port = get_leader_port()

    if len(host) > 0:
        # we need to update the qdb node configuration, stop the service and restart it
        set_peer(host, port)

        hookenv.log(get_this_hostname() + ':' + str(get_this_port('qdb_port')) + ' now peering to leader ' + host + ':' + str(port))
    
def make_this_leader():
    host = get_this_hostname()
    port = get_this_port('qdb_port')

    hookenv.leader_set(leader_hostname=host)
    hookenv.leader_set(leader_port=port)

    hookenv.log('leader elected: ' + host + ':' + str(port))    

# **********************************
#           leader hooks
# **********************************

@hooks.hook('leader-elected')
def leader_elected():
    
    if hookenv.is_leader():
        make_this_leader()
    else:
        # update peer information but don't restart the node
        peer_to_leader()

@hooks.hook('leader-settings-changed')
def leader_settings_changed():
    hookenv.log('leader settings changed')        

# **********************************
#            admin hooks
# **********************************

# someone wants to connect to the administration console
@hooks.hook('admin-relation-joined')
def admin_relation_joined():
    hookenv.log('admin relation joined')
    return hookenv.relation_set(hookenv.relation_id(), return_information('http', get_this_hostname(), get_this_port('admin_port')))

# **********************************
#           cluster hooks
# **********************************

# relation joined means someone is connecting to our cluster
# we don't have to do anything about our configuration, this is taken care of by the quasardb protocol
@hooks.hook('cluster-relation-joined')
def cluster_relation_joined():
    hookenv.log('cluster relation joined')
    return hookenv.relation_set(hookenv.relation_id(), return_information('qdb-cluster', get_this_hostname(), get_this_port('qdb_port')))

# relation changed means we got some information about a remote node to which we'd like to connect
# let's get that information to update our configuration file
@hooks.hook('cluster-relation-changed')
def cluster_relation_changed():
    hookenv.log('cluster relation changed')

    if not hookenv.is_leader():
        peer_to_leader()
        restart_qdbd()

# when a node quits the qdb cluster here is the number of things you have to do: 0

@hooks.hook('cluster-relation-broken')
def cluster_relation_broken():
    hookenv.log('cluster relation broken')

@hooks.hook('cluster-relation-departed')
def cluster_relation_departed():
    hookenv.log('cluster relation departed')

# **********************************
#           database hooks
# **********************************

# someone is connecting to the quasardb cluster, let us provide him with information
@hooks.hook('database-relation-joined')
def database_relation_joined():
    hookenv.log("database relation joined")
    return hookenv.relation_set(hookenv.relation_id(), return_information('qdb', get_this_hostname(), get_this_port('qdb_port')))

if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    hooks.execute(sys.argv)