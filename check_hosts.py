import Staytus
import socket, json, os, urllib2, ssl
import subprocess as sp
from datetime import datetime


Staytus.auth_token = '' #add your own keys
Staytus.auth_secret = ''
Staytus.base_url = "http://172.20.111.220:8787"

defaultStatus = Staytus.defaultStatusList[0]

trackingList = json.load(open('hosts.json'))
logFile = "log"


def logPrint(text):
	f = open(logFile, "a")
	f.write(str(datetime.now()) + ": " + text + "\n")
	f.close()
	print(text)


print "os name: " + os.name
		
def isInMaintenance(permalink):
	temp = Staytus.getService(permalink)
	if temp["data"]["status"]["permalink"] == "maintenance":
		return True
	else:
		return False
		
def checkPing(ips):
	total = len(ips)
	up = 0
	
	for ip in ips:
		if os.name == "posix":
			child = sp.Popen("ping -c 1 " + ip, stdout=sp.PIPE, shell=True)
		else:
			child = sp.Popen("ping -n 1 " + ip, stdout=sp.PIPE, shell=True)
		streamdata = child.communicate()[0]
		rc = child.returncode
	
		if rc == 0:
			logPrint("  Ping: " + ip + " YES")
			up += 1
		else:
			logPrint("  Ping: " + ip + " NO")
	
	return up, total
	
def htmlWordCheck(ip_word):
	total = len(ip_word)
	current = 0
	
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	
	for ip in ip_word:
		try:
			response = urllib2.urlopen(ip, context=ctx, timeout=5).read()
			response = response.decode("utf-8")
			if response.find(ip_word[ip]) != -1:
				current += 1
				logPrint('  "' + ip_word[ip] + '" in "' + ip + '" YES')
			else:
				logPrint('  "' + ip_word[ip] + '" in "' + ip + '" NO')
		except:
			logPrint('  "' + ip_word[ip] + '" in "' + ip + '" NO')
			
	return current, total
	
def httpsCheck(addresses):
	total = len(addresses)
	current = 0
	
	ctx = ssl.create_default_context()
	
	for ip in addresses:
		try:
			response = urllib2.urlopen(ip, context=ctx, timeout=5).read()
			current += 1
			logPrint('  SSL:"' + ip + '" YES')
		except:
			logPrint('  SSL:"' + ip + '" NO')
			
	return current, total
	
def checkPortUp(ip_port_list):
	total = 0
	for ip in ip_port_list:
		ports = ip_port_list[ip]
		total += len(ports)
		#print ports
	
	current = 0
	
	#print "Checking host(s): " + self.permalink
	
	for ip in ip_port_list:
		#print "  Port checking ip: " + ip + ":"
		
		for port in ip_port_list[ip]:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((ip, port))
			if result == 0:
				logPrint("  Port: " + ip + ":" + str(port) + " YES")
				current += 1
			else:
				logPrint("  Port: " + ip + ":" + str(port) + " NO")
	

	return current, total
	


logPrint("NEW RUN")

for host in trackingList:
	logPrint(host)
	totalAmount = 0
	upAmount = 0
	
	if isInMaintenance(host):
		logPrint("Skipping because the group is in maintenance mode")
	else:
		if "ping" in trackingList[host]:
			temp = checkPing(trackingList[host]["ping"])
			upAmount += temp[0]
			totalAmount += temp[1]
			
		if "ports" in trackingList[host]:
			temp = checkPortUp(trackingList[host]["ports"])
			upAmount += temp[0]
			totalAmount += temp[1]
			
		if "html-word-check" in trackingList[host]:
			temp = htmlWordCheck(trackingList[host]["html-word-check"])
			upAmount += temp[0]
			totalAmount += temp[1]
			
		if "https-check" in trackingList[host]:
			temp = httpsCheck(trackingList[host]["https-check"])
			upAmount += temp[0]
			totalAmount += temp[1]
		
		
		
		logPrint("  Amount up: " + str(upAmount))
		logPrint("  Total Amount: " + str(totalAmount))
		logPrint("")
		
		if upAmount == totalAmount:
			Staytus.setServiceStatus(host, defaultStatus)
		elif upAmount > 0:
			Staytus.setServiceStatus(host, Staytus.defaultStatusList[2])
		elif upAmount == 0:
			Staytus.setServiceStatus(host, Staytus.defaultStatusList[3])



logPrint("RUN DONE")

		
		
