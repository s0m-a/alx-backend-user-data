#!/usr/bin/env python3
"""
Module for simple end-to-end
"""

import requests

from app import AUTH

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Test the registration of a user.

    Args:
        email (str): The user's email.
        password (str): The user's password.
    """
    url = "{}/users".format(BASE_URL)
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test logging in with wrong password.

    Args:
        email (str): The email address of the user to log in.
        password (str): The user's password.
    """
    url = "{}/sessions".format(BASE_URL)
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """
    Tests behavior of trying to retrieve profile information
    while being logged out.
    """
    url = "{}/profile".format(BASE_URL)
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests retrieving profile information whilst logged in.

    Args:
        session_id (str): The session ID of the logged in user.
    """
    url = "{}/profile".format(BASE_URL)
    cookies = {
        "session_id": session_id
    }
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    payload = response.json()
    assert "email" in payload
    user = AUTH.get_user_from_session_id(session_id)
    assert user.email == payload["email"]


def log_out(session_id: str) -> None:
    """Tests tests the process of logging out from a session.

    Args:
        session_id (str): The session ID of the user to log out.
    """
    url = "{}/sessions".format(BASE_URL)
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "session_id": session_id
    }
    response = requests.delete(url, headers=headers, cookies=data)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Tests the process of requesting a password reset.

    Args:
        email (str): The email to request password reset for.
    """
    url = "{}/reset_password".format(BASE_URL)
    data = {
        "email": email
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    reset_token = response.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Tests updating a user's password.

    Args:
        email (str): The email of the user whose password should be updated.
        reset_token (str): The reset token generated for the user.
        new_password (str): The new password to set for the user.
    """
    url = "{}/reset_password".format(BASE_URL)
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated"
    assert response.json()["email"] == email


def log_in(email: str, password: str) -> str:
    """
    Tests logging in.

    Args:
        email (str): The email address of the user to log in.
        password (str): The user's password.
    """
    url = "{}/sessions".format(BASE_URL)
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    if response.status_code == 401:
        return "Invalid credentials"
    assert response.status_code == 200
    response_json = response.json()
    assert "email" in response_json
    assert "message" in response_json
    assert response_json["email"] == email
    return response.cookies.get("session_id")


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
