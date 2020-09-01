# Alfresco Healthcheck Harvester

This tool allows Alfresco Premier Services engineers or Alfresco administrators to get informations in order for an Healthcheck report to be rolled-out
It must be executed on a unix-like system, preferably not the servers themselves. It could be for exmaple, a mac OSX laptop or a linux VM satisfying requirements bellow.

## Requirements

### Software requirements

 - Ansible 2.5+
 - Python 2.7+ (may work with 2.6 when disabling some auto-detection features, see [/doc/]
 - unzip
 - git
 - maven

You need SSH access to the target infrastructure together with administrative rights on the machine (small packages may be required - e.g. python2-lxml).
The playbook has been written and tested with Ansible 2.7.

### Architectural requirements

 - Network SSH access to servers from the machine running hc-harvester
 - Internet access on the machine running hc-harvester
 - SSH user with appropriate rights (see [/doc/user-permissions.md](/doc/user-permissions.md) for more details)
 - Access to basic package managers repositorties

## How to use:

### Prepare inventory file:

Edit the `inventory` file and add your hostnames to the appropriate section (ansible inventory group):
 - repo_tiers: Hosts running Alfresco `repository` webapp (regardless of wether this is used for ingestion, serving users requests or tracking)
 - share_tiers: Hosts running Alfresco `Share` webapp
 - index_tiers: Hosts running Solr webapp (at the moment Solr6/Insight-Engine is not supported)

> Hosts are specified one per line and can be DNS names, IP addresses or ssh_config aliases

### Provide required information:

#### Passwords:

Credentials are needed to:
 - Generate JMXdumps: administrative user credentials (e.g: admin/admin)
 - Query the Database: database user credentials (e.g: alfresco/admin)

Credentails must be provided using the command bellow:

```
$ ansible-vault edit yml/roles/alfresco/vars/secrets.yml
```

> the Vault password is set to "alfresco" by default. If you want to know more about password management see [/doc/passwords.md](/doc/passwords.md)

#### Ready to run?

If you have a very basic setup - all hosts installed using the Alfresco installer with no other custom configuration - then you're good to go.
Otherwise please review the [advanced configuration topic](/doc/advanced-config.md) before running hc-harvester.

### Execute

As stated in the pre-requisite, make sure you can login to your hosts using ssh for Linux boxes before trying to run.
The recommandation is to configure your local ssh/config file so you can login to the machine in a non-interactive manner with the appropriate user (please refer to ssh documentation).
Once you've prepared your inventory file and provided necessary informations (like passwords and maybe others), you'll need to initialize the tool:

```
$ git submodule init
$ git submodule update
$ cd alfresco-db-queries
$ mvn install:install-file -Dfile=./lib/ojdbc6.jar -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=11.2.0.3 -Dpackaging=jar && mvn package
$ cd -
```

You only need to do this once (unless you update the alfresco-db-queries tool).
You can now start the play by running:

```
$ ./hc-harvester
```

You will be asked some easy questions you need to answer - use `True` or `False` when needed (case matters!). You may also be prompted for passwords.

## TODO

 * Complete most common environement (Linux, tomcat, postgreSQL)
 * Add support for Solr6/Alfresco Search Servives
 * Add appropriate tasks for windows
 * Add other J2EE servers tasks
 * Plenty of stuff!
