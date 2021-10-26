.. Satyrus documentation master file, created by
   sphinx-quickstart on Wed Feb 24 17:46:52 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Getting Started
***************

Installation
============
Satyrus requires a 3.7+ CPython (`python.org <https://www.python.org/>`_) distribution. You may install it directly via `pip <https://pypi.org/>`_ or build from source.


pip - Linux, OSx
----------------
.. code-block:: bash
        
    $ python3 -m pip install satyrus[all]

pip - Windows
-------------
.. code-block:: shell

    > pip install satyrus[all]

Building from source
--------------------
.. code-block:: bash

    $ git clone https://github.com/pedromxavier/Satyrus3
    $ cd Satyrus3
    $ pip install .[all]

The ``[all]`` suffix is optional but recommended since it automatically installs the dependencies required for running the available solver interfaces (DWave & Gurobi).

**Note:** Satyrus is still under constant development. If you have already installed, please install using the ``--upgrade`` option.

.. code-block:: bash

   $ pip install .[all] --upgrade

Command line interface
======================

After installation, the ``satyrus`` executable should be available in the command line interface: give it a try!

.. code-block:: shell

    $ satyrus --help
    $ satyrus source.sat

..  * :ref:`genindex`
    * :ref:`search`

Also, consider visiting the `examples page <./examples.html>`_.