from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """Cloudflare R2 storage for media files."""
    location = 'media'
    file_overwrite = False
    custom_domain = None

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        if settings.AWS_S3_CUSTOM_DOMAIN:
            self.custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
        super().__init__(*args, **kwargs)


class StaticStorage(S3Boto3Storage):
    """Cloudflare R2 storage for static files."""
    location = 'static'
    default_acl = 'public-read'
