import sys
sys.path.append('../course_scheduler')

from course_scheduler.mapper import *

def test_craft_url():
    im = InfoManager()
    assert im._craft_url("MATH2004", "F17") == "http://at.eng.carleton.ca/engsched/wishlist.php?&courses=MATH2004&term=201730&list="
