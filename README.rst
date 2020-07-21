edx-e2e-tests
=============

End-to-end tests for edX applications.

Overview
--------

UI-level tests for edX applications:

- ``pages``: PageObjects for interacting with pages under test.
- ``e2e_test``: Bokchoy tests for the Learning Management System (LMS) and Studio.


Installation
------------

You will also need a deployed installation of edX lms and studio to run the tests against.
See `edx/configuration <http://github.com/edx/configuration>`_ for instructions on provisioning an edX instance.
For additional information on how to setup your development environment, see `Developer Onboarding <https://openedx.atlassian.net/wiki/pages/viewpage.action?spaceKey=ENG&title=Developer+Onboarding#DeveloperOnboarding-Step4:Getreadytodevelop>`_

Devstack
--------

If you are running against devstack you are in luck! E2E test functionality is built-in and you can run it using the
``make e2e-tests`` make command from the ``devstack`` directory.

Using Docker
------------

1. Clone the repo:

.. code:: bash

    git clone https://github.com/edx/edx-e2e-tests

2. Share your directory:

Make sure your edx-e2e-tests directory is shared in Docker settings or the next step will fail

3. Build up:

.. code:: bash

    docker-compose up --build

4. Open a new terminal window and work inside the container:

.. code:: bash

    docker exec -it edxe2etests /bin/bash

5. Set the environment variables:

You will need to configure the target environment that you want to run tests against. There is an example file that
has all of the environment variables that need to be exported. Copy local_env.sh.sample to a new file and update the
variables as necessary. Once done, source the file to get all of the variables into your environment.

6. Run lms and studio tests, as given below in 'How to run LMS and Studio tests' section

7. In OSX at least (not sure about other host systems) you can VNC in with the following (the password is 'secret'):

.. code:: bash

    open vnc://localhost:35900


Creating a test course on stage
-------------------------------

By default, the tests in this repo run against our staging server. If you plan to keep this as the target environment, you must create your own course on stage (this requires an account with staff access). Using your own course will prevent collisions with other developers and ensure that your test results are accurate.

To create the course:

1. Log into studio.edx.org with staff credentials

2. Create a new course. To ensure that your course is unique, use your github username as the Course Number. Make sure you select Organization and Course Run as well. The Course Name won't matter here, as it will be overwritten to "E2E Test Course" by the next step. These values will be set as environment variables when actually running the tests. For more on this, see ``How to run LMS and Studio tests``

3. Go to the course import page and upload the ``course.tar.gz`` file found in the ``upload_files`` directory of this repo. This tarball will generate a fairly simple test course that includes all of the advanced modules necessary for the e2e tests.


Configuration
-------------

1. Before running the commands change your working directory to `edx-e2e-tests`. Note that
   the 'e2e' python virtual environment will automatically be activated.

.. code:: bash

    cd edx-e2e-tests/

2. Update the base python requirements in case they have changed
   since you created the environment:

.. code:: bash

    pip install -r requirements/base.txt


How to run LMS and Studio tests
--------------------------------

Before running tests, please ensure that following environment variables are set.

.. code:: bash

    ==> BASIC_AUTH_USER
    ==> BASIC_AUTH_PASSWORD
    ==> USER_LOGIN_EMAIL
    ==> USER_LOGIN_PASSWORD
    ==> COURSE_RUN
    ==> COURSE_DISPLAY_NAME
    ==> COURSE_NUMBER
    ==> COURSE_ORG

To run all the tests:

.. code:: bash

    paver e2e_test


The commands also accept pytest-style specifiers for test case or module:

To run all the tests in the file:

.. code:: bash

    paver e2e_test lms/test_dashboard.py

To run all the tests in a particular class:

.. code:: bash

    paver e2e_test lms/test_dashboard.py:DashboardTest

To run a single test:

.. code:: bash

    paver e2e_test lms/test_dashboard.py:DashboardTest.test_resume_course


How to run Whitelabel tests
----------------------------

1. Create a virtual environment for installation/executing tests.


