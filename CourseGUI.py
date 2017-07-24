###############################################################################
#
#	Outlines GUI for course scheduling program
#	Classes: TopFrame, CourseEntryFrame, UserControlFrame, TimetableFrame
# 	Uses built-in module: Tkinter
#
###############################################################################

from Tkinter import *
from SchedulingTools import *

###############################################################################
#	
#							CourseEntryFrame
#
###############################################################################

class CourseEntryFrame(Frame):

	def __init__(self):
		Frame.__init__(self)

		# Course code input via entry fields
		courseLabel = Label(self, text="Enter course codes:")
		courseLabel.pack()
		courseExample = Label(self, text="Ex. MATH2004")
		courseExample.pack()

		self._courseEntries = []
		for num in range(7):
			self._courseEntries.append(Entry(self))
			self._courseEntries[num].pack()

		# Semester input via drop down list
		semesterLabel = Label(self, text="Choose semester:")
		semesterLabel.pack()

		self._selectedSemester = StringVar(self)
		self._selectedSemester.set("Fall 2017")
		semesterList = OptionMenu(self, self._selectedSemester, "Fall 2017", "Winter 2018")
		semesterList.pack()


	def getCourseCodes(self):
		courseCodes = []
		for entry in self._courseEntries:
			if entry.get() != '':
				courseCodes.append(entry.get())

		return courseCodes

	def getSelectedSemester(self):
		"""Returns 3 char string for semester and year. Ex: F15, W15, S15"""
		longString = self._selectedSemester.get()
		return longString[:1] + longString[-2:]


###############################################################################
#	
#							UserControlFrame
#
###############################################################################

class UserControlFrame(Frame):

	def __init__(self, courseEntry, observers):
		Frame.__init__(self)
		self._courseEntry = courseEntry
		self._observers = observers
		self._userFilters = []

		# FILTERS
		filterFrame = Frame(self)
		Label(filterFrame, text="Filters:").pack()
		# Day filters
		self._userFilters.append(Checkbutton(filterFrame, text="Mondays off", onvalue=1))
		self._userFilters.append(Checkbutton(filterFrame, text="Tuesdays off", onvalue=2))
		self._userFilters.append(Checkbutton(filterFrame, text="Wednesdays off", onvalue=3))
		self._userFilters.append(Checkbutton(filterFrame, text="Thursdays off", onvalue=4))
		self._userFilters.append(Checkbutton(filterFrame, text="Fridays off", onvalue=5))
		
		# Start after filter
		self._userFilters.append(Checkbutton(filterFrame, text="Start after:", onvalue=6))
		self._startAfter = AdjustableClock(filterFrame)
		# Finish before filter
		self._userFilters.append(Checkbutton(filterFrame, text="Finish before: ", onvalue=7))
		self._finishBefore = AdjustableClock(filterFrame)

		# Add int var to checkboxes
		self._userFilterIntVar = []
		for checkbox in self._userFilters: 
			self._userFilterIntVar.append(IntVar())
			checkbox['variable'] = self._userFilterIntVar[-1]

		# Pack filters
		for checkbox in self._userFilters[:5]:
			checkbox.pack()								# Days off and Least down time
		self._userFilters[5].pack()						# Starting after option
		self._startAfter.pack()							# Starting after clock
		self._userFilters[6].pack()						# Finish before option
		self._finishBefore.pack()						# Finish before clock


		# PREFERENCES
		preferenceFrame = Frame(self)
		self._userPref = IntVar()

		Label(preferenceFrame, text="Preferences:").pack()
		Radiobutton(preferenceFrame, text="None", variable=self._userPref, value=0).pack()
		Radiobutton(preferenceFrame, text="Least down time", variable=self._userPref, value=1).pack()
		Radiobutton(preferenceFrame, text="Morning classes", variable=self._userPref, value=2).pack()
		Radiobutton(preferenceFrame, text="Evening classes", variable=self._userPref, value=3).pack()


		filterFrame.pack()
		Frame(self, height=50).pack()
		preferenceFrame.pack()

		# Button to generate schedule
		goButton = Button(self, text="Schedule it!", command=self.startCourseSelection)
		goButton.pack()

	def startCourseSelection(self):
		startEndTimes = {'start':self._startAfter.getValue(), 'end':self._finishBefore.getValue()}
		scheduler = Scheduler(self._observers, self._courseEntry.getCourseCodes(), self._courseEntry.getSelectedSemester(), self.getUserOptions(), startEndTimes)
		scheduler.startScheduling()

	def getUserOptions(self): 
		filtersList = []
		for var in self._userFilterIntVar: 
			filtersList.append(var.get())

		# Returns tuple of (list of filters selected, preference selected)
		return (list(set(filtersList))[1:], self._userPref.get())




###############################################################################
#	
#							TimetableFrame
#
###############################################################################

