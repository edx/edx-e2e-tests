#Using the official ubuntu OS as a Base Image
FROM ubuntu:16.04

USER root

#Configuration
RUN pip install -r requirements/base.txt
RUN paver install_pages

#Setting up environment variables. Change the value according to the value of the ENV_VAR

ENV BASIC_AUTH_USER value	
ENV BASIC_AUTH_PASSWORD value
ENV USER_LOGIN_EMAIL value
ENV USER_LOGIN_PASSWORD value

#Edit the CMD command to run speciifc tests
CMD paver e2e_test
