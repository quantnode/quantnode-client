try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.1.1'

install_requires = [
    'requests >= 0.8.8',
    'Pyro4 >= 4.25',
    'serpent >= 1.5',
    'slumber >= 0.6.0',
    'python-dateutil >= 2.1',
    'argparse >= 1.1'
]

long_description = ''
with open('description.txt', 'rb') as f:
    long_description = f.read()

setup(
    name='quantnode',
    version=VERSION,
    description='Quantnode framework for building financial trading algorithms',
    long_description=long_description,
    author='Quantnode',
    author_email='hello@quantnode.com',
    url='https://www.quantnode.com/',
    packages=['quantnode'],
    package_data={'quantnode': ['../VERSION', '../description.txt']},
    install_requires=install_requires,
    scripts=['quantnode/bin/quantnode-run.py'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
