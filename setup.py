import os
import re
from itertools import chain
from setuptools import setup, find_packages


EXTRAS = {
    'telegram': ['httpx'],
    'dev': ['pytest', 'pylint', 'flake8', 'isort']
}


def read(filename: str):
    """Open file"""
    return open(os.path.join(os.path.dirname(__file__), filename)).read().strip()


def read_version():
    """Read version from __init__.py"""
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(
        os.path.dirname(__file__),
        'easy_notifyer',
        '__init__.py'
    )
    with open(init_py) as file:
        for line in file:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        raise RuntimeError('Cannot find version in easy_notifyer/__init__.py')


setup(
    name='easy_notifyer',
    version=read_version(),
    description='Easy bug reporter for small projects or Sentry on minimums. Async support.',
    author='strpc',
    url='https://github.com/strpc/easy_notifyer',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    download_url='https://pypi.python.org/pypi/easy-notifyer',
    packages=find_packages(include=['easy_notifyer']),
    install_requires=EXTRAS['telegram'],
    extras_require={
        'telegram': EXTRAS['telegram'],
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
