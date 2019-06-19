import boto3

# Let's use Amazon S3

# low-level client interface
s3_client = boto3.client('s3')

#high-level interface
s3_resource = boto3.resource('s3')

# Find current region
session = boto3.session.Session()
current_region = session.region_name

import uuid
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    print(current_region)
    bucket_name = create_bucket_name(bucket_prefix)

	# reolving error when region is 'us-east-1', botocore.exceptions.ClientError: An error occurred (InvalidLocationConstraint) 
    if current_region == 'us-east-1':
        bucket_response = s3_resource.create_bucket(
            Bucket=bucket_name,
        )
    else:
    	bucket_response = s3_resource.create_bucket(
    		Bucket=bucket_name,
    		CreateBucketConfiguration={'LocationConstraint': current_region}) 

    print("bucket name = {}, current_region = {}".format(bucket_name,current_region))
    return bucket_name, bucket_response

# create bucket
# bucket_name, response = create_bucket(
# 	bucket_prefix='pythonbucket', 
# 	s3_connection=s3resource.meta.client)

# Output the bucket names by s3_client
response = s3_client.list_buckets()
print('Existing buckets:')
for bucket in response['Buckets']:
    print("bucket name = ", bucket["Name"])

# Print out bucket names by s3_resource
print("iterating on buckets")
for bucket in s3_resource.buckets.all():
    print("bucket name: = {}".format(bucket.name))

# # Upload a new file
# data = open('test.jpg', 'rb')
# s3.Bucket('bucket11gg').put_object(Key='test.jpg', Body=data)

bucket = s3_resource.Bucket('bucket_name')
bucket.object_versions.delete()

for bucket in s3_resource.buckets.all():
    print("bucket name: = {}".format(bucket.name))

