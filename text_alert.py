import boto3
import yaml

def get_config():
    return yaml.safe_load(open("config.yaml"))

def signin_text_msg(config,phone_num,password,username):
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=config['sns_access_key'],
        aws_secret_access_key=config['sns_secret_key'],
        region_name = config['aws_region']
    )
    msg = 'Thank you for signing in an account \n'
    msg += 'Here is your account username and password\n'
    msg += 'Username: ' + username + '\nPassword: ' + password
    phone_number_with_region = '+1' + phone_num
    sns_client.publish(
        PhoneNumber=phone_number_with_region,
        Message=msg
    )

def main():
    config = get_config()
    num = '2066378356' #'4257700031'
    username = 'tarcisiusdaniel'
    password = 'jingtot123'
    send_text_msg(config,num,password,username)

if __name__ == '__main__':
    main()