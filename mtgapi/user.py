import bcrypt
import datetime
from dotenv import load_dotenv
import jwt
import os

class User:
    def __init__(self, dbm):
        self.dbm = dbm

        self.auth_token_algo = 'HS256'
        self.auth_token_msg_expired = 'Signature expired. Please re-authenticate.'
        self.auth_token_msg_invalid = 'Invalid token. Please re-authenticate.'

        load_dotenv()

    def get_user(self, email):
        collection = self.dbm.db.users
        return collection.find_one({'email': email})

    def hash_password(self, pwd):
        if not pwd:
            return False

        salt = os.environ.get('PASSWORD_SALT')
        return bcrypt.hashpw(pwd.encode('utf-8'), salt.encode('utf-8'))

    def validate_password(self, email, pwd):
        user = self.get_user(email)
        if not user:
            return False

        if self.hash_password(pwd) != user['password']:
            return False

        return True

    def create(self, email, pwd):
        if not email or not pwd:
            return False

        user = self.get_user(email)
        if user:
            return False

        collection = self.dbm.db.users

        result = collection.insert_one({
            'email': email,
            'password': self.hash_password(pwd)
        })

        return result

    def create_auth_token(self, email, payload = None, secret = None):
        payload = payload if payload != None else {
            'exp': datetime.datetime.now(datetime.UTC) +
                    datetime.timedelta(minutes = 30),
            'iat': datetime.datetime.now(datetime.UTC),
            'sub': email
        }

        secret = secret if secret else os.environ.get('AUTH_TOKEN_SECRET')

        try:
            return jwt.encode(
                payload,
                secret,
                algorithm = self.auth_token_algo
            )
        except Exception as e:
            return e

    def gen_auth_token(self, email, pwd):
        if not email or not pwd:
            return False

        pass_valid = self.validate_password(email, pwd)
        if not pass_valid:
            return False

        return self.create_auth_token(email)

    def validate_auth_token(self, token):
        try:
            payload = jwt.decode(
                token,
                os.environ.get('AUTH_TOKEN_SECRET'),
                self.auth_token_algo
            )

            return payload['sub']

        except jwt.ExpiredSignatureError:
            return self.auth_token_msg_expired

        except jwt.InvalidTokenError:
            return self.auth_token_msg_invalid

        return False
