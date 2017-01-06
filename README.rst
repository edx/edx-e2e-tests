1
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

You will also need an installation of the edX to run the tests on.
See `edx/configuration <http://github.com/edx/configuration>`_ for instructions on provisioning an edX instance.



Configuration
-------------
Before running the commands change your working directory to `edx-e2e-tests`

1. Install requirements:

.. code:: bash

    pip install -r requirements/base.txt

2 - Install edx platform pages:

.. code:: bash

    paver install_pages



Running Tests Locally
---------------------

Within the Vagrant environment, the tests are installed in /opt/dev/edx-e2e-tests,
so before running the paver commands:

.. code:: bash

    cd $HOME/edx-e2e-tests


To run the tests locally, following environmental variables needs to be changed before running tests.

.. code:: bash

    ==> BASIC_AUTH_USER
    ==> BASIC_AUTH_PASSWORD
    ==> USER_LOGIN_EMAIL
    ==> USER_LOGIN_PASSWORD



To run all the tests:

.. code:: bash

    paver e2e_test





The commands also accept nose-style specifiers for test case or module:

To run all the tests in the file:

.. code:: bash

    paver e2e_test lms/test_dasboard.py

To run all the tests in a particular class:

.. code:: bash

    paver e2e_test lms/test_dasboard.py: DashboardTest

To run a single test:

.. code:: bash

    paver e2e_test lms/test_dasboard.py: DashboardTest.test_resume_course


To update page objects installed from external repos:

.. code:: bash

    paver install_pages


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
