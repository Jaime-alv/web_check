from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Web_check',
    version='v1.0.0',
    packages=['web_check', 'image'],
    data_files=[('image', ['image/logo.png'])],
    package_data={'': ['requirements.txt']},
    install_requires=['requests', 'beautifulsoup4', 'tkScrolledFrame', 'Pillow'],
    url='https://github.com/Jaime-alv/web_check.git',
    license='GPL-3.0-or-later',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jaime Álvarez Fernández',
    author_email='jaime.alv.fdz@gmail.com',
    description='A simple script that will warn you when there are new content in your favourite websites.',
    python_requires=">=3.9"
)
