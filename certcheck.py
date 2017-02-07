import logging

from fabric.api import run, env
from fabric.utils import fastprint
from datetime import datetime


logging.basicConfig(filename='when-expires.log',level=logging.INFO)

def runcmd(cmd, args, on_success, on_error):
    logging.info('Running cmd [%s] %s', env.host, cmd)
    output = run(cmd % args)
    if output.succeeded:
        on_success(output, args)
    else:
        on_error(output, args)

def map_each_line(path, mapfn):
    mapped = []
    with open(path, 'r') as lines:
        for line in lines:
            mapped.append(mapfn(line))
    return mapped

def get_hosts():
    return map_each_line('hosts.txt', lambda line: line.split(' ')[0])    

def get_weblist():
    return map_each_line('web.txt', lambda line: line.rstrip('\n'))

def get_certs_to_check(selected_host):
    hosts_and_certs = map_each_line('hosts.txt', lambda line: line.split(' '))
    certs = filter(lambda (host, cert): host == selected_host, hosts_and_certs)
    certs = map(lambda (host, cert): cert.rstrip('\n'), certs)
    return certs

def check_error(output, args):
    fastprint('error checking the certificate %s\n' % (args))

def check_success(output, args):
    cert_path = args
    exp = output.split("=")[1]
    exp = datetime.strptime(exp, '%b %d %H:%M:%S %Y GMT')
    if exp > datetime.now():
        valid = (exp - datetime.now()).days
        fastprint('%s:%s OK (expires in %d days)\n' % (env.host, cert_path, valid))
    else:
        fastprint('%s:%s EXPIRED!\n' % (env.host, cert_path))

def check_certs(certs):
    for cert_path in certs:
        logging.info('checking %s', cert_path)
        runcmd('openssl x509 -enddate -noout -in %s', (cert_path), check_success, check_error)        

def check_on_web(urls):
    for host in urls:
         runcmd('echo | openssl s_client -servername %s -connect %s:443 2>/dev/null | openssl x509 -noout -enddate', (host, host), check_success, check_error)
