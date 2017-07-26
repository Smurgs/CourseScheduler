
###############################################################################
#	
#							Course
#
###############################################################################

class Course(object):
	def __init__(self, dept, course, title):
		"""Couse object constructor"""

		self._dept = str(dept)
		self._course = str(course)
		self._title = str(title)
		self._sections = []

	def getTitle(self):
		"""Returns string of course title ex Circuit and Signals"""
		return self._title

	def getDept(self):
		"""Returns string of course dept ex ELEC"""
		return self._dept

	def getCourse(self):
		"""Returns string of course code ex 2501"""
		return self._course

	def getSections(self):
		"""Returns list of course sections objects"""
		return self._sections

	def getNumberOfSections(self):
		"""Returns int of number of sections associated with course"""
		return len(self._sections)

	def addSection(self, section):
		"""Adds *section* to the list of Sections for the course"""
		if type(section) == Section:
			self._sections.append(section)
			return True

		return False

	def removeSection(self, sec):
		self._sections.remove(sec)
		if len(self._sections) == 0:
			return -1

		return 0

	def setSections(self, newSectionList):
		self._sections = newSectionList


###############################################################################
#	
#							Classroom
#
###############################################################################


class Classroom(object):
	def __init__(self, name, timeSlot):
		self._name = str(name)
		self._timeSlot = timeSlot

	def getName(self):
		return self._name

	def getTimeSlot(self):
		return self._timeSlot

	def getDays(self):
		return self._timeSlot.getDays()

	def getStartTime(self):
		return self._timeSlot.getStartTime()

	def getEndTime(self):
		return self._timeSlot.getEndTime()


###############################################################################
#	
#							Section
#
###############################################################################


class Section(Classroom):
	def __init__(self, name, timeSlot):
		"""Constructor for section object"""
		super(Section, self).__init__(name, timeSlot)
		self._labs = []

	def getLabs(self):
		return self._labs

	def getNumberOfLabs(self):
		return len(self._labs)

	def addLab(self, lab):
		if type(lab) == Lab:
			self._labs.append(lab)
			return True

		return False

	def removeLab(self, lab):
		self._labs.remove(lab)
		if len(self._labs) == 1:
			return -1

		return 0

	def setLabs(self, newLabsList):
		self._labs = newLabsList


###############################################################################
#	
#							Lab
#
###############################################################################


class Lab(Classroom):
	def __init__(self, name, timeSlot):
		"""Constructor for lab object"""
		super(Lab, self).__init__(name, timeSlot)

	def __eq__(self, other):
		return type(self)==type(other) and self.getTimeSlot()==other.getTimeSlot()

	def __hash__(self):
		return hash((self.getDays(), self.getStartTime(), self.getEndTime()))


###############################################################################
#	
#							TimeSlot
#
###############################################################################


class TimeSlot(object):
	def __init__(self, days, startTime, endTime):
		self._days = str(days)
		self._startTime = self._stringTimeToInt(startTime)
		self._endTime = self._stringTimeToInt(endTime)

	def __eq__(self, other):
		return self.getDays()==other.getDays() and self.getStartTime()==other.getStartTime()\
		and self.getEndTime()==other.getEndTime()

	def getDays(self):
		return self._days

	def getStartTime(self):
		return self._startTime

	def getEndTime(self):
		return self._endTime

	def _stringTimeToInt(self, t):
		return int(t[0] + t[1] + t[3] + t[4])