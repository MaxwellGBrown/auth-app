import pytest


@pytest.mark.functional
def test_get_index(test_app):
    response = test_app.get('/', status=200)
    assert response
