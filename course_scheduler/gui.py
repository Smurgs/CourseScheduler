from Tkinter import *

from scheduling_tools import *


class CourseEntryFrame(Frame):
    def __init__(self):
        Frame.__init__(self)

        # Course code input via entry fields
        course_label = Label(self, text="Enter course codes:")
        course_label.pack()
        course_example = Label(self, text="Ex. MATH2004")
        course_example.pack()

        self._course_entries = []
        for num in range(7):
            self._course_entries.append(Entry(self))
            self._course_entries[num].pack()

        # Semester input via drop down list
        semester_label = Label(self, text="Choose semester:")
        semester_label.pack()

        self._selected_semester = StringVar(self)
        self._selected_semester.set("Fall 2017")
        semester_list = OptionMenu(self, self._selected_semester, "Fall 2017", "Winter 2018")
        semester_list.pack()

    def get_course_codes(self):
        course_codes = []
        for entry in self._course_entries:
            if entry.get() != '':
                course_codes.append(entry.get())

        return course_codes

    def get_selected_semester(self):
        """Returns 3 char string for semester and year. Ex: F15, W15, S15"""
        long_string = self._selected_semester.get()
        return long_string[:1] + long_string[-2:]


class UserControlFrame(Frame):
    def __init__(self, course_entry, observers):
        Frame.__init__(self)
        self._course_entry = course_entry
        self._observers = observers
        self._user_filters = []

        # FILTERS
        filter_frame = Frame(self)
        Label(filter_frame, text="Filters:").pack()
        # Day filters
        self._user_filters.append(Checkbutton(filter_frame, text="Mondays off", onvalue=1))
        self._user_filters.append(Checkbutton(filter_frame, text="Tuesdays off", onvalue=2))
        self._user_filters.append(Checkbutton(filter_frame, text="Wednesdays off", onvalue=3))
        self._user_filters.append(Checkbutton(filter_frame, text="Thursdays off", onvalue=4))
        self._user_filters.append(Checkbutton(filter_frame, text="Fridays off", onvalue=5))

        # Start after filter
        self._user_filters.append(Checkbutton(filter_frame, text="Start after:", onvalue=6))
        self._start_after = AdjustableClock(filter_frame)
        # Finish before filter
        self._user_filters.append(Checkbutton(filter_frame, text="Finish before: ", onvalue=7))
        self._finish_before = AdjustableClock(filter_frame)

        # Add int var to checkboxes
        self._user_filter_int_var = []
        for checkbox in self._user_filters:
            self._user_filter_int_var.append(IntVar())
            checkbox['variable'] = self._user_filter_int_var[-1]

        # Pack filters
        for checkbox in self._user_filters[:5]:
            checkbox.pack()  # Days off and Least down time
        self._user_filters[5].pack()  # Starting after option
        self._start_after.pack()  # Starting after clock
        self._user_filters[6].pack()  # Finish before option
        self._finish_before.pack()  # Finish before clock

        # PREFERENCES
        preference_frame = Frame(self)
        self._user_pref = IntVar()

        Label(preference_frame, text="Preferences:").pack()
        Radiobutton(preference_frame, text="None", variable=self._user_pref, value=0).pack()
        Radiobutton(preference_frame, text="Least down time", variable=self._user_pref, value=1).pack()
        Radiobutton(preference_frame, text="Morning classes", variable=self._user_pref, value=2).pack()
        Radiobutton(preference_frame, text="Evening classes", variable=self._user_pref, value=3).pack()

        filter_frame.pack()
        Frame(self, height=50).pack()
        preference_frame.pack()

        # Button to generate schedule
        go_button = Button(self, text="Schedule it!", command=self.start_course_selection)
        go_button.pack()

    def start_course_selection(self):
        start_end_times = {'start': self._start_after.get_value(), 'end': self._finish_before.get_value()}
        scheduler = Scheduler(self._observers, self._course_entry.get_course_codes(),
                              self._course_entry.get_selected_semester(), self.get_user_options(), start_end_times)
        scheduler.start_scheduling()

    def get_user_options(self):
        filters_list = []
        for var in self._user_filter_int_var:
            filters_list.append(var.get())

        # Returns tuple of (list of filters selected, preference selected)
        return list(set(filters_list))[1:], self._user_pref.get()


