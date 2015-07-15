# https://flask-httpauth.readthedocs.org/en/latest/
from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()

#FIXME!
users = {
    "dcsrd": "happy"
}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@auth.verify_password
def verify_password(username, password):
    return password == get_pw(username)
