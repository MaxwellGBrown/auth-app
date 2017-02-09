import pytest

from auth_app.config import main


@pytest.fixture(scope="class")
def test_app(request, ini_config, ini_filepath):
    """ returns pyramid app object initialized as a webtest.TestApp object """
    from webtest import TestApp

    global_config = {
        "__file__": ini_filepath,  # config file used to initialize app
        "here": "auth_app"  # filepath of the app
    }

    settings = ini_config["app:main"]

    app = main(global_config, **settings)
    return TestApp(app)
