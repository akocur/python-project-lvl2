import argparse

from gendiff.formats import get_available_formatters
from gendiff.formats import get_default_format_name
from gendiff.gendiff import generate_diff


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '-f', '--format',
        choices=get_available_formatters(),
        default=get_default_format_name(),
        metavar='FORMAT',
        help='output format (default: "{}"). Available: {}'.format(
            get_default_format_name(), get_available_formatters()
        )
    )
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == '__main__':
    main()
