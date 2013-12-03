import getpass
import mechanize
import cookielib
from bs4 import BeautifulSoup

loginPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
logoutPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_Logout'
addPage = 'https://horizon.mcgill.ca/pban1/bwskfcls.p_sel_crse_search'
quickAddPage = 'https://horizon.mcgill.ca/pban1/bwskfreg.P_AltPin'

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

def login():
	successful = False
	while not successful:
		br.open(loginPage)
		br.select_form(nr=1)
		br.form['sid'] = raw_input("Username: (firstname.lastname) \n") + '@mail.mcgill.ca'
		br.form['PIN'] = getpass.getpass(prompt="\nPassword: (hidden)\n")
		br.submit()
		response = br.response().read()
		if "You have entered an invalid McGill Username" in response:
			print "That username/password combination is invalid. Please try again."
		else:
			successful = True

def selectSemester(semester):
	br.open(addPage)
	br.select_form(nr=1)
	if semester == 'WINTER':
		br.form['p_term'] = ['201401']
		response = br.submit()
	elif semester == 'FALL':
		br.form['p_term'] = ['201309']
		response = br.submit()
	else:
		raise Exception("Only FALL and WINTER semesters supported")

def getCourseInfo(courseSubject, courseNum):
	br.select_form(nr=1)
	subjControl = br.find_control(name='sel_subj', type='select')
	subjControl.value = [courseSubject]
	br.form['sel_crse'] = courseNum
	# set faculty to null because it takes default val of 'MG'
	br.form['sel_coll'] = []
	br.submit()
	
	# Get course info table, unless course not found
	resultPage = br.response().read()
	if 'No classes were found' in resultPage:
		return None
	soup = BeautifulSoup(resultPage)
	table = soup.find('table', summary='This layout table is used to present the sections found')
	return table

def canRegister(courseTable):
	tds = courseTable.findAll('tr')[2]('td')
	rem = int(tds[12].string)
	wlNum = int(tds[14].string)
	status = tds[19].string
	if rem > 0 and wlNum == 0 and status == 'Active':
		return True
	return False

def canJoinWaitlist(courseTable):
	tds = courseTable.findAll('tr')[2]('td')
	rem = int(tds[15].string)
	status = tds[19].string
	if rem > 0 and status == 'Active':
		return True
	return False

def registerForCourse(course):
	# Attempt to register for course
	br.select_form(nr=1)
	br.find_control(name='sel_crn', type='checkbox').items[0].selected=True
	br.submit()
	
	# If there's a registration error, display why
	resultPage = br.response().read()
	if "Registration Add Errors" in resultPage:
		soup = BeautifulSoup(resultPage)
		errorTable = soup.find('table', summary='This layout table is used to present Registration Errors.')
		tds = errorTable.findAll('tr')[1]('td')
		error = tds[0].string
		print "Unfortunately there were problems registering you for " + course + ": " + error
	# Otherwise, make sure that the course is in the 'current schedule'
	else:
		soup = BeautifulSoup(resultPage)
		scheduleTable = soup.find('table', summary='Current Schedule')
		if courseAddedToSchedule(course, scheduleTable):
			print "Successfully registered for " + course
		else:
			print "There was a mysterious error while attempting to register for " + course + ". Uh oh!"

def joinWaitlist(course, CRN):
	# Semester should already be saved
	br.open(quickAddPage)
	br.select_form(nr=1)
	enterCRNControl = br.find_control(name='CRN_IN', type='text', nr=0)
	enterCRNControl.value = CRN
	br.submit()
	# Resultant page prompt user to join waitlist
	br.select_form(nr=1)
	joinWLControl = br.find_control(name='RSTS_IN', type='select', id='waitaction_id1')
	joinWLControl.value = ['LW']
	br.submit()

	# Verify that course is in 'current schedule'
	resultPage = br.response().read()
	soup = BeautifulSoup(resultPage)
	scheduleTable = soup.find('table', summary='Current Schedule')
	if courseAddedToSchedule(course, scheduleTable):
		print "Successfully added to the waitlist for " + course
	else:
		print "There was a mysterious error while attempting to join the waitlist for " + course + ". Uh oh!"
	
def courseAddedToSchedule(course, schedule):
	rows = schedule.findAll('tr')
	for i in range(2, len(rows)):
		tds = rows[i]('td')
		if tds[3].string == course.split()[0] and tds[4].string == course.split()[1]:
			return True
	return False

# Main
login()

# Get desired courses
fallCoursesInput = raw_input("Enter FALL semester courses you want to enroll in, comma-separated (e.g. COMP 330, COMP 409, MATH 323). Enter blank line if no FALL courses needed. \n")
winterCoursesInput = raw_input("\nEnter WINTER semester courses you want to enroll in, comma-separated (e.g. MATH 315, COMP 529). Enter blank line if no WINTER courses needed. \n")
fallCourses = []
winterCourses = []
if fallCoursesInput != "":
	fallCourses = fallCoursesInput.split(', ')
if winterCoursesInput != "":
	winterCourses = winterCoursesInput.split(', ')
coursesPerSemester = {'FALL': fallCourses, 'WINTER': winterCourses}

# Attempt to register by semester
for semester in coursesPerSemester:
	for course in coursesPerSemester[semester]:
		print "Searching for " + course
		selectSemester(semester)
		courseInfo = getCourseInfo(course.split()[0], course.split()[1])
		if courseInfo is None:
			print course + " doesn't appear to be offered in the " + semester + " semester"
		else:
			# Try to register for course
			if canRegister(courseInfo):
				print "Spot available for registration in " + course
				registerForCourse(course)
			# Check for waitlist opening
			else:
				print "No spots for registration in " + course
				if canJoinWaitlist(courseInfo):
					print "Spot available on the waitlist for " + course
					CRN = courseInfo.findAll('tr')[2]('td')[1].string
					joinWaitlist(course, CRN)
				else:
					print "No spots available on the waitlist for " + course

br.open(logoutPage)