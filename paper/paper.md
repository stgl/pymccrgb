---
title: 'pymccrgb: Color- and curvature-based classification of multispectral point clouds in Python'
tags:
  - Python
  - point classification
  - lidar data
  - photogrammetric data
  - geomorphology
  - ecology
authors:
  - name: Robert Sare
    orcid: 0000-0003-3711-6771
    affiliation: 1
  - name: George E. Hilley
    orcid: 0000-0002-1761-7547
    affiliation: 1
affiliations:
  - name: Department of Geological Sciences, Stanford University
    index: 1          
date: 
bibliography: paper.bib
---

# Summary

Digital elevation data are used extensively in the geophysical
sciences, including conventional light detection and ranging (lidar) point
clouds and very high density photogrammetric datasets produced from
drone surveys or stereo imagery. Classifying ground and vegetation
points is an important step in topographic data analysis in geomorphology and
environmental science, especially as many datasets increasingly image vegetation and other subtle features in fine detail. `pymccrgb` is a package for classification of point cloud data with point colors or other multispectral information, providing a simple interface for point classification to scientific Python users.

This package offers Earth scientists studying surface processes or hazards an efficient
method for extracting ground points from unclassified point clouds, and
may also be useful for detailed vegetation height measurements in forestry or
rangeland ecology. The method’s implementation uses Numpy, scikit-learn, and
PDAL and it is intended to be easy to extend to other supervised classification
methods or point classes [@pdal2018,@pedregosa2011,@vanderwalt2011]. It also
includes a preprocessing tool to project point colors from overhead imagery
onto a georeferenced point cloud using PDAL (e.g., colorizing single-channel lidar data with aerial imagery).

The core functionality builds on a popular open source algorithm, multiscale curvature
classification (MCC) [@evans2007], by training a support vector machine
classifier using color features of vegetation points and updating ground
classified points according to color similarity. This new two-stage algorithm,
MCC-RGB, requires fewer iterations than the MCC method and removes low vegetation points in settings that can challenge MCC. Users can choose to re-classify ground points in a single step or at user defined height ranges representing multiple vegetation classes. The package provides a command line interface and Python API to both algorithms.

# Acknowledgements

Example data in this package was collected by the National Center for
Airborne Laser Mapping and hosted by by the OpenTopography facility with
support from the National Science Foundation under NSF award numbers
1557484, 1557319, and 1557330.

# References


