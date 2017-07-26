import json

import requests

from school_objects import *


class InfoManager(object):
    def __init__(self):
        pass

    def get_course_info(self, course_id, semester):
        """Get and parse course info for *courseID*. Return Course obj"""

        # Get course JSON via HTTP req
        url = self._craft_url(course_id, semester)
        # pdb.set_trace()
        http_request = requests.get(url)
        course_json_str = http_request.content.split("<html")[0]
        if course_json_str == [[[]], []]:
            raise ValueError("No data available for course: " + str(course_id))

        # Parse JSON into Course containing Sections
        return self._parse_course_json(json.loads(course_json_str))

    def _craft_url(self, course_id, semester):
        crafted_sem = "20"
        crafted_sem += semester[1:]
        if "F" in semester:
            crafted_sem += "30"
        elif "W" in semester:
            crafted_sem += "10"
        else:
            raise ValueError("Could not craftURL from given semester data")

        crafted_url = "http://at.eng.carleton.ca/engsched/wishlist.php?&courses="
        crafted_url += str(course_id)
        crafted_url += "&term="
        crafted_url += crafted_sem
        crafted_url += "&list="

        print (crafted_url)

        return crafted_url

    def _parse_course_json(self, course_json):
        # Get rid of empty lists
        course_json = course_json[1][0]

        # Create Course obj from data avail in the first section json
        dept = course_json[0]['dept']
        course_num = course_json[0]['course']
        title = course_json[0]['title']
        course = Course(dept, course_num, title)

        # Create each Section obj and add to Course
        for section_json in course_json:
            course.add_section(self._parse_section_json(section_json, dept, course_num))

        return course

    def _parse_section_json(self, section_json, dept, course_num):
        # Create Section
        name = dept + course_num + " " + section_json['section']
        time_slot = TimeSlot(section_json['days'], section_json['start'], section_json['end'])
        section = Section(name, time_slot)

        # Create and add Lab objects and add to Section
        if len(section_json['labs']) > 0:
            for lab_json in section_json['labs'][0]:
                section.add_lab(self._parse_lab_json(lab_json, dept, course_num))
            section.set_labs(list(set(section.get_labs())))

        return section

    def _parse_lab_json(self, lab_json, dept, course_num):
        # Create and return Lab obj
        name = dept + course_num + " " + lab_json['section']
        time_slot = TimeSlot(lab_json['days'], lab_json['start'], lab_json['end'])
        return Lab(name, time_slot)
