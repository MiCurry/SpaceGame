import os
import subprocess
import argparse
from pprint import pprint

BASE_DIRECTORY = 'build'

PRODUCT_NAME = "Space Game"
DESCRIPTION = "Space Game created by Miles A. Curry"
COMPANY_NAME = "Miles A. Curry"

DATA_DIRECTORY_SPEC = "resources=resources"


def get_current_tag_with_rev():
    result = subprocess.run(['git', 'describe', '--tags'], capture_output=True)
    return result.stdout.decode('utf-8').strip()


def get_current_tag_as_string():
    result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], capture_output=True)
    version = result.stdout.decode('utf-8').strip()
    return version


def get_current_tag_as_float():
    result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], capture_output=True)
    version = result.stdout.decode('utf-8').strip()
    version = float(version.removeprefix('v'))
    return version


def construct_filename():
    return f"space.{get_current_tag_with_rev()}.exe"


def get_or_construct_build_directory():
    if not os.path.isdir(BASE_DIRECTORY):
        os.mkdir(BASE_DIRECTORY)

    # The Build version directory i.e. build/v0.2
    ver_dir = os.path.join(BASE_DIRECTORY, get_current_tag_as_string())
    if not os.path.isdir(ver_dir):
        os.mkdir(ver_dir)

    # Now create the revision build directory build/v0.2/rev
    ver_rev_dir = os.path.join(ver_dir, get_current_tag_with_rev())
    if not os.path.isdir(ver_rev_dir):
        os.mkdir(ver_rev_dir)

    return ver_rev_dir


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dryrun',
                    help="Just print the constructed nuitka build command",
                    action='store_true',
                    default=False)

args = parser.parse_args()

nuitka_command = [
    'python3.11.exe', '-m', 'nuitka',
    f'--product-name={PRODUCT_NAME}',
    f'--product-version={get_current_tag_as_float()}',
    f'--include-data-dir={DATA_DIRECTORY_SPEC}',
    f'--file-description={DESCRIPTION}',
    f'--company-name={COMPANY_NAME}',
    f'--output-filename=space.exe',
    f'--output-dir={get_or_construct_build_directory()}',
    '--remove-output',
    './space.py',
    '--standalone',
    '--onefile'
]

print("Nuitka Command to run:")
pprint(nuitka_command)

if not args.dryrun:
    subprocess.run(nuitka_command)
