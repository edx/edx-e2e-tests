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


Running Tests Locally
---------------------
Make sure you are in the correct folder.

.. code:: bash

    cd $HOME/edx-e2e-tests


These environment variables need to be set before running tests.
By default the browser used is the local Firefox application from the vagrant image.

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


Using the Browser from a Docker Container
-----------------------------------------
* You first need some basic understanding of how Docker works and have a
  working `Docker installation <https://docs.docker.com/engine/installation/>`_
* Launch a container with selenium server and a browser. Here's how to run with Firefox:

  * `DBUS_SESSION_BUS_ADDRESS=/dev/null` is needed to prevent error messages about the hostname
  * `-p 4444:4444` maps port 4444 on the container to port 4444 on the host

.. code:: bash

    docker run -d --env DBUS_SESSION_BUS_ADDRESS=/dev/null -p 4444:4444 selenium/standalone-firefox

* These environment variable settings on the system from which you are running the
  tests (the vagrant image), set prior to issuing the `paver e2e_test` command,
  will tell the test runner to use the container's browser.
  Note: see http://stackoverflow.com/questions/16244601/vagrant-reverse-port-forwarding
  for why the SELENIUM_HOST value is 10.0.2.2.

.. code:: bash

    export SELENIUM_BROWSER=firefox
    export SELENIUM_HOST=10.0.2.2
    export SELENIUM_PORT=4444


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
