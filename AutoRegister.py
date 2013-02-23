#!/usr/bin/env python

# Tina Latif
# Minerva Hacker AutoRegister

import getpass
import mechanize
import cookielib
import os.path
import time
import pickle
from bs4 import BeautifulSoup

loginPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
logoutPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_Logout'
quickAddPage = 'https://horizon.mcgill.ca/pban1/bwskfreg.P_AltPin'

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

username = ""
password = ""
fallCRN = []
winterCRN = []

def login():
	global username
	global password
	successful = False
    
	# attempt to login to Minerva with given information
	while not successful:
		br.open(loginPage)
		br.select_form(nr=1)
		br.form['sid'] = username
		br.form['PIN'] = password
		br.submit()
        
		# if login info incorrect, prompt for info again and retry
		if 'Authorization Failure' in br.response().read():
			print 'Unable to login. Please try again:'
			username = raw_input("Username: (firstname.lastname) \n")
			username += '@mail.mcgill.ca'
			password = getpass.getpass(prompt="Password: (hidden)\n")
		else:
			successful = True

def verifyRegistration(semester):
	soup = BeautifulSoup(br.response().read())
	table = soup.find('table',summary='This layout table is used to present Registration Errors.')
	crns = []
	reasons = []
	toRemove = []
    
    # check to see if there were problems in registration
	if table != None:
		for r in table.find_all('tr')[1:]:
			elements = r.find_all('td')
			reasons.append("".join(elements[0].findAll(text=True)))
			crns.append(elements[1].string)
	for bad,why in zip(crns,reasons):
		print "Unable to register for {} CRN {}: \"{}\"".format(semester, bad, why)
	
    # if something was successfully registered, send a growl notification
	if semester == 'fall':
		for i in fallCRN:
			if str(i) not in crns:
				os.system('growlnotify -s -t "Registration Success!" -m "You have been registered for a fall course"')
				toRemove.append(i)
		for i in toRemove:
			fallCRN.remove(i)	
	if semester == 'winter':
		for i in winterCRN:
			if str(i) not in crns:
				os.system('growlnotify -s -t "Registration success!" -m "You have been registered for a fall course"')
				toRemove.append(i)
		for i in toRemove:
			winterCRN.remove(i)

# main
freshLogin = True
# check to see if autoregistration data for someone exists
if os.path.exists('registrationdata'):
	registrationData = open('registrationdata')
	pickleJar = pickle.load(registrationData)
	registrationData.close() 
	print "Username detected: " + pickleJar[0]
	print "Fall CRNs:"
	print pickleJar[1]
	print "Winter CRNs:"
	print pickleJar[2]
	password = getpass.getpass(prompt="Password: (hidden) (blank line to change login or edit CRNs\n")
	# if returning user, use pickled information
	if password != "":
		freshLogin = False
		username = pickleJar[0]
		fallCRN = pickleJar[1]
		winterCRN = pickleJar[2]

# if new user or user wants to change CRNs, get all information
if freshLogin:
	username = raw_input("Username: (firstname.lastname) \n")
	username += '@mail.mcgill.ca'
	password = getpass.getpass(prompt="Password: (hidden)\n")
	print "Input the CRN codes of up to 7 courses for the Fall semester (press enter after each CRN, blank line to end)"
	for i in range(7):
		try:
			fallCRN.append(int(raw_input()))
		except ValueError:
			break
	print "Input the CRN codes of up to 7 courses for the Winter semester (press enter after each CRN, blank line to end)"
	for i in range(7):
		try:
			winterCRN.append(int(raw_input()))
		except ValueError:
			break
    
	print "CRNs have been accepted. Press ctrl-C to cancel"

try:
	while fallCRN or winterCRN:
		# log in to Minerva
		login()
        
		# navigate to the add/drop page for the fall semester
		br.open(quickAddPage)
		br.select_form(nr=1)
		br.form['term_in'] = ['201209']
		br.submit()

		# register for fall courses
		br.open(quickAddPage)
		br.select_form(nr=1)
		for i,v in enumerate(fallCRN):
			br.form.set_value(str(v),name='CRN_IN',type='text',nr=i)
		br.submit()
		verifyRegistration('fall')

		# logout, login to reset form
		br.open(logoutPage)
		login()

		# navigate to the add/drop page for the winter semester
		br.open(quickAddPage)
		br.select_form(nr=1)
		br.form['term_in'] = ['201301']
		br.submit()

		# register for winter courses
		br.open(quickAddPage)
		br.select_form(nr=1)
		for i,v in enumerate(winterCRN):
			br.form.set_value(str(v),name='CRN_IN',type='text',nr=i)
		br.submit()
		verifyRegistration('winter')

		br.open(logoutPage)
        
		# if there are unregistered courses remaining, wait and try again
		if fallCRN or winterCRN:
			time.sleep(300)

except:
	print "Interrupt detected. Saving and exiting."
	registrationData = open('registrationdata', 'w')
	pickleJar = [username, fallCRN, winterCRN]
	pickle.dump(pickleJar, registrationData)
	registrationData.close()