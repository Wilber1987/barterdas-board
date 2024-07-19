from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import logging

class SecurityTokenWorkaroundS3Boto3Storage(S3Boto3Storage):
    def _get_security_token(self):
        return None

class QRCodeStorage(SecurityTokenWorkaroundS3Boto3Storage):
    location = 'qr_code/'
    file_overwrite = True
    default_acl = 'public-read'

    def __init__(self, *args, **kwargs):
        # If DEBUG is True, use a different bucket name
        if settings.DEBUG:
            self.bucket_name = 'barter-capital-users-dev'
        else:
            self.bucket_name = 'barter-capital-users'
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        # Print some debug information
        logger = logging.getLogger('django')
        logger.info(f"Saving file {name} to bucket {self.bucket_name}/{self.location}")
        
        # Call the parent _save method to save the file to S3
        return super()._save(name, content)