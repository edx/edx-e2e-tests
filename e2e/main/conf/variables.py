#-----MAIN INFO-----
from pexpect.ANSI import term

COURSE_NONE = "/course_none.tar.gz"
COURSE_BOTH = "/course_both.tar.gz"
COURSE_ORA = "/course_ora.tar.gz"

URL_LINKEDIN_PROFILE = "https://www.linkedin.com/in/andrey-mishchenko-2aa77612b/"
URL_FACEBOOK_PROFILE = "https://www.facebook.com/andrey.mishchenko.754"
URL_TWITTER_PROFILE = "https://twitter.com/AndreyMishchen1"
PATH_TO_LIB = "/Users/andreymishchenko/PycharmProjects/edx-e2e-tests/e2e"
URL_EMAIL = "https://mail.google.com/mail/u/0/?ogbl#inbox"
LOGIN_EMAIL_STAFF = "staff@example.com"
LOGIN_EMAIL_ADMIN = "staff"

#-----PROJECTS-----
PROJECT = ""
VERSION = ""

VERSION_IRONWOOD = "Ironwood"
PROJECT_LETSTUDY = "Letstudy"

VERSION_HAWTHORN = "Hawthorn"
PROJECT_DEMOUNIVERSITY = "Demo university"
PROJECT_ASUSGAB = "Asu Sgab"
PROJECT_DIMINGWAY = "Deming Way"
PROJECT_USDS = "USDS" #TestCoursesSearch + TestCoursesSettings + #TestMembership + #TestProfile + TestAccount #TestDiscussion #ORA #TestStudentAdmin

VERSION_GINKO = "Ginko"
PROJECT_GREEN_HOST = "Green Host"
PROJECT_ASUOSPP = "Asu Ospp"

VERSION_FIKUS = "Ficus"
PROJECT_TBS = "Toulouse BS" #TestProfile + TestAccount #TestMembership #TestDiscussion #ORA #TestStudentAdmin
PROJECT_E4H = "E4H" #ALL
PROJECT_GIJIMA = "Gijima"
PROJECT_WARDY = "Wardy it"
PROJECT_SPECTRUM = "Spectrum"

#-----PROJECTS VALUES-----
#Letstudy PROD
'''URL_LMS = "https://lms-letstudy-ironwood.raccoongang.com"
URL_DASHBOARD = "https://lms-letstudy-ironwood.raccoongang.com/dashboard"
URL_CMS = "https://cms-letstudy-ironwood.raccoongang.com/admin"
URL_ADMIN = "https://lms-letstudy-ironwood.raccoongang.com/admin/"
LOGIN_PASSWORD_STAFF = "BXfo1U6VQpHwBvxoNkPOnE"
VERSION = VERSION_IRONWOOD
PROJECT = PROJECT_LETSTUDY'''

"--------------------------------------------------------------------------------------------"

#New University Dev
'''URL_LMS = "https://new-university-dev.raccoongang.com"
URL_CMS = "https://new-university-dev-studio.raccoongang.com"
URL_ADMIN = "https://new-university-dev.raccoongang.com/admin/"
LOGIN_PASSWORD_STAFF = "F3XBvzrzxziOQ77utPM6UZ"
VERSION = VERSION_HAWTHORN
PROJECT = PROJECT_DEMOUNIVERSITY'''
#New University Stage'''
'''URL_LMS = "https://new-university-staging.raccoongang.com"
URL_CMS = "https://new-studio-staging.raccoongang.com"
URL_ADMIN = "https://new-university-staging.raccoongang.com/admin/"
LOGIN_PASSWORD_STAFF = "HI7Q2zGwpBrSVOyKiIt1BO"
VERSION = VERSION_HAWTHORN
PROJECT = PROJECT_DEMOUNIVERSITY'''
#New University Prod
'''URL_LMS = "https://new-university.raccoongang.com"
URL_CMS = "https://new-studio.raccoongang.com"
URL_ADMIN = "https://new-university.raccoongang.com/admin/"
LOGIN_PASSWORD_STAFF = "A3kMr8cmqI2uy4zroV4gEo"
VERSION = VERSION_HAWTHORN
PROJECT = PROJECT_DEMOUNIVERSITY'''

