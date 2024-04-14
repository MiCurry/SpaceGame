import subprocess

subprocess.run(['python3.11.exe', '-m', 'nuitka',
                '--product-name="Space Game"',
                '--product-version=0.2',
                './space.py',
                '--onefile',
                '--include-data-dir=E:/Projects/SpaceGame/resources=resources'
                ])