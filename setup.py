from setuptools import setup

requires = [
    'mako',
    'pyramid_mako',
    'pyramid',
    'sqlalchemy'
]

setup(
    name="auth_app",
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = auth_app.config:main
    """
)
