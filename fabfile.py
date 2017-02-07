from fabric.api import run, env
from certcheck import get_hosts, get_certs_to_check, check_certs

env.hosts = get_hosts()

def check_cert():
    current_host = env.host
    print "checking on %s " % (current_host)
    certs_to_check = get_certs_to_check(current_host)
    check_certs(certs_to_check)

