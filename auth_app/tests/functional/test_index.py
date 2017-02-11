import pytest


@pytest.mark.functional
def test_get_index(test_app):
    """ GET / 200 """
    response = test_app.get('/', status=200)
    assert response
