# -*- coding: utf-8 -*-
"""
List of constants to be used throughout the tests
"""
import os
import uuid

# Get HTTP Authentication credentials from environment variables
AUTH_USERNAME = os.environ['BASIC_AUTH_USER']
AUTH_PASSWORD = os.environ['BASIC_AUTH_PASSWORD']

# Get API Access token

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

# Select the Org for which to run the tests, Default is MITProfessionalX
ORG = os.getenv('ORG', 'MITProfessionalX')

# Select the Email API to be used, default is TempMAil
EMAIL_API = os.getenv('EMAIL_API', 'GuerrillaMail')

# Global password
PASSWORD = os.environ['GLOBAL_PASSWORD']

BASIC_AUTH = AUTH_USERNAME + ":" + AUTH_PASSWORD + "@"

# Organization Based Settings
##############################################################################
# E-commerce raw url
RAW_ECOMMERCE_URL = {
    'HarvardXPLUS': u'https://{}stage-payments.harvardxplus.harvard.edu/',
    'MITProfessionalX': u'https://{}payments.mitprofessionalx-stage.mit.edu/'
}

# BASIC raw URL
RAW_URL = {
    'HarvardXPLUS': u'https://{}stage-courses.harvardxplus.harvard.edu/',
    'MITProfessionalX': u'https://{}mitprofessionalx-stage.mit.edu/'
}

# E-commerce urls
ECOMMERCE_URL_WITHOUT_AUTH = RAW_ECOMMERCE_URL[ORG].format("")

ECOMMERCE_URL_WITH_AUTH = RAW_ECOMMERCE_URL[ORG].format(BASIC_AUTH)

# BASIC URLs
URL_WITHOUT_AUTH = RAW_URL[ORG].format("")

URL_WITH_AUTH = RAW_URL[ORG].format(BASIC_AUTH)

ECOMMERCE_API_URL = ECOMMERCE_URL_WITHOUT_AUTH + 'api/v2/'

PROF_COURSE_ID = {
    'HarvardXPLUS': u'course-v1:HarvardXPLUS+MCB63xPLUS+3T2016',
    'MITProfessionalX': u'course-v1:MITProfessionalX+IOTx+2016_T1'
}

PROF_COURSE_TITLE = {
    'HarvardXPLUS': u'Principles of Biochemistry',
    'MITProfessionalX': u'Internet of Things: Roadmap to a Connected World'
}

PROF_COURSE_PRICE = {
    'HarvardXPLUS': 295,
    'MITProfessionalX': 100
}

EMAIL_SENDER_ACCOUNT = {
    'HarvardXPLUS': 'hxplus-support@edx.org',
    'MITProfessionalX': 'mitprofessionalx@mit.edu'
}

LOGO_LINK = {
    'HarvardXPLUS': 'harvardX-logo',
    'MITProfessionalX': 'mit-prof-logo',
}

LOGO_ALT_TEXT = {
    'HarvardXPLUS': 'HarvardX Logo',
    'MITProfessionalX': 'MIT Logo',
}

SOCIAL_MEDIA_LINK = {
    'HarvardXPLUS': [
        'https://www.facebook.com/HarvardX-187429968296722/',
        'https://twitter.com/harvardonline'
    ],
    'MITProfessionalX': [
        'https://www.facebook.com/MITProfessionalEducation',
        'https://twitter.com/mitprofessional',
        'https://www.linkedin.com/groups/73833/profile',
        'https://www.youtube.com/user/MITProfessionalEd'
    ],
}

COUPON_COURSES = {
    'HarvardXPLUS': {
        'course-v1:HarvardXPLUS+PHCT01+2016': 100,
        'course-v1:HarvardXPLUS+PHCT02+2016': 200,
        'course-v1:HarvardXPLUS+PHCT03+2016': 300,
        'course-v1:HarvardXPLUS+PHCT04+2016': 400,
        'course-v1:HarvardXPLUS+PHCT05+2016': 500,
        'course-v1:HarvardXPLUS+PHCT06+2016': 600
    },
    'MITProfessionalX': {
        'course-v1:MITProfessionalX+PMCT01+2016': 100,
        'course-v1:MITProfessionalX+PMCT02+2017': 200,
        'course-v1:MITProfessionalX+PMCT03+2018': 300,
        'course-v1:MITProfessionalX+PMCT04+2016': 400,
        'course-v1:MITProfessionalX+PMCT05+2017': 500,
        'course-v1:MITProfessionalX+PMCT06+2016': 600
    }
}

