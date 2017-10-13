import os
import shutil
import tempfile

import boto
import pytest
from flask import Flask


@pytest.yield_fixture(scope='function')
def app():
    """App fixture."""
    app_ = Flask(__name__)
    app_.config['STORAGE'] = 's3'

    context = app_.app_context()
    context.push()

    yield app_
    context.pop()


@pytest.fixture(scope='function')
def delete_temp_files(app, request):
    """Remove files created by filesystem tests."""
    app.config['LOCAL_STORAGE'] = tempfile.mkdtemp()

    def teardown():
        """Define the teardown function."""
        home_path = app.config['LOCAL_STORAGE']
        if os.path.exists(home_path):
            shutil.rmtree(home_path)
    request.addfinalizer(teardown)
    return True


@pytest.fixture(scope='function')
def bucket(app):
    """A fixture to inject a function to create buckets.

    It has to return a function because as pytest setup fixtures before the function is called there is no time to
    mock s3."""
    app.config['AWS_ACCESS_KEY'] = 'access-key'
    app.config['AWS_SECRET_KEY'] = 'secret-key'
    app.config['S3_BUCKET'] = 'bucket'

    def create_connection():
        """Define connection to get the bucket.

        This S3_BUCKET bucket should be pre-created manually before the tests.
        """
        conn = boto.connect_s3(app.config['AWS_ACCESS_KEY'], app.config['AWS_SECRET_KEY'])

        # The virtual bucket needs to be created, see https://github.com/spulec/moto.
        conn.create_bucket(app.config['S3_BUCKET'])

        bucket_ = conn.get_bucket(app.config['S3_BUCKET'])

        return bucket_

    return create_connection
