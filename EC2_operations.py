import boto3

running_instance = []
ec2 = boto3.resource('ec2')

for instance in ec2.instances.all():
	print(instance)
    print(instance.state['Name'])