##############################################################################

# COURSE DETAILS
HONOR_COURSE_ID = u'course-v1:MITProfessionalX+XM101+2016'
HONOR_COURSE_TITLE = u'X-men Series'
HONOR_COURSE_PRICE = 450

# REGISTRATION INFORMATION
REG_INFO = {
    'full_name': 'White label Test User',
    'first_name': 'White Label',
    'last_name': 'Test User',
    'gender': 'm',
    'yob': '1994',
    'state': 'Massachusetts',
    'country': 'US',
    'edu_level': 'm',
    'company': 'Arbisoft',
    'title': 'SQA'
}

# BILLING INFORMATION
BILLING_INFO = {
    'first_name': 'billing',
    'last_name': 'user',
    'address01': '23-b',
    'address02': 'service lane',
    'city': 'Boston',
    'country': 'US',
    'state': 'MA',
    'postal_code': '02108',
    'email': 'billing_user@example.com'
}

# PAYMENT DETAILS
PAYMENT_DETAILS = {
    'card_number': '4111111111111111',
    'cvn': '123',
    'expiry_month': '07',
    'expiry_year': '2018'
}

# STAGES IN PAYMENT SECTION
INITIAL_STAGE = 'Review'
FINAL_STAGE = 'Confirmation'

# Single seat user credentials
STUDENT_USERNAME = 'ST' + str(uuid.uuid4().node)
STUDENT_EMAIL = STUDENT_USERNAME + '@guerrillamailblock.com'

# Existing user email
EXISTING_USER_EMAIL = 'wl_smoke_user01@yopmail.com'

# Staff user email
STAFF_EMAIL = os.environ['STAFF_USER_EMAIL']

# Student user email
STUDENT_USER_EMAIL = 'mit_smoke_test02@yopmail.com'

# Student user email
VISUAL_USER_EMAIL = 'wl_visual_test01@yopmail.com'

