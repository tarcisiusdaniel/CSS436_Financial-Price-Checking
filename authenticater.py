import boto3
import botocore
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from application import login_manager
import yaml

def get_config():
    return yaml.safe_load(open("config.yaml"))

config = get_config()

bCrypt = Bcrypt()
table = boto3.resource(
    'dynamodb',
    aws_access_key_id=config['db_access_key'],
    aws_secret_access_key=config['db_secret_access_key'],
    region_name='us-west-2').Table('Accounts')

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    def loginUser(self, password):
        try:
            response = table.get_item(Key={'username': self.id})
            return (bCrypt.check_password_hash(response['Item']['password'], password))
        except KeyError as e:
            return False

    def registerUser(self, password, phone_number):
        try:
            response = table.get_item(Key={'username': self.id})
            response['Item']
            return False
        except KeyError as e:
            response = table.put_item(
                Item={
                    'username': self.id,
                    'password': bCrypt.generate_password_hash(password).decode('ascii'),
                    'phone_number': phone_number
                })
            return True

    def get(self, user_id):
        try:
            response = table.get_item(Key={'username': user_id})
            response['Item']
            return User(user_id)
        except KeyError as e:
            return None
