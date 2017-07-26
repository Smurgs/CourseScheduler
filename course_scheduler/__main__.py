from gui import *


def main():
    gui = Tk()
    timetable = TimetableFrame()
    course_entry = CourseEntryFrame()
    results_frame = ResultsFrame()
    observers = [timetable, results_frame]
    user_control = UserControlFrame(course_entry, observers)

    course_entry.grid(row=0, column=0)
    user_control.grid(row=0, column=1)
    timetable.grid(row=0, column=2)
    results_frame.grid(row=0, column=3)

    gui.mainloop()


if __name__ == "__main__":
    main()
