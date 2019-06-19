import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

data = open('test.jpg', 'rb')
s3.Bucket('bucket11gg').put_object(Key='test.jpg', Body=data)

