from fabric.api import run, env
from datetime import datetime

def get_hosts():
    hosts = []
    path = "hosts.txt"
    with open(path, "r") as lines:
        for line in lines:
            host, cert_path = line.split(" ")
            hosts.append(host)

    aux = set(hosts)
    return list(aux)

def get_certs_to_check(selected_host):
    certs = []
    path = "hosts.txt"
    with open(path, "r") as lines:
        for line in lines:
            host, cert_path = line.split(" ")
            if host == selected_host:
                certs.append(cert_path.rstrip('\n'))

    return certs

def check_certs(certs):
    for cert_path in certs:
        # cert_path = '/etc/ssl/foo/foo.pem'
        print "checking %s" % (cert_path)
        o = run('openssl x509 -enddate -noout -in ' + cert_path)
        if not o.succeeded:
            print "error checking..."
        else:
            exp = o.split("=")[1]
            exp = datetime.strptime(exp, '%b %d %H:%M:%S %Y GMT')
            if exp > datetime.now():
                valid = (exp - datetime.now()).days
                print "%s:%s OK (expires in %d days)" % (env.host, cert_path, valid)
            else:
                print "expired!!"
