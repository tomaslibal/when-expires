import logging

from fabric.api import run, env
from datetime import datetime


logging.basicConfig(filename='when-expires.log',level=logging.INFO)

def runcmd(cmd, args, on_success, on_error):
    logging.info('Running cmd [%s] %s', env.host, cmd)
    output = run(cmd % args)
    if output.succeeded:
        on_success(output, args)
    else:
        on_error(output, args)

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

def check_error(output, args):
    print "error checking the certificate"

def check_success(output, args):
    cert_path = args
    exp = output.split("=")[1]
    exp = datetime.strptime(exp, '%b %d %H:%M:%S %Y GMT')
    if exp > datetime.now():
        valid = (exp - datetime.now()).days
        print "%s:%s OK (expires in %d days)" % (env.host, cert_path, valid)
    else:
        print "%s:%s EXPIRED!" % (env.host, cert_path)

def check_certs(certs):
    for cert_path in certs:
        logging.info("checking %s", cert_path)
        runcmd('openssl x509 -enddate -noout -in %s', (cert_path), check_success, check_error)        

def check_on_web(urls):
    port = 443
    for url in urls:
         o = run('echo | openssl s_client -connect %s.com:443 2>/dev/null | openssl x509 -noout -dates' % (url))         
