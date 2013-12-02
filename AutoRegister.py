import getpass
import mechanize
import cookielib
import os
import time
from bs4 import BeautifulSoup

loginPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
logoutPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_Logout'
addPage = 'https://horizon.mcgill.ca/pban1/bwskfcls.p_sel_crse_search'

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

def login():
	br.open(loginPage)
	br.select_form(nr=1)
	br.form['sid'] = raw_input("Username: (firstname.lastname) \n") + "@mail.mcgill.ca"
	br.form['PIN'] = getpass.getpass(prompt="Password: (hidden)\n")
	br.submit()


# FALL or WINTER
def selectSemester(semester):
	br.open(addPage)
	br.select_form(nr=1)
	if semester == "WINTER":
		br.form["p_term"] = ["201401"]
		response = br.submit()
	elif semester == "FALL":
		br.form["p_term"] = ["201309"]
		response = br.submit()
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
		return None
	
	soup = BeautifulSoup(resultPage)
	table = soup.find('table', summary='This layout table is used to present the sections found')
	return table

def canRegister(courseTable):
	tds = courseTable.findAll('tr')[2]('td')
	rem = int(tds[12].string)
	status = tds[19].string
	if rem > 0 and status == 'Active':
		return True
	return False

def canJoinWaitlist(courseTable):
	tds = courseTable.findAll('tr')[2]('td')
	rem = int(tds[15].string)
	status = tds[19].string
	if rem > 0 and status == 'Active':
		return True
	return False

def searchBySemester(semester, courseList):
	for course in courseList:
		print "Searching for " + course
		selectSemester(semester)
		table = searchForCourse(course.split()[0], course.split()[1])
		if table is None:
			print "That class doesn't appear to be offered in that semester!"
		else:
			if canRegister(table):
				print "Spot available for registration in " + course
				registerForCourse(course)
			else:
				print "No spots available for registration in " + course
				# check for waitlist
				if canJoinWaitlist(table):
					print "Spot available on the waitlist for " + course
					registerForCourse(course)
				else:
					print "No spots available on the waitlist for " + course


def registerForCourse(course):
	# Add to worksheet and stuff
	br.select_form(nr=1)
	br.find_control(name='sel_crn', type="checkbox").items[0].selected=True
	br.submit()
	resultPage = br.response().read()
	if "Registration Add Errors" in resultPage:
		print "Unfortunately there were problems registering you for " + course
	else:
		print "Successfully registered for " + course + " (probably - lol)"   
#	try:
#		courseAdd = open('courseAdd.html', 'w+')
#	except IOError:
#		print "Something bad! Panic!"
#	courseAdd.write(resultPage)
#	courseAdd.close()

# Main
login()

fallCoursesInput = raw_input("Enter FALL semester courses you want to enroll in, comma-separated (e.g. COMP 330, COMP 409, MATH 323). Enter blank line if no FALL courses needed. \n")
winterCoursesInput = raw_input("WINTER semester courses you want to enroll in, comma-separated (e.g. MATH 315, COMP 529). Enter blank line if no WINTER courses needed. \n")

fallCourses = []
winterCourses = []
if fallCoursesInput != "":
	fallCourses = fallCoursesInput.split(", ")
if winterCoursesInput != "":
	winterCourses = winterCoursesInput.split(", ")

searchBySemester("FALL", fallCourses)
searchBySemester("WINTER", winterCourses)

br.open(logoutPage)