import re
import sys
import validators
from os.path import isfile
import requests
import argparse

IMPORT_REGEX = r'(?!.*(/\*|\*/))(.*@import url\((.*)\).*)'


def expand(contents, s_print):
    for line in contents:
        match = re.match(IMPORT_REGEX, str(line))
        if match:
            url = re.sub('[^A-Za-z0-9:/\.\-@=_]+', '', str(match.group(3)))
            if not s_print:
                print(f'following link to {url}')
            tmp = url_open(url)
            contents[contents.index(line)] = expand(tmp, s_print)
    return '\n'.join(contents).strip('"b').strip("'")


def url_open(url):
    return str(requests.get(url,  allow_redirects=True).content).strip().split('\\n')


def file_open(path):
    return open("file_path", "r").read().strip().split('\n')


def check_input(file_path, s_print):
    if validators.url(file_path):
        contents = url_open(file_path)
        c = str(expand(contents, s_print))
        return c
    elif isfile(file_path):
        contents = file_open(file_path)
        c = str(expand(contents, s_print))
        return c
    else:
        print('Not a file or url, please try again')
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='cssxpd',
        description='Will search through a CSS file and recursively download additional CSS imports and write to one file',
    )
    parser.add_argument('-u', '--url', required=False)
    parser.add_argument('-o', '--out-file', required=False)
    parser.add_argument('-s', '--stdout',
                        action='store_true')
    parser.add_argument('-nw', '--no-write',
                        action='store_true')
    args = parser.parse_args()
    if args.no_write and args.out_file:
        print("No write and outfile supplied, exiting....")
        exit(1)

    file_path = ''
    if args.url is None:
        file_path = input('Input a file path or url to the css file: ')
    else:
        file_path = args.url

    s = check_input(file_path, args.stdout)
    if not s:
        exit(1)
    s = s.replace('\\t', '\t')
    s = s.replace('\\n', '\n')
    s = s.replace('\\r', '\r')
    s = s.replace("\\'", "'")
    s = s.replace('\\"', '"')

    f_name = 'out.css' if args.out_file == None else args.out_file
    if not args.no_write:
        open(f_name, 'w').write(s)
    if args.stdout:
        sys.stdout.write(s)
