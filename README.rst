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

We recommend using the provided Vagrant environment to develop and run tests.

1. `Install Vagrant <http://docs.vagrantup.com/v2/installation/index.html>`_


2. In the `edx-e2e-tests` directory, execute this command:

.. code:: bash

    vagrant up

3. This will create and provision a new Vagrant environment.

4. Enter a terminal session in the virtual environment with:

.. code:: bash

    vagrant ssh


You will also need a deployed installation of edX lms and studio to run the tests against.
See `edx/configuration <http://github.com/edx/configuration>`_ for instructions on provisioning an edX instance.
For additional information on how to setup your development environment, see `Developer Onboarding <https://openedx.atlassian.net/wiki/pages/viewpage.action?spaceKey=ENG&title=Developer+Onboarding#DeveloperOnboarding-Step4:Getreadytodevelop>`_



Configuration
-------------

1. Before running the commands change your working directory to `edx-e2e-tests`. Note that
   the 'e2e' python virtual environment will automatically be activated.

.. code:: bash

    cd edx-e2e-tests/

2. Update the base python requirements in case they have changed
   since you created the vagrant environment:

.. code:: bash

    pip install -r requirements/base.txt

3. OPTIONAL: Cloning the edx-platform repo into a mounted directory in a vagrant environment
   can take a long time (several minutes). An alternative is to navigate to the lib directory
   back on your host system and clone the edx-platform repo there before proceeding.

4. Install the page objects for the application from the edx platform repo. This will
   clone the entire repo into lib/edx-platform so that it can use the page objects and
   helper methods from common/test/acceptance. We also install capa and xmodule into the
   virtual environment from common/lib.


.. code:: bash

    paver install_pages


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

    paver e2e_test --exclude=whitelabel


The commands also accept nose-style specifiers for test case or module:

To run all the tests in the file:

.. code:: bash

    paver e2e_test lms/test_dashboard.py

To run all the tests in a particular class:

.. code:: bash

    paver e2e_test lms/test_dashboard.py:DashboardTest

To run a single test:

.. code:: bash

    paver e2e_test lms/test_dashboard.py:DashboardTest.test_resume_course


To update page objects installed from external repos:

.. code:: bash

    paver install_pages


How to run Whitelabel tests
----------------------------

Before running whitelabel tests please ensure that these environment variables are set.

.. code:: bash

    ==> BASIC_AUTH_USER
    ==> BASIC_AUTH_PASSWORD
    ==> USER_LOGIN_EMAIL
    ==> USER_LOGIN_PASSWORD
    ==> COURSE_RUN
    ==> COURSE_DISPLAY_NAME
    ==> COURSE_NUMBER
    ==> COURSE_ORG
    ==> GLOBAL_PASSWORD
    ==> STAFF_USER_EMAIL
    ==> TEST_EMAIL_SERVICE
    ==> TEST_EMAIL_ACCOUNT
    ==> TEST_EMAIL_PASSWORD
    ==> ACCESS_TOKEN


To run all the tests in the file:

.. code:: bash

    paver e2e_wl_test whitelabel/test_user_account.py

NOTE: In order to run tests in a particular class or a single test, use the same Nose specifiers as mentioned in the above section. However, do not forget to change the paver target to e2e_wl_test 


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
do anything extra to run tests on the stage. By default, all tests
run on the stage.

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
