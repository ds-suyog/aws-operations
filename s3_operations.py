import boto3

# Let's use Amazon S3

# # low-level client interface
# s3_client = boto3.client('s3')

#high-level interface
s3 = boto3.resource('s3')

import uuid
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

session = boto3.session.Session()
current_region = session.region_name

# # Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

# # Upload a new file
# data = open('test.jpg', 'rb')
# s3.Bucket('bucket11gg').put_object(Key='test.jpg', Body=data)

