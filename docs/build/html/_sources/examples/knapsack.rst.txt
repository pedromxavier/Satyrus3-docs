Knapsack
--------

The Knapsack Problem involves some extra tricks when written in SATish. Its usual formulation is indeed very straightforward and is usually referred to as one of the first steps in the combinatorial optimization kindergarten.

Take :math:`n` items, where each one has an associated weight :math:`w_{i}` and value :math:`v_{i}`. One wants to maximize the total carried value without surpassing the knapsack's capacity :math:`M`.

.. math::
   :nowrap:

   \begin{array}{c c}
   ~ & \displaystyle \max \sum_{i = 1}^{n} x_{i}\, v_{i}\\
   \text{s.t.} & \displaystyle \sum_{i = 1}^{n} x_{i}\, w_{i} \le M
   \end{array}

Let's suppose we have three items with the following weights and values to fit in a knapsack with size :math:`M = 4`.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - :math:`w_{i}`
     - :math:`v_{i}`
   * - :math:`1`
     - :math:`4`
   * - :math:`4`
     - :math:`6`
   * - :math:`3`
     - :math:`3`

.. code-block:: satish

    n = 3;

    x[n];
    w[n] = {(1) : 1, (2) : 4, (3) : 3};
    v[n] = {(1) : 4, (2) : 6, (3) : 3};

    M = 4;

To achieve the declaration of the viability constraint in our framework it is necessary to transform inequalities into equality relations. We can do that by introducing a few auxiliary variables. We write

.. math::
   :nowrap:

   \begin{align*}
   \sum_{i = 1}^{n} x_{i}\,w_{i} + s = M
   \end{align*}

where :math:`0 \lt s \le M` is represented through its binary expansion

.. math::
   :nowrap:

   \begin{align*}
   s = \sum_{j = 1}^{m} 2^{j-1}\, s_{j}
   \end{align*}

that is, :math:`m = \log_{2} M` and :math:`s_{j} \in \mathbb{B}^{m}`.

That said, the problem can be stated as

.. math::
   :nowrap:
   
   \begin{align*}
   \min -\sum_{i=1}^{n} x_{i}\, v_{i} + \lambda \left({ \sum_{i=1}^{n} x_{i}\, w_{i} + \sum_{j=1}^{m} 2^{j-1}\, s_{j} - M }\right)^{2}
   \end{align*}

for some penalty :math:`\lambda` which might be left for Satyrus to compute.

.. code-block:: satish

   n = 3;

   x[n];

   w[n] = {
       (1) : 1,
       (2) : 4,
       (3) : 3
   };

   v[n] = {
       (1) : 4,
       (2) : 6,
       (3) : 3
   };

   s[2];

   # Capacity
   M = 4;

   # Penalty Levels
   LOW = 1;

   (opt) eita[LOW]: (x[1] * w[1] + x[2] * w[2] + x[3] * w[3] + (s[1] + 2 * s[2]) - M) ** 2.0;

   (opt) cost: sum{i = [1:n]} -v[i] * x[i];

**Note**: As of version 3.0.7, there is no available syntax for writing the general form of this problem as is in SATish, due to the lack of inner loops. This feature is scheduled to be present on the first release of the 3.1.x series. A future version will allow one to write the constraints from the code above as

.. code-block:: satish

   # Capacity
   M = 4;

   # Log_2 M
   m = 2;

   s[m];

   # Penalty Levels
   LOW = 1;

   (opt) eita[LOW]: ((sum{i=[1:n} x[i] * w[i]) + (sum{j=[1:m]} 2**(j-1) * s[j]) - M) ** 2.0;

   (opt) cost: sum{i = [1:n]} -v[i] * x[i];