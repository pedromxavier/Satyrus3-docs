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

Solver Interfaces
=================

Solver interfaces, available via the Satyrus Python API allow the user to interact with the compilation output in many different ways, from straightforward passing it into solver machinery to conversion between output types. In order to pass the generated energy equation to a solver, it is enough to use the ``-s, --solver`` option.

.. code-block:: bash

   $ satyrus source.sat -s solver

The expected behaviour is to store the solution in the ``source.out.json`` file, under keys "solution" and "energy", where the first is a mapping between variables and its values and the latter is the total energy for the given setup.

**Note:** Run ``sat-api`` for a list of the available solvers in your installation.

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

   from satyrus import SatAPI, Posiform
   import random

   class bogo(SatAPI):
      
       def solve(self, energy: Posiform, **params: dict) -> tuple[dict, float]:
           X = energy.variables 
           s = {x: random.randint(0, 1) for x in X}
           e = float(energy(s))
           return (s, e)

Your new class must implement the ``solve`` method, which must have one of the two signatures presented above. It receives a ``Posiform`` object and some eventual parameters as keyword arguments. If the return type is a tuple containing a solution mapping and its respective energy, the solution is considered to be *complete*, receiving special formatting when delivered to the output file. Otherwise, a string representation of the output object is dumped to the target destination as-is.

After writing the contents above to the ``bogoapi.py`` file, it becomes possible to include the custom interface by typing

.. code-block:: bash
   
   $ sat-api add bogoapi.py
   $ satyrus graph_color.sat -s bogo

**Note:** As you might be thinking, it is important to chose the class name wisely!

More in-depth explanation about the Python API is found on `this page <./api.html>`_.

..  * :ref:`genindex`
    * :ref:`search`