#ASUOSGA QA
'''URL_LENG = "https://courses-sga-stage.starbucksglobalacademy.com/update_lang"
URL_LMS = "https://courses-sga-stage.starbucksglobalacademy.com"
URL_CMS = "https://studio-sga-stage.starbucksglobalacademy.com"
URL_ADMIN = "https://courses-sga-stage.starbucksglobalacademy.com/admin/"
LOGIN_PASSWORD_STAFF = "p3dUa5wrIKnl3ATVxxjELp"
VERSION = VERSION_HAWTHORN
PROJECT = PROJECT_ASUSGAB'''
#ASUOSGA Prod
'''URL_LENG = "https://courses-sga.starbucksglobalacademy.com/update_lang"
URL_LMS = "https://courses-sga.starbucksglobalacademy.com"
URL_CMS = "https://studio-sga.starbucksglobalacademy.com"
URL_ADMIN = "https://courses-sga.starbucksglobalacademy.com/admin/"
LOGIN_PASSWORD_STAFF = "SLCIZWtQBmlXApTb1NdK9r"
VERSION = VERSION_HAWTHORN
PROJECT = PROJECT_ASUSGAB'''

#Deming Way QA
'''URL_LMS = "https://lms-staging-demingway.raccoongang.com"
URL_CMS = "https://cms-staging-demingway.raccoongang.com"
URL_ADMIN = "https://lms-staging-demingway.raccoongang.com/admin/"
LOGIN_PASSWORD_STAFF = "KZvx6AO2On3F3z0zTHgbys"
VERSION = VERSION_HAWTHORN
PROJECT = PROJECT_DIMINGWAY'''
#Deming Way Prod
'''URL_LMS = "https://thedemingway.com"
URL_CMS = "https://studio.demingway.com"
URL_ADMIN = "https://thedemingway.com/admin/"
LOGIN_PASSWORD_STAFF = "VJt5KhqKF1SXbQqpNXFyJe"
VERSION = "Havthorn"
PROJECT = PROJECT_DIMINGWAY'''

#USDS Prod Пока не работает
'''URL_LMS = "https://courses-test.phc.org.ua"
URL_CMS = "https://studio-test.phc.org.ua"
URL_ADMIN = "https://courses-test.phc.org.ua/admin/"
LOGIN_PASSWORD_STAFF = "3cPeh6IcPgYQBM7rkbTg0j"
VERSION = VERVERSION_HAWTHORN
PROJECT = PROJECT_USDS'''

"--------------------------------------------------------------------------------------------"

#Greenhost Stage
'''URL_LMS = "https://lms-staging-greenhost.raccoongang.com"
URL_CMS = "https://cms-staging-greenhost.raccoongang.com"
URL_ADMIN = "https://lms-staging-greenhost.raccoongang.com/admin/"
LOGIN_PASSWORD_STAFF = "U8r2T9blPBG9wNS3nzr864"
VERSION = VERSION_GINKO
PROJECT = PROJECT_GREEN_HOST'''
#Greenhost Prod
'''LOGIN_EMAIL_STAFF = "info@totem-project.org"
URL_LMS = "https://learn.totem-project.org"
URL_CMS = "https://studio.totem-project.org"
URL_ADMIN = "https://learn.totem-project.org/admin/"
LOGIN_PASSWORD_STAFF = "kldkNMuV1ZMX0OhFAqzfTKhrKxJg49Ew"
VERSION = VERSION_GINKO
PROJECT = PROJECT_GREEN_HOST'''

#ASUOSPP QA
'''URL_LMS = "https://courses-qa.ea.asu.edu/beta-testers-login"
URL_CMS = "https://studio-qa.ea.asu.edu/admin/login/?next=/admin/"
URL_ADMIN = "https://courses-qa.ea.asu.edu/admin/"
URL_DASHBOARD = "https://courses-qa.ea.asu.edu/dashboard"
URL_SYSADMIN = "https://courses-qa.ea.asu.edu/sysadmin"
LOGIN_PASSWORD_STAFF = "A9Xi3yjSMPy2F5dJPqkVgg"
VERSION = VERSION_GINKO
PROJECT = PROJECT_ASUOSPP'''
#ASUOSPP DEV
'''URL_LMS = "https://courses-dev.ea.asu.edu/beta-testers-login"
URL_CMS = "https://studio-dev.ea.asu.edu/admin/login/?next=/admin/"
URL_ADMIN = "https://courses-dev.ea.asu.edu/admin/"
URL_SYSADMIN = "https://courses-dev.ea.asu.edu/sysadmin"
LOGIN_PASSWORD_STAFF = "Afewrw8gOEHsdfsdkXZ0vlQW=f"
VERSION = VERSION_GINKO
PROJECT = PROJECT_ASUOSPP'''
#ASUOSPP Prod
'''URL_LMS = "https://courses.ea.asu.edu/beta-testers-login"
URL_CMS = "https://studio.ea.asu.edu/login/?next=/admin/"
URL_ADMIN = "https://courses.ea.asu.edu/admin/"
URL_SYSADMIN = "https://courses.ea.asu.edu/sysadmin"
LOGIN_PASSWORD_STAFF = "WFcI6avjWFu4XsCBCwKyeg"
VERSION = VERSION_GINKO
PROJECT = PROJECT_ASUOSPP'''

