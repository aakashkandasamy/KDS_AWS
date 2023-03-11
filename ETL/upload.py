import boto3
import os


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# print(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

bucket_name = "labpicschemistryextracted"
directory_path = "../Extracted"

#boto s3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#loop through the directory to upload each file
for root, dirs, files in os.walk(directory_path):
    for file in files:
        local_path = os.path.join(root, file)
        s3_key = os.path.relpath(local_path, directory_path)
        s3_resource.Bucket(bucket_name).upload_file(local_path, s3_key)
