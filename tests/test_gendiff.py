from gendiff.gendiff import generate_diff


def test_generate_diff():
    expected = """{
  - follow: false
    host: hexlet.io
  + none: null
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    file_path1 = 'tests/fixtures/file1.json'
    file_path2 = 'tests/fixtures/file2.json'
    assert generate_diff(file_path1, file_path2) == expected

    file_path1 = 'tests/fixtures/file1.yaml'
    file_path2 = 'tests/fixtures/file2.yaml'
    assert generate_diff(file_path1, file_path2) == expected