2. Change your working directory to `edx-e2e-tests`.

.. code:: bash

    cd edx-e2e-tests/

3. Install the requirements

.. code:: bash

    pip install -r requirements/base.txt

4. Set these Environment variables

.. code:: bash

    ==> TEST_ENV (Only required if tests are not running on stage, e.g. for sandbox just assign value `sandbox')
    ==> TARGET_DNS (Only required if tests are not running on stage, just provide DNS e.g. just provide "helio" for "https://mitxpro-helio.sandbox.edx.org")
    ==> ORG (Only valid values for now are "MITxPRO" and "HarvardMedGlobalAcademy", if not provided the tests wil run against MITxPRO by default)
    ==> BASIC_AUTH_USER
    ==> BASIC_AUTH_PASSWORD
    ==> GLOBAL_PASSWORD
    ==> OAUTH_CLIENT_ID (Only required for stage or sandbox is not using the default id)
    ==> OAUTH_CLIENT_SECRET (Only required for stage or sandbox is not using the default secret)
    ==> COURSE_RUN (Optional, use only if you are using a value other than default)
    ==> COURSE_DISPLAY_NAME (Optional, use only if you are using a value other than default)
    ==> COURSE_NUMBER (Optional, use only if you are using a value other than default)
    ==> COURSE_ORG (Optional, use only if you are using a value other than specified in ORG var)


To run all the tests in the file:

.. code:: bash

    paver e2e_wl_test

To run all the tests in the file:

.. code:: bash

    paver e2e_wl_test test_otto_enrollment.py

To run all the tests in a particular class:

.. code:: bash

    paver e2e_wl_test test_misc.py:TestMisc

To run a single test:

.. code:: bash

    paver e2e_wl_test test_misc.py:TestMisc.test_logos


Where and How to add new tests
-------------------------------

Change your working directory to `regression/tests`. Add your tests to the below mentioned directories based on the relevancy of the tests.

    1. `lms`: tests for the LMS pages
    2. `studio`: tests for the studio pages
    3. `whitelabel`: tests for microsites
    4. `helpers`: helper methods for the tests
    5. `common`: tests required for common components of lms and studio

NOTE: Please make a pull request from the master branch before writing and adding new tests.


How to change target environment?
---------------------------------

Studio and LMS urls for stage are ``https://studio.stage.edx.org``
and ``https://courses.stage.edx.org`` respectively. We don't need to
do anything extra to run tests on stage. By default, all tests
run on stage.

If we want to change this behaviour then we would need to set
environment variables to point to our desired environment.
To be specific, we would need to set

1. For studio, ``STUDIO_BASE_URL`` which defaults to ``studio.stage.edx.org`` and

2. For LMS, ``LMS_BASE_URL`` which defaults to ``courses.stage.edx.org``.

Lets say we want to run tests on a sandbox which has studio and LMS urls as ``https://studio.sandbox.edx.org``
and ``https://lms.sandbox.edx.org`` respectively. To let repo know, set environment variables as

.. code:: bash

    export STUDIO_BASE_URL=studio.sandbox.edx.org
    export LMS_BASE_URL=lms.sandbox.edx.org

Depending on the target environment you may also need to change ``LMS_PROTOCOL`` and ``STUDIO_PROTOCOL`` to ``http`` or
``https``.

To run tests back on stage, unset the above set environment variables.

.. code:: bash

    unset STUDIO_BASE_URL
    unset LMS_BASE_URL


License
-------

The code in this repository is licensed under version 3 of the AGPL unless
otherwise noted.

Please see ``LICENSE.txt`` for details.


How to Contribute
-----------------

Contributions are very welcome. The easiest way is to fork this repo, and then
make a pull request from your fork. The first time you make a pull request, you
may be asked to sign a Contributor Agreement.


Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org


Mailing List and IRC Channel
----------------------------

You can discuss this code on the `edx-code Google Group`__ or in the
``edx-code`` IRC channel on Freenode.

__ https://groups.google.com/forum/#!forum/edx-code
