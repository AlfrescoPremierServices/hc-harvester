# Alfresco Healthcheck Harvester

This ansible playbook allows Alfresco Premier Services engineers to get informations in order to deliver an Healthcheck report to customers

## Requirements

### Software requirement

You of course need Ansible in order to use this playbook (version 2.4 minimum is needed as we use the xml Ansible module).
Remote machines will need python 2.7.
You need SSH acces to the target infrastructure together with administrative rights on the machine (small packages may be required - e.g. python2-lxml).
The playbook has been written and tested with Ansible 2.7.

### Architectural requirement

 - ***This playbook doesn't deploy SSH keys so please make sure you're using it on machines which already have the needed SSH keys.***
 - ***At the moment the target hosts need to have direct acces to internet as we are using public repos.***

## How to use:

Edit the _inventory_ file and add your hostnames to the appropriate section (ansible inventory group):
 - repo_tiers: Those are the nodes which are running an `alfresco` webapp (regardless of wether this is used for ingestion, serving users requests or tracking
 - share_tiers: Those are the nodes which are running a `share` webapp
 - index_tiers: Those are the nodes which are running either a solr1.4 or solr4 webapp within a servlet container, or even solr6 throught the Alfresco Search Service or Insight Service

To start using the playbook simply start it with:

```
$ ansible-playbook -i inventory hc.yml -K
```

You will be prompted for the sudo password in order to get administrative privileges on the remote hosts.

If some options need to be changed (e.g. java or tomcat version, etc...), edit the group_vars/all file or the host_vars/<HOSTNAME> if the variable is host specific.

## TODO

 * Complete most common environement (Linux, tomcat, postgreSQL)
   - Add support for multiple tomcat instances running on the same host
 * Add appropriate tasks for windows
 * Add other J2EE servers tasks
 * Plenty of stuff!
