# import os
from storages.backends.s3boto import S3BotoStorage

# os.environ['S3_USE_SIGV4'] = 'True'
from tfg.settings import *


# class StaticStorage(S3BotoStorage):
##"""uploads to 'mybucket/static/', serves from 'cloudfront.net/static/'"""
#    location = settings.STATICFILES_LOCATION
#
#    def __init__(self, *args, **kwargs):
#        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
#        super(StaticStorage, self).__init__(*args, **kwargs)
#
# class MediaStorage(S3BotoStorage):
##"""uploads to 'mybucket/media/', serves from 'cloudfront.net/media/'"""
#    location = settings.MEDIAFILES_LOCATION
#
#    def __init__(self, *args, **kwargs):
#        kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
#        super(MediaStorage, self).__init__(*args, **kwargs)


class S3Storage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs["custom_domain"] = settings.AWS_CLOUDFRONT_DOMAIN
        super(MediaStorage, self).__init__(*args, **kwargs)

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key,
                self.secret_key,
                calling_format=self.calling_format,
                host="s3.eu-central-1.amazonaws.com",
            )
        return self._connection


def StaticS3BotoStorage():
    return S3BotoStorage(location="daresny/static")


def MediaS3BotoStorage():
    return S3BotoStorage(location="tfg/media")
