edx-e2e-tests
=============

End-to-end tests for edX applications.

Overview
--------

UI-level tests for edX applications:

- ``pages``: PageObjects for interacting with pages under test.
- ``test_lms``: Selenium tests for the Learning Management System (LMS).
- ``test_studio``: Selenium tests for Studio.


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

Edit the configuration file ``config.ini`` to provide information about the system under test.
You can specify another configuration file by setting the ``CONFIG_PATH`` environment variable.


Running Tests Locally
---------------------

Within the Vagrant environment, the tests are installed in /opt/dev/edx-e2e-tests,
so before running the fabric commands:

.. code:: bash

    cd $HOME/edx-e2e-tests


You can use the following command to list the available fabric commands:

.. code:: bash

    fab --list


To run all the tests:

.. code:: bash

    fab test


The following commands can be used to execute the test suites for the edX
app or the marketing site:

.. code:: bash

    fab test_lms
    fab test_studio


The commands also accept nose-style specifiers for test case or module:

.. code:: bash

    fab test_lms:test_lms.py:RegistrationTest.test_register
    fab test_studio:test_studio.py:LoggedOutTest


To update page objects installed from external repos:

.. code:: bash

    fab install_pages


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