"--------------------------------------------------------------------------------------------"

#Touluse BS Prod Doesn't work now
'''URL_LMS = "http://e-learning.tbs-education.ma"
URL_CMS = "http://studio.e-learning.tbs-education.ma/"
URL_ADMIN = "http://e-learning.tbs-education.ma/admin/"
LOGIN_PASSWORD_STAFF = "SdO074DkNiSzpL9k0rdLVd"
VERSION = VERSION_FIKUS
PROJECT = PROJECT_TBS'''

#E4H Stage Doesn't work now
'''URL_COURSES = "https://stagelms.e4h-test.com/courses"
URL_DASHBOARD = "https://stagelms.e4h-test.com/dashboard"
URL_LMS = "https://stagelms.e4h-test.com"
URL_CMS = "https://studio.e4h-test.com"
URL_ADMIN = "https://stagelms.e4h-test.com/admin/"
LOGIN_PASSWORD_STAFF = "hEkPOsI5NsZyfl9BLm4b62"
VERSION = VERSION_FIKUS
PROJECT = PROJECT_E4H'''

#Gijima Prod
'''URL_LMS = "https://lms-gijima.raccoon.bar"
URL_CMS = "https://studio.gijima.com/"
URL_ADMIN = "https://lms-gijima.raccoon.bar/admin/"
LOGIN_PASSWORD_STAFF = "PyqigROhx73FfhqQbg2o3W"
VERSION = VERSION_FIKUS
PROJECT = PROJECT_GIJIMA'''

#Wardy IT Prod
'''URL_LMS = "https://learning.wardyit.com"
URL_CMS = "https://studio.wardyit.com"
URL_ADMIN = "https://learning.wardyit.com/admin/"
LOGIN_PASSWORD_STAFF = "kf8SsMVbp3KzMRDDF1EjDS"
VERSION = VERSION_FIKUS
PROJECT = PROJECT_WARDY'''

#Spectrum Prod
'''URL_LMS = "https://learn.specnt.com"
URL_CMS = "https://courses.specnt.com"
URL_ADMIN = "https://learn.specnt.com/admin/"
LOGIN_PASSWORD_STAFF = "PmsKoGemBIXwcOMX94C9fI"
VERSION = VERSION_FIKUS
PROJECT = PROJECT_SPECTRUM'''

#-----LOGINS AND PASSWORDS-----
LOGIN_EMAIL_FIRST = "andrey.v.mishchenko@gmail.com"
LOGIN_EMAIL_SECOND = "andrey.vl.mishchenko@gmail.com"
LOGIN_EMAIL_INCORRECT = "andrey.incorrect.mishchenko@gmail.com"
LOGIN_EMAIL_BROCKEN = "andrey.v.gamegmail.com"

LOGIN_PASSWORD = "A13121985VMRG"
LOGIN_PASSWORD_INCORRECT = "A13121985VNRG"
LOGIN_PASSWORD_NEW = "A13121985VMRGNEW"

LOGIN_EMAIL_CREATED_USER = "andrey.v.game@gmail.com"
LOGIN_PASSWORD_CREATED_USER = "123456"

#GMAIL_EMAIL = "andrey.v.test1@gmail.com"
#GMAIL_EMAIL = "andrey.v.test2@gmail.com"
GMAIL_EMAIL = "andrey.v.test3@gmail.com"
GMAIL_PASSWORD = "A123456vm"

FULL_NAME = "Andrey Mishchenko"
FULL_NAME_NEW = "Some New Full Name"
FULL_NAME_STAFF = "Staff"
USERNAME_STAFF = "staff"
NAME_FIRST = "1_Test1"
NAME_SECOND = "1_Test2"
if PROJECT in (PROJECT_ASUOSPP + PROJECT_E4H):
    NAME_FIRST = LOGIN_EMAIL_FIRST
    NAME_SECOND = LOGIN_EMAIL_SECOND

EMAIL_FOR_CREATE = "andrey.test."
NAME_FOR_CREATE = "Andrey Mishchenko Test"

