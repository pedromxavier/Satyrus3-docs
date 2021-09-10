Examples
********

Problem Modelling
=================

For a modelling example we will take a look at a graph colouring in a simple setup with 5 nodes.

.. figure:: ./_static/images/graph.svg
   :alt: A graph with 5 nodes
   :width: 100%

To represent this graph in SATish we write an array declaration foolowed by its structure initialization.

.. code-block:: satish

   # Number of verties in the graph.
   n = 5;

   # Graph representation
   neigh[n][n] = {
      (1,1) : 0,
      (1,2) : 0,
      (1,3) : 1,
      (1,4) : 1,
      (1,5) : 1,

      (2,1) : 0,
      (2,2) : 0,
      (2,3) : 1,
      (2,4) : 1,
      (2,5) : 1,

      (3,1) : 1,
      (3,2) : 1,
      (3,3) : 0,
      (3,4) : 1,
      (3,5) : 1,

      (4,1) : 1,
      (4,2) : 1,
      (4,3) : 1,
      (4,4) : 0,
      (4,5) : 0,

      (5,1) : 1,
      (5,2) : 1,
      (5,3) : 1,
      (5,4) : 0,
      (5,5) : 0
   };

In this case, all array entries are constants. Next, we declare our problem unknowns, the color assignment for each vertex and also the list of used colors.

.. code-block:: satish

   # Correspondence between each vertex and its color
   vc[n][n];

   # Used colors, a quantity we wish to minimize.
   c[n];

Now, we state the constraints that well define the graph colouring problem. First of all, it is fundamental that neighbours :math:`i` and :math:`j` do not share a same color :math:`k`.

.. code-block:: satish

   (int) neighbour_coloring[2]:
       forall{i = [1:n]}
       forall{j = [1:n], j > i}
       forall{k = [1:n]}
       neigh[i][j] -> ~(vc[i][k] & vc[j][k]);

It is also important to keep track of the colors being used, that is, for each vertex :math:`i` dyed with a color :math:`k` we say that :math:`k` is used.

That yields the logical expression :math:`\forall i \,\, \forall k \,\, vc_{i, k} \implies c_{k}`.

.. code-block:: satish

   (int) use_color[1]:
       forall{i = [1:n]}
       forall{k = [1:n]}
       vc[i][k] -> c[k];

Following, we say that to every vertex must be assigned a unique color, where we may use the ``unique`` quantifier keyword i.e. there exists exactly one color :math:`k` related to vertex :math:`i`.

.. code-block:: satish

   (int) color_all[1]:
       forall{i = [1:n]}
       unique{k = [1:n]}
       vc[i][k];

Last but not least, we define our optimality constraint, where we state that every color used increases the overall cost.

.. code-block:: satish

   (opt) cost: exists{k = [1:n]} c[k];

**Note:** The whole ``graph_color.sat`` file is available for downaload :download:`here <./_static/examples/graph_color.sat>`.

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

   from satyrus import SatAPI, Posiform

   class MyPartialAPI(SatAPI):

       def solve(self, posiform: Posiform, **params: dict) -> object:
           return "My Solution"

   class MyCompleteAPI(SatAPI):
      
       def solve(self, posiform: Posiform, **params: dict) -> tuple[dict, float]:
           x = {'x': 0, 'y': 1, 'z': 0}
           e = 2.0
           return (x, e)

Your new class must implement the ``solve`` method, which must have one of the two signatures presented above. It receives a ``Posiform`` object and some eventual keyword arguments. If the return type is a tuple containing a solution mapping and its respective energy, the solution is considered to be *complete*, receiving special formatting when delivered to the output file. Otherwise, a string representation of the output object is dumped to the target destination as-is.

After writing the contents above to the ``myapi.py`` file, it becomes possible to include the custom interface by typing

.. code-block:: bash
   
   $ satyrus graph_color.sat --api myapi.py -s MyCompleteAPI

**Note:** As you might be thinking, it is important to chose the class name wisely!

..  * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`