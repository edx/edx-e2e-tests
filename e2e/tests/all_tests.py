import unittest

from e2e.tests import create_courses, delete_all_changes
from e2e.tests.courses import test_courses_visibility, test_pages_visibility, \
    test_courses_settings, test_courses_search, test_certificate
from e2e.tests.instructor import test_cohorts, test_membership, test_student_admin
from e2e.tests.login import test_logging, test_account, test_profile
from e2e.tests.sysadmin import test_courses, test_users
from e2e.tests.units import test_units_activity, test_unit_visibility, test_discussion, test_xblocks

testSuite = unittest.TestSuite()

testSuite.addTest(unittest.makeSuite(create_courses.CreateCourse))

testSuite.addTest(unittest.makeSuite(test_logging.TestLogging)) # 4m
testSuite.addTest(unittest.makeSuite(test_account.TestAccount)) # 36m
testSuite.addTest(unittest.makeSuite(test_profile.TestProfile)) # 15m

testSuite.addTest(unittest.makeSuite(test_courses.TestCourses)) # 5m
testSuite.addTest(unittest.makeSuite(test_users.TestUsers)) # 20m

testSuite.addTest(unittest.makeSuite(test_courses_search.TestCoursesSearch)) # 14m
testSuite.addTest(unittest.makeSuite(test_courses_visibility.TestCoursesVisibility)) # 39m
testSuite.addTest(unittest.makeSuite(test_pages_visibility.TestPagesVisibility)) # 8m
testSuite.addTest(unittest.makeSuite(test_unit_visibility.TestUnitVisibility)) # 18m TOODO
testSuite.addTest(unittest.makeSuite(test_courses_settings.TestCoursesSettings)) # 55m

testSuite.addTest(unittest.makeSuite(test_certificate.TestCertificate)) # 9m
testSuite.addTest(unittest.makeSuite(test_units_activity.TestUnitsActivity)) # 1h 20m
testSuite.addTest(unittest.makeSuite(test_discussion.TestDiscussion)) # 38m
testSuite.addTest(unittest.makeSuite(test_xblocks.TestXblocks)) # 39m

testSuite.addTest(unittest.makeSuite(test_membership.TestMembership)) # 1h 11m
testSuite.addTest(unittest.makeSuite(test_cohorts.TestCohorts)) # 6m
testSuite.addTest(unittest.makeSuite(test_student_admin.TestStudentAdmin))

testSuite.addTest(unittest.makeSuite(delete_all_changes.DeleteAllChanges))

print("count of tests: " + str(testSuite.countTestCases()) + "\n")
runner = unittest.TextTestRunner(verbosity=2)
runner.run(testSuite)