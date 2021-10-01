Examples
********

Problem Modelling
=================

.. include:: ./examples/graph_color.rst

.. include:: ./examples/tsp.rst

.. include:: ./examples/knapsack.rst

Compilation
===========

As the source file is complete, one could simply run

.. code-block:: bash

   $ satyrus graph_color.sat

This will output the ``graph_color.json`` file, with an array object containing in each entry a "term" array of unknowns and its respective multiplicative constant "cons". If there is any constant term, its value for the "term" key will be ``null``.

This is intended to represent the problem's energy equation.

**Note:** It is possible to set the output destination using the ``-o, --ouput`` option, followed by the desired target.

Solver Interface
================

In order to pass the generated energy equation to a solver, it is enough to use the ``-s, --solver`` option.

.. code-block:: bash

   $ satyrus graph_color.sat -s gurobi

The expected behaviour is to store the solution in the ``graph_color.json`` file, under keys "solution" and "energy", being the first a mapping between variables and its values and the latter the total energy for the given setup.

**Note:** Run ``satyrus --help`` for a list of the available solvers in your installation.

Parameters may be passed to the solver using a separate JSON file containing the corresponding mapping. The destination for feeding the parameters file must be provided using the ``-p, --params`` command-line option.

When running the ``dwave`` solver, it is possible to specify both ``num_reads`` and ``num_sweeps`` by providing the ``dwave.json`` file as follows:

.. code-block:: json

   {
      "num_reads": 1000,
      "num_sweeps": 10000
   }

and then, by typing the right command and hitting enter.

.. code-block:: bash

   $ satyrus graph_color.sat -s dwave -p dwave.json

Custom API Setup
================

Defining custom solver interfaces is pretty straightforward. In a separate Python file, import the ``SatAPI`` type from the ``satyrus`` package and subclass it as shown below:

.. code-block:: python

   # Future Imports
   from __future__ import annotations

   # Satyrus Imports
   from satyrus import SatAPI, Posiform

   class MyPartialAPI(SatAPI):

       def solve(self, posiform: Posiform, **params: dict) -> object:
           return "My Solution"

   class MyCompleteAPI(SatAPI):
      
       def solve(self, posiform: Posiform, **params: dict) -> tuple[dict, float]:
           # Completely ignores problem defined by 'posiform'
           # giving always the same solution:
           x = {'x': 0, 'y': 1, 'z': 0}
           e = 2.0
           return (x, e)

Your new class must implement the ``solve`` method, which must have one of the two signatures presented above. It receives a ``Posiform`` object and some eventual keyword arguments. If the return type is a tuple containing a solution mapping and its respective energy, the solution is considered to be *complete*, receiving special formatting when delivered to the output file. Otherwise, a string representation of the output object is dumped to the target destination as-is.

After writing the contents above to the ``myapi.py`` file, it becomes possible to include the custom interface by typing

.. code-block:: bash
   
   $ satyrus graph_color.sat --api myapi.py -s MyCompleteAPI

**Note:** As you might be thinking, it is important to chose the class name wisely!

More about the Python API is found on this `page <./api.html>`_.

..  * :ref:`genindex`
    * :ref:`search`