edx-e2e-tests
=============

End-to-end tests for edX applications.

Overview
--------

UI-level tests for edX applications:

- ``e2e_framework``: A framework for writing end-to-end Selenium tests using the `Page Object`__ design pattern.
- ``pages``: PageObjects for interacting with pages under test.
- ``test_edxapp``: Selenium tests for edX applications.
- ``test_mktg``: Selenium tests for the edX marketing site.

__ https://code.google.com/p/selenium/wiki/PageObjects


Installation
------------

We recommend using the provided Vagrant environment to develop and run tests.

1. `Install Vagrant`__
2. `Install Ansible`__
3. In the `edx-e2e-tests/vagrant` directory, execute this command:

.. code:: bash

    vagrant up

4. This will create and provision a new Vagrant environment.

You will also need an installation of the edX to run the tests on.
See `edx/configuration`__ for instructions on provisioning an edX instance.

__ http://docs.vagrantup.com/v2/installation/index.html
__ http://www.ansibleworks.com/docs/intro_installation.html
__ https://github.com/edx/configuration


Configuration
-------------

Edit the configuration file ``config.ini`` to provide information about the system under test.
You can specify another configuration file by setting the ``CONFIG_PATH`` environment variable.


Running Tests Locally
---------------------

To run tests within the Vagrant environment:

.. code:: bash

    cd /opt/dev/edx-e2e-tests
    fab test_edxapp

You can run a specific test using nose-style test specifiers:

.. code:: bash

    fab test_edxapp:test_lms.py:LoggedOutTest.test_register

By default, tests run locally in Firefox.  You can also use Chrome:

.. code:: bash

    SELENIUM_BROWSER=chrome fab test_edxapp



Running Tests in SauceLabs
--------------------------

By setting the appropriate environment variables, you can configure
the tests to run using `SauceLabs`__.  This uses the same environment
variables as the `Sauce OnDemand Plugin`__ for Jenkins

1. Edit ``/opt/dev/jenkins_env`` to provide your SauceLabs credentials and specified browsers.
2. Start Sauce Connect:

.. code:: bash

    /opt/dev/start_sauce.sh

3. In another terminal, run the tests:

.. code:: bash

    source /opt/dev/jenkins_env
    fab test_edxapp

To speed things up, you can also run tests in parallel:

.. code:: bash

    NUM_PARALLEL=4 fab test_edxapp

__ https://saucelabs.com/docs/connect
__ https://wiki.jenkins-ci.org/display/JENKINS/Sauce+OnDemand+Plugin



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
