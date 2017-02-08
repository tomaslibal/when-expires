# checks `when-expires` date for your certificates

Uses the Fabric library (so you'll need Python and Fabric). Can check both website certificates and certificates on a filesystem.

## Check an arbitrary certificate file on a filesystem

```
fab check_cert
```

Specify the hosts and the certificate paths on those hosts in the `host.txt` file, e.g.:

```
host1.example.org /some/foo/cert.pem
10.0.0.168 /bar/foo/cert.crt
```

This relies on the host having `openssl` installed.

## Check a certificate on a website

```
fab check_web
```

Specify the websites in the `web.txt` file, e.g.:

```
example.com
foo.example.com
```

## Example output

Website certificates

```
localhost:('secure.example.com', 'secure.example.com') OK (expires in 29 days)

```

Remote certificates on hosts

```
checking on example.service.corp
example.service.corp:/etc/ssl/cert/example.pem OK (expires in 362 days)
example.service.corp:/etc/ssl/service-foo/expired.pem EXPIRED!
```
