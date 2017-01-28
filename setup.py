from setuptools import setup

requires = [
    'pyramid'
]

setup(
    name="auth_app",
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = auth_app.config:main
    """
)
