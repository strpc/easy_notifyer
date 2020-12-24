import os
from itertools import chain
from setuptools import setup


EXTRAS = {
    'telegram': ['httpx'],
    'dev': ['pytest', 'pylint', 'flake8', 'isort']
}


def read(filename: str):
    """Open file"""
    return open(os.path.join(os.path.dirname(__file__), filename)).read().strip()


setup(
    name='easy_notifyer',
    version='0.0.2',
    description='Easy bug reporter for small projects or Sentry on minimums.',
    author='strpc',
    url='https://github.com/strpc/easy_notifyer',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    download_url='https://pypi.python.org/pypi/easy-notifyer',
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
