import subprocess
import argparse


def get_current_version():
    subprocess.run(["git", ])
    version = 0.0
    return version

def get_current_revision():
    revision = 00000
    return revision

def construct_file_name(version, revision):
    if revision:
        filename = f"space.{version}.{revision}.exe"

directory = './build'
filaneme = 'space.exe'

subprocess.run(['python3.11.exe', '-m', 'nuitka',
                '--product-name="Space Game"',
                '--product-version=0.2',
                './space.py',
                '--standalone',
                '--include-data-dir=E:/Projects/SpaceGame/resources=resources'
                ])