from fabric.api import run, env, hosts, task
from fabric.state import output
from certcheck import get_hosts, get_certs_to_check, check_certs, get_weblist, check_on_web

env.hosts = get_hosts()

output.running = False
output.status = False
output.stdout = False

@task
def check_cert():
    current_host = env.host
    print "checking on %s " % (current_host)
    certs_to_check = get_certs_to_check(current_host)
    check_certs(certs_to_check)

@task
@hosts('localhost')
def check_web():
    web_certs = get_weblist()
    check_on_web(web_certs)
