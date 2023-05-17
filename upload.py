import os
import mimetypes
import boto3

def upload_files_to_s3(bucket_name, local_directory, remote_path):
    s3_client = boto3.client('s3')

    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            local_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_key = os.path.join(remote_path, relative_path).replace("\\","/")  # Replace backslashes with forward slashes on Windows
            content_type = mimetypes.guess_type(file_name)[0]
            if content_type is None:
                content_type = 'application/octet-stream'
            print(f"Uploading {local_path} to {s3_key} in bucket {bucket_name} with content type {content_type}")
            s3_client.upload_file(local_path, bucket_name, s3_key, ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'})

    print('Upload completed.')
    #print(f'Connect to the output on https://{bucket_name}/{remote_path}index.html')
    print(f'http://{bucket_name}.s3-website-eu-west-1.amazonaws.com/{remote_path}')

# Usage example
bucket_name = 'demo.amazoninstructor.info'
local_directory = './build/'
remote_path='react-image-slideshow/'

upload_files_to_s3(bucket_name, local_directory, remote_path)
