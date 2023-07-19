# Certificates

## Security Considerations

This playbook contains the default client certificate and key which were disrtibuted as part of Alfresco 4.x and 5.x (for Solr 1.4 & Solr 4). Those certificates have been generated long ago and security requirement have largely evolved since then.
Running the playbook on modern distribution of Linux, you may encounter errors like:

```
140AB18F:SSL routines:SSL_CTX_use_certificate:ee key too small
```

> This is because your Linux distribution prevent you from using this client certificate (Distros shipping OpenSSL 1.1.1a-pre9 and beyond).                                                   

This client certificate is now very old and uses key length which are considered weak.
You should really consider using certificates from your own PKI instead!

> If you still need to use that certificate on modern Linux, you will need to lessen the security of the distribution. For example on Debian-like systems:
[https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1)

## Generate PEM certificates

If use your own PKI or you have re-generated the Solr certificates (as recommanded by Alfresco), you'll need to provide the client certificate and key in unencrypted PEM format.
Conversion can be done using openssl:

```
$ openssl pkcs12 -in yml/roles/solr/files/mypkicert.p12 -nokeys -clcerts -out yml/roles/solr/files/mypkicert.crt
$ openssl pkcs12 -in yml/roles/solr/files/mypkicert.p12 -nocerts -nodes -out yml/roles/solr/files/mypkicert.key
```

You can also use a single file for both certificate and key and only specify `solr_client_cert` configuration variable:

```
$ openssl pkcs12 -in mypkicert.p12 -clcerts -nodes -out mypkicert.pem
```

