.. pymccrgb documentation master file, created by
   sphinx-quickstart on Thu Jun 13 15:05:37 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pymccrgb: Classifying point clouds with color attributes 
========================================================

``pymccrgb`` is a Python package for curvature- and color-based point classification. 

It provides Python interfaces to the multiscale curvature classification algorithm 
(MCC; `Evans and Hudak, 2007 <https://sourceforge.net/p/mcclidar/wiki/Home/>`_) and a supervised extension to MCC, MCC-RGB, that uses point colors. It supports lidar data, photogrammetric point clouds, or other 3D point data in text (CSV) and LAS/LAZ formats.

Evans, J. S., & Hudak, A. T. 2007. A multiscale curvature algorithm for classifying discrete return LiDAR in forested environments. IEEE Transactions on Geoscience and Remote Sensing, 45(4), 1029-1038 `doi <https://doi.org/10.1109/TGRS.2006.890412>`_

.. toctree::
   :maxdepth: 1 
   :caption: Getting started

   installation
   quickstart

.. toctree::
   :maxdepth: 1 
   :caption: Examples 

   examples/mcc-rgb.ipynb
   examples/parameter-selection.ipynb

.. toctree::
   :maxdepth: 3 
   :caption: API reference 

   pymccrgb 
