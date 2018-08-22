"""EatFirst FileSystem tests."""
from io import BytesIO
from uuid import uuid4

import pytest
from botocore.exceptions import ClientError
from faker import Faker

from efs import EFS

fake = Faker()
TEST_FILE = 'test_file_{0}.txt'.format(uuid4())
RANDOM_DATA = BytesIO(fake.sha256().encode())


def test_create_file(bucket):
    """Test file creation."""
    bucket = bucket()

    efs = EFS(storage="s3")
    RANDOM_DATA.seek(0)
    efs.upload(TEST_FILE, RANDOM_DATA)

    key = bucket.Object(TEST_FILE)
    RANDOM_DATA.seek(0)
    assert key.get()["Body"].read() == RANDOM_DATA.read()


def test_read_file(bucket):
    """Test read file."""
    bucket = bucket()
    k = bucket.Object(TEST_FILE)
    RANDOM_DATA.seek(0)
    k.put(Body=RANDOM_DATA)
    RANDOM_DATA.seek(0)

    efs = EFS(storage="s3")
    uploaded_content = efs.open(TEST_FILE)
    content = uploaded_content.read()
    assert content == RANDOM_DATA.read()


def test_remove_file(bucket):
    """Test remove file."""
    bucket = bucket()

    assert not list(bucket.objects.all())
    k = bucket.Object(TEST_FILE)
    RANDOM_DATA.seek(0)
    k.put(Body=RANDOM_DATA)
    RANDOM_DATA.seek(0)
    assert list(bucket.objects.all())

    efs = EFS(storage="s3")
    efs.remove(TEST_FILE)
    assert not list(bucket.objects.all())


def test_upload_and_remove_folder(bucket):
    """Test remove folder with content."""
    bucket = bucket()

    efs = EFS(storage="s3")
    RANDOM_DATA.seek(0)
    efs.upload("very/long/path/to/be/created/" + TEST_FILE, RANDOM_DATA)
    key = bucket.Object("very/long/path/to/be/created/" + TEST_FILE)
    assert key

    efs.remove("very/")
    key = bucket.Object("very/long/path/to/be/created/" + TEST_FILE)
    with pytest.raises(ClientError) as e:
        key.get()
    assert e.value.response["Error"]["Code"] == "NoSuchKey"


def test_rename_file(bucket):
    """Test rename file."""
    bucket = bucket()

    efs = EFS(storage="s3")
    RANDOM_DATA.seek(0)
    efs.upload(TEST_FILE, RANDOM_DATA)
    key = bucket.Object(TEST_FILE)
    assert key

    efs.rename(TEST_FILE, "new_test_file.txt")
    key = bucket.Object(TEST_FILE)
    with pytest.raises(ClientError) as e:
        key.get()
    assert e.value.response["Error"]["Code"] == "NoSuchKey"
    key = bucket.Object("new_test_file.txt")
    assert key


def test_move_file(bucket):
    """Test move file to a new folder."""
    bucket = bucket()

    efs = EFS(storage="s3")
    RANDOM_DATA.seek(0)
    efs.upload(TEST_FILE, RANDOM_DATA)

    key = bucket.Object(TEST_FILE)
    assert key.get()

    efs.move(TEST_FILE, "special_text/test_file.txt")
    key = bucket.Object(TEST_FILE)
    with pytest.raises(ClientError) as e:
        key.get()
    assert e.value.response["Error"]["Code"] == "NoSuchKey"
    key = bucket.Object("special_text/test_file.txt")
    assert key.get()
