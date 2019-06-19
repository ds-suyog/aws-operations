import boto3
import botocore

# Let's use Amazon S3

class S3Helper:
    # methods for this module
    pass

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

# # create bucket
# bucket_name, response = create_bucket(
# 	bucket_prefix='pythonbucket', 
# 	s3_connection=s3_resource.meta.client)

# # Output the bucket names by s3_client
# response = s3_client.list_buckets()
# print('Existing buckets:')
# for bucket in response['Buckets']:
#     print("bucket name = ", bucket["Name"])

bucketname = ""

# iterating over buckets and respective keys
print("iterating on buckets:")
for bucket in s3_resource.buckets.all():    
    print("bucket name = {}".format(bucket.name))
    bucketname = bucket.name
    #print(bucket.get_available_subresources())
    for key in bucket.objects.all():
        print("key.key = {}, size = {} KB".format(key.key, key.size/1024))


# # Upload file based on file structure
# data = open('test.py', 'rb')
# status = s3_resource.Bucket(bucketname).put_object(Key='code/test.py/', Body=data)
# print("status = {}".format(status))

# data = open('office1.jpg', 'rb')
# status = s3_resource.Bucket(bucketname).put_object(Key='data/office1.jpg/', Body=data)
# print("status = {}".format(status))

# Download file
#def download_file(bucketname, s3key, localpath)
try:
    s3_resource.Bucket(bucketname).download_file('code/test.py/', 'test.py')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

key = s3_resource.Bucket(bucketname).get_key('data/office1.jpg/')
key.get_contents_to_filename('dd.jpg')

# obj = s3_resource.Bucket(bucketname).Object('code/test.py')
# print("obj type = {}".format(type(obj)))


# # Empty bucket
# for bucket in s3_resource.buckets.all():
#     bucket = s3_resource.Bucket(bucket.name)
#     bucket.object_versions.delete()

# # # must delete all keys before deleting bucket
# bucket = s3_resource.Bucket(bucketname)
# for key in bucket.objects.all():
#     key.delete()
# bucket.delete()

for bucket in s3_resource.buckets.all():
    print("bucket name = {}".format(bucket.name))

