
class Course(object):
    def __init__(self, dept, course, title):
        """Course object constructor"""

        self._dept = str(dept)
        self._course = str(course)
        self._title = str(title)
        self._sections = []

    def get_title(self):
        """Returns string of course title ex Circuit and Signals"""
        return self._title

    def get_dept(self):
        """Returns string of course dept ex ELEC"""
        return self._dept

    def get_course(self):
        """Returns string of course code ex 2501"""
        return self._course

    def get_sections(self):
        """Returns list of course sections objects"""
        return self._sections

    def get_number_of_sections(self):
        """Returns int of number of sections associated with course"""
        return len(self._sections)

    def add_section(self, section):
        """Adds *section* to the list of Sections for the course"""
        if type(section) == Section:
            self._sections.append(section)
            return True

        return False

    def remove_section(self, sec):
        self._sections.remove(sec)
        if len(self._sections) == 0:
            return -1

        return 0

    def set_sections(self, new_section_list):
        self._sections = new_section_list


class Classroom(object):
    def __init__(self, name, time_slot):
        self._name = str(name)
        self._timeSlot = time_slot

    def get_name(self):
        return self._name

    def get_time_slot(self):
        return self._timeSlot

    def get_days(self):
        return self._timeSlot.get_days()

    def get_start_time(self):
        return self._timeSlot.get_start_time()

    def get_end_time(self):
        return self._timeSlot.get_end_time()


class Section(Classroom):
    def __init__(self, name, time_slot):
        """Constructor for section object"""
        super(Section, self).__init__(name, time_slot)
        self._labs = []

    def get_labs(self):
        return self._labs

    def get_number_of_labs(self):
        return len(self._labs)

    def add_lab(self, lab):
        if type(lab) == Lab:
            self._labs.append(lab)
            return True

        return False

    def remove_lab(self, lab):
        self._labs.remove(lab)
        if len(self._labs) == 1:
            return -1

        return 0

    def set_labs(self, new_labs_list):
        self._labs = new_labs_list


class Lab(Classroom):
    def __init__(self, name, time_slot):
        """Constructor for lab object"""
        super(Lab, self).__init__(name, time_slot)

    def __eq__(self, other):
        return type(self) == type(other) and self.get_time_slot() == other.get_time_slot()

    def __hash__(self):
        return hash((self.get_days(), self.get_start_time(), self.get_end_time()))


class TimeSlot(object):
    def __init__(self, days, start_time, end_time):
        self._days = str(days)
        self._start_time = self._string_time_to_int(start_time)
        self._end_time = self._string_time_to_int(end_time)

    def __eq__(self, other):
        return self.get_days() == other.get_days() and self.get_start_time() == other.get_start_time() \
               and self.get_end_time() == other.get_end_time()

    def get_days(self):
        return self._days

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def _string_time_to_int(self, t):
        return int(t[0] + t[1] + t[3] + t[4])
