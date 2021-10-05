from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Web_check',
    version='v0.5.2',
    packages=find_packages(where='web_check'),
    package_dir={'': 'web_check'},
    url='https://github.com/Jaime-alv',
    license='GPL-3.0-or-later',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jaime Álvarez Fernández',
    author_email='jaime.alv.fdz@gmail.com',
    description='A simple script that will warn you when there are new content in your favourite websites.',
    python_requires=">=3.9"
)