#-----COURSES CREDANTIALS-----
ID = "course-v1:"
ID_BASE_COURSE = ID + "edX+DemoX+Demo_Course"
BASE_COURSE_NAME = 'edx demonstration course'
BASE_ORGANIZATION = "edX"
BASE_COURSE_NUMBER = "DemoX"
BASE_COURSE_RUN = "Demo_Course"

COURSE_NAME = 'test demonstration course'
COURSE_NAME_FIRST = 'test course first'
COURSE_NAME_SECOND = 'test course second'
NEW_COURSE_NAME = "test demonstration new course"
if(PROJECT in PROJECT_ASUSGAB):
    BASE_COURSE_NAME = 'edx - demox'
ORGANIZATION = "andrey_v_m"
ORGANIZATION_FOR_DELETE = "andrey_v_m_delete"
FOR_COURSE_NUMBER = "test_course_number_"
COURSE_NUMBER_POSITIVE = "e2e-testing_course_positive"
COURSE_NUMBER_NEGATIVE = "e2e-testing_course_negative"
COURSE_RUN = "2019"

#-----TEXTS OF ELEMENTS-----
TEXT_MY_COURSES = "my courses"
TEXT_COURSE_OUTLINE = "Course Outline"
VIEW_COURSE = "view course"
VIEW_ARCHIVED_COURSE = "view archived course"
COHORT_CONTAINS_STUDENT = "(contains 1 student)"
SAVED_COHORT = "Saved cohort"
CERTIFICATE_DETAILS = "Certificate Details"

#-----TEXTS FOR PATHES-----
PATH_DAYS_FOR_BETA = "days_early_for_beta"
PATH_CERTIFICATES_DISPLAY_BEHAVIOR = "certificates_display_behavior"
PATH_INVITATION_ONLY = "invitation_only"
PATH_CATALOG_VISIBILITY = "catalog_visibility"
PATH_COURSE_NOT_GRATED = "no_grade"
PATH_DISABLE_PROGRESS = "disable_progress_graph"
PATH_MAXIMUM_ATTEMPTS = "max_attempts"
PATH_SHOW_ANSWER = "showanswer"
PATH_SHOW_CALCULATOR = "show_calculator"
PATH_SHOW_RESET = "show_reset_button"
PATH_DISPLAY_NAME = "display_name"
PATH_CLASS_SHOW_ANSWER = "response-label field-label label-inline choicegroup_correct"
PATH_ORA_TEXT_FIELD = "openassessment_submission_text_response"
PATH_ORA_FILE_FIELD = "openassessment_submission_file_upload_response"
PATH_ORA_MUST_GRADE_FIELD = "peer_assessment_must_grade"
PATH_ORA_GRADED_BY_FIELD = "peer_assessment_graded_by"

PATH_ORA_LEARNERS_RESPONSE = "learner_response_"
PATH_ORA_PEER_ASSESSMENTS_FOR = "peer_"
PATH_ORA_PEER_ASSESSMENTS_BY = "submitted_"
PATH_ORA_SELF_ASSESSMENT = "self_"
PATH_ORA_STAFF_ASSESSMENT = "staff_"
PATH_ORA_FINAL_GRADE = "final_grade_"
PATH_ORA_SUBMIT_ASSESSMENT = "grade_override_"
PATH_ORA_REMOVE_SUBMISSION = "remove_submission_"


#-----NAMES OF PAGES-----
PAGE_HOME = "Home"
PAGE_COURSE = "Course"
PAGE_DISCUSSION = "Discussion"
PAGE_WIKI = "Wiki"
PAGE_PROGRESS = "Progress"
PAGES_DEFOULT_NAME = "Empty"
PAGES_NAME = "Some new page"
PAGES_BODY = "Some text for page"

#-----UNITS ACTIVITY (ANSWER)-----
ANSWER_ALWAYS = "always"
ANSWER_ANSWERED = "answered"
ANSWER_ATTEMPTED = "attempted"
ANSWER_CLOSED = "closed"
ANSWER_FINISHED = "finished"
ANSWER_PAST_DUE = "past_due"
ANSWER_CORRECT_PAST_DUE = "correct_or_past_due"
ANSWER_NEWER = "never"
ID_UNIT_1 = "block-v1:andrey_v_m+e2e-testing_course_positive+2019+type@problem+block@77d0021642094be8bc24e7d1e8425943"
ID_UNIT_1_NEGATIVE = "block-v1:andrey_v_m+e2e-testing_course_negative+2019+type@problem+block@77d0021642094be8bc24e7d1e8425943"
ID_UNIT_2 = "block-v1:andrey_v_m+e2e-testing_course_positive+2019+type@problem+block@cc18de3f3d364b8eb3ba8f8c93121b53"
ID_UNIT_2_NEGATIVE = "block-v1:andrey_v_m+e2e-testing_course_negative+2019+type@problem+block@cc18de3f3d364b8eb3ba8f8c93121b53"
ID_UNIT_3 = "block-v1:andrey_v_m+e2e-testing_course_positive+2019+type@problem+block@7cb8c85631df4804949506aa34e0ef02"
ID_UNIT_3_NEGATIVE = "block-v1:andrey_v_m+e2e-testing_course_negative+2019+type@problem+block@7cb8c85631df4804949506aa34e0ef02"

