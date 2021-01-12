import os
import re
from itertools import chain
from setuptools import setup, find_packages


NAME_PACKAGE = 'easy_notifyer'
DESCRIPTION = 'Easy bug reporter for small projects. ' \
              'Zero dependencies - download and run. Asyncio support.'
EXTRAS = {
    'dev': [
        'pytest',
        'pytest-mock',
        'pytest-asyncio',
        'pylint',
        'flake8',
        'isort',
        'bumpversion',
    ]
}


def read(filename: str):
    """Open file"""
    return open(os.path.join(os.path.dirname(__file__), filename)).read().strip()


def read_version() -> str:
    """Read version from __init__.py"""
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(
        os.path.dirname(__file__),
        NAME_PACKAGE,
        '__init__.py'
    )
    with open(init_py) as file:
        for line in file:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        raise RuntimeError(f'Cannot find version in {NAME_PACKAGE}/__init__.py')


setup(
    name=NAME_PACKAGE,
    version=read_version(),
    description=DESCRIPTION,
    author='strpc',
    url='https://github.com/strpc/easy_notifyer',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    download_url='https://pypi.python.org/pypi/easy-notifyer',
    packages=find_packages(include=[NAME_PACKAGE]),
    extras_require={
        'dev': EXTRAS['dev'],
        'all': list(chain.from_iterable(EXTRAS.values())),
    },
    python_requires='>=3.7, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    keywords=['easy-notifyer', 'telegram', 'mailer', 'mail-client'],
)
