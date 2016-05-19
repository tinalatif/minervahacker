# Minerva Hacker

Minerva Hacker is a few of scripts with a tongue-in-cheek name meant to make administrative nonsense more convenient for McGill students by automating repetitive tasks on Minerva.

## GetGrades

This will periodically check your transcript for changes and send you a text message (with Twilio) if anything has been updated.

### Installation

* Make a (free) Twilio account and verify your phone number
* Put your Twilio info in config.py
* Install requirements with `pip install -r requirements.txt` (you may need to install pip first)
* Run the script!
  
## AutoRegister

This has to be redone completely because the old method of periodically going through quick-add and attempting to register for courses until successful ended up getting people's registration abilities revoked... oops.

Intent is to provide a script to periodically check if a course has open spots and if so, either register the user or try to add the user to the waitlist if the course is full.
