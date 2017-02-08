from fabric.api import run, env, hosts, task, runs_once
from fabric.state import output
from fabric.utils import fastprint
from certcheck import get_hosts, get_certs_to_check, check_certs, get_weblist, check_on_web

env.hosts = get_hosts()

output.running = False
output.status = False
output.stdout = False

@task
def check_cert():
    fastprint("checking on %s " % (env.host))
    check_certs(get_certs_to_check(env.host))

@task
@runs_once
def check_web():
    check_on_web(get_weblist())
