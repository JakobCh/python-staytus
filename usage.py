import Staytus

#set some information
Staytus.base_url = '' #"http://172.20.111.220:8787"
Staytus.auth_token = 'C00L_ACCESS_TOKEN' #add your own keys
Staytus.auth_secret = 'C00L_ACCESS_SECRET'

def assertRequest(jsonDict):
	if temp["status"] == 'success':
		return True
	else:
		return False

#get all services api point
#remember that all functions return dictionarys and that you can check there contents with dict()
for i in Staytus.getAllServices()["data"]: #send a request for all services and only grab the returned data
	print i["name"] #the name of the service
	
	temp = Staytus.getService(i["permalink"]) #use the service permlink to get more info about it
	if assertRequest(temp):
		print "  Successfully got the service"
	else:
		print "  Failed to get the service"
	
	temp = Staytus.setServiceStatus(i["permalink"], Staytus.defaultStatusList[0]) #set the status of the service to "operational"
	if assertRequest(temp):
		print "  Successfully set the status"
	else:
		print "  Failed to set the status"
	
	print ""
	
temp = Staytus.getAllIssues()
if assertRequest(temp):
	print "Successfully got issues"
else:
	print "Failed to get issues"
	
for i in temp["data"]:
	print "  " + i["title"], i["id"]
	temp = Staytus.getIssue(i["id"])
	if assertRequest(temp):
		print "  Successfully got issue"
	else:
		print "  Failed to get issue"
	