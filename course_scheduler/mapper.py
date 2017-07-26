###############################################################################
#	
#							InfoManager
#
# Note: Uses third party module 'Requests'
###############################################################################

import requests
import json
from school_objects import *

class InfoManager(object):

    def __init__(self): pass

    def getCourseInfo(self, courseID, semester):
        """Get and parse course info for *courseID*. Return Course obj"""

        # Get course JSON via HTTP req
        url = self._craftURL(courseID, semester)
        # pdb.set_trace()
        httpRequest = requests.get(url)
        courseJsonStr = httpRequest.content.split("<html")[0]
        if courseJsonStr == [[[]], []]:
            raise ValueError("No data available for course: " + str(courseID))

        # Parse JSON into Course containing Sections
        return self._parseCourseJson(json.loads(courseJsonStr))


    def _craftURL(self, courseID, semester):
	craftedSem = "20"
	craftedSem += semester[1:]
	if "F" in semester:
		craftedSem += "30"
	elif "W" in semester:
		craftedSem += "10"
	else:
            raise ValueError("Could not craftURL from given semester data")

	craftedURL = "http://at.eng.carleton.ca/engsched/wishlist.php?&courses="
	craftedURL += str(courseID)
	craftedURL += "&term="
	craftedURL += craftedSem
	craftedURL += "&list="

	print (craftedURL)

	return craftedURL


    def _parseCourseJson(self, courseJson):
	# Get rid of empty lists
	courseJson = courseJson[1][0]

	# Create Course obj from data avail in the frist section json
	dept = courseJson[0]['dept']
	courseNum = courseJson[0]['course']
	title = courseJson[0]['title']
	course = Course(dept, courseNum, title)

	# Create each Section obj and add to Course
	for sectionJson in courseJson:
		course.addSection(self._parseSectionJson(sectionJson, dept, courseNum))

	return course


    def _parseSectionJson(self, sectionJson, dept, courseNum):
	# Create Section
	name = dept + courseNum  + " " + sectionJson['section']
	timeSlot = TimeSlot(sectionJson['days'], sectionJson['start'], sectionJson['end'])
	section = Section(name, timeSlot)

	# Create and add Lab objects and add to Section
	if len(sectionJson['labs']) > 0:
		for labJson in sectionJson['labs'][0]:
			section.addLab(self._parseLabJson(labJson, dept, courseNum))
		section.setLabs(list(set(section.getLabs())))

	return section


    def _parseLabJson(self, labJson, dept, courseNum):
	#Create and return Lab obj
	name = dept + courseNum + " " + labJson['section']
	timeSlot = TimeSlot(labJson['days'], labJson['start'], labJson['end'])
	return Lab(name, timeSlot)

