# pymccrgb

[![Build Status](https://travis-ci.com/rmsare/pymccrgb.svg?branch=master)](https://travis-ci.com/rmsare/pymccrgb)
[![Documentation Status](https://readthedocs.org/projects/pymccrgb/badge/?version=latest)](https://pymccrgb.readthedocs.io/en/latest/?badge=latest)

**pymccrgb** is a Python utility for multiscale curvature classification of
point clouds with color features. It extends a popular classification method
([MCC lidar](https://sourceforge.net/p/mcclidar/wiki/Home/)) [[0]](#references) to point cloud datasets with multiple color channels,
commonly produced in drone surveys. It can be used to extract points from the
ground surface and vegetation in photogrammetric data for which multiple laser
returns are not available.

It is intended for scientists in geomorphology, forest ecology, or planetary science
who wish to classify points in datasets from structure from motion,
stereo photogrammetry, or multi-spectral lidar.

## Getting started

### Installation

It is best to [use a virtual environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) to install this package:

```bash
git clone https://github.com/rmsare/pymccrgb
cd pymccrgb
conda create -n pymcc -f environment.yml
conda activate pymcc
```

## Examples

### Microtopography under tree cover

### Removing bushes from a UAV-SFM survey of an earthquake fault scarp

### Rangeland vegetation height

## Documentation

Read the documentation for example use cases, an API reference, and more. They
are hosted at [pymccrgb.readthedocs.io](https://pymccrgb.readthedocs.io).

## Contributing

### Bug reports

Bug reports are much appreciated. Please [open an issue](https://github.com/rmsare/pymccrgb/issues/new) with the `bug` label,
and provide a minimal example illustrating the problem.

### Suggestions

Feel free to [suggest new features](https://github.com/rmsare/pymccrgb/issues/new) in an issue with the `new-feature` label.

### Pull requests

If you would like to add a feature or fix a bug, please fork the repository, create a feature branch, and [submit a PR](https://github.com/rmsare/pymccrgb/compare) and reference any relevant issues. There are nice guides to contributing with GitHub [here](https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/) and [here](https://yourfirstpr.github.io/). Please include tests where appropriate and check that the test suite passes (a Travis build or `pytest pymccrgb/tests`) before submitting.


### Support and questions

Please [open an issue](https://github.com/rmsare/pymccrgb/issues/new) with your question.

## References
[0] Evans, J. S., & Hudak, A. T. 2007. A multiscale curvature algorithm for classifying discrete return LiDAR in forested environments. IEEE Transactions on Geoscience and Remote Sensing, 45(4), 1029-1038. 

[1] 

[2] 

## License
This work is licensed under the MIT License (see [LICENSE](LICENSE)).

