import logging
import boto3
from botocore.exceptions import ClientError
import constant

running_instance = []
ec2 = boto3.resource('ec2')

session = boto3.session.Session()
current_region = session.region_name
print("current_region = {}".format(current_region))

ec2_c = boto3.client('ec2')
response = ec2_c.describe_instances()
print(response)

def create_ec2_instance(image_id, instance_type, keypair_name):
    """Provision and launch an EC2 instance
    """

    # Provision and launch the EC2 instance
    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.run_instances(ImageId='ami-0b99c7725b9484f9e',
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            MinCount=1,
                                            MaxCount=1)
    except ClientError as e:
        logging.error(e)
        return None
    return response['Instances'][0]

resp = create_ec2_instance('ami-0b99c7725b9484f9e', 't2.micro', constant.KEYPAIR_NAME)
print(resp)