"""EatFirst file system for S3."""

from autorepr import autorepr
from fs_s3fs import S3FS


class EatFirstS3(S3FS):
    """Extension of S3FS class, fixing it to work with python 3k."""

    __repr__ = autorepr(['bucket', 'aws_access_key_id',], bucket=lambda self: self._bucket_name)
