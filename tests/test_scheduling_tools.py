import sys
sys.path.append('../course_scheduler')

from course_scheduler.scheduling_tools import *


class TestVirtualSchedule(object):

    def setup(self):
        self.vs = VirtualSchedule()

    def test_empty_schedule(self):
        assert len(self.vs.get_registered_classes()) == 0

    def test_add_section(self):
        time_slot = TimeSlot("M", "08:35", "11:35")
        section = Section("MATH2004A", time_slot)
        assert self.vs.add_to_schedule(section)
        assert len(self.vs.get_registered_classes()) == 1

    def test_add_lab(self):
        time_slot = TimeSlot("T", "08:35", "11:35")
        lab = Lab("MATH2004A", time_slot)
        assert self.vs.add_to_schedule(lab)
        assert len(self.vs.get_registered_classes()) == 1

    def test_no_overlap(self):
        time_slot = TimeSlot("M", "08:35", "11:35")
        section = Section("MATH2004A", time_slot)
        assert self.vs.add_to_schedule(section)

        time_slot = TimeSlot("M", "08:35", "11:35")
        lab = Lab("ELEC2004A", time_slot)
        assert not self.vs.add_to_schedule(lab)

        time_slot = TimeSlot("M", "10:35", "12:35")
        lab = Lab("ELEC2004A", time_slot)
        assert not self.vs.add_to_schedule(lab)

        time_slot = TimeSlot("M", "06:35", "09:35")
        lab = Lab("ELEC2004A", time_slot)
        assert not self.vs.add_to_schedule(lab)

        time_slot = TimeSlot("M", "06:35", "12:35")
        lab = Lab("ELEC2004A", time_slot)
        assert not self.vs.add_to_schedule(lab)

    def test_boundary(self):
        time_slot = TimeSlot("M", "08:35", "11:25")
        section = Section("MATH2004A", time_slot)
        assert self.vs.add_to_schedule(section)

        time_slot = TimeSlot("M", "11:35", "12:25")
        lab = Lab("ELEC2004A", time_slot)
        assert self.vs.add_to_schedule(lab)

        time_slot = TimeSlot("M", "07:35", "08:25")
        lab = Lab("ELEC2004A", time_slot)
        assert self.vs.add_to_schedule(lab)

