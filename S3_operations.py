import boto3
import botocore

class S3Helper:
    """This is handcrafted helper class for easy reusability of AWS S3 operations.
    Please configure your AWS before using this helper class
    """

    def __init__(self):
        pass      

    def current_region(self):
        session = boto3.session.Session()
        current_region = session.region_name
        return current_region

    def create_bucket_name(self, bucket_prefix):
        # The generated bucket name must be between 3 and 63 chars long
        import uuid
        return ''.join([bucket_prefix, str(uuid.uuid4())])

    def create_bucket(self, s3_resource, bucket_prefix, s3_resource):
        bucket_name = self.create_bucket_name(bucket_prefix)
        current_region = self.current_region()

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

    def bucket_iter_s3client(self, s3_client):
        """Output the bucket names by s3_client
        """
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            print("bucket name = ", bucket["Name"])

    def bucket_iterator(self, s3_resource):
        """ Iterates over buckets and their respective keys
        """
        print("iterating on buckets:")
        for bucket in s3_resource.buckets.all():    
            print("bucket name = {}".format(bucket.name))
            bucketname = bucket.name
            #print(bucket.get_available_subresources())
            for key in bucket.objects.all():
                print("key.key = {}, size = {} KB".format(key.key, key.size/1024))

    def upload_file(self, s3_resource, bucketname, file_path, s3key):
        """Upload file based on file structure
        """
        data = open(file_path, 'rb')
        status = s3_resource.Bucket(bucketname).put_object(Key='code/test.py/', Body=data)
        print("status = {}".format(status))

        data = open('office1.jpg', 'rb')
        status = s3_resource.Bucket(bucketname).put_object(Key='data/office1.jpg/', Body=data)
        print("status = {}".format(status))

        # #alternate way
        # s3_resource.Bucket(bucketname).upload_file('test.py','code/test.py/')

    def download_file(self, s3_resource, bucketname, s3key, localpath):
        try:
            s3_resource.Bucket(bucketname).download_file(s3key, localpath)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    def access_object(self, s3_resource, bucketname, key):
        obj = s3_resource.Object(bucketname, key)
        body = obj.get()['Body'].read().decode('utf-8')
        print("obj type = {}, \nobj.content_length = {}, \nobj.content_type = {}, \nbody = {}".format(type(obj), 
            obj.content_length, obj.content_type, body))

    def delete_object(self, s3_resource, bucketname, key):
        # deleted folder
        obj = s3_resource.Object(bucketname, key)
        obj.delete()

    def empty_bucket(self, s3_resource):
        for bucket in s3_resource.buckets.all():
            bucket = s3_resource.Bucket(bucket.name)
            bucket.object_versions.delete()

    def delete_bucket(self, s3_resource, bucketname):
        """must delete all keys before deleting bucket
        """
        bucket = s3_resource.Bucket(bucketname)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()


def main():
    s3_helper = S3Helper()
    bucketname = "pythonbucket0a75811f-efa3-4d85-927e-b89c71cf914f"

    # low-level client interface
    s3_client = boto3.client('s3')

    # high-level interface
    s3_resource = boto3.resource('s3')

    print("current_region = {}".format(s3_helper.current_region()))
    
    #bucket_name, response = self.create_bucket(bucket_prefix = 'pythonbucket', s3_resource = s3_resource.meta.client)

    #s3_helper.bucket_iterator(s3_resource)
    #print("bucketname = ", bucketname)
    #s3_helper.bucket_iter_s3client(s3_client)

    #s3_helper.upload_file(s3_resource, bucketname, 'code/test.py/', 'test.py')

    s3_helper.access_object(s3_resource, bucketname, 'code/test.py/')
    
    #s3_helper.download_file(s3_resource, bucketname, 'code/test.py/','test.py')

    #s3_helper.delete_object(s3_resource, bucketname, 'code/test.py/')
    #s3_helper.empty_bucket(s3_resource)
    #s3_helper.delete_bucket(s3_resource, bucketname)


if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()

