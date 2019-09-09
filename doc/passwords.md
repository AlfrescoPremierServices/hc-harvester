# Credentials management

## Applicative credebtials

Some credentials are required for the playbook to run. The Alfresco admin username & password is needed in order to generate a jmxdump, any admin user can be provided.
Also the username and password to access the database is needed in order to issue some SQL queries, any user with read access to the tables would do the trick, but the database owner is recommented.
Credentals are stored and accessed in a secure maner - within a vault - so nobody can read them without providing the vault password. Ansible provide the `ansible-vault` command in order to manage sensitive data like passwords.

Both credentials are stored in the vault file `yml/roles/alfresco/vars/secrets.yml`. By default the vault password is set to "alfresco".
***First thing you should do is to change the vault password to something else*** by using the command bellow (you will be prompted for the old and new passwords):
                                                                                                                                                                                              
```                                                                                                                                                                                           
$ ansible-vault rekey yml/roles/alfresco/vars/secrets.yml
```
You can then edit the vault file using the command bellow and the previously provided password:                                                                                               

```
$ ansible-vault edit yml/roles/alfresco/vars/secrets.yml                                                                                                                                      
```                                                                                                                                                                                           

## SSH Authentication

hc-harvester prompts for passwords upon execution, thus avoiding the need to store and retrieve login passwords. It may prompt for:

 - SSH password if one is needed (interactive vs key authentication)
 - SUDO or SU password (depending on the `become_method`)
 - Vault password (unrelated to SSH access)

Having a properly configured ssh_config file will ease a lot the authentication configuration. 

There are some unusual cases where passwords and privileges escalation methods differ from hosts to host within the same platform. In this case the command line cannot handle all possible different credentials and authentication methods. Those must be specified manually in the `inventory` file for each host, see [/doc/user-permission.md#](/doc/user-permission.md) for more details.
