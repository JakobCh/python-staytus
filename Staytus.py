import urllib2, json
from urllib import urlencode

auth_token = ""
auth_secret = ""

base_url = "" #"http://172.20.111.220:8787"

defaultStatusList = [
	"operational",
	"degraded-performance",
	"partial-outage",
	"major-outage",
	"maintenance"
]

#All functions return dictionarys

#SERVICES

def getAllServices():
	head = {
		#'Content-type': 'application/json',
		'X-Auth-Token': auth_token,
		'X-Auth-Secret': auth_secret
	}
	req = urllib2.Request(base_url + "/api/v1/services/all", headers=head)
	response = urllib2.urlopen(req).read()
	jsonResponse = json.loads(response)
	return jsonResponse

def getService(service):
	head = {
		'Content-type': 'application/json',
		'X-Auth-Token': auth_token,
		'X-Auth-Secret': auth_secret
	}

	#'{"service": "api"}'
	encodedMessage = '{"service": "' + service + '"}'

	newurl = base_url + '/api/v1/services/info'
	req = urllib2.Request(newurl, headers=head)
	req.add_data(encodedMessage)

	response = urllib2.urlopen(req).read()
	jsonResponse = json.loads(response)
	return jsonResponse


def setServiceStatus(service, status):
	head = {
		'Content-type': 'application/json',
		'X-Auth-Token': auth_token,
		'X-Auth-Secret': auth_secret
	}
	
	#'{"service": "api", "status": "maintenance"}'
	encodedMessage = '{"service": "' + service + '", "status": "' + status + '"}'

	newurl = base_url + '/api/v1/services/set_status'
	req = urllib2.Request(newurl, headers=head)
	req.add_data(encodedMessage)

	response = urllib2.urlopen(req).read()
	jsonResponse = json.loads(response)
	return jsonResponse


#ISSUES

def getAllIssues():
	head = {
		#'Content-type': 'application/json',
		'X-Auth-Token': auth_token,
		'X-Auth-Secret': auth_secret
	}
	req = urllib2.Request(base_url + "/api/v1/issues/all", headers=head)
	response = urllib2.urlopen(req).read()
	jsonResponse = json.loads(response)
	return jsonResponse


def getIssue(issue):
	"""Takes a issue id(int)
		and returns a dict"""

	head = {
		'Content-type': 'application/json',
		'X-Auth-Token': auth_token,
		'X-Auth-Secret': auth_secret
	}

	#'{"service": "api"}'
	encodedMessage = '{"issue": ' + str(issue) + '}'

	newurl = base_url + '/api/v1/issues/info'
	req = urllib2.Request(newurl, headers=head)
	req.add_data(encodedMessage)

	response = urllib2.urlopen(req).read()
	jsonResponse = json.loads(response)
	return jsonResponse

#SUBSCRIBERS
#TODO

