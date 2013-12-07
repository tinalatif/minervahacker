# Minerva Hacker

Minerva Hacker is a few of scripts with a tongue-in-cheek name meant to make administrative nonsense more convenient for McGill students by automating repetitive tasks on Minerva.

## GetGrades

This will periodically check your transcript for changes and send you a text message (with Twilio) if anything has been updated.

### Installation

* Make a (free) Twilio account and verify your phone number
* Put Twilio info in config.py
* Install requirements with `pip install -r requirements.txt`
* Run it in your console ghetto-style or be fancier and set it up using launchd or cron or whatever your heart desires
  
## AutoRegister

This has to be redone completely because the old method of going through quick-add and periodically attempting to register for courses until successful ended up getting people's registration abilities revoked... lol oops.

Intent is to provide a script to periodically check if a course has open spots and if so, register the user, or alternatively add the user to the waitlist if possible.