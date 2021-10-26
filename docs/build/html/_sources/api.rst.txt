Python API
**********

The Satyrus API, available through the ``sat-api`` command-line tool, provides the main way to manage solver interfaces. It may be used for querying available solver options, adding, updating and removing interfaces.

Since version 3.0.7, Satyrus offers a few built-in solver and output options:
   - Gurobi®
   - D-Wave® Neal
   - CSV
   - QUBO

A few more are scheduled to be included in the next releases, namely 3.1.0 and 3.0.8:
   - FICO® XPRESS
   - GNU GLPK

How to
======

In order to define new solver interfaces, one may write a Python file (``.py``) with a ``SatAPI`` subclass implementing the ``solve(energy, **params)`` method.

.. code-block:: python

   from satyrus import SatAPI, Posiform

   # Your Favourite Solver
   from solvers import BestSolver

   class custom(SatAPI):

       def solve(self, energy: Posiform, **params: dict):
           """"""
           model = BestSolver.model(
               expression=str(energy),
               variables=energy.variables,
               objective=BestSolver.MINIMIZE
               )

           return model.solve()

In the example above, suppose we have some solver interface ``BestSolver`` that takes as input some expression to be optimized, the problem variables list and an objective option either to minimize or maximize the expression's value. The ``params`` keyword argumentss are provided by the command-line ``-p, --params`` option and read from the corresponding JSON file.

Let's say that the code above was written to a file called ``customapi.py``.

Running
=======

In order to launch a custom interface, one must provide the subclass definition file as argument for the ``sat-api add`` command, as follows:

.. code-block:: bash

   $ sat-api add ./customapi.py

This will enable the ``custom`` solver interface to be recognized and used during the output phase of the compilation.

.. code-block:: bash

   $ satyrus ./source.sat -s custom

Other Examples
==============

For a more practical example, onde could install the FICO® XPRESS Python module via pip

.. code-block:: bash

   $ pip install xpress

and write the following definition to the ``xpressapi.py`` file:

.. code-block:: python

   from satyrus import SatAPI, Posiform

   import xpress as xp
   import numpy as np

   class xpress(SatAPI):

       def solve(self, energy: Posiform, **params) -> tuple[dict, float]:
           x, Q, c = energy.qubo()

           V = np.array([xp.var(vartype=xp.binary, name=v) for v in x])

           P = xp.problem(*V, V @ Q @ V)
           P.solve()

           s = {v: int(P.getSolution(V[x[v]])) for v in x}
           e = P.getObjVal()

           return (s, e + c)

After running ``$ sat-api add ./xpressapi.py``, the new API will be automatically enabled for running problems. This file is available :download:`here </_static/examples/xpressapi.py>`.

Another suggestion is for you to write a custom solver. A brute-force sampler seems like a reasonable toy and will be presented below:

.. code-block:: python

   from satyrus import SatAPI, Posiform

   import itertools as it
   import numpy as np

   class brutus(SatAPI):
       """"""
       
       def solve(self, energy: Posiform, **params):
           """"""
           x = energy.variables
   
           E = None
           S = None
   
           n = len(x)

           for s in self.states(n):
               e = float(energy({x[i]: s[i] for i in range(n)}))
               if E is None or e < E:
                   E = e
                   S = s
           
           return ({x[i]: int(S[i]) for i in range(n)}, E)
   
       @staticmethod
       def states(n: int) -> np.ndarray:
           """\
           Generates all possible $2^{n}$ binary states
   
           Parameters
           ----------
           n: int
   
           Yields
           ------
           np.ndarray[float]
           """
           for s in it.product(*((1, 0) for _ in range(n))):
               yield np.array(s, dtype=float)
                   
Here, instead of using the ``.qubo()`` or the ``.ising()`` utilities we simply evaluate our posiform at a given point.

As always, this file is available :download:`here </_static/examples/brutus.py>` 

Appendix - Posiform
===================

A *Posiform*, as it is called in the context of pseudo-boolean optimization [#]_, is a specific mathematical form given by a real polynomial on boolean variables, i.e.

.. math::

   P(x) = \sum_{\omega \subseteq [n]} c_{\omega} \prod_{k \in \omega} x_{k}

where :math:`P: \mathbb{B}^{n} \to \mathbb{R}`, :math:`x_j \in \mathbb{B}` and :math:`c_{\omega} \in \mathbb{R}`.

The ``satyrus`` Python module implements the ``Posiform`` type. It does support common arithmetic operations between posiforms and scalars, which is done by regular operator overloading. This type subclasses the built-in ``dict`` type and its keys are hashable sets of strings (made with the built-in ``frozenset`` and ``str`` types).

Its values are given by floating-point (``float``) numbers. It also happens for the key to be ``None`` in order to represent an eventual constant term.

Calling the ``str(...)`` built-in function on a ``Posiform`` instance yields the corresponding energy equation as an arithmetic expression string. Another feature, the ``.variables`` property, enables the retriaval of the set of variables as an lexically ordered list. Also, there are the ``.qubo()`` and ``.ising()`` bound methods, that translates the posiform's contents into a `QUBO <https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization>`_ or `Ising Model <https://en.wikipedia.org/wiki/Ising_model>`_ formulation, attained by applying degree reduction as needed.

These are the main ways to provide information to your favourite solver.

.. rubric:: References

.. [#] E. Boros, P. L. Hammer, *Pseudo-Boolean optimization*, 2002.