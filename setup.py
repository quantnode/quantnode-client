from distutils.core import setup

VERSION = '0.1.0'

install_requires = [
    'requests >= 0.8.8',
    'Pyro4 >= 4.25',
    'slumber >= 0.6.0',
    'python-dateutil >= 2.1'
]

setup(
    name='quantnode',
    version=VERSION,
    description='Quantnode client framework',
    author='Quantnode',
    author_email='hello@quantnode.com',
    url='https://www.quantnode.com/',
    packages=['quantnode'],
    package_data={'quantnode': ['../VERSION']},
    install_requires=install_requires,
    scripts=['bin/quantnode-run.py'],
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
