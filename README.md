# Alfresco Healthcheck Harvester

This ansible playbook allows Alfresco Premier Services engineers to get informations in order to deliver an Healthcheck report to customers

## Requirements

### Software requirement

You of course need Ansible in order to use this playbook.
Tomcat port autodetection logic may not work if you're using Ansible lower than 2.4 as it uses the xml module.
This xml module in turn require python-lxml 2.3 or above, whi in turn require python 2.7. If you can't satisfy this requirement you may want to try disabling the Tomcat port autodeteection (see bellow).

Ansible-vault is also needed in order to store and access sensitive informations like passwords.

Remote machines will need python. Version 2.7 of python is recommended as a minimum. The playbook may stiil run on 2.6 if tomcat port autodetection is disabled.
SuSE based systems also need the python-xml module installed before being able to play the playbook.

You need SSH access to the target infrastructure together with administrative rights on the machine (small packages may be required - e.g. python2-lxml).
The playbook has been written and tested with Ansible 2.7.

### Architectural requirement

 - ***This playbook doesn't deploy SSH keys so please make sure you're using it on machines which already have the needed SSH keys.***
 - ***At the moment the target hosts need to have direct acces to internet as we are using public repos.***

## How to use:

### Prepare inventory file:

Edit the _inventory_ file and add your hostnames to the appropriate section (ansible inventory group):
 - repo_tiers: Those are the nodes which are running an `alfresco` webapp (regardless of wether this is used for ingestion, serving users requests or tracking
 - share_tiers: Those are the nodes which are running a `share` webapp
 - index_tiers: Those are the nodes which are running either a solr1.4 or solr4 webapp within a servlet container, or even solr6 throught the Alfresco Search Service or Insight Service

### Provide required information:

#### Passwords:

They are provided and accessed in a secure maner so nobody can read them without access. To allow for secure access and storage we use the ansible Vault feature which sotres data encrypted by a password.
By default this password is set to "alfresco". ***First make sure to change that password to something else*** by using the command bellow (you will be prompted for the old and new passwords):

```
$ ansible-vault rekey yml/roles/alfresco/vars/secrets.yml
```
You can then edit the vault file using the command bellow and the previously provided password:

```
$ ansible-vault edit yml/roles/alfresco/vars/secrets.yml
```

Fill in the placeholder variable with the Alfresco admin and database usernames and passwords.

#### Provide specific configuration:

hc-harvester tries to guess most of the configuration so you don't spend time on trying to fill-in some configuration file. But in some cases it may not be as clever as you'd expect and it's better to just use statically defined variables. Using hosts and groups variables can be a good solution. Here are the variables that can be overridden:

##### Web applications contexts

It is possible to configure Alfresco Content Service, Share or even Solr to use differents tomcat contexts. If so you can specify them in the respective group variable files `group_vars/all`:

```
solr_version: 4
solr_context: 'mysearch'
alfresco_context: 'myecm'
share_context: 'mycollab'
```
#### Disabling Tomcat port autodetection (Specifying tomcat port)

The playbook normally guess the port tomcat is running on automatically. If this process fails for any reason, it is still possible to specify the port manually.
There are 2 wayd of doing so.

##### All tomcat are using the same port

You can then add the variable bellow in the `tomcat_servers` group variable file `groups_vars/tomcat_servers`

```
webapp_server_port: 7979
```

##### Tomcat servers are using different ports

You'll then have to specify the tomcat port for each host using hosts variables. For example, for the hosts `node1.domain.tld` & `node2.domain.tld`, you would have

`host_vars/node1.domain.tld`

```
webapp_server_port: 7979
```

and `host_vars/node2.domain.tld`

```
webapp_server_port: 9393
```

#### Custom shared loader

Alfresco uses the tomcat shared loader feature to find additionnal resources (this is often refered to as the ${extension-root}.
This tool expect to find the such resources in the ${TOMCAT_HOME}/shared/classes/ directory. If the Alfresco extension folder is not located there
you need to manually set it as described bellow:

```
alfresco_shared_loader: /opt/alfresco/extension-root
share_shared_loader: /opt/share/extension-root
```

you can set those variables in groups (see examples in the placeholders `group_vars/repo_tiers` & `group_vars/share_tiers`) or hosts variable files.

> #TOCOMPLETE

### Execute

As stated in the pre-requisite, make sure you can login to your hosts using ssh for Linux boxes before trying to run.
The recommandation is to configure your local ssh/config file so you can login to the machine in a non-interactive maner with the appropriate user (please refer to ssh documentation).
Once you've prepared your inventory file and provided necessary informations (lie passwords and maybe others), you'll need to initialize the tool:

```
$ git submodule init
$ git submodule update
$ cd alfresco-db-queries && mvn package
$ cd -
```

You only need to do this once (unless you update the alfresco-db-queries tool.
You can now start the play by running:
```
$ ansible-playbook -i inventory hc.yml -K --ask-vault-pass
```

You will be prompted for both:
 - the Vault password you set earlier
 - the sudo password in order to get administrative privileges on the remote hosts.

## TODO

 * Complete most common environement (Linux, tomcat, postgreSQL)
 * Add support for Solr6/Alfresco Search Servives
 * Add appropriate tasks for windows
 * Add other J2EE servers tasks
 * Plenty of stuff!
