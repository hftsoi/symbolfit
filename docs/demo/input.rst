Input format
============


.. code-block:: python

  x = [1, 4, 9]
  y = [2, 3, 4]
  y_up = [0.5, 1, 1]
  y_down = [0.5, 1, 2]
  bin_widths_1d = [2, 4, 6]

.. image:: ../figures/input1d.png

.. image:: ../figures/input1d_x.png

.. image:: ../figures/input1d_y.png

.. image:: ../figures/input1d_y_up.png

.. image:: ../figures/input1d_y_down.png

.. image:: ../figures/input1d_width.png

.. code-block:: python
  x = np.array([[-1, -1], [-1, 1], [2, -1], [2, 1], [8, -1], [8, 1]])
  # bin content in the same order as x
  y=np.array([1, 2, 3, 4, 5, 6])
  y_up=np.sqrt(y)
  y_down=np.sqrt(y)
  bin_edges_2d = [
  # bin edges for x0, including both the leftmost and rightmost bin edge locations
    [-2, 0, 4, 12],
  # bin edges for x1, including both the leftmost and rightmost bin edge locations
    [-2, 0, 2]
  ]

.. image:: ../figures/input2d.png

.. image:: ../figures/input2d_x.png

.. image:: ../figures/input2d_y.png

.. image:: ../figures/input1d_y_edge.png