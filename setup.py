from setuptools import setup

requires = [
    'alembic',
    'mako',
    'pyramid_mako',
    'pyramid',
    'pytest',
    'sqlalchemy',
    'webtest'
]

setup(
    name="auth_app",
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = auth_app.config:main
    """
)
