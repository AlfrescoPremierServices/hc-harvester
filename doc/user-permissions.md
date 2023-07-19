# SSH access to servers

Depending on your server configuration, you can log in to servers in different manners. For example, a permissive infrastructure will allow logging in as root but a less permissive infrastructure will only allow to log in as a normal user and once logged in become root, either using the `su` command and providing the root password, or using the `sudo` command without providing a password...
You got the point, there are a lot of possible combinations.

hc-harvester tries to make it simpler for users to deal with those combinations by:

 - asking simple questions about the servers
 - wrapping multiple command line arguments
 - providing an authentication wrapper which works in most cases

## Required permissions

The user needs to be able to:

 - access & list the content of the log directory and read log files
 - access & list the content of the config directory and read config files
 - access & execute java binaries
 - access tomcat process environment (optional)
 - read & write contentstore and index folders (optionnal)
 - install python module python-lxml (optional)

If a user can become root, all of the permissions above will be granted.
If a user can become the user alfresco is running as, all permissions will be granted except the last one (see [Dealing with non root access](#Dealing-with-non-root-access) to deal with such cases)

## Privilege escalation methods

hc-harvester uses Ansible, which offers several options when trying to execute a task as a different user. It also implements a small authentication wrapper which minimize the use cases where additionnal configuration is required.

### sudo

If `sudo` is the prefered way of issuing privilege escalation on the servers, no specific configuration is needed. This use case is the default in Ansible, and the hc-harvester authentication wrapper also covers this use case.
However there are many different ways of configuring `sudo`, and some paranoid configurations may prevent hc-harvester to complete (typically configurations where user is only allowed to run predefined commands - excluding python and other necessary commands). The authentication wrapper script however allows to deal with situations where `sudo` only allows usage of `su`.

### su

In cases where `su` command is the preferred way of escalating privileges, it is needed to specify it in the config files. To do edit the `group_vars/all` files and makes sure to set the variables below:

```
...
become_method: su
# Make sure ansible_become_exe is not defined if not using sudo
#ansible_become_exe: 
...
```

### Mixed authentication methods

Alfresco platforms should always be as consistent as possible. However it may happen that different servers in the platform use different methods of privilege escalation.
In this case `become_*` parameters can be specified for each host. Instead of using the `group_vars/all` file, the `inventory` file can be used:

```
[repo_tiers]
alfresco.domain.tld ansible_become_method=su ansible_become_exe=su ansible_ssh_user=wheeler ansible_become_pass=secret1

[share_tiers]
share.domain.tld ansible_become_method=sudo ansible_become_exe=sudo ansible_ssh_user=admin ansible_become_pass=secret2

[index_tiers]
solr.domain.tld ansible_become_method=sudo ansible_become_exe="{{ hc_tmp }}/bin/sudosu-wrapper.sh" ansible_ssh_user=ecm ansible_become_pass=secret3
```

> - `ansible_ssh_user`: user to connect to SSH as
> - `ansible_become_method`: method to gain alfresco or root privileges
> - `ansible_become_pass`: password to gain alfresco or root privileges
> - `ansible_become_exe`: script to call to gain alfresco or root privileges
>
> **Warning**: Dealing with heterogeneous platforms lowers the security as passwords are written down in non-encrypted files...

## Dealing with non root access

In case the user you log in as is not allowed to become the root user anyhow, the playbook will not be able to install the lxml python module. This module is required to parse xml configuration files and automatically detect some parts of the architecture (namely, the tomcat ports, schemes and the solr home folder).
If you know python-lxml is already installed on the servers, then you can skip this section and proceed normally. hc-harvester will return an error checking for root permission, but that is not harmful for the playbook.
On the other hand, if this module is not installed on the servers, it is required to configure the tool with:

 - Which port tomcat instances are running on
 - What schemes tomcat instances are using
 - Where is the solr home folder located

Refer to [/doc/advanced-config.md](/doc/advanced-config.md#Disabling-Autodetection) to get details on how to configure that.