class TimetableFrame(Frame):

	TIMETABLE_BACKGROUND_COLOR = "#EAE9E9"
	TIME_BLOCKS = [830,900,930,1000,1030,1100,1130,1200,1230,1300,1330, \
	1400,1430,1500,1530,1600,1630,1700,1730,1800,1830,1900,1930,2000,2030]
	DAYS = ['M', 'T', 'W', 'R', 'F']

	def __init__(self):
		Frame.__init__(self)
		self._timeLabels = self._addTimeLabels()
		self._dayLabels = self._addDayLabels()
		self._timeSlots = self._addBlankTimeSlots()

	def _addTimeLabels(self):
		timeLabels = []
		for slot in self.TIME_BLOCKS:
			time = str(slot)[:-2] + ":" + str(slot)[-2:]
			timeLabels.append (Label(self, text=time, width=5, relief=RIDGE))
			timeLabels[self.TIME_BLOCKS.index(slot)].grid(row=1+self.TIME_BLOCKS.index(slot), column=0)

		return timeLabels


	def _addBlankTimeSlots(self):
		timeSlots = []
		for halfhour in range(25):
			timeSlots.append([])
			for day in range(5):
				timeSlots[halfhour].append(Label(self, bg=self.TIMETABLE_BACKGROUND_COLOR, height=1, width=15, relief=RIDGE))
				timeSlots[halfhour][day].grid(row=1+halfhour, column=1+day)

		return timeSlots


	def _addDayLabels(self):
		dayLabels = []
		dayLabels.append(Label(self, text="Monday", width=15, relief=RIDGE))
		dayLabels.append(Label(self, text="Tuesday", width=15, relief=RIDGE))
		dayLabels.append(Label(self, text="Wednesday", width=15, relief=RIDGE))
		dayLabels.append(Label(self, text="Thursday", width=15, relief=RIDGE))
		dayLabels.append(Label(self, text="Friday", width=15, relief=RIDGE))

		for x in range(5):
			dayLabels[x].grid(row=0, column=x+1)

		return dayLabels

	def _addBlockToTimetable(self, newValue, days, startTime, endTime):
		startTime -= 5
		endTime -= 25
		changeFlag = False
		twoDayEntryFlag = False
		dayPosition0 = self.DAYS.index(days[0])
		dayPosition1 = -1

		if len(days) > 1: 
			twoDayEntryFlag = True
			dayPosition1 = self.DAYS.index(days[1])

		for slot in self.TIME_BLOCKS:
			if changeFlag:
				self._changeLabel(newValue, self.TIME_BLOCKS.index(slot), dayPosition0, dayPosition1)

			if slot == startTime:
				changeFlag = True
				self._changeLabel(newValue, self.TIME_BLOCKS.index(slot), dayPosition0, dayPosition1)

			if slot == endTime:
				break

	def _changeLabel(self, newValue, timePos, dayPos, dayPos2=-1):
		self._timeSlots[timePos][dayPos]['text'] = newValue
		if dayPos2 >= 0:
			self._timeSlots[timePos][dayPos2]['text'] = newValue

	def _reset(self):
		self._timeSlots = self._addBlankTimeSlots()

	def update(self, newTimetable, otherInfo):
		self._reset()
		for entry in newTimetable.getRegisteredClasses():
			self._addBlockToTimetable(entry.getName(), entry.getDays(), entry.getStartTime(), entry.getEndTime())



###############################################################################
#	
#							AdjustableClock
#
###############################################################################

class AdjustableClock(Frame): 
	def __init__(self, container):
		Frame.__init__(self, container)

		self._hourValue = StringVar(self)
		self._hourValue.set("8")
		hourList = OptionMenu(self, self._hourValue, "8","9","10","11","12","13","14","15","16","17","18","19","20","21","22")
		hourList.config(width=6)
		hourList.grid(row=0, column=0)

		self._minValue = StringVar(self)
		self._minValue.set("30")
		minList = OptionMenu(self, self._minValue, "00","15","30","45")
		minList.config(width=6)
		minList.grid(row=0, column=1)

	def getValue(self):
		return (int(self._hourValue.get()) * 100) + int(self._minValue.get())


###############################################################################
#	
#							ResultsFrame
#
###############################################################################

class ResultsFrame(Frame):

	EMPTY_INDEX_STRING = "0 / 0"

	def __init__(self):
		Frame.__init__(self)

		width = Label (self, text="                              ")
		width.pack()

		self._courseResults = []
		for x in range (14):
			self._courseResults.append(Label(self))
		for label in self._courseResults:
			label.pack()

		self._indexLabel = Label(self)
		self._indexLabel.pack()

		self._resetResults()
		
		backButton = Button(self, text="<<", command=self._getLastTimetable)
		backButton.pack()

		nextButton = Button(self, text=">>", command=self._getNextTimetable)
		nextButton.pack()

	def _getLastTimetable(self): 
		if self._currentIndex == None: return
		if self._currentIndex == 0: return
		self._scheduler.getTimeTableAtIndex(self._currentIndex - 1)

	def _getNextTimetable(self): 
		if self._currentIndex == None: return
		if self._currentIndex + 1 == self._totalNumber: return
		self._scheduler.getTimeTableAtIndex(self._currentIndex + 1)


	def _resetResults(self):
		for label in self._courseResults:
			label['text'] = ""

		self._indexLabel['text'] = ResultsFrame.EMPTY_INDEX_STRING

		self._currentIndex = None
		self._totalNumber = None
		self._scheduler = None
		

	def update(self, newTimetable, info): 
		self._resetResults()

		# Add labels for alphabetically sorted courses in this timetable
		stringLabels = []
		for entry in newTimetable.getRegisteredClasses():
			stringLabels.append(entry.getName())
		stringLabels.sort()
		for x in range(len(stringLabels)):
			self._courseResults[x]['text'] = stringLabels[x]

		# Modify index label
		self._indexLabel['text'] = str(info['currentIndex']+1) + " / " + str(info['totalNumber'])
		self._currentIndex = info['currentIndex']
		self._totalNumber = info['totalNumber']
		self._scheduler = info['scheduler']


