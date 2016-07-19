
###############################################################################
#
#   This file will be used for testing purposes only.
#
###############################################################################



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

