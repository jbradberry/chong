Chong
=====


Requirements
------------

* Python 3.10+; PyPy; PyPy3


Getting Started
---------------

To set up your local environment you should create a virtualenv and
install everything into it. ::

    $ mkvirtualenv chong

Pip install this repo, either from a local copy, ::

    $ pip install -e chong

or from github, ::

    $ pip install git+https://github.com/jbradberry/chong#egg=chong

and then install the requirements ::

    $ pip install -r requirements_server.txt
    $ pip install -r requirements_player.txt

To run the server with Chong ::

    $ board-serve chong

Optionally, the server ip address and port number can be added ::

    $ board-serve chong 0.0.0.0
    $ board-serve chong 0.0.0.0 8000

To connect a client as a human player ::

    $ board-play chong human
    $ board-play chong human 192.168.1.1 8000   # with ip addr and port

To connect a client using one of the compatible `Monte Carlo Tree
Search AI <https://github.com/jbradberry/mcts>`_ players ::

    $ board-play chong jrb.mcts.uct    # number of wins metric
    $ board-play chong jrb.mcts.uctv   # point value of the board metric
