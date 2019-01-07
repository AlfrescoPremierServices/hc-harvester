# Alfresco Healthcheck Harvester

This ansible playbook allows Alfresco Premier Services engineers to get informations in order to deliver an Healthcheck report to customers

## Requirements

### Software requirement

You of course need Ansible in order to use this playbook (version 2.4 minimum is needed as we use the xml Ansible module).
Ansible-vault is also needed in order to store and access sensitive informations like passwords.
Remote machines will need python 2.7.
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

#### Provide specific configuration:

hc-harvester tries to guess most of the configuration so you don't spend time on trying to fill-in some configuration file. But in some cases it may not be as clever as you'd expect and it's better to just use statically defined variables. Using hosts and groups variables can be a good solution. Here are the variables that can be overridden:

> #TODO

### Execute

As stated in the pre-requisite, make sure you can login to your hosts using ssh for Linux boxes before trying to run.
The recommandation is to configure your local ssh/config file so you can login to the machine in a non-interactive maner with the appropriate user (please refer to ssh documentation).
To start the playbook simply run:

```
$ ansible-playbook -i inventory hc.yml -K --ask-vault-pass
```

You will be prompted for both:
 - the Vault password you set earlier
 - the sudo password in order to get administrative privileges on the remote hosts.

## TODO

 * Complete most common environement (Linux, tomcat, postgreSQL)
 * Add appropriate tasks for windows
 * Add other J2EE servers tasks
 * Plenty of stuff!
