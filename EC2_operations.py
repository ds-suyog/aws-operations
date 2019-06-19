import boto3

running_instance = []
ec2 = boto3.resource('ec2')

#ami-0b99c7725b9484f9e, t2.micro, mem 1 GiB
#ec2.create_instances(ImageId='ami-0b99c7725b9484f9e', MinCount=1, MaxCount=5)
    #InstanceType='t2.micro', KeyName='YOUR_SSH_KEY_NAME',


instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

for instance in instances:
    print(instance.id, instance.instance_type)

