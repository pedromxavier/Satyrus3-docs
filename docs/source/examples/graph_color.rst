
Graph Coloring
--------------

For a first modelling example we will take a look at some graph coloring in a simple setup with 5 nodes.

.. figure:: /_static/images/graph.svg
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

      (2,3) : 1,
      (2,4) : 1,
      (2,5) : 1,

      (3,4) : 1,
      (3,5) : 1,

      (4,5) : 0
   };

In this case, all array entries are constants. Next, we declare our problem unknowns, the color assignment for each vertex and also the list of used colors.

.. code-block:: satish

   # Correspondence between each vertex and its color
   vc[n][n];

   # Used colors, a quantity we wish to minimize.
   c[n];

Now, we state the constraints that well define the graph coloring problem. First of all, it is fundamental that neighbours :math:`i` and :math:`j` do not share a same color :math:`k`.

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

**Note:** The whole ``graph_color.sat`` file is available for downaload :download:`here </_static/examples/graph_color.sat>`.