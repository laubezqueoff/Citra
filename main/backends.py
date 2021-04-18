from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorageBackend(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False