"""Eatfirst FileSystem tests."""
from io import StringIO
from uuid import uuid4

from faker import Faker
from moto import mock_s3_deprecated as mock_s3

from efs import EFS

fake = Faker()
TEST_FILE = 'test_file_{0}.txt'.format(uuid4())
RANDOM_DATA = StringIO(fake.sha256())


@mock_s3
def test_create_file(bucket):
    """Test file creation."""
    bucket = bucket()

    efs = EFS(storage='s3')
    RANDOM_DATA.seek(0)
    efs.upload(TEST_FILE, RANDOM_DATA, async_=False)

    key = bucket.get_key(TEST_FILE)
    RANDOM_DATA.seek(0)
    assert key.get_contents_as_string().decode() == RANDOM_DATA.read()


@mock_s3
def test_read_file(bucket):
    """Test read file."""
    bucket = bucket()
    k = bucket.new_key(TEST_FILE)
    RANDOM_DATA.seek(0)
    k.set_contents_from_file(RANDOM_DATA)
    RANDOM_DATA.seek(0)

    efs = EFS(storage='s3')
    uploaded_content = efs.open(TEST_FILE)
    content = uploaded_content.read()
    assert content == RANDOM_DATA.read()


@mock_s3
def test_remove_file(bucket):
    """Test remove file."""
    bucket = bucket()

    assert len(bucket.get_all_keys()) == 0
    k = bucket.new_key(TEST_FILE)
    RANDOM_DATA.seek(0)
    k.set_contents_from_file(RANDOM_DATA)
    RANDOM_DATA.seek(0)
    assert len(bucket.get_all_keys()) == 1

    efs = EFS(storage='s3')
    efs.remove(TEST_FILE)
    assert len(bucket.get_all_keys()) == 0


@mock_s3
def test_upload_and_remove_folder(bucket):
    """Test remove folder with content."""
    bucket = bucket()

    efs = EFS(storage='s3')
    RANDOM_DATA.seek(0)
    efs.upload('very/long/path/to/be/created/' + TEST_FILE, RANDOM_DATA, async_=False)
    key = bucket.get_key('very/long/path/to/be/created/' + TEST_FILE)
    assert key

    efs.remove('very/')
    key = bucket.get_key('very/long/path/to/be/created/' + TEST_FILE)
    assert not key


@mock_s3
def test_rename_file(bucket):
    """Test rename file."""
    bucket = bucket()

    efs = EFS(storage='s3')
    RANDOM_DATA.seek(0)
    efs.upload(TEST_FILE, RANDOM_DATA, async_=False)
    key = bucket.get_key(TEST_FILE)
    assert key

    efs.rename(TEST_FILE, 'new_test_file.txt')
    key = bucket.get_key(TEST_FILE)
    assert not key
    key = bucket.get_key('new_test_file.txt')
    assert key


@mock_s3
def test_move_file(bucket):
    """Test move file to a new folder."""
    bucket = bucket()

    efs = EFS(storage='s3')
    RANDOM_DATA.seek(0)
    efs.upload(TEST_FILE, RANDOM_DATA, async_=False)

    key = bucket.get_key(TEST_FILE)
    assert key

    efs.move(TEST_FILE, 'special_text/test_file.txt')
    key = bucket.get_key(TEST_FILE)
    assert not key
    key = bucket.get_key('special_text/test_file.txt')
    assert key