class TimetableFrame(Frame):
    TIMETABLE_BACKGROUND_COLOR = "#EAE9E9"
    TIME_BLOCKS = [830, 900, 930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430,
                   1500, 1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930, 2000, 2030]
    DAYS = ['M', 'T', 'W', 'R', 'F']

    def __init__(self):
        Frame.__init__(self)
        self._time_labels = self._add_time_labels()
        self._day_labels = self._add_day_labels()
        self._time_slots = self._add_blank_time_slots()

    def _add_time_labels(self):
        time_labels = []
        for slot in self.TIME_BLOCKS:
            time = str(slot)[:-2] + ":" + str(slot)[-2:]
            time_labels.append(Label(self, text=time, width=5, relief=RIDGE))
            time_labels[self.TIME_BLOCKS.index(slot)].grid(row=1 + self.TIME_BLOCKS.index(slot), column=0)

        return time_labels

    def _add_blank_time_slots(self):
        time_slots = []
        for half_hour in range(25):
            time_slots.append([])
            for day in range(5):
                time_slots[half_hour].append(
                    Label(self, bg=self.TIMETABLE_BACKGROUND_COLOR, height=1, width=15, relief=RIDGE))
                time_slots[half_hour][day].grid(row=1 + half_hour, column=1 + day)

        return time_slots

    def _add_day_labels(self):
        day_labels = [
            Label(self, text="Monday", width=15, relief=RIDGE),
            Label(self, text="Tuesday", width=15, relief=RIDGE),
            Label(self, text="Wednesday", width=15, relief=RIDGE),
            Label(self, text="Thursday", width=15, relief=RIDGE),
            Label(self, text="Friday", width=15, relief=RIDGE)
        ]

        for x in range(5):
            day_labels[x].grid(row=0, column=x + 1)

        return day_labels

    def _add_block_to_timetable(self, new_value, days, start_time, end_time):
        start_time -= 5
        end_time -= 25
        change_flag = False
        day_position0 = self.DAYS.index(days[0])
        day_position1 = -1

        if len(days) > 1:
            day_position1 = self.DAYS.index(days[1])

        for slot in self.TIME_BLOCKS:
            if change_flag:
                self._change_label(new_value, self.TIME_BLOCKS.index(slot), day_position0, day_position1)

            if slot == start_time:
                change_flag = True
                self._change_label(new_value, self.TIME_BLOCKS.index(slot), day_position0, day_position1)

            if slot == end_time:
                break

    def _change_label(self, new_value, time_pos, day_pos, day_pos2=-1):
        self._time_slots[time_pos][day_pos]['text'] = new_value
        if day_pos2 >= 0:
            self._time_slots[time_pos][day_pos2]['text'] = new_value

    def _reset(self):
        self._time_slots = self._add_blank_time_slots()

    def update(self, newTimetable, otherInfo):
        self._reset()
        for entry in newTimetable.get_registered_classes():
            self._add_block_to_timetable(entry.get_name(), entry.get_days(), entry.get_start_time(), entry.get_end_time())


class AdjustableClock(Frame):
    def __init__(self, container):
        Frame.__init__(self, container)

        self._hour_value = StringVar(self)
        self._hour_value.set("8")
        hour_list = OptionMenu(self, self._hour_value, "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18",
                               "19", "20", "21", "22")
        hour_list.config(width=6)
        hour_list.grid(row=0, column=0)

        self._min_value = StringVar(self)
        self._min_value.set("30")
        min_list = OptionMenu(self, self._min_value, "00", "15", "30", "45")
        min_list.config(width=6)
        min_list.grid(row=0, column=1)

    def get_value(self):
        return (int(self._hour_value.get()) * 100) + int(self._min_value.get())


class ResultsFrame(Frame):
    EMPTY_INDEX_STRING = "0 / 0"

    def __init__(self):
        Frame.__init__(self)

        width = Label(self, text="                              ")
        width.pack()

        self._course_results = []
        for x in range(14):
            self._course_results.append(Label(self))
        for label in self._course_results:
            label.pack()

        self._index_label = Label(self)
        self._index_label.pack()

        self._reset_results()

        back_button = Button(self, text="<<", command=self._get_last_timetable)
        back_button.pack()

        next_button = Button(self, text=">>", command=self._get_next_timetable)
        next_button.pack()

    def _get_last_timetable(self):
        if self._current_index is None:
            return
        if self._current_index == 0:
            return
        self._scheduler.get_time_table_at_index(self._current_index - 1)

    def _get_next_timetable(self):
        if self._current_index is None:
            return
        if self._current_index + 1 == self._total_number:
            return
        self._scheduler.get_time_table_at_index(self._current_index + 1)

    def _reset_results(self):
        for label in self._course_results:
            label['text'] = ""

        self._index_label['text'] = ResultsFrame.EMPTY_INDEX_STRING

        self._current_index = None
        self._total_number = None
        self._scheduler = None

    def update(self, new_timetable, info):
        self._reset_results()

        # Add labels for alphabetically sorted courses in this timetable
        string_labels = []
        for entry in new_timetable.get_registered_classes():
            string_labels.append(entry.get_name())
        string_labels.sort()
        for x in range(len(string_labels)):
            self._course_results[x]['text'] = string_labels[x]

        # Modify index label
        self._index_label['text'] = str(info['currentIndex'] + 1) + " / " + str(info['totalNumber'])
        self._current_index = info['currentIndex']
        self._total_number = info['totalNumber']
        self._scheduler = info['scheduler']
