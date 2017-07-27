import tkMessageBox
import copy
import random

from mapper import *


class Scheduler(object):
    def __init__(self, observers, course_codes, semester, user_options, start_end_times):
        self._observers = observers
        self._course_codes = course_codes
        self._semester = semester
        self._user_filters, self._user_preference = user_options
        self._start_after = start_end_times['start'] if 6 in self._user_filters else 0
        self._end_before = start_end_times['end'] if 7 in self._user_filters else 2400
        self._valid_timetables = []
        self.PREFERENCES = [self._no_preference, self._least_down_time, self._morning_classes, self._evening_classes]

    def start_scheduling(self):
        self._course_objects = self._get_course_data()

        # Filter out sections and courses
        if self._filter_days() == -1:
            self._no_possible_timetable()

        if self._filter_start_end_times() == -1:
            self._no_possible_timetable()

        self._find_and_rate_all(self.PREFERENCES[self._user_preference])
        self._valid_timetables = sorted(self._valid_timetables, key=lambda entry: entry._score, reverse=True)

        self._update_observers(self._valid_timetables[0])

    def get_time_table_at_index(self, index):
        self._update_observers(self._valid_timetables[index])

    def _update_observers(self, timetable):
        info = {
            'totalNumber': len(self._valid_timetables),
            'currentIndex': self._valid_timetables.index(timetable),
            'scheduler': self
        }

        for observer in self._observers:
            observer.update(timetable, info)

    def _get_course_data(self):
        course_objs = []
        for course_code in self._course_codes:
            course_objs.append(InfoManager.get_course_info(course_code, self._semester))
        return course_objs

    def _find_and_rate_all(self, preference_function):
        virtual_schedule = VirtualSchedule(len(self._course_objects))
        self._recursive_section_loop(0, virtual_schedule, preference_function)

    def _recursive_section_loop(self, depth_of_recursion, vs, preference_function):
        if depth_of_recursion == len(self._course_objects):
            self._recursive_lab_loop(0, vs, vs.get_registered_classes(), preference_function)
            return

        for section in self._course_objects[depth_of_recursion].get_sections():
            virtual_schedule = copy.deepcopy(vs)
            if virtual_schedule.add_to_schedule(section):
                self._recursive_section_loop(depth_of_recursion + 1, virtual_schedule, preference_function)

    def _recursive_lab_loop(self, depth_of_recursion, vs, sections, preference_function):
        if depth_of_recursion == len(self._course_objects):
            self._valid_timetables.append(ValidTimetable(vs.get_registered_classes(), preference_function))
            return

        if len(sections[depth_of_recursion].get_labs()) < 1:
            self._recursive_lab_loop(depth_of_recursion + 1, vs, sections, preference_function)

        for lab in sections[depth_of_recursion].get_labs():
            virtual_schedule = copy.deepcopy(vs)
            if virtual_schedule.add_to_schedule(lab):
                self._recursive_lab_loop(depth_of_recursion + 1, virtual_schedule, sections, preference_function)

    def _no_preference(self, x=None):
        return random.randint(0, 99)

    def _least_down_time(self, valid_timetable):
        pass

    def _morning_classes(self, valid_timetable):
        score = 0
        for entry in valid_timetable.get_registered_classes():
            score += (25 - entry.get_start_time())
        return score

    def _evening_classes(self, valid_timetable):
        score = 0
        for entry in valid_timetable.get_registered_classes():
            score += entry.get_start_time()
        return score

    def _filter_start_end_times(self):
        # Check if the constraint should be applied
        if 6 not in self._user_filters and 7 not in self._user_filters:
            return 0

        return self._apply_filter(self._time_filter, None)

    def _filter_days(self):
        days_off = []
        for option in self._user_filters:
            if option == 1:
                days_off.append('M')
            if option == 2:
                days_off.append('T')
            if option == 3:
                days_off.append('W')
            if option == 4:
                days_off.append('R')
            if option == 5:
                days_off.append('F')

        if len(days_off) == 0:
            return 0

        return self._apply_filter(self._day_filter, days_off)

    def _apply_filter(self, filter_function, filter_variable):
        for course in self._course_objects:
            course.set_sections([sec for sec in course.get_sections() if not filter_function(sec, filter_variable)])

            for section in course.get_sections():
                section.set_labs([lab for lab in section.get_labs() if not filter_function(lab, filter_variable)])

            course.set_sections([sec for sec in course.get_sections() if len(sec.get_labs()) != 0])
            if len(course.get_sections()) == 0:
                return -1
        return 0

    def _time_filter(self, classroom, variable):
        return classroom.get_start_time() < self._start_after or classroom.get_end_time() > self._end_before

    def _day_filter(self, classroom, days_off):
        return len([i for e in days_off for i in classroom.get_days() if e in i]) > 0

    def _no_possible_timetable(self):
        tkMessageBox.showinfo("Course Scheduler",
                              "Sorry! There aren't any possible timetables with the chosen filters.")


class ValidTimetable(object):
    def __init__(self, registered_classes, preference_function):
        self._classes = registered_classes
        self._score = preference_function(self)

    def get_score(self):
        return self._score

    def get_registered_classes(self):
        return self._classes

    def to_string(self):
        string = ""
        for c in self._classes:
            string += c.get_name() + " " + str(c.get_start_time()) + "-" + str(c.get_end_time()) + "\n"
        return string


class VirtualSchedule(object):
    def __init__(self, num_of_courses, ):
        self._days = {
            'M': [],
            'T': [],
            'W': [],
            'R': [],
            'F': []
        }
        self._classes = []

    def add_to_schedule(self, classroom):
        # Break the time interval down into 5 min intervals
        time_intervals = [x for x in range(classroom.get_start_time(), classroom.get_end_time() + 5, 5) if x % 100 < 60]

        # Check if those time slots are already being used, is so return false
        for day in classroom.get_days():
            if len([i for i in time_intervals if i in self._days[day]]) > 0:
                return False

        # Add the time intervals to the respective days and return true
        for day in classroom.get_days():
            self._days[day].extend(time_intervals)
        self._classes.append(classroom)
        return True

    def get_registered_classes(self):
        return copy.deepcopy(self._classes)
