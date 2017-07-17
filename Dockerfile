#Using the official python 2.7 as a Base Image
FROM python:2

USER root

#Configuration
RUN apt-get update
RUN pip install paver

RUN pip install virtualenv==1.10.1
RUN pip install virtualenvwrapper

RUN apt-get install git
RUN pip install bok_choy

RUN pip install -r requirements/base.txt
RUN paver install_pages

#Setting up environment variables
RUN /local_env.sh

#Edit the CMD command to run specific tests
CMD paver e2e_test

