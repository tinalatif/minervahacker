#!/usr/bin/env python

# Tina Latif
# MinervaHacker Python Enroller

import getpass
import mechanize
import cgi
import cookielib
import os
import time
from bs4 import BeautifulSoup

loginPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
logoutPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_Logout'
addPage = 'https://horizon.mcgill.ca/pban1/bwskfcls.p_sel_crse_search'

# username = raw_input("Username: (firstname.lastname) \n")
# username += "@mail.mcgill.ca"
# password = getpass.getpass(prompt="Password: (hidden)\n")


br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

def login():
	br.open(loginPage)
	br.select_form(nr=1)
	br.form['sid'] = raw_input("Username: (firstname.lastname) \n") + "@mail.mcgill.ca"
	br.form['PIN'] = getpass.getpass(prompt="Password: (hidden)\n")
	br.submit()
	

def selectSemester(semester):
	br.open(addPage)
	br.select_form(nr=1)
	if semester == "WINTER":
		br.form["p_term"] = ["201401"]
		response = br.submit()
	elif semester == "FALL":
		print "Fall not implemented yet lol"
	else:
		print "I said FALL or WINTER"

def searchForCourse(courseSubject, courseNum):
	br.select_form(nr=1)
	
	subjControl = br.find_control(name='sel_subj', type="select")
	subjControl.value = [courseSubject]
	
	br.form['sel_crse'] = courseNum
	
	# set faculty to null because it takes default val of 'MG'
	br.form['sel_coll'] = []
	
	br.submit()
	resultPage = br.response().read()
	if 'No classes were found' in resultPage:
		return null

	soup = BeautifulSoup(resultPage)
	table = soup.find('table', summary='This layout table is used to present the sections found')
	return table

def canRegister(courseTable):
	tds = table.findAll('tr')[2]('td')
	rem = int(tds[12].string)
	status = tds[19].string 
	if rem > 0 and status == 'Active':
		return True
	return False

def canJoinWaitlist(courseTable):
	tds = table.findAll('tr')[2]('td')
	rem = int(tds[15].string)
	status = tds[19].string 
	if rem > 0 and status == 'Active':
		return True
	return False

# Main
login()

course = raw_input("Course you want to enroll in (e.g. COMP 330): \n")
semester = raw_input("Semester you want to enroll in (FALL or WINTER): \n")
courseSubject = course.split()[0]
courseNum = course.split()[1]

selectSemester(semester)

table = searchForCourse(courseSubject, courseNum)
if table is None:
	print "That class doesn't appear to be offered in that semester!"
else:
	if canRegister(table):
		print "Spot available for registration"
		# Add to worksheet and stuff
	else:
		print "No spots available for registration"
		# check for waitlist
		if canJoinWaitlist(table):
			print "Spot available on the waitlist"
		else:
			print "No spots available on the waitlist"