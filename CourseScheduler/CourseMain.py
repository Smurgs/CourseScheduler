from Tkinter import *
from CourseGUI import *
###############################################################################
#					  		  	MAIN 										  #
###############################################################################

gui = Tk()
timetable = TimetableFrame()
courseEntry = CourseEntryFrame()
resultsFrame = ResultsFrame()
observers = [timetable, resultsFrame]
userControl = UserControlFrame(courseEntry, observers)


courseEntry.grid(row=0, column=0)
userControl.grid(row=0, column=1)
timetable.grid(row=0, column=2)
resultsFrame.grid(row=0, column=3)

gui.mainloop()
