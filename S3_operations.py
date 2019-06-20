import boto3
import botocore

class S3Helper:
    """This is handcrafted helper class is for easy reusability of AWS S3 operations.
    Please configure your AWS before using this helper class
    """

    def __init__(self, debug = 'False'):
        self._debug = debug

    def current_region(self):
        session = boto3.session.Session()
        current_region = session.region_name
        return current_region

    def create_bucket_name(self, bucket_prefix):
        # The generated bucket name must be between 3 and 63 chars long
        import uuid
        return ''.join([bucket_prefix, str(uuid.uuid4())])

    def create_bucket(self, s3_resource, bucket_prefix):
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

    def buckets_iterator(self, s3_resource):
        """ Iterates over buckets and their respective keys
        """
        for bucket in s3_resource.buckets.all():    
            print("******** bucket name = {}".format(bucket.name))
            bucketname = bucket.name
            #print(bucket.get_available_subresources())
            for key in bucket.objects.all():
                print("key.key = {}, size = {}".format(key.key, key.size/1024))

    def bucket_iterator(self, s3_resource, bucketname):
        """ Iterates over respective keys of particular bucket
        """        
        bucket = s3_resource.Bucket(bucketname)
        print("********** bucket name = {}".format(bucket.name))        
        for key in bucket.objects.all():
            print("key.key = {}, size = {} KB".format(key.key, self.prettify_size(key.size)))

    def buckets_iter_s3client(self, s3_client):
        """Output the bucket names by s3_client
        """
        response = s3_client.list_buckets()
        for bucket in response['Buckets']:
            print("bucket name = ", bucket["Name"])

    def upload_file(self, file_path, s3_resource, bucketname, s3key):
        """Upload file based on file structure
        """
        data = open(file_path, 'rb')
        status = s3_resource.Bucket(bucketname).put_object(Key=s3key, Body=data)
        if self._debug == 'True': print("status = {}".format(status))

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

    def prettify_size(self, size):
        one_kb, one_mb, one_gb, one_tb = 1024, 1024*1024, 1024*1024*1024, 1024*1024*1024*1024
        if size < one_kb:
            size_str = "{} Bytes".format(size)
        elif one_kb <= size < one_mb:
            size_str = "{} KB".format(round(size/1024, 2))
        elif one_mb <= size < one_gb:
            size_str = "{} MB".format(round(size/(1024*1024),2))
        elif one_gb <= size < one_tb:
            size_str = "{} GB".format(round(size/(1024*1024*1024),2))
        elif one_tb <= size:
            size_str = "{} TB".format(round(size/(1024*1024*1024*1024),2))
        return size_str

    def access_object(self, s3_resource, bucketname, key):
        obj = s3_resource.Object(bucketname, key)
        body = obj.get()['Body'].read().decode('utf-8')
        body_str = "-----------------------------------body start\n{}\n-----------------------------------body end".format(body)
        size = obj.content_length
        size_str = self.prettify_size(size)
        print("************* Details of object:\nobj type = {}, \nobj.content_length = {}, \nobj.content_type = {}, \nbody = \n{}".format(type(obj), 
            size_str, obj.content_type, body_str))

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
    s3_helper = S3Helper(debug = 'True')

    # low-level client interface
    s3_client = boto3.client('s3')

    # high-level interface
    s3_resource = boto3.resource('s3')

    if s3_helper._debug == 'True': print("current_region = {}".format(s3_helper.current_region()))
    
    if s3_helper._debug == 'True': print('\ncreating bucket...')    
    bucket_name, response = s3_helper.create_bucket(s3_resource = s3_resource.meta.client, bucket_prefix = 'boto3bucket')
    #bucket_name = "boto3bucket08cdc9b1-2c60-4c7e-ad4b-09e437992d26"

    if s3_helper._debug == 'True': print("\nuploading files...") 
    s3_helper.upload_file('test.py', s3_resource, bucket_name, 'code/test.py/')
    s3_helper.upload_file('test.py', s3_resource, bucket_name, 'code/test2.py/')
    s3_helper.upload_file('office1.jpg', s3_resource, bucket_name, 'data/office1.jpg/')

    if s3_helper._debug == 'True': print("\niterating over bucket's keys...") 
    s3_helper.bucket_iterator(s3_resource, bucket_name)
    #s3_helper.buckets_iterator(s3_resource)
    #s3_helper.buckets_iter_s3client(s3_client)

    if s3_helper._debug == 'True': print('\naccessing object and displaying details...') 
    s3_helper.access_object(s3_resource, bucket_name, 'code/test.py/')

    if s3_helper._debug == 'True': print("\ndownloading object...")     
    s3_helper.download_file(s3_resource, bucket_name, 'code/test2.py/','test2.py')

    import os;os.remove('test2.py')

    if s3_helper._debug == 'True': print("\ndeleting object...") 
    s3_helper.delete_object(s3_resource, bucket_name, 'code/test2.py/')

    if s3_helper._debug == 'True': print("\nemptying bucket...") 
    s3_helper.empty_bucket(s3_resource)
    if s3_helper._debug == 'True': print("\ndeleting bucket...")     
    s3_helper.delete_bucket(s3_resource, bucket_name)


if __name__ == '__main__':
    main()
