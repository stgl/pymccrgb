.. pymccrgb documentation master file, created by
   sphinx-quickstart on Thu Jun 13 15:05:37 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pymccrgb: Classifying point clouds with color features
======================================================

pymccrgb is a Python package for curvature- and color-based point classification. 
It provides Python interfaces to the multiscale curvature classification algorithm 
(MCC; Evans and Hudak, 2007) and a supervised extension to MCC, MCC-RGB, 
that uses point colors. It supports lidar data, photogrammetric point clouds, 
or other 3D point data in text (CSV) and LAS/LAZ formats.

.. toctree::
   :maxdepth: 1 
   :caption: Getting started

    installation
    quickstart

.. toctree::
   :maxdepth: 1 
   :caption: Example notebooks

   examples/mcc-rgb.ipynb

.. toctree::
   :maxdepth: 1 
   :caption: API documentation

   pymccrgb 
