#!/usr/bin/python3
import socket
import tqdm
import os
#import ldap 


def connect():
	global SEPARATOR
	global BUFFER_SIZE
	global host
	global filename
	global filesize
	global s	
	SEPARATOR = "<SEPARATOR>"
	BUFFER_SIZE = 4096 # send 4096 bytes each time step
	# the ip address or hostname of the server, the receiver
	host = "127.0.0.1"
	# the port, let's use 5001
	port = 54321
	# the name of file we want to send, make sure it exists
	filename = "file.txt"
	# get the file size
	filesize = os.path.getsize(filename)
	# create the client socket
	s = socket.socket()
	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.")
	# send the filename and filesize
	s.send(f"{filename}{SEPARATOR}{filesize}".encode())

def upload():
	# start sending the file
	progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	with open(filename, "rb") as f:
		while True:
			# read the bytes from the file
			bytes_read = f.read(BUFFER_SIZE)
			if not bytes_read:
				# file transmitting is done
				break
		# we use sendall to assure transimission in 
		# busy networks
		s.sendall(bytes_read)
		# update the progress bar
		progress.update(len(bytes_read))
#def ldap_auth():
#	l = ldap.initialize('ldap://ldap.myserver.com:389')
#	binddn = "cn=myUserName,ou=GenericID,dc=my,dc=company,dc=com"
#	pw = "myPassword"
#	basedn = "ou=UserUnits,dc=my,dc=company,dc=com"
#	searchFilter = "(&(gidNumber=123456)(objectClass=posixAccount))"
#	searchAttribute = ["mail","department"]
#	#this will scope the entire subtree under UserUnits
#	searchScope = ldap.SCOPE_SUBTREE
#	#Bind to the server
#	try:
#	    l.protocol_version = ldap.VERSION3
#	    l.simple_bind_s(binddn, pw) 
#	except ldap.INVALID_CREDENTIALS:
#	  print("Your username or password is incorrect.")
#	  sys.exit(0)
#	except ldap.LDAPError, e:
#	  if type(e.message) == dict and e.message.has_key('desc'):
#	      print e.message['desc']
#	  else: 
#	      print e
#	  sys.exit(0)
#	try:    
#	    ldap_result_id = l.search(basedn, searchScope, searchFilter, searchAttribute)
#	    result_set = []
#	    while 1:
#		result_type, result_data = l.result(ldap_result_id, 0)
#		if (result_data == []):
#		    break
#		else:
#		    ## if you are expecting multiple results you can append them
#		    ## otherwise you can just wait until the initial result and break out
#		    if result_type == ldap.RES_SEARCH_ENTRY:
#		        result_set.append(result_data)
#	    print result_set
#	except ldap.LDAPError, e:
#	    print e
#	l.unbind_s()
			
connect()
upload()
# close the socket
s.close()
