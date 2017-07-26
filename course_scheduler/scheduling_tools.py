from mapper import *
import tkMessageBox, copy, random

###############################################################################
#	
#							Scheduler
#
###############################################################################

class Scheduler(object):

	

	def __init__(self, observers, courseCodes, semester, userOptions, startEndTimes):
		self._observers = observers
		self._courseCodes = courseCodes
		self._semester = semester
		self._userFilters, self._userPreference = userOptions
		self._infoManager = InfoManager()
		self._startAfter = startEndTimes['start'] if 6 in self._userFilters else 0
		self._endBefore = startEndTimes['end'] if 7 in self._userFilters else 2400
		self._validTimetables = []
		self.PREFERENCES = [self._noPreference, self._leastDownTime, self._morningClasses, self._eveningClasses]

	def startScheduling(self):
		self._courseObjects = self._getCourseData()

		# Filter out sections and courses
		if self._filterDays() == -1:
			self._noPossibleTimetable()

		if self._filterStartEndTimes() == -1:
			self._noPossibleTimetable()

		self._findAndRateAll(self.PREFERENCES[self._userPreference])
		self._validTimetables = sorted(self._validTimetables, key=lambda entry: entry._score, reverse=True)

		self._updateObservers(self._validTimetables[0])

	def getTimeTableAtIndex(self, index):
		self._updateObservers(self._validTimetables[index])

	def _updateObservers(self, timetable):
		info = {}
		info['totalNumber'] = len(self._validTimetables)
		info['currentIndex'] = self._validTimetables.index(timetable)
		info['scheduler'] = self

		for observer in self._observers:
			observer.update(timetable, info)

	def _getCourseData(self):
		courseObjs = []
		for courseCode in self._courseCodes:
			courseObjs.append(self._infoManager.getCourseInfo(courseCode, self._semester))
		return courseObjs

	def _findAndRateAll(self, preferenceFunction):
		virtualSchedule = VirtualSchedule(len(self._courseObjects))
		self._recursiveSectionLoop(0, virtualSchedule, preferenceFunction)

	def _recursiveSectionLoop(self, depthOfRecursion, vs, preferenceFunction):
		if depthOfRecursion == len(self._courseObjects):
			self._recursiveLabLoop(0, vs, vs.getRegisteredClasses(), preferenceFunction)
			return

		for section in self._courseObjects[depthOfRecursion].getSections():
			virtualSchedule = copy.deepcopy(vs)
			if virtualSchedule.addToSchedule(section):
				self._recursiveSectionLoop(depthOfRecursion + 1, virtualSchedule, preferenceFunction)

	def _recursiveLabLoop(self, depthOfRecursion, vs, sections, preferenceFunction):
		if depthOfRecursion == len(self._courseObjects):
			self._validTimetables.append(ValidTimetable(vs.getRegisteredClasses(), preferenceFunction))
			return

		if len(sections[depthOfRecursion].getLabs()) < 1:
			self._recursiveLabLoop(depthOfRecursion + 1, vs, sections, preferenceFunction)

		for lab in sections[depthOfRecursion].getLabs():
			virtualSchedule = copy.deepcopy(vs)
			if virtualSchedule.addToSchedule(lab):
				self._recursiveLabLoop(depthOfRecursion + 1, virtualSchedule, sections, preferenceFunction)


	def _noPreference(self, x=None):
		return random.randint(0,99)

	def _leastDownTime(self, validTimetable):
		pass

	def _morningClasses(self, validTimetable):
		score = 0
		for entry in validTimetable.getRegisteredClasses():
			score += (25 - entry.getStartTime())
		return score

	def _eveningClasses(self, validTimetable):
		score = 0
		for entry in validTimetable.getRegisteredClasses():
			score += entry.getStartTime()
		return score

	def _filterStartEndTimes(self):
		# Check if the constraint should be applied
		if 6 not in self._userFilters and 7 not in self._userFilters: 
			return 0

		return self._applyFliter(self._timeFilter, None)

	def _filterDays(self):
		daysOff = []
		for option in self._userFilters:
			if option == 1:
				daysOff.append('M')
			if option == 2:
				daysOff.append('T')
			if option == 3:
				daysOff.append('W')
			if option == 4:
				daysOff.append('R')
			if option == 5:
				daysOff.append('F')

		if len(daysOff) == 0:
			return 0

		return self._applyFliter(self._dayFilter, daysOff)

	def _applyFliter(self, filterFunction, filterVariable):
		for course in self._courseObjects:
			course.setSections( [sec for sec in course.getSections() if not filterFunction(sec, filterVariable)] )

			for section in course.getSections():
				section.setLabs( [lab for lab in section.getLabs() if not filterFunction(lab,filterVariable)] )

			course.setSections( [sec for sec in course.getSections() if len(sec.getLabs()) != 0] )
			if len(course.getSections()) == 0: 
				return -1
		return 0

	def _timeFilter(self, classroom, variable):
		return classroom.getStartTime() < self._startAfter or classroom.getEndTime() > self._endBefore

	def _dayFilter(self, classroom, daysOff):
		return len([i for e in daysOff for i in classroom.getDays() if e in i]) > 0

	def _noPossibleTimetable(self):
		tkMessageBox.showinfo("Course Scheduler", "Sorry! There aren't any possible timetables with the chosen filters.")


###############################################################################
#	
#							ValidTimetable
#
###############################################################################

class ValidTimetable(object):
	def __init__(self, registeredClasses, preferenceFunction):
		self._classes = registeredClasses
		self._score = preferenceFunction(self);

	def getScore(self):
		return self._score

	def getRegisteredClasses(self):
		return self._classes

	def toString(self):
		string = ""
		for c in self._classes:
			string += c.getName() + " " + str(c.getStartTime()) + "-" + str(c.getEndTime()) + "\n"
		return string


###############################################################################
#	
#							VirtualSchedule
#
###############################################################################

class VirtualSchedule(object):
	def __init__(self, numOfCourses, ):
		self._days = {}
		self._days['M'] = []
		self._days['T'] = []
		self._days['W'] = []
		self._days['R'] = []
		self._days['F'] = []
		self._classes = []

	def addToSchedule(self, classroom):
		# Break the time interval down into 5 min intervals
		timeIntervals = [x for x in range(classroom.getStartTime(), classroom.getEndTime()+5, 5) if x % 100 < 60]

		# Check if those timeslots are already being used, is so return false
		for day in classroom.getDays():
			if len([i for i in timeIntervals if i in self._days[day]]) > 0:
				return False

		# Add the time intervals to the respective days and return true
		for day in classroom.getDays():
			self._days[day].extend(timeIntervals)
		self._classes.append(classroom)
		return True

	def getRegisteredClasses(self):
		return copy.deepcopy(self._classes)
			

