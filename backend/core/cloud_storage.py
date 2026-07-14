import boto3
import os
from botocore.exceptions import NoCredentialsError
from core.config import settings

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.s3_bucket_name

    def upload_file(self, file_path: str, object_name: str) -> str:
        try:
            self.s3.upload_file(file_path, self.bucket_name, object_name)
            return f"s3://{self.bucket_name}/{object_name}"
        except FileNotFoundError:
            raise FileNotFoundError("The file was not found.")
        except NoCredentialsError:
            raise Exception("Credentials not available.")

    def download_file(self, object_name: str, file_path: str):
        try:
            self.s3.download_file(self.bucket_name, object_name, file_path)
        except Exception as e:
            raise Exception(f"Error downloading file: {e}")

    def list_files(self, prefix: str = ""):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            return [content['Key'] for content in response.get('Contents', [])]
        except Exception as e:
            raise Exception(f"Error listing files: {e}")
