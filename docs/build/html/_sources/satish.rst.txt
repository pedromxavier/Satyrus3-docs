.. Satyrus documentation master file, created by
   sphinx-quickstart on Wed Feb 24 17:46:52 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SATish Language
***************

Syntax
======

SATish syntax follows most of the design patterns found in mainstream programming languages such as C/C++, Fortran and Python and should be of easy understanding for the begginer programmer.

Directives and Comments
-----------------------

Comments are either single-line (found after the comment mark ``#``) or multi-line, embraced by a ``#{``, ``}#`` pair.

.. code-block:: satish

   # Some inline comment

   #{ open ------------- 
      Now some multiline
      stuff: Let's write
      some more...
      ------------ close }#

   ?alpha: 1.0;
   ?epsilon: 1E-5; # Defines tiebreak factor

Directives are ``?<key>: <value>;`` statements used to configure special compiler environment variables. The main two are ``?alpha`` and ``?epsilon``, namely the base penalty level :math:`\alpha` and the tiebreaker factor :math:`\epsilon`.

Assignment
----------
Assingning variables may refer to two types:
   1. Constants (number)
   2. Arrays (numbers and variables)

Constants will simply store a number under some variable's name. Array definition is a little bit trickier, as there will be both *implicit* and *explicit* entries. First of all, one must specify the array's dimensions between square brackets, as in C's static memory allocation. Initializing its entries is done simultaneously, by specifying its pairs of indices and values.

.. code-block:: satish

   # constant definition
   n = 3;

   x[n][n] = { 
       (1, 1): 1, # sets first element to 1
       (n, n): 0  # sets last element to 0
   }; 

   y[n]; # Unknown-only array

Unespecified array entries will be treated as the problem's unknowns. If our structure contains only unknowns, no initializing syntax is needed.

**Note:** Even if we want a single unknown to be used in our entire problem, we must do so by declaring a 1-dimensional, single-component array.

Constraints
-----------

There are two types of constraints: integrity (``int``) and optimality (``opt``). Integrity constraints must belong to some penalty level, given by a number between brackets after the constraint name. Constraint definition is then followed by a quantifier section, where the ``forall``, ``exists`` and ``unique`` keywords may be used before the variable range specification, as in ``<quantifier>{<var> = [<start>:<stop>]}``. An additional ``step`` parameter (which defaults to 1) can be used, as in ``[<start>:<stop>:<step>]``. Also, conditions may be provided after range specification, by inserting comma-separated expressions before the closing curly bracket.

.. code-block:: satish
   
   (int) int_const[1]:
      forall{i = [1:n]}
      exists{j = [1:n], i!=j}
      ~(x[i] -> y[j]);
	
   (opt) opt_const:
      exists{i = [1:n]} x[i];

Definition is ended with the logical expression itself, followed by a semicolon.

Legacy Syntax
=============
One might want to use the older SATish syntax, present in the previous versions of the compiler (``<3.0``) . This can be achieved by providing the ``--legacy`` option through the command line interface.

.. code-block:: shell

   $ satyrus oldsource.sat --legacy
	
..  * :ref:`genindex`
    * :ref:`search`