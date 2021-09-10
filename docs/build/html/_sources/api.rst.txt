.. Satyrus documentation master file, created by
   sphinx-quickstart on Wed Feb 24 17:46:52 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python API
**********

How to
======

In order to define new solver interfaces, one may write a Python file (``.py``) with ``SatAPI`` subclasses who implement the ``solve(posiform, **params)`` method.

.. code-block:: python

   # Future Imports (Python < 3.10)
   from __future__ import annotations
   from satyrus import SatAPI, Posiform

   # Your Favourite Solver
   from solvers import BestSolver

   class custom(SatAPI):

       def solve(self, posiform: Posiform, **params: dict) -> object:
           """"""
           model = BestSolver.model(
               expression=str(posiform),
               variables=posiform.variables()
               objective=BestSolver.MINIMIZE
               )

           return model.solve()

The ``params`` keyword argumentss are provided by the command-line ``-p, --params`` option and read from the corresponding JSON file. In the example above, suppose we have some solver interface ``BestSolver`` that takes as input some expression to be optimized, the problem variables list and an objective option either to minimize or maximize the expression's value. Let's say that this code was written to a file called ``customapi.py``.

Running
=======

In order to launch a custom interface, one must provide the subclass definition file as argument for the ``-a, --api`` command-line option, as follows:

.. code-block:: bash

   $ satyrus source.sat --api customapi.py -s custom

This will enable the ``custom`` solver interface to be recognized and used during the solving proccess.







                   


Appendix - Posiform
===================

A *Posiform* is a specific mathematical form given by a polynomial on boolean variables, i.e.

.. math::

   P(x_1, \dots, x_k) = \sum_{i = 1}^{n} c_{i} \prod_{j} x_{j}

where :math:`x_j \in \{0, 1\}` and :math:`c_i \in \mathbb{R}`.

The ``satyrus`` Python module implements the ``Posiform`` type. It does support common arithmetic operations between posiforms and scalars, which is done by regular operator overloading. This type subclasses the built-in ``dict`` type and its keys are hashable sets of strings (built with the built-in ``frozenset`` and ``str`` types).

Its values are given by floating-point (``float``) numbers. It also happens for the key to be ``None`` in order to represent an eventual constant term.

Calling the ``str(...)`` built-in function on a ``Posiform`` instance yields the corresponding energy equation as an arithmetic expression string. Another feature, the ``.variables()`` method call, enables the retriaval of the set of variables. Also, there is the bound method ``.qubo()`` that translates the posiform's contents into a `QUBO <https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization>`_ formulation, applying degree reduction as needed [#]_.

These are the main ways to provide information to your favourite solver.

.. rubric:: Footnotes

.. [#] This is, in fact, in need for further study.