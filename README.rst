========
Auth App
========

This application is a basic setup for authentication & authorization in a `pyramid <https://trypyramid.com/>`__ application.

Auth App also comes with a Dockerfile so it can be deployed using `docker <https://docker.com>`__.

Auth App comes complete with...

* A basic User SQLAlchemy model with password hashing & token recovery
* Pyramid authentication & authorization using the SQLAlchemy User model
* Unit & Functional tests on an authentication & authorization app using pytest
* A Dockerfile for application development and deployment


Development Quickstart
----------------------

Auth App comes packaged with a Dockerfile which can be used for deployment.

To begin, make sure that `docker is installed <https://www.docker.com/get-docker>`__.

#. Build the docker image using the Dockerfile

   ::
   
     $ docker build -t auth-app .


#. Create & migrate the database specified in ``development.ini`` under ``[app:main]``'s ``sqlalchemy.url``

   ::

     $ docker run auth-app alembic -c development.ini upgrade head


#. Mount the app directory as a volume and serve the app!

   ::

     $ docker run -it -v $(pwd):/auth-app -p 8643:80 auth-app 


Running Tests
-------------

Auth App uses `pytest <http://doc.pytest.org/en/latest/>`__ to run it's unit tests and some functional tests.

After building, make sure that the ``sqlalchemy.url`` in ``test.ini`` is setup so that tests can reference it.

To run the pytest fixtures & tests, run...

::

  $ docker run -it auth-app py.test
