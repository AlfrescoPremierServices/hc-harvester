from ansible import errors
import re

def get_vendor_from_url(url):
	try:
		return url.split(':')[1]
	except IndexError:
		raise errors.AnsibleFilterError('Provided URL was not a JDBC URL')

def get_simple_db_host_from_url(url):
	host_regex = re.compile('^jdbc:\w+:(?:replication:|failover:|sequential:|aurora:)?//(?P<dbhost>[a-zA-Z0-9\.\-]+)(?::[0-9]{1,5})?/')
	try:
		host_match = host_regex.search(url)
		return host_match.group('dbhost')
	except AttributeError:
		raise errors.AnsibleFilterError('Provided URL was not a JDBC URL')

def get_oracle_db_host_from_url(url):
	oranet_regex = re.compile('^jdbc:oracle:(?:oci|thin):@\(DESCRIPTION=\(.*?\(\s*HOST\s*=\s*(?P<dbhost>[a-zA-Z0-9\.\-]+)\s*\)')
	thin_host_regex = re.compile('^jdbc:oracle:thin:(?:\w+/.*?)?@(?://)?(?P<dbhost>[a-zA-Z0-9\.\-]+)(?::[0-9]{1,5})?[:/]')
	try:
		oranet_host_match = oranet_regex.search(url)
		thin_host_match = thin_host_regex.search(url)
		if oranet_host_match:
			return oranet_host_match.group('dbhost')
		elif thin_host_match:
			return thin_host_match.group('dbhost')
		else:
			return 'localhost'
	except AttributeError:
		raise errors.AnsibleFilterError('Provided URL was not a recognized Oracle URL')

def get_ms_db_host_from_url(url):
	host_regex = re.compile('^jdbc:(?:jtds:)?sqlserver://(?P<dbhost>[a-zA-Z0-9\.\-]+)(?::[0-9]{1,5})?[/;]')
	try:
		host_match = host_regex.search(url)
		return host_match.group('dbhost')
	except AttributeError:
		raise errors.AnsibleFilterError('Provided URL was not a recognized SQL server JDBC URL')

def db_host_from_url_specifier(url):
	vendor = get_vendor_from_url(url)
	if (vendor in ['mysql','mariadb','postgres','postgresql']):
		dbhost = get_simple_db_host_from_url(url)
	if (vendor == 'oracle'):
		dbhost = get_oracle_db_host_from_url(url)
	if (vendor in [ 'jtds','sqlserver']):
		dbhost = get_ms_db_host_from_url(url)
	return dbhost
		
class FilterModule(object):
	''' A filter to parse database URL specifers '''
	def filters(self):
		return {
			'host_jdbc': db_host_from_url_specifier
			}
