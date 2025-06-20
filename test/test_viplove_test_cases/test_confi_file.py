import pytest


@pytest.mark.login
def test_valid_login(credentials):
    username = credentials["username"]
    password = credentials["password"]
    print(f"Username: {username}, Password: {password}")
    assert username == "admin"
    assert password == "secret123"