# Countries list
COUNTRIES_WITH_SPACES = [
    u'Afghanistan', u'\xc5land Islands', u'Albania', u'Algeria',
    u'American Samoa', u'Andorra', u'Angola',
    u'Anguilla', u'Antarctica', u'Antigua and Barbuda', u'Argentina',
    u'Armenia', u'Aruba', u'Australia',
    u'Austria', u'Azerbaijan', u'Bahamas', u'Bahrain', u'Bangladesh',
    u'Barbados', u'Belarus', u'Belgium',
    u'Belize', u'Benin', u'Bermuda', u'Bhutan', u'Bolivia',
    u'Bonaire, Sint Eustatius and Saba',
    u'Bosnia and Herzegovina', u'Botswana', u'Bouvet Island', u'Brazil',
    u'British Indian Ocean Territory',
    u'Brunei', u'Bulgaria', u'Burkina Faso', u'Burundi', u'Cabo Verde',
    u'Cambodia', u'Cameroon', u'Canada',
    u'Cayman Islands', u'Central African Republic', u'Chad', u'Chile',
    u'China', u'Christmas Island',
    u'Cocos (Keeling) Islands', u'Colombia', u'Comoros', u'Congo',
    u'Congo (the Democratic Republic of the)',
    u'Cook Islands', u'Costa Rica', u"C\xf4te d'Ivoire", u'Croatia', u'Cuba',
    u'Cura\xe7ao', u'Cyprus',
    u'Czech Republic', u'Denmark', u'Djibouti', u'Dominica',
    u'Dominican Republic', u'Ecuador', u'Egypt',
    u'El Salvador', u'Equatorial Guinea', u'Eritrea', u'Estonia',
    u'Ethiopia', u'Falkland Islands [Malvinas]',
    u'Faroe Islands', u'Fiji', u'Finland', u'France', u'French Guiana',
    u'French Polynesia',
    u'French Southern Territories', u'Gabon', u'Gambia', u'Georgia',
    u'Germany', u'Ghana', u'Gibraltar',
    u'Greece', u'Greenland', u'Grenada', u'Guadeloupe', u'Guam',
    u'Guatemala', u'Guernsey', u'Guinea',
    u'Guinea-Bissau', u'Guyana', u'Haiti',
    u'Heard Island and McDonald Islands', u'Holy See', u'Honduras',
    u'Hong Kong', u'Hungary', u'Iceland', u'India', u'Indonesia', u'Iran',
    u'Iraq', u'Ireland', u'Isle of Man',
    u'Israel', u'Italy', u'Jamaica', u'Japan', u'Jersey', u'Jordan',
    u'Kazakhstan', u'Kenya', u'Kiribati', u'Kosovo',
    u'Kuwait', u'Kyrgyzstan', u'Laos', u'Latvia', u'Lebanon', u'Lesotho',
    u'Liberia', u'Libya', u'Liechtenstein',
    u'Lithuania', u'Luxembourg', u'Macao', u'Macedonia', u'Madagascar',
    u'Malawi', u'Malaysia', u'Maldives',
    u'Mali', u'Malta', u'Marshall Islands', u'Martinique', u'Mauritania',
    u'Mauritius', u'Mayotte', u'Mexico',
    u'Micronesia (Federated States of)', u'Moldovia', u'Monaco', u'Mongolia',
    u'Montenegro', u'Montserrat',
    u'Morocco', u'Mozambique', u'Myanmar', u'Namibia', u'Nauru', u'Nepal',
    u'Netherlands', u'New Caledonia',
    u'New Zealand', u'Nicaragua', u'Niger', u'Nigeria', u'Niue',
    u'Norfolk Island', u'North Korea',
    u'Northern Mariana Islands', u'Norway', u'Oman', u'Pakistan', u'Palau',
    u'Palestine, State of',
    u'Panama', u'Papua New Guinea', u'Paraguay', u'Peru', u'Philippines',
    u'Pitcairn', u'Poland', u'Portugal',
    u'Puerto Rico', u'Qatar', u'R\xe9union', u'Romania', u'Russia',
    u'Rwanda', u'Saint Barth\xe9lemy',
    u'Saint Helena, Ascension and Tristan da Cunha', u'Saint Kitts and Nevis',
    u'Saint Lucia',
    u'Saint Martin (French part)', u'Saint Pierre and Miquelon',
    u'Saint Vincent and the Grenadines',
    u'Samoa', u'San Marino', u'Sao Tome and Principe', u'Saudi Arabia',
    u'Senegal', u'Serbia', u'Seychelles',
    u'Sierra Leone', u'Singapore', u'Sint Maarten (Dutch part)', u'Slovakia',
    u'Slovenia', u'Solomon Islands',
    u'Somalia', u'South Africa',
    u'South Georgia and the South Sandwich Islands', u'South Korea',
    u'South Sudan',
    u'Spain', u'Sri Lanka', u'Sudan', u'Suriname', u'Svalbard and Jan Mayen',
    u'Swaziland', u'Sweden',
    u'Switzerland', u'Syria', u'Taiwan', u'Tajikistan', u'Tanzania',
    u'Thailand', u'Timor-Leste', u'Togo',
    u'Tokelau', u'Tonga', u'Trinidad and Tobago', u'Tunisia', u'Turkey',
    u'Turkmenistan',
    u'Turks and Caicos Islands', u'Tuvalu', u'Uganda', u'Ukraine',
    u'United Arab Emirates',
    u'United Kingdom of Great Britain and Northern Ireland',
    u'United States Minor Outlying Islands',
    u'United States of America', u'Uruguay', u'Uzbekistan', u'Vanuatu',
    u'Venezuela', u'Vietnam',
    u'Virgin Islands (British)', u'Virgin Islands (U.S.)',
    u'Wallis and Futuna', u'Western Sahara', u'Yemen',
    u'Zambia', u'Zimbabwe'
]

COUNTRIES = [x.replace(' ', '') for x in COUNTRIES_WITH_SPACES]

