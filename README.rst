========
Auth App
========

This application is a basic setup for authentication & authorization in a `pyramid <https://trypyramid.com/>`__ application.

Auth App also comes with a Dockerfile so it can be deployed using `docker <https://docker.com>`__.

Auth App comes complete with...

* A basic User SQLAlchemy model with password hashing & token recovery
* Pyramid authentication & authorization using Amazon ``cognito-idp``
* Unit & Functional tests on an authentication & authorization app using pytest
* A Dockerfile for application development and deployment


Development Quickstart
----------------------

Auth App comes packaged with a Dockerfile which can be used for deployment.

To begin, make sure that `docker is installed <https://www.docker.com/get-docker>`__.

#. Build the docker image using the Dockerfile

   ::
   
     $ docker build -t auth-app .


#. Build ``auth_app.egg-info`` for pyramid to read when mounting volumes

   ::

     $ docker run -v $(pwd):/auth-app auth-app pip install -e .


#. Mount the app directory as a volume and serve the app!

   ::

     $ docker run -it -v $(pwd):/auth-app -p 8643:80 -d --name auth-app auth-app


#. Set the password for the initial admin account ``admin@localhost`` (if it hasn't already been set up)

   ::

     http://localhost:8643/redeem/init


Running Tests
-------------

Auth App uses `pytest <http://doc.pytest.org/en/latest/>`__ to run it's unit tests and some functional tests.

After building, make sure that the ``sqlalchemy.url`` in ``test.ini`` is setup so that tests can reference it.

To run the pytest fixtures & tests, run...

::

  $ docker run -it auth-app py.test


To run the pytest fixtures on a detached dev container, use ``docker exec``

::

  $ docker exec -it auth-app py.test
