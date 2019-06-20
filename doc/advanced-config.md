# Advanced Configuration

hc-harvester tries to guess most of the configuration so you don't spend time on trying to fill-in some configuration file. But in some cases it may not be as clever as you'd expect and it's
better to provide configuration manually.
Using hosts and groups variables is an esay way to provide manual configuration. There are multiple places where this variable can be set. For consistancy reason, we'll use the inventory file (check [Ansible variable documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html) for more details).

#### Certificates

In order to connect to Solr and generate reports it is necessary to authenticate using SSL client certificate. IF your platform is using solr certificates shipped by Alfresco default installation, you should not need to provide any additionnal configuration. You may still need to read the notes about default ssl certificates in [/doc/ssl.md](/doc/ssl.md#Security-Considerations).

If you deployed your own certificates for solr you need to provide a client certificate in PEM format to be able to generate solr summary.
Details on creating the PEM format certificates can be found in [/doc/ssl.md](/doc/ssl.md#Generate-PEM-certificates).
Such certificate and its key can be specified using variables bellow:

```
[index_tiers:vars]
solr_client_cert=somecert.crt
solr_client_key=somekey.key
```

> files must be located in `yml/roles/solr/files`.

## Web applications contexts

It is possible to configure Alfresco Content Service, Share or even Solr to use differents tomcat contexts.
If your platform uses custom application contexts you must specify them as follow:

```
[all:vars]
solr_context: 'mysearch'
alfresco_context: 'myecm'
share_context: 'mycollab'
```

> The context refers to the name of the web application archive file (war file). If the context is translated by a reverse proxy this is not to take into consideration.

## Log file locations

There are hundreds of different ways of configuring application logs locations. As of now, hc-harvester will not try to guess the location where to find log files. It expects those to be where Alfresco applications normally puts them (being the `$CATALINA_BASE`). If this is not the case on your setup, please specify the log locations for each web applications.

```
[repo_tiers:vars]
alfresco_log_pattern=/var/log/alfresco/alfresco.log*

[share_tiers:vars]
share_log_pattern=/var/log/alfresco/share.log*

[index_tiers:vars]
solr_log_pattern=/var/log/alfresco/solr.log*
```

> Log location can be set per host if log location differs from hosts to hosts in the architecture

## Custom shared loader

Alfresco uses the tomcat shared loader feature to find additionnal resources (this is often refered to as the ${extension-root}.
This tool expect to find the such resources in the ${TOMCAT_HOME}/shared/classes/ directory. If the Alfresco extension folder is not located there
you need to manually set it as described bellow:                                                                                                                                              

```
[repo_tiers:vars]
alfresco_shared_loader=/opt/alfresco/extension-root

[share_tiers:vars]
share_shared_loader:/opt/share/extension-root
```

## Custom contentstore location

In case you have specified a custom contentstore location hc-harvester may not be able to retrieve it. If that location is set by modifying dir.root property and/or modifying dir.contenstore property (without involving custom properties in the value of that properties), then detection should work. But if you use custom property like for instance `dir.contentstore=${filer.mountpoint.root}/contentstore`, then we can't automatically detect that and you need to manually specify that folder using the `contentstore_directory` variable as shown bellow:

```
[repo_tiers]
alfresco1.domain.tld contentstore_directory=/filer/data/contentstore

```

## Disabling Autodetection

hc-harvester normally autodetects some parameters of you architecture. If this process fails for any reason, it is still possible to manually specify the parameters that would normally be auto-detected.

Setting all the variables bellow (namely, tomcat port & solr home), will skip autodetection.

> Autodetection relies on xml parsing which requires python lxml library. If this library is not present on target systems and cannot be installed (non-root permissions access or escalation) autodetection will fail.

### Tomcat port & scheme

hc-harvester needs to know which port tomcat instances is listening on. It normally guesses it reading the server.xml file but can be set with the following variable `webapp_server_port`.

```
[repo_tiers]
ecm1.domain.tld webapp_server_port=7979 webapp_server_scheme=http
ecm2.domain.tld webapp_server_port=9443 webapp_server_scheme=https
```

An hosts group is available to set the port to all hosts running tomcat at the same time if they all use the same port.

```
[repo_tiers]
ecm1.domain.tld
ecm2.domain.tld

[tomcat_servers:children]
repo_tiers
share_tiers

[tomcat_servers:vars]
webapp_server_port=9090
webapp_server_scheme=http
```

### Solr Home

the same autodetection mecanism is used to figure out what folder Solr is using as its home folder. Again this location can be set manually thus disabling autodetection.

```
[index_tiers]
search1.domain.tld solr_home=/some/folder/
search1.domain.tld solr_home=/some/other/folder/
```                                                                                                                                                                                           

