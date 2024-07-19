from storages.backends.s3boto3 import S3Boto3Storage


class SecurityTokenWorkaroundS3Boto3Storage(S3Boto3Storage):
    def _get_security_token(self):
        return None


class MediaStorage(SecurityTokenWorkaroundS3Boto3Storage):
    bucket_name = "dashboard-backend-api"
    location = "assets-root/media"


class MediaStorageProd(SecurityTokenWorkaroundS3Boto3Storage):
    bucket_name = "dashboard-backend-api-prod"
    location = "assets-root/media"


class StaticStorage(SecurityTokenWorkaroundS3Boto3Storage):
    bucket_name = "dashboard-backend-api"
    location = "assets-root/static"


class StaticStorageProd(SecurityTokenWorkaroundS3Boto3Storage):
    bucket_name = "dashboard-backend-api-prod"
    location = "assets-root/static"
