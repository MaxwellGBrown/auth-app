========
Auth App
========

This application is a basic setup for authentication & authorization in a `pyramid <https://trypyramid.com/>`__ application.

It's main purpose is to both be an example of how to implement both these features and as a repo to fork off of for applications that may want to include these features.

This application includes:

* Creating a user model
* Hooking the user model into pyramid authentication
* Implementing basic authorization to views
* Performing unit & functional tests on views with authentication & authorization



Getting Started
---------------


#. Use ``setup.py`` to install the application

   ::
   
      $ python setup.py develop

   OR

   ::

      $ python setup.py install


#. Set up the database & application model using `alembic <http://alembic.zzzcomputing.com/en/latest/>`__

   ::

      $ alembic -c development.ini upgrade head


#. Serve the application using pserve
   
   ::

      $ pserve development.ini
