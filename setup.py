from itertools import chain
from setuptools import setup


EXTRAS = {
    'telegram': ['httpx'],
    'dev': ['pytest', 'pylint', 'flake8', 'isort']
}


setup(
    name='easy_notifyer',
    version='0.0.1',
    description='Easy notifyer from python to your messangers',
    author='strpc',
    url='https://github.com/strpc/easy_notifyer',
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
)
