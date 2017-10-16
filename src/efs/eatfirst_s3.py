"""EatFirst file system for S3."""

from autorepr import autorepr
from fs.path import iteratepath
from fs.path import normpath
from fs.path import relpath
from fs.s3fs import S3FS
from fs.s3fs import thread_local


class EatFirstS3(S3FS):
    """Extension of S3FS class, fixing it to work with python 3k."""

    def __init__(self, bucket, prefix='', aws_access_key=None, aws_secret_key=None, separator='/',
                 thread_synchronize=True, key_sync_timeout=1):
        """Constructor for S3FS objects.

        S3FS objects require the name of the S3 bucket in which to store
        files, and can optionally be given a prefix under which the files
        should be stored.  The AWS public and private keys may be specified
        as additional arguments; if they are not specified they will be
        read from the two environment variables AWS_ACCESS_KEY_ID and
        AWS_SECRET_ACCESS_KEY.

        The keyword argument 'key_sync_timeout' specifies the maximum
        time in seconds that the filesystem will spend trying to confirm
        that a newly-uploaded S3 key is available for reading.  For no
        timeout set it to zero.  To disable these checks entirely (and
        thus reduce the filesystem's consistency guarantees to those of
        S3's "eventual consistency" model) set it to None.

        By default the path separator is '/', but this can be overridden
        by specifying the keyword 'separator' in the constructor.
        """
        self._bucket_name = bucket
        self._access_keys = (aws_access_key, aws_secret_key)
        self._separator = separator
        self._key_sync_timeout = key_sync_timeout
        # Normalise prefix to this form: path/to/files/
        prefix = normpath(prefix)
        while prefix.startswith(separator):
            prefix = prefix[1:]
        if prefix and not prefix.endswith(separator):
            prefix = prefix + separator
        self._prefix = prefix
        self._tlocal = thread_local()
        super(S3FS, self).__init__(thread_synchronize=thread_synchronize)

    __repr__ = autorepr([], bucket=lambda self: self._bucket_name, key=lambda self: self._access_keys[0])

    def _s3path(self, path):
        """Get the absolute path to a file stored in S3."""
        path = relpath(normpath(path))
        path = self._separator.join(iteratepath(path))
        s3path = self._prefix + path
        if s3path and s3path[-1] == self._separator:
            s3path = s3path[:-1]
        return s3path