#-----COURSES VISIBILITY-----
STATUS_VISIBILITY_BOTH = "both"
STATUS_VISIBILITY_ABOUT = "about"
STATUS_VISIBILITY_NONE = "none"

#-----DISCUSSIONS-----
STATUS_QUESTION = "question"
STATUS_DISCUSSION = "discussion"
TEXT_PINNED = "Pinned"
TEXT_REPORTED = "Reported"
TEXT_CLOSED = "Closed"
DISCUSSION_TITLE_STAFF = "Title by staff"
DISCUSSION_IDEA_STAFF = "Idea by staff"
DISCUSSION_TITLE_FIRST = "Title by user 1 + "
DISCUSSION_TITLE_FIRST_NEW = "New title by user 1 + "
DISCUSSION_TITLE_SECOND = "Title by user 2 + "
DISCUSSION_IDEA_FIRST = "Idea by user 1 + "
DISCUSSION_IDEA_FIRST_NEW = "New idea by user 1 + "
DISCUSSION_IDEA_SECOND = "Idea by user 2 + "
DISCUSSION_REPLY_FIRST = "Reply by user 1 + "
DISCUSSION_REPLY_FIRST_NEW = "New reply by user 1 + "
DISCUSSION_REPLY_SECOND = "Reply by user 1 + "

#-----ROLES-----
ROLE_STAFF = "Staff"
ROLE_ADMIN = "Admin"
ROLE_BETA_TESTERS = "Beta Testers"
ROLE_DISCUSSION_ADMINS = "Discussion Admins"
ROLE_DISCUSSION_MODERATORS = "Discussion Moderators"
ROLE_DISCUSSION_COMMUNITY_TAS = "Discussion Community TAs"
ROLE_GROUP_COMMUNITY_TA = "Group Community TA"
ROLE_COMMUNITY_TA = "Community TA"

#-----SOME STATUSES-----
STATUS_INPUT = "Input"
STATUS_CHANGE = "Change"
STATUS_ENROLL = "Enroll"
STATUS_UNENROLL = "Unenroll"
STATUS_CMS = "CMS"
STATUS_LMS = "LMS"
STATUS_ADMIN = "Admin"
STATUS_PASSWORD = "password"
STATUS_TRUE = "true"
STATUS_FALSE = "false"
STATUS_REQUIRED = "Required"
STATUS_OPTIONAL = "Optional"
STATUS_PDF = "PDF or Image Files"
STATUS_IMG = "Image Files"
STATUS_DOC = "Custom File Types"
STATUS_NONE = "None"
STATUS_ON = "1"
STATUS_OFF = "0"
STATUS_MODE_HONOR = "honor"

#-----COURSES TEXTS-----
FILE_PATH_COURSE_OVERVIEW = "/tests/courses/course_overview.txt"
FILE_PATH_COURSE_OVERVIEW_FOR_SEARCH = "/tests/courses/course_overview_for_search.txt"
FILE_PATH_FIRST_CORRECT_ANSWER = "/tests/instructor/first_correct_answer.txt"
TEXT_COURSE_SHORT_DESCRIPTION = "сourse short description fot testing"
TEXT_CLASSES_START = "jan 1, 2018;"
TEXT_CLASSES_END = "jan 1, 203"
TEXT_ABOUT_THIS_COURSE = "about this course"
TEXT_ABOUT_COURSE_INFO = "test info about course"
TEXT_NEW_STAFF_MEMBER_1 = "new staff member #1"
TEXT_NEW_STAFF_MEMBER_2 = "new staff member #2"
TEXT_SOME_TEXT = "some text"
TEXT_SOME_NEW_TEXT = "some new text"
TEXT_WEEK_WORK_HOURS = "40:00"
TEXT_AMHARIC = "Amharic"
TEXT_AM = "am"
TEXT_HAUSA = "Hausa"
TEXT_HA = "ha"
TEXT_ALL_RIGHTS_RESERVED = "All Rights Reserved"
TEXT_SOME_RIGHT_RESERVED = "Some Rights Reserved"
TEXT_ATTRIBUTION = "Attribution"
TEXT_NONCOMMERCIAL = "Noncommercial"
TEXT_NO_DERIVATIVES = "No Derivatives"
TEXT_SHARE_ALIKE = "Share Alike"
TEXT_COURSE_UPDATES = "some text for course updates"
TEXT_COURSE_HANDOUTS = "some text for course handouts"
TEXT_NEW_COURSE_UPDATES = "some new text for course updates"
TEXT_NEW_COURSE_HANDOUTS = "some new text for course handouts"
TEXT_YOU_ARE_ENROLLED = "you are enrolled in this course"

