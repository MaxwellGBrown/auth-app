from setuptools import setup


with open('requirements.txt') as requirements_file:
    requires = requirements_file.read().splitlines()


setup(
    name="auth_app",
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = auth_app.config:main
    """
)
