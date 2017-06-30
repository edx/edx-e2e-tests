#Using the official ubuntu OS as a Base Image
FROM ubuntu:16.04

USER root

#Add the e2e-repo to the container
ADD https://github.com/edx/edx-e2e-tests.git /edx_e2e_tests

#Configuration
RUN apt-get update
RUN apt-get install git
RUN apt-get install python
RUN apt-get install python-setuptools python-dev build-essential
RUN easy_install pip
RUN pip install paver

RUN apt-get install -y firefox=45.0.2+build1-0ubuntu1

RUN pip install virtualenv==1.10.1
RUN pip install virtualenvwrapper

RUN pip install -r requirements/base.txt
RUN paver install_pages

#Setting up environment variables. Change the value according to the value of the ENV_VAR

ENV BASIC_AUTH_USER value	
ENV BASIC_AUTH_PASSWORD value
ENV USER_LOGIN_EMAIL value
ENV USER_LOGIN_PASSWORD value

#Edit the CMD command to run speciifc tests
CMD paver e2e_test

