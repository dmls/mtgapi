import bcrypt
from dotenv import load_dotenv
import json
import os
import secrets

from db_manager import DBManager
from user import User

def create_config_file():
    # Define path to the .env file
    dotenv_path = os.path.expanduser('./.env')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(dotenv_path), exist_ok=True)

    # Check if the .env file already exists
    if os.path.exists(dotenv_path):
        print(f'Dotenv file "{dotenv_path}" already exists.')
        return

    # Generate configuration variables
    salt = bcrypt.gensalt()
    auth_token_secret = secrets.token_hex(24)

    # Write config to .env file
    with open(dotenv_path, 'w') as dotenv_file:
        dotenv_file.write(f'PASSWORD_SALT={salt.decode("utf-8")}\n')
        dotenv_file.write(f'AUTH_TOKEN_SECRET={auth_token_secret}\n')

    print(f'Dotenv file "{dotenv_path}" created.')

    return

# Create sample user, not for prod use.
def create_user(dbm):
    email = 'user@example.com'
    pwd = 'password'

    user = User(dbm)
    result = user.create('user@example.com', 'password')

    if not result:
        print('Sample user not created.')
        return

    print('Created sample user: user@example.com, password: password')

    return

def main():
    dbm = DBManager()

    create_config_file()
    create_user(dbm)

    print('Setup complete.')

if __name__ == '__main__':
    main()
