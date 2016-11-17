#!/usr/bin/env python

# 
# Command line GeoIpTool Wrapper to obtain geolocalization from a host
#
# http://eternal-todo.com
# Jose Miguel Esparza
#

import sys,urllib2


def getElement(elementName, source):
	indice = source.find(elementName)
	source = source[indice:]
	indice = source.find("\n")+1
	line = source[indice:indice+source[indice:].find("\n")]
	while True:
		indice = line.find('>')
		if indice == -1:
			break
		line = line[indice+1:]
		indice = line.find('<')
		if indice == -1:
			break
		element = line[:indice]
		if not element.isspace() and len(element) > 2:
			element = element.lstrip()
			print '%20s %s' % (elementName,element)
			break



if len(sys.argv) != 2:
	sys.exit("Usage: geoloc host\nBased on GeoIpTool.com")

host = sys.argv[1]
response = urllib2.urlopen("http://www.geoiptool.com/?IP="+host)
source = response.read()
getElement("Host Name:",source)
getElement("IP Address:",source)
getElement("Country:",source)
getElement("Region:",source)
getElement("City:",source)
getElement("Postal Code:",source)
getElement("Longitude:",source)
getElement("Latitude:",source)
