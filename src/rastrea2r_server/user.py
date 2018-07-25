"""
API User Functions
"""
import sys
import logging
import time
from passlib.hash import sha256_crypt
from rastrea2r_server import auth, db

logger = logging.getLogger(__name__)


class User(db.Model): # type: ignore
    """ SQL User Model """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(40))

    def __init__(self, username, password, role="default"):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return "<User {:}>".format(self.username)


@auth.verify_password
def verify_password(username, password):
    """API Password Verification"""

    return authenticate_user(username, password)


def authenticate_user(username, passwd):
    """ Authenticate a user """

    user = User.query.filter_by(username=username).first()

    authenticated = False

    if user:
        authenticated = sha256_crypt.verify(passwd, user.password)
    else:
        time.sleep(1)
        logger.info("Authentication Error: User not found in DB: %s", username)
        return False

    if authenticated:
        logger.debug("Successfully Authenticated user: %s", username)
    else:
        logger.info("Authentication Failed: %s", username)

    return authenticated


def get_phash(passwd):
    """ Get a new hashed password """

    return sha256_crypt.encrypt(passwd, rounds=100000)


def add_user(username, passwd):
    """
    Add a new user to the database
    """

    user = User.query.filter_by(username=username).first()

    if user:
        # print("Error: User already exists in DB", file=sys.stderr)
        raise Exception("Error: User already exists in DB")
    elif len(passwd) < 6:
        print("Error: Password must be 6 or more characters", file=sys.stderr)
        exit(1)
    else:
        logger.info("Adding new user to the database: %s", username)

        phash = get_phash(passwd)

        newuser = User(username, phash)
        db.session.add(newuser)
        db.session.commit()

        return phash


def update_password(username, passwd):
    """ Update password for user """

    user = User.query.filter_by(username=username).first()

    if len(passwd) < 6:
        print("Error: Password must be 6 or more characters", file=sys.stderr)
        exit(1)
    elif user:
        logger.info("Updating password for user: %s", username)

        phash = phash = get_phash(passwd)

        user.password = phash
        db.session.commit()

        return phash
    else:

        print("Error: User does not exists in DB", file=sys.stderr)
        exit(1)


def del_user(username):
    """ Delete a user from the database """

    user = User.query.filter_by(username=username).first()

    if user:
        logger.info("Deleting user: %s", username)

        db.session.delete(user)
        db.session.commit()

        return True
    else:

        print("Error: User does not exists in DB", file=sys.stderr)
        exit(1)
