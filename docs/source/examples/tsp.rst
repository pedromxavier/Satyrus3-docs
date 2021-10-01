Travelling Salesman Problem
---------------------------

One more graph-oriented example will be a Travelling Salesman Problem (TSP) instance with 4 cities.

.. figure:: /_static/images/tsp.svg
   :alt: A graph with 5 nodes
   :width: 100%

We start by representing our graph structure. As the starting position doesn't matter f
or the problem formulation, we duplicate the *first town*, thus creating a *ghost town*, intended to be the last on the tour. The *ghost town* has the same connections as its twin and the distance between this two is zero, as is the distance between any node to itself.

.. code-block:: satish

   n=5;

   dist[n][n] = {
      (1,1): 0,
      (1,2): 4,
      (1,3): 4,
      (1,4): 9,
      (1,5): 0,

      (2,1): 4,
      (2,2): 0,
      (2,3): 9,
      (2,4): 4,
      (2,5): 4,

      (3,1): 4,
      (3,2): 9,
      (3,3): 0,
      (3,4): 4,
      (3,5): 4,

      (4,1): 9,
      (4,2): 4,
      (4,3): 4,
      (4,4): 0,
      (4,5): 9,

      (5,1): 0,
      (5,2): 4,
      (5,3): 4,
      (5,4): 9,
      (5,5): 0
   };

   tour[n][n]; # (town, tour position) pairs

We defined also a ``tour`` structure, which assigns every town a position on the tour. Also, it is important to clamp the mirrored towns to the tour's endpoints.

.. code-block:: satish

   # Low Penalty Level
   LOW = 1;

   # Fix both endpoints (the first town and its ghost town)
   (int) mirror_town[LOW]: tour[1][1] and tour[n][n];

Another option would be to define these boudaries directyle into the ``tour`` declaration.

.. code-block:: satish
    
    tour[n][n] = {
        (1, 1): 1,
        (n, n): 1
    };

All other entries are left as variables.

The sole integrity constraint to be guaranteed is that every town occupies a single position on the tour. Conversely, every turn must be assigned to a single town.

.. code-block:: satish

   (int) visit_all_once[LOW]: 
      # Every city 'i' appears uniquely across the tour.
      forall{i = [1:n]} 
      unique{j = [1:n]}
      tour[i][j];

   (int) fill_all_once[LOW]: 
      # Every tour position 'i' has exactly one city 'j' associated to it.
      unique{i = [1:n]}
      forall{j = [1:n]}
      tour[i][j];

The optimality constraints are built upon accounting for the costs that lie between nodes who are neighbours on the tour. This must be done twice in order to handle assymetrical setups.

.. code-block:: satish

   (opt) backwards_cost:
       exists{i = [1:n]} # for each city 'i'
       exists{j = [1:n], i != j} # for each other city 'j'
       exists{k = [2:n]} # for each position
       (tour[i][k] and tour[j][k-1]) * dist[i][j];

   (opt) forwards_cost:
       exists{i = [1:n]} # for each city 'i'
       exists{j = [1:n], i != j} # for each other city 'j'
       exists{k = [1:n-1]} # for each position
       (tour[i][k] and tour[j][k+1]) * dist[i][j];

**Note:** The whole ``tsp.sat`` file is available for downaload :download:`here </_static/examples/tsp.sat>`.