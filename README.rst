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


The application comes pre-setup with the user ``admin@localhost`` w/ the password ``hunter2``.


.. warning::

    Remember to either remove the initial user ``admin@localhost`` or change it's password if ever doing any production work w/ this!


Extending the Application
-------------------------

This application can be used as a starting point to develop applications that require authentication & authorization. 

This is especially helpful because this application already comes with testing fixtures for creating the application, database, testing data, and authenticating for both unit and functional tests!

This section breaks down how to begin expanding the application!


Adding Models
~~~~~~~~~~~~~

#. Define the new model with ``models.meta.Base``

#. Import the model into ``models/__init__.py``

#. Autogenerate & edit the new ``alembic`` migration

   ::

      $ alembic -c development.ini revision --autogenerate -m "message"

#. Create a ``pytest`` fixture for the new model that returns a `transient <http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.make_transient>`__ instance of the ORM object.


Adding Views via Routes
~~~~~~~~~~~~~~~~~~~~~~~

This section covers the steps to be taken when adding new routes using pyramid's `URL Dispatch <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html>`__ routing.

#. Define the new view callable in ``views.py`` (or ``/views``). Make sure ``@view_config(route_name="")`` is wrapping the callable.

#. Hook the associated ``route_name`` of the new view into the configurator in ``config.py``

#. If necessary, attach the route to a template using ``@view_config(renderer="")`` which corrosponds to a file in ``/templates``.

#. Implement unit & functional tests within ``/tests`` using the appropriate fixtures in the ``conftest.py`` files


Adding Views via Traversal (or Hybrid-Traversal)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section covers the steps to be taken when adding views using pyramid's resource tree via `Traversal <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/traversal.html>`__ or `Hybrid-Traversal <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hybrid.html>`__.


#. Extend the `resource tree <http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree>`__ by either extending ``RootFactory`` or providing a separate factory resource to a route.

#. Implement views in ``views.py`` (or ``/views``) associated to the resource by using ``@view_config(context=ResourceClass)``. 

   The context resource can be referenced as part of the ``request`` object:

   ::

      @view_config(context=Resource)
      def view(request):
         context = request.context

   OR as a new argument to the view function

   ::

      @view_config(context=Resource)
      def view(request, context):
          pass

#. Implement any renderers associated with the new views in ``@view_config(renderer="")`` in ``/templates``.

   **Reminder** that traversal routes are looked up using ``request.resource_url()`` instead of ``request.route_url()``, or ``request.resource_url(resource, route_name="")`` for Hybrid-Traversal.

#. Create both unit & functional tests related to new views in ``/tests`` using the appropriate fixtures.
