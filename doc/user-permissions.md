# SSH access to servers

Depending on your server configuration you can login to servers in different maners. For example, permissive setup will allow loging in as root, less permissive setups will allow login as a normal user and become root once logged in using the `su` command and providing the root password, or using the sudo command providing no password...
You got the point, there aare a lot of possible combinations.

hc-harvester tries to make it simpler for user to deal with those combination by:

 - asking simple questions about the systems
 - wrapping multiple command line arguments
 - providing authentication wrapper which work in most cases

## Required permissions

The user needs to be able to:

 - access & list log directory content and read logs files
 - access & list config directory content and read config files
 - access & execute java binaries
 - access tomcat process environment (optional)
 - read & write contentstore and index folders (optionnal)
 - install python module python-lxml (optional)

If a user can become root all of the permissions above will be granted.
If a user can become the user alfresco is running as, all permissions will be granted except the last one (see [Dealing with non root access](#Dealing-with-non-root-access) to deal with such cases)

## Privileges escalation methods

hc-harvester uses Ansible, which offers several options when trying to execute a task as a different user. It also implements a small authentication wrapper which minimize the use cases where additionnal configuration is necessary.

### sudo

If `sudo` is the prefered way of issuing privilege escalation on the systems, no specific configuration is needed. This use case is the default in Ansible, and the hc-harvester authentication wrapper also cover this use case.
However there are many different ways of configuring `sudo`, and some paranoid configurations may prevent hc-harvester to complete (typically configurations where user is only allowed to run predefined commands - excluding python and other necessary commands). The authentication wrapper script however allow to deal with situations where `sudo` only allows usage of `su`.

### su

In cases where `su` command is the preferred way of escalating privileges, it is needed to specify it in the config files. To do edit the group_vars/all files and makes sure to set the variables bellow:

```
...
become_method: su
# Make sure ansible_become_exe is not defined if not using sudo
#ansible_become_exe: 
...
```

### Mixed authentication methods

Alfresco platforms should always be as conssitent as possible. However it may be different servers in the platform uses different methods of privileges escalation.
In this case `become_*` parameters can be specified per hosts. Instead of using the group_vars/all file the inventory file can be used:

```
[repo_tiers]
alfresco.domain.tld ansible_become_method=su ansible_become_exe=su ansible_ssh_user=wheeler ansible_become_pass=secret1

[share_tiers]
share.domain.tld ansible_become_method=sudo ansible_become_exe=sudo ansible_ssh_user=admin ansible_become_pass=secret2

[index_tiers]
solr.domain.tld ansible_become_method=sudo ansible_become_exe="{{ hc_tmp }}/bin/sudosu-wrapper.sh" ansible_ssh_user=ecm ansible_become_pass=secret3
```

> ansible_ssh_user: user to connect to SSH as
> ansible_become_method: method to gain alfresco or root privileges
> ansible_become_pass: password to gain alfresco or root privileges
> ansible_become_exe: 
> Dealing with heterogeneous setups lower the security as password are written down in non-encrypted files...

## Dealing with non root access

In case the user you log in as is not allowed to become the root user anyhow, the playbook won't be able to install the lxml python module. This module is required to parse xml configuration files and automatically detect some parts of architecture (namely, the tomcat ports, schemes and the solr home folder).
If you know python-lxml is already installed on the servers, then you can skip this section and proceed normally. hc-harvester will return an error checking for root permission, but that's not harmful for the playbook if the module is anyway already installed.
On the other hand if the module is not installed, we will need to tell to tool:

 - What port tomcat instances are running on
 - What schemes tomcat instances are using
 - Where is the solr home folder located

Refer to [/doc/advanced-config.md](/doc/advanced-config.md#Disabling-Autodetection) to get details on how to do that.

