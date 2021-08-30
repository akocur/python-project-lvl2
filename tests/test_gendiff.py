from gendiff.gendiff import generate_diff


def test_generate_diff():
    expected = open('tests/fixtures/diff').read()
    file_path1 = 'tests/fixtures/file1.json'
    file_path2 = 'tests/fixtures/file2.json'
    assert generate_diff(file_path1, file_path2) == expected

    file_path1 = 'tests/fixtures/file1.yaml'
    file_path2 = 'tests/fixtures/file2.yaml'
    assert generate_diff(file_path1, file_path2) == expected

    file_path1 = 'tests/fixtures/file1.yaml'
    file_path2 = 'tests/fixtures/file2.yaml'
    expected = open('tests/fixtures/diff_plain')
    assert generate_diff(file_path1, file_path2, 'plain') == expected