#-----X-Blocks-----
TEXT_RELEASE_DATE = "Release Date"
TEXT_HOMEWORK = "Homework"
TEXT_HW = "HW"
BLOCK_MULTIPLE_CHOICE = "Multiple Choice"
BLOCK_CHECKBOXES = "Checkboxes"
BLOCK_DISCUSSION = "Discussion"
BLOCK_ORA = "Open Response Assessment"
if(PROJECT in PROJECT_GIJIMA + PROJECT_WARDY + PROJECT_SPECTRUM):
    BLOCK_ORA = "Peer Assessment"
SECTION_NAME_1 = "Section_1"
SECTION_NAME_2 = "Section_2"
SUBSECTION_NAME_1 = "Subsection_1"
SUBSECTION_NAME_2 = "Subsection_2"
UNIT_NAME_EXAM = "Unit for exam"
UNIT_NAME_1 = "Unit_1"
UNIT_NAME_2 = "Unit_2"
UNIT_NAME_3 = "Unit_3"
UNIT_NAME_4 = "Unit_4"
UNIT_NAME_5 = "Unit_5"
UNIT_NAME_6 = "Unit_6"
UNIT_NAME_7 = "Unit_7"
UNIT_NAME_8 = "Unit_8"
TEXT_ANSWER_HULF_OF_3 = "(0.5/3) 17%"
TEXT_ANSWER_1_OF_3 = "(1/3) 33%"
TEXT_ANSWER_2_OF_3 = "(2/3) 67%"
TEXT_ANSWER_8_OF_72 = "(8/72)"
TEXT_ANSWER_6 = "(6/72)"
TEXT_ANSWER_4_OF_72 = "(4/72)"
TEXT_ANSWER_1_72 = "(1/72)"
TEXT_ANSWER_0_OF_3 = "(0/3)"
TEXT_GRADE_0 = "Overall Score; 0%"
TEXT_GRADE_67 = "Overall Score; 67%"
TEXT_GRADE_33 = "Overall Score; 33%"
TEXT_GRADE_17 = "Overall Score; 17%"
TEXT_GRADE_11 = "Overall Score; 11%"
TEXT_GRADE_8 = "Overall Score; 8%"
TEXT_GRADE_6 = "Overall Score; 6%"
TEXT_GRADE_1 = "Overall Score; 1%"
TEXT_CORRECT_ANSWER = "Correct (1/1 point)"
TEXT_INCORRECT_ANSWER = "Incorrect (0/1 point)"
SHOW_ANSWER = "Show Answer"
RESET = "Reset"

#-----Account/Profile-----
LINE_LANGUAGE = "language"
LANGUAGE_ALBANIAN = "Albanian"
LANGUAGE_ALBANIAN_SHORT = "sq"
LANGUAGE_ARABIC = "Arabic"
LANGUAGE_ARABIC_SHORT = "ar"
LINE_LOCATION = "location"
AUSTRIA = "Austria"
AUSTRIA_SHORT = "AT"
ARUBA = "Aruba"
ARUBA_SHORT = "AW"
LINE_TIME_ZOON = "Time zoon"
TIME_ZOON_AFRICA = "Africa/Casablanca"
TIME_ZOON_AFRICA_SHORT = "Africa/Casablanca"
TIME_ZOON_AMERICA = "America/Cambridge Bay"
TIME_ZOON_AMERICA_SHORT = "America/Cambridge_Bay"
LINE_EDUCATION = "Education"
DOCTORATE = "Doctorate"
DOCTORATE_SHORT = "p"
ASSOCIATE_DEGREE = "Associate degree"
ASSOCIATE_DEGREE_SHORT = "a"
LINE_GENDER = "Gender"
MALE = "Male"
MALE_SHORT = "m"
FEMALE = "Female"
FEMALE_SHORT = "f"
LINE_BIRSDAY = "Birsday"
YEAR_YOUNG = "2015"
YEAR_2000 = "2000"
SIGN_IN = "sign in"
LOG_IN = "log in"
TEXT_JOINED = "Joined"
TEXT_LOCATION = "Location"
TEXT_LANGUAGE = "Language"
TEXT_ABOUT_ME = "About me"
TEXT_EXPLORE_NEW_COURSES = "EXPLORE NEW COURSES"
FULL_PROFILE = "Full Profile"
LIMITED_PROFILE = "Limited Profile"
THIS_VALUE_IS_INVALID = "This value is invalid."
VALID_EMAIL_ADDRESS_REQUIRED = "Valid e-mail address required."
EMAIL_ALREADY_EXISTS = "An account with this e-mail already exists."

