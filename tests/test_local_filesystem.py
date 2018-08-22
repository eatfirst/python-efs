"""EatFirst FileSystem tests."""

import os
from io import BytesIO

from faker import Faker
from flask import current_app

from efs import EFS

fake = Faker()
TEST_FILE = 'test_file.txt'
RANDOM_DATA = BytesIO(fake.sha256().encode())


def test_create_file(app, delete_temp_files):
    """Test file creation."""
    assert app
    assert delete_temp_files
    home_path = current_app.config['LOCAL_STORAGE']
    efs = EFS()
    efs.upload(TEST_FILE, RANDOM_DATA)

    assert os.path.exists(os.path.join(home_path, TEST_FILE))


def test_read_file(app, delete_temp_files):
    """Test read file."""
    assert app
    assert delete_temp_files
    efs = EFS()
    efs.upload(TEST_FILE, RANDOM_DATA)

    uploaded_content = efs.open(TEST_FILE)
    content = uploaded_content.read()
    assert content == RANDOM_DATA.read()
    uploaded_content.close()


def test_remove_file(app, delete_temp_files):
    """Test remove file."""
    assert app
    assert delete_temp_files

    efs = EFS()
    home_path = current_app.config['LOCAL_STORAGE']
    efs.upload(TEST_FILE, RANDOM_DATA)
    assert os.path.exists(os.path.join(home_path, TEST_FILE))

    efs.remove(TEST_FILE)
    assert not os.path.exists(os.path.join(home_path, TEST_FILE))


def test_remove_folder(app, delete_temp_files):
    """Test remove folder with content."""
    assert app
    assert delete_temp_files

    efs = EFS()
    home_path = current_app.config['LOCAL_STORAGE']
    efs.upload('very/long/path/to/be/created/' + TEST_FILE, RANDOM_DATA)
    assert os.path.exists(os.path.join(home_path, 'very/long/path/to/be/created/', TEST_FILE))

    efs.remove('very')
    assert not os.path.exists(os.path.join(home_path, 'very'))


def test_rename_file(app, delete_temp_files):
    """Test rename file."""
    assert app
    assert delete_temp_files

    efs = EFS()
    home_path = current_app.config['LOCAL_STORAGE']
    efs.upload(TEST_FILE, RANDOM_DATA)
    assert os.path.exists(os.path.join(home_path, TEST_FILE))

    efs.rename(TEST_FILE, 'new_test_file.txt')
    assert not os.path.exists(os.path.join(home_path, TEST_FILE))
    assert os.path.exists(os.path.join(home_path, 'new_test_file.txt'))


def test_move_file(app, delete_temp_files):
    """Test move file to a new folder."""
    assert app
    assert delete_temp_files

    efs = EFS()
    home_path = current_app.config['LOCAL_STORAGE']
    efs.upload(TEST_FILE, RANDOM_DATA)
    assert os.path.exists(os.path.join(home_path, TEST_FILE))

    efs.move(TEST_FILE, 'special_text/test_file.txt')
    assert not os.path.exists(os.path.join(home_path, TEST_FILE))
    assert os.path.exists(os.path.join(home_path, 'special_text/' + TEST_FILE))
