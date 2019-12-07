import boto3
import yaml

def get_config():
    return yaml.safe_load(open("config.yaml"))

def send_text_msg(config,phone_num,msg):
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=config['sns_access_key'],
        aws_secret_access_key=config['sns_secret_key'],
        region_name = config['aws_region']
    )
    sns_client.publish(
        PhoneNumber=phone_num,
        Message=msg
    )

def main():
    config = get_config()
    num = '+14257700031'#'+12066378356'
    send_text_msg(config,num,"this is a test message")

if __name__ == '__main__':
    main()