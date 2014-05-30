# Quantnode

Quantnode is a framework for building financial trading algorithms.

A trading algorithm generally consists of calculations, assumptions, trading logic and position management.
Quantnode allows you to specify all of these with simple Python code.

The developer experience is similar to any other application - you write and test your
algorithm in your local IDE and push it to the cloud directly from your git repository.

A node is a unit of computational capacity. Nodes execute your algorithm in parallel
and can be scaled up or down instantly on quantnode.com as necessary.


## Installation

Get started by creating an algorithm at quantnode.com first.
When you do a repository will be setup with the templates for building your trading algorithm.

You can then clone that repository, setup a virtual environment and install
the necessary requirements, listed in requirements.txt


Quantnode can be installed in your virtual environment with pip:

    pip install quantnode


## Tutorials

Tutorials to learn Quantnode are available at: http://quantnode.com/tutorials/

## Documentation

Full documentation is available at: http://quantnode.com/docs/

## Debugging your algorithm

You can stream data from Quantnode to your trading algorithm through a test server.

Launch a test server at https://www.quantnode.com/testserver (you'll need to be logged into your Quantnode account)

Run your algorithm using the test server:

    $ ./quantnode-run.py run -t [test-server-hostname]

More details (full tutorial): https://www.quantnode.com/tutorials/testing/

