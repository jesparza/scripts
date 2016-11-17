#!/usr/bin/env python

# 
# Script that searches one webpage for hostnames with a given domain and resolves them. By default the domain is the URL domain.
#
# http://eternal-todo.com
# Jose Miguel Esparza
#

import sys,urllib2,re,socket

def searchHosts(url,secondld,tld):
	matchUrls = []
	hosts = []
	regexp = "(?i)http://.{1,20}\."+secondld+"\."+tld 
	try:
		response = urllib2.urlopen(url)
		source = response.read()
		matchUrls = re.findall(regexp,source)
		matchUrls = list(set(matchUrls))
		for i in range(len(matchUrls)):
			index1 = matchUrls[i].find('//') + 2
			index2 = matchUrls[i].find('.'+secondld+'.'+tld) + len(secondld) + len(tld) + 2
			hosts.append(matchUrls[i][index1:index2])
		hosts = list(set(hosts))
	except:
		if str(sys.exc_info()[1]).find('403') != -1:
			print "Attention: The URL '"+url+"' is forbidden!!"
		elif str(sys.exc_info()[1]).find('401') != -1:
			print "Attention: The URL '"+url+"' needs authentication!!"
		elif str(sys.exc_info()[1]).find('404') != -1:
			print "Attention: The URL '"+url+"' is not valid!!"
		else:
			print "Attention: The URL '"+url+"' returns this error '"+str(sys.exc_info()[1])+"'!!"
	return matchUrls,hosts

recursive = False
domain = ''
hosts = []
usage = "Usage: "  + sys.argv[0] + ''' [-r] url [domain]

Arguments:

    url: the URL of the page which must be searched for hostnames
    domain: the domain of the hostnames to look for. By default it's the url domain.

Options:

    -r: recursive
'''

if len(sys.argv) < 2 or len(sys.argv) > 4:
	sys.exit(usage)

if sys.argv[1] == '-r':
	recursive = True
	url = sys.argv[2]
	if len(sys.argv) == 4:
		domain = sys.argv[3]
else:
	url = sys.argv[1]
	if len(sys.argv) == 3:
		domain = sys.argv[2]

if url[:7] != "http://":
   url = "http://" + url

if domain != '':
	tld = domain[domain.find('.') + 1:]
	secondld = domain[:domain.find('.')]
else:
	endDomainIndex = url[7:].find('/')
	if endDomainIndex == -1:
		endDomainIndex = len(url)
	else:
		endDomainIndex += 7
	fqdn = url[7:endDomainIndex]
	tld = fqdn[fqdn.rfind('.') + 1:]
	secondld = fqdn[fqdn[:fqdn.rfind('.')-1].rfind('.')+1:fqdn.rfind('.')]

urls,hosts = searchHosts(url,secondld,tld)

if recursive:
	URLqueue = []
	URLqueue += urls
	if url in URLqueue:
		URLqueue.remove(url)
	while len(URLqueue) > 0:
		url = URLqueue.pop()
		urlsR,hostsR = searchHosts(url,secondld,tld)
		for urlR in urlsR:
			if urlR not in urls:
				urls.append(urlR)
				URLqueue.append(urlR)
		hosts += hostsR
	
hosts = sorted(list(set(hosts)))
print ""
for host in hosts:
	try:
		ip = socket.gethostbyname(host)
	except:
		ip = 'Not resolving!!'
	print '%30s -> %s' % (host,ip)

