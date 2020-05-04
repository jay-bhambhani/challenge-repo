import io
import boto3
import pytest
from testcontainers.compose import DockerCompose

from src.s3_stats import get_s3_stats
from src.abstractions.display_converter import DisplayConverter


def get_test_s3(compose):
    host = compose.get_service_host("minio1", 9000)
    port = compose.get_service_port("minio1", 9000)
    endpoint_url = "http://{}:{}".format(host, port)
    return boto3.resource('s3', endpoint_url=endpoint_url, aws_access_key_id='minio', aws_secret_access_key='minio123')

def file_with_size(byte_size):
    f = io.BytesIO()
    f.write(b'\0'*byte_size)
    f.seek(0)
    return f

@pytest.fixture(scope="session")
def test_s3():
    """Ensure that HTTP service is up and responsive."""
    compose = DockerCompose('tests')
    with compose:
        s3 = get_test_s3(compose)
        s3.Bucket('test1').create()
        s3.Bucket('test2').create()
        s3.Object('test1','test1key').upload_fileobj(file_with_size(1024*1024*10))
        s3.Object('test2', 'test2key').upload_fileobj(file_with_size(1024 * 1024))
        s3.Object('test2', 'test2key2').upload_fileobj(file_with_size(1024 * 1024*2))
        yield compose


def test_get_s3_stats(test_s3):
    s3_stats = get_s3_stats(get_test_s3(test_s3))
    test1, test2 = s3_stats[0], s3_stats[1]
    converter = DisplayConverter('Mi')
    assert test1.last_modified > test1.creation_date
    assert test2.last_modified > test2.creation_date
    assert converter.convert(test1.total_file_size) == 10.0
    assert converter.convert(test2.total_file_size) == 3.0
    assert test1.number_of_files == 1
    assert test2.number_of_files == 2