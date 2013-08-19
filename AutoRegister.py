#!/usr/bin/env python

# Tina Latif
# MinervaHacker Python Enroller

import getpass
import mechanize
import cookielib
import os
import time

loginPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
logoutPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_Logout'
quickAddPage = 'https://horizon.mcgill.ca/pban1/bwskfreg.P_AltPin'

username = raw_input("Username: (firstname.lastname) \n")
username += "@mail.mcgill.ca"
password = getpass.getpass(prompt="Password: (hidden)\n")
CRN = raw_input("CRN you want to enroll in: \n")
semester = raw_input("Semester you want to enroll in (FALL or WINTER): \n")

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

for i in range (2016):
	br.open(loginPage)
	br.select_form(nr=1)
	br.form['sid'] = username
	br.form['PIN'] = password
	br.submit()

	br.open(quickAddPage)
	br.select_form(nr=1)
	if semester == 'FALL':
		br.form['term_in'] = ['201309']
	elif semester == 'WINTER':
		br.form['term_in'] = ['201401']
	br.submit()

	br.select_form(nr=1)
	br.form.set_value(CRN, name='CRN_IN', type='text', nr=0)
	br.submit()

	resultPage = br.response().read()
	resultPageFile = open('page.html', 'w+')
	resultPageFile.write(resultPage)
	resultPageFile.close()

	if 'Registration Add Errors' not in resultPage:
		os.system('growlnotify -s -t "Registration??" -m "Maybe!"')					 

	br.open(logoutPage)

	time.sleep(600)
