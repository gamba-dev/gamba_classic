gamba.data
==========================

.. automodule:: gamba.data
	:members:


**Note**: you may have seen in some of the examples that when using this framework, transactions from individual players are each stored in their own CSV file. Whilst this introduces a (large) overhead on some of the calculation times, it does mean that they can be performed on a typically low memory device like a laptop. If you have the hardware to load large datasets in to memory, not splitting the datasets up like this is recommended!

**Note**: this module may benefit from integrating `parellel processing <https://www.machinelearningplus.com/python/parallel-processing-python/>`_ in some methods.

`notes on reading in large csv files using pandas <https://www.kaggle.com/timetraveller98/testing-pandas-read-csv-performance>`_



**Note**: using `HDF5 file format <https://portal.hdfgroup.org/display/knowledge/What+is+HDF5>`_ may be a good option for larger files eventually.

