import pytest
from gendiff.gendiff import generate_diff


@pytest.fixture
def file_path1():
    return 'file1.json'


@pytest.fixture
def file_path2():
    return 'file2.json'


def test_generate_diff():
    expected = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    assert generate_diff(file_path1, file_path2) == expected
