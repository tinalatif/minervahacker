import getpass
import mechanize
import cookielib
import time
from twilio.rest import TwilioRestClient
import config

loginPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
logoutPage = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_Logout'
transcriptPage = 'https://horizon.mcgill.ca/pban1/bzsktran.P_Display_Form?user_type=S&tran_type=V'

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

client = TwilioRestClient(config.account_sid, config.auth_token)

def login():
    global username
    global password
    successful = False
    while not successful:
        br.open(loginPage)
        br.select_form(nr=1)
        br.form['sid'] = username
        br.form['PIN'] = password
        br.submit()
        response = br.response().read()
        if "You have entered an invalid McGill Username" in response:
            print "That username/password combination is invalid. Please try again."
            username = raw_input("Username: (firstname.lastname) \n") + '@mail.mcgill.ca'
            password = getpass.getpass(prompt="Password: (hidden)\n")
        else:
            successful = True

def getTranscript():
    login()
    br.open(transcriptPage)
    grades = br.response().read()
    br.open(logoutPage)
    return grades

username = raw_input("Username: (firstname.lastname) \n") + '@mail.mcgill.ca'
password = getpass.getpass(prompt="Password: (hidden)\n")

# init transcript
grades = getTranscript()

# periodically check for updates
while(True):
    time.sleep(config.interval)
    newGrades = getTranscript()
    if 'UNOFFICIAL Transcript' not in newGrades:
        # probably problem with minerva/internet
        continue
    if newGrades != grades:
        grades = newGrades
        client.messages.create(to=config.cell_num, from_=config.twilio_num, body="Your transcript has been updated")