#-----SOME TEXTS-----
EMPTY = ""
TEXT_COMPLETE = "COMPLETE"
TEXT_IN_PROGRESS = "IN PROGRESS"
TEXT_NOT_AVAILABLE = "NOT AVAILABLE"
TEXT_IN_PROGRESS_1 = "IN PROGRESS (1 OF 2)"
TEXT_IN_PROGRESS_2 = "IN PROGRESS (2 OF 2)"
TEXT_1_OF_8 = "1 out of 8"
TEXT_4_OF_8 = "4 out of 8"
TEXT_6_OF_8 = "6 out of 8"
TEXT_8_OF_8 = "8 out of 8"
TEXT_IDEAS_GOOD_5_5 = "Ideas Good 5 5"
TEXT_IDEAS_FAIR_3_5 = "Ideas Fair 3 5"
TEXT_IDEAS_POOR_0_5 = "Ideas Poor 0 5"
TEXT_CONTENT_EXCELLENT_3_3 = "Content Excellent 3 3"
TEXT_CONTENT_GOOD_3_3 = "Content Good 3 3"
TEXT_CONTENT_FAIR_1_3 = "Content Fair 1 3"
TEXT_CONTENT_POOR_0_3 = "Content Poor 0 3"
TEXT_AVAILABLE_2_0 = "2 AVAILABLE AND 0 CHECKED OUT"
TEXT_AVAILABLE_0_1 = "0 AVAILABLE AND 1 CHECKED OUT"
TEXT_SUCCESS = "SUCCESS"

TEXT_TEST = "Test"
NUMBER_0 = "0"
NUMBER_1 = "1"
NUMBER_3 = "3"
NUMBER_100 = "100"
DATE_BEFORE_TODAY_01 = "01/01/2018"
DATE_BEFORE_TODAY_02 = "01/02/2018"
DATE_AFTER_TODAY_01 = "01/01/2030"
DATE_AFTER_TODAY_02 = "01/02/2030"
EARLY_NO_INFO = 'early_no_info'
DAYS_FOR_BETA_TESTERS = "10000"
SYMBOL_A = "a"
LENGTH_FIELD_30 = "123456789012345678901234567890"
LENGTH_FIELD_31 = "1234567890123456789012345678901"
LENGTH_FIELD_75 = "123456789012345678901234567890123456789012345678901234567890123456789012345"
LENGTH_FIELD_76 = "1234567890123456789012345678901234567890123456789012345678901234567890123456"
LENGTH_FIELD_254 = "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234"
LENGTH_FIELD_255 = "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345"
LENGTH_FIELD_256 = "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456"
LENGTH_FIELD_301 = "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901"
LENGTH_FIELD_300 = "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
TEXT_DELETE_SELECTED_COURSE_MODES = "Delete selected course modes"
TEXT_RESPONSE_WASNT_FOUND_LEARNER = "A response was not found for this learner."

SOME_INDIVIDUAL_TEXT = "ANDREYCHIK"
SOME_TEXT_FROM_UNIT = "You can use this template"
SEARCH_RESULTS = "Search Results"
NO_RESULTS_FOUND = "Sorry, no results were found."
ADD_ADMIN_ACCESS = "Add Admin Access"
REMOVE_ADMIN_ACCESS = "Remove Admin Access"
DELETE_THE_USER = "Delete the user, "
COULD_NOT_FIND_USER = "Could not find user by email address '"
YOU_MUST_ENTER_EMAIL = "You must enter a valid email address in order to add a new team member"
ADD_NEW_TEAM_MEMBER = "Add a New Team Member"

#-----PROMPTS TEXTS-----
ENROLLED = "You have been enrolled"
UN_ENROLLED = "You have been un-enrolled"
INVITED_BETA = "You have been invited to a beta"
REMOVED_BETA = "You have been removed from a beta"
PROMPT_MESSAGE_INCORRECT_DATAES_LOGIN = "Email or password is incorrect."
PROMPT_MESSAGE_EMPTY_EMAIL_LOGIN = "Please enter your Email."
PROMPT_MESSAGE_EMPTY_PASSWORD_LOGIN = "Please enter your Password."
PROMPT_MESSAGE_EMPTY_EMAIL_REGISTRATION = "Please enter your Email."
PROMPT_MESSAGE_EMPTY_FULL_NAME_REGISTRATION = "Please enter your Full name."
PROMPT_MESSAGE_EMPTY_USERNAME_REGISTRATION = "Please enter your Public username."
PROMPT_MESSAGE_EMPTY_PASSWORD_REGISTRATION = "Please enter your Password."
PROMPT_MESSAGE_SMALLER_FULL_NAME_REGISTRATION = "Your legal name must be a minimum of two characters long"
PROMPT_MESSAGE_SMALLER_USERNAME_REGISTRATION = "Public username must have at least 2 characters."
PROMPT_MESSAGE_SMALLER_PASSWORD_REGISTRATION = "Password must have at least 2 characters."
PROMPT_MESSAGE_WITHOUT_AGREE_REGISTRATION = "You must "
PROMPT_MESSAGE_INCORRECT_EMAIL = "The email address you've provided isn't formatted correctly."
if PROJECT in (PROJECT_DEMOUNIVERSITY):
    PROMPT_MESSAGE_EMPTY_EMAIL_REGISTRATION = "Enter a valid email address that contains at least 3 characters."
    PROMPT_MESSAGE_EMPTY_FULL_NAME_REGISTRATION = "Enter your full name."
    PROMPT_MESSAGE_EMPTY_USERNAME_REGISTRATION = "Username must be between 2 and 30 characters long."
    PROMPT_MESSAGE_EMPTY_PASSWORD_REGISTRATION = "Enter a password with at least 2 characters."
    PROMPT_MESSAGE_SMALLER_USERNAME_REGISTRATION = "Username must be between 2 and 30 characters long."
    PROMPT_MESSAGE_SMALLER_PASSWORD_REGISTRATION = "Enter a password with at least 2 characters."
elif PROJECT in (PROJECT_ASUOSPP + PROJECT_E4H):
    PROMPT_MESSAGE_EMPTY_EMAIL_LOGIN = "Email or password is incorrect."
    PROMPT_MESSAGE_EMPTY_PASSWORD_LOGIN = "Email or password is incorrect."
    PROMPT_MESSAGE_INCORRECT_EMAIL = "Email or password is incorrect."
PROMPT_THIS_ANSWER_CORRECT = "This answer is correct."
PROMPT_PAGES_TEXT = "Add the content you want students to see on this page."
PROMPT_ANSWER_ARE_DISPLAYED = "Answers are displayed within the problem"
PROMPT_YOU_MUST_SUBMIT = "You must submit an answer before you can select Reset."
PROMPT_PLEASE_ENTER_STUDENT_EMAIL = "Please enter a student email address or username."
PROMPT_MAKE_SURE_STUDENT_INDENTINIER = "Make sure that the student identifier is spelled correctly."
PROMPT_MAKE_SURE_PROBLEM_INDENTINIER = "Make sure that the problem and student identifiers are complete and correct."
PROMPT_MAKE_SURE_PROBLEM_INDENTINIER_COMPLETE = "Make sure that the problem identifier is complete and correct."
PROMPT_PLEASE_ENTER_PROBLEM_LOCATION = "Please enter a problem location."
PROMPT_PLEASE_ENTER_SCORE = 'Please enter a score.'
PROMPT_INVALID_LITERAL_FOR_FLOAT = '{ "error": "invalid literal for float(): 1,5" }'
PROMPT_SCORE_MUST_BE = '{ "error": "Scores must be between 0 and the value of the problem." }'
PROMPT_COULD_NOT_CONVERT_SCORE = '{ "error": "could not convert string to float: ' + TEXT_SOME_TEXT + '" }'
PROMPT_PROBLEM_OVERRIDDEN = "Problem successfully overridden"
PROMPT_USER_DOES_NOT_EXIST = "User does not exist."
PROMPT_LEARNERS_GRADE_PROBLEM = "Adjust a learner's grade for a specific problem"
if(VERSION in VERSION_FIKUS):
    PROMPT_USER_DOES_NOT_EXIST = "Make sure that the the problem and student identifiers are complete and correct."









