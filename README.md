# Minerva Hacker

Minerva Hacker is a tool intended for make the lives of McGill students a little bit more convenient by dealing with Minerva so they don't have to. It comes in 2 parts: GetGrades and AutoRegister. 

#### GetGrades
This script will regularly check your trasncript for changes and notify you via growlnotify if any new grades have been updated.

#### AutoRegister
Given a list of CRNs (course registration numbers), this script will attempt to register the user until successful (thereby avoiding the need to constantly check to see if a spot has opened up in a course). Upon success, it will notify the user via growlnotify.

## Dependencies

* [Mechanize](http://wwwsearch.sourceforge.net/mechanize/)
* [Growlnotify](http://growl.info/extras.php)

## Installation

Install the above dependencies, then simply run the script as desired through command line, and follow the command line instructions:

	python GetGrades.py