from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class SecurityTokenWorkaroundS3Boto3Storage(S3Boto3Storage):
    def _get_security_token(self):
        return None

class MediaStorage(SecurityTokenWorkaroundS3Boto3Storage):
    location = 'funnels/'
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
        print(f"Saving file {name} to bucket {self.bucket_name}")
        
        # Call the parent _save method to save the file to S3
        return super()._save(name, content)
    
class FunnelStepThumbnailImageStorage(SecurityTokenWorkaroundS3Boto3Storage):
    file_overwrite = True
    default_acl = 'public-read'

    def __init__(self, *args, **kwargs):
        # If DEBUG is True, use a different bucket name
        if settings.DEBUG:
            self.location = 'funnel-steps-thumbnails-dev/'
            self.bucket_name = 'barter-capital-users-dev'
        else:
            self.location = 'funnel-steps-thumbnails/'
            self.bucket_name = 'barter-capital-users'
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        # Print some debug information
        print(f"Saving funne step image {name} to bucket {self.bucket_name}")
        
        # Call the parent _save method to save the file to S3
        return super()._save(name, content)
