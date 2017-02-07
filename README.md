# checks `when-expires` date for your certificates

Uses the Fabric library (so you'll need Python and Fabric)

```
fab check_cert
```

Specify the hosts and the certificate paths on those hosts in the `host.txt` file, e.g.:

```
host1.example.org /some/foo/cert.pem
10.0.0.168 /bar/foo/cert.pem
```
