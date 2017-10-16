"""The file system abstraction."""
import urllib.parse

from autorepr import autorepr
from flask import current_app

from .eatfirst_osfs import EatFirstOSFS
from .eatfirst_s3 import EatFirstS3


class EFS:
    """The EatFirst File system."""

    def __init__(self, storage='local', *args, **kwargs):
        """The constructor method of the filesystem abstraction."""
        self.separator = kwargs.get('separator', '/')
        self.current_file = ''
        self.storage = storage
        if storage.lower() == 'local':
            self.home = EatFirstOSFS(current_app.config['LOCAL_STORAGE'], create=True, *args, **kwargs)
        elif storage.lower() == 's3':
            self.home = EatFirstS3(current_app.config['S3_BUCKET'], aws_access_key=current_app.config['AWS_ACCESS_KEY'],
                                   aws_secret_key=current_app.config['AWS_SECRET_KEY'], *args, **kwargs)
        else:
            raise RuntimeError('{} does not support {} storage'.format(self.__class__.__name__, storage))

    __repr__ = autorepr(['storage', 'separator', 'home'])

    def make_public(self, path):
        """Make sure a file is public."""
        if hasattr(self.home, 'makepublic'):
            self.home.makepublic(path)

    def upload(self, path, content, async_=False, content_type=None, *args, **kwargs):
        """Upload a file and return its size in bytes.

        :param path: the relative path to file, including filename.
        :param content: the content to be written.
        :param async_: Create a thread to send the data in case True is sent.
        :param content_type: Enforce content-type on destination.
        :return: size of the saved file.
        """
        path_list = path.split(self.separator)
        if len(path_list) > 1:
            self.home.makedir(self.separator.join(path_list[:-1]), recursive=True, allow_recreate=True)
        self.home.createfile(path, wipe=False)

        if async_:
            self.home.setcontents_async(path, content, *args, **kwargs).wait()
        else:
            self.home.setcontents(path, content, *args, **kwargs)

        if isinstance(self.home, EatFirstS3) and content_type is not None:
            # AWS is guessing the content type wrong. Bellow is our dirty fix for that.
            key = self.home._s3bukt.get_key(path)
            key.copy(key.bucket, key.name, preserve_acl=True, metadata={'Content-Type': content_type})

        self.make_public(path)

    def open(self, path, *args, **kwargs):
        """Open a file and return a file pointer.

        :param path: the relative path to file, including filename.
        :return: a pointer to the file.
        """
        if not self.home.exists(path):
            exp = FileNotFoundError()
            exp.filename = path
            raise exp
        return self.home.safeopen(path, *args, **kwargs)

    def remove(self, path):
        """Remove a file or folder.

        :param path: the relative path to file, including filename.
        """
        if self.home.isdir(path):
            self.home.removedir(path, force=True)
        else:
            self.home.remove(path)

    def rename(self, path, new_path):
        """Rename a file.

        :param path: the relative path to file, including filename.
        :param path: the relative path to new file, including new filename.
        """
        self.home.rename(path, new_path)

    def move(self, path, new_path):
        """Move a file.

        :param path: the relative path to file, including filename.
        :param new_path: the relative path to new file, including filename.
        """
        path_list = new_path.split(self.separator)
        if len(path_list) > 1:
            self.home.makedir(self.separator.join(path_list[:-1]), recursive=True, allow_recreate=True)
        self.home.move(path, new_path, overwrite=True)

    def file_url(self, path, with_cdn=True):
        """Get a file url.

        :param path: the relative path to file, including filename.
        :param with_cdn: specify if the url should return with the cdn information, only used for images.
        """
        if not self.home.haspathurl(path):
            if isinstance(self.home, EatFirstOSFS):
                return path
            raise PermissionError('The file {} has no defined url'.format(path))

        url = self.home.getpathurl(path)
        if current_app.config.get('S3_CDN_URL', None) and with_cdn:
            parsed_url = urllib.parse.urlparse(url)
            url = url.replace(parsed_url.hostname, current_app.config['S3_CDN_URL'])
        url = url.replace('http://', 'https://')
        return url

    @classmethod
    def get_filesystem(cls):
        """Return an instance of the filesystem abstraction."""
        return cls(storage=current_app.config['DEFAULT_STORAGE'])
