import pytest
from gendiff.gendiff import generate_diff


@pytest.fixture
def file1():
    return {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": false
    }


@pytest.fixture
def file2():
    return {
        "timeout": 20,
        "verbose": true,
        "host": "hexlet.io"
    }


def test_generate_diff():
    expected = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    assert generate_diff(file1, file2) == expected
