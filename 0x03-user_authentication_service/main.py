#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    '''assert register user'''
    params = {'email': email, 'password': password}
    res = requests.post('http://0.0.0.0:5000/users', params=params)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post('http://0.0.0.0:5000/users', params=params)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    '''check wrong login'''
    params = {'email': email, 'password': password}
    res = requests.post('http://0.0.0.0:5000/sessions', params=params)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    '''login user'''
    params = {'email': email, 'password': password}
    res = requests.post('http://0.0.0.0:5000/sessions', params=params)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    '''profile unlogged'''
    res = requests.get('http://0.0.0.0:5000/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    '''profile verified'''
    params = {'session_id', session_id}
    res = requests.get('http://0.0.0.0:5000/profile', params=params)
    assert res.status_code == 200
    assert res.json() == {"email": res.json[email]}


def log_out(session_id: str) -> None:
    '''Log out'''
    params = {'sessioon_id': session_id}
    res = requests.delete('http://0.0.0.0:5000/sessions', params=params)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    '''reset password'''
    params = {'email': email}
    res = requests.post('http://0.0.0.0:5000/reset_password', params=params)
    assert res.status_code == 200
    assert res.json()["email"] == email
    token = res.json()['reset_token']
    assert res.json() == {"email": email, "reset_token": token}
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''update password'''
    params = {'email': email, 'password': password}
    res = request.put('http://0.0.0.0:5000/reset_password', params=params)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
