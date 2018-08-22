import os
import shutil
import tempfile

import boto3
import pytest
from flask import Flask
from moto import mock_s3


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
def bucket(request, app):
    """A fixture to inject a function to create buckets.

    It has to return a function because as pytest setup fixtures before the function is called there is no time to
    mock s3."""
    app.config['AWS_ACCESS_KEY'] = 'access-key'
    app.config['AWS_SECRET_KEY'] = 'secret-key'
    app.config['S3_BUCKET'] = 'bucket'

    mock = mock_s3()
    mock.start()

    def create_connection():
        """Define connection to get the bucket.

        This S3_BUCKET bucket should be pre-created manually before the tests.
        """
        resource = boto3.resource("s3")

        bucket_ = resource.Bucket(app.config["S3_BUCKET"])
        # The virtual bucket needs to be created, see https://github.com/spulec/moto.
        bucket_.create()

        def tear_down():
            """Define the teardown function."""
            for file in bucket_.objects.all():
                file.delete()

            mock.stop()

        request.addfinalizer(tear_down)

        return bucket_

    return create_connection
