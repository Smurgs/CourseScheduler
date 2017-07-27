import pkg_resources
import json
import sys
sys.path.append('../course_scheduler')

from course_scheduler.mapper import InfoManager


class TestMapper(object):

    def test_craft_url_fall_17(self):
        assert InfoManager._craft_url("MATH2004", "F17") == "http://at.eng.carleton.ca/engsched/wishlist.php?" \
                                               "&courses=MATH2004&term=201730&list="

    def test_craft_url_winter_18(self):
        assert InfoManager._craft_url("SYSC2004", "W18") == "http://at.eng.carleton.ca/engsched/wishlist.php?" \
                                               "&courses=SYSC2004&term=201810&list="

    def test_craft_url_summer_20(self):
        assert InfoManager._craft_url("MATH2004", "S20") == "http://at.eng.carleton.ca/engsched/wishlist.php?" \
                                               "&courses=MATH2004&term=202020&list="

    def test_mapper(self):
        text = pkg_resources.resource_string(__name__, "math2004_response.json")
        json_object = json.loads(text)
        course = InfoManager._parse_course_json(json_object)

        assert course.get_course() == "2004"
        assert course.get_dept() == "MATH"
        assert course.get_title() == "Multivariable Cal. Eng or Phys"
        assert course.get_number_of_sections() == 5

        assert course.get_sections()[0].get_name() == "MATH2004 F"
        assert course.get_sections()[0].get_time_slot().get_days() == "TR"
        assert course.get_sections()[0].get_time_slot().get_start_time() == 1135
        assert course.get_sections()[0].get_time_slot().get_end_time() == 1255

        assert len(course.get_sections()[0].get_labs()) == 1
        assert course.get_sections()[0].get_labs()[0].get_name() == "MATH2004 FT"
        assert course.get_sections()[0].get_labs()[0].get_time_slot().get_days() == "R"
        assert course.get_sections()[0].get_labs()[0].get_time_slot().get_start_time() == 1735
        assert course.get_sections()[0].get_labs()[0].get_time_slot().get_end_time() == 1825