LANGUAGES_WITH_SPACES = [
    u'', u'Afar', u'Abkhazian', u'Afrikaans', u'Akan', u'Albanian',
    u'Amharic', u'Arabic', u'Aragonese',
    u'Armenian', u'Assamese', u'Avaric', u'Avestan', u'Aymara',
    u'Azerbaijani', u'Bashkir', u'Bambara',
    u'Basque', u'Belarusian', u'Bengali', u'Bihari languages',
    u'Bislama', u'Bosnian', u'Breton',
    u'Bulgarian', u'Burmese', u'Catalan', u'Chamorro', u'Chechen',
    u'Chinese', u'Simplified Chinese',
    u'Traditional Chinese', u'Church Slavic', u'Chuvash', u'Cornish',
    u'Corsican', u'Cree', u'Czech',
    u'Danish', u'Divehi', u'Dutch', u'Dzongkha', u'English',
    u'Esperanto', u'Estonian', u'Ewe', u'Faroese',
    u'Fijian', u'Finnish', u'French', u'Western Frisian',
    u'Fulah', u'Georgian', u'German', u'Gaelic',
    u'Irish', u'Galician', u'Manx', u'Greek', u'Guarani',
    u'Gujarati', u'Haitian', u'Hausa', u'Hebrew',
    u'Herero', u'Hindi', u'Hiri Motu', u'Croatian', u'Hungarian',
    u'Igbo', u'Icelandic', u'Ido', u'Sichuan Yi',
    u'Inuktitut', u'Interlingue', u'Interlingua', u'Indonesian',
    u'Inupiaq', u'Italian', u'Javanese',
    u'Japanese', u'Kalaallisut', u'Kannada', u'Kashmiri', u'Kanuri',
    u'Kazakh', u'Central Khmer', u'Kikuyu',
    u'Kinyarwanda', u'Kirghiz', u'Komi', u'Kongo', u'Korean',
    u'Kuanyama', u'Kurdish', u'Lao', u'Latin',
    u'Latvian', u'Limburgan', u'Lingala', u'Lithuanian',
    u'Luxembourgish', u'Luba-Katanga', u'Ganda',
    u'Macedonian', u'Marshallese', u'Malayalam', u'Maori',
    u'Marathi', u'Malay', u'Malagasy', u'Maltese',
    u'Mongolian', u'Nauru', u'Navajo', u'Ndebele, South',
    u'Ndebele, North', u'Ndonga', u'Nepali',
    u'Norwegian Nynorsk', u'Bokm\xe5l, Norwegian', u'Norwegian',
    u'Chichewa', u'Occitan', u'Ojibwa', u'Oriya',
    u'Oromo', u'Ossetian', u'Panjabi', u'Persian', u'Pali',
    u'Polish', u'Portuguese', u'Pushto', u'Quechua',
    u'Romansh', u'Romanian', u'Rundi', u'Russian', u'Sango',
    u'Sanskrit', u'Sinhala', u'Slovak', u'Slovenian',
    u'Northern Sami', u'Samoan', u'Shona', u'Sindhi', u'Somali',
    u'Sotho, Southern', u'Spanish', u'Sardinian',
    u'Serbian', u'Swati', u'Sundanese', u'Swahili', u'Swedish',
    u'Tahitian', u'Tamil', u'Tatar', u'Telugu',
    u'Tajik', u'Tagalog', u'Thai', u'Tibetan', u'Tigrinya',
    u'Tonga (Tonga Islands)', u'Tswana', u'Tsonga',
    u'Turkmen', u'Turkish', u'Twi', u'Uighur', u'Ukrainian',
    u'Urdu', u'Uzbek', u'Venda', u'Vietnamese',
    u'Volap\xfck', u'Welsh', u'Walloon', u'Wolof', u'Xhosa',
    u'Yiddish', u'Yoruba', u'Zhuang', u'Zulu'
]

LANGUAGES = [x.replace(' ', '') for x in LANGUAGES_WITH_SPACES]

# Default Threshold for visual difference
DIFF_THRESHOLD = 5000

# Timeouts
DEFAULT_TIMEOUT = 30

TIME_OUT_LIMIT = 90

INITIAL_WAIT_TIME = 3

WAIT_TIME = 5
