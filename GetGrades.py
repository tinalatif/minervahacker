#!/usr/bin/env python

# Tina Latif
# Minerva Hacker Python

import getpass
import os
import mechanize
import cookielib
import filecmp
import time

loginPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
logoutPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_Logout'
transcriptPage = 'https://horizon.mcgill.ca/pban1/bzsktran.P_Display_Form?user_type=S&tran_type=V'

username = raw_input("Username: (firstname.lastname) \n")
password = getpass.getpass(prompt="Password: (hidden)\n")
username += '@mail.mcgill.ca'

def login():
    br.open(loginPage)
    br.select_form(nr=1)
    br.form['sid'] = username
    br.form['PIN'] = password
    br.submit()
    return

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

if os.path.exists('./grades.html') == False:
    print "doesnt exist!"
    login()
    br.open(transcriptPage)
    grades = br.response().read()
    try:
        transcript = open('grades.html', 'w+')
    except IOError:
        print "Something bad! Panic!"
    transcript.write(grades)
    transcript.close()
    br.open(logoutPage)

# 2 weeks on 10 minute intervals
for i in range (2016):
    login()
    br.open(transcriptPage)
    grades = br.response().read()
    try:
        transcript = open('newgrades.html', 'w+')
    except IOError:
        print "Something bad! Panic!"
    transcript.write(grades)
    transcript.close()
    br.open(logoutPage)

    # new grades?!
    if filecmp.cmp('newgrades.html', 'grades.html') == False:
        os.remove('grades.html')
        os.rename('newgrades.html', 'grades.html')
   
        # OS X
        os.system('growlnotify -s -t "New grades!" -m "Your transcript has been updated"')
        # UBUNTU (untested)
        # os.system('notify-send firefox "New grade" "Your transcript has been updated"')
        # WINDOWS (untested)
        # os.system('growlnotify.com /s:true /t:"New grade" "Your transcript has been updated"')
    
    else:
        os.remove('grades.html')
        os.rename('newgrades.html', 'grades.html')
        #os.system('growlnotify -t "No change" -m "Your transcript has not updated"')

    time.sleep(300)



    

