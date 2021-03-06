Installation
============

``pymccrgb`` is hosted on GitHub and PyPI. It requires LibLAS, Boost, and CMake and common Python packages like sklearn, skimage, and numpy.

LibLAS must be installed first:

.. code-block:: bash

    sudo apt-get install liblas-c-dev
    
Then create a new virtual environment and install the package:

.. code-block:: bash

    git clone https://github.com/rmsare/pymccrgb
    cd pymccrgb
    conda env create -f environment.yml
    conda activate pymcc
    pip install pymccrgb
    py.test pymccrgb/tests

Conda installation
------------------

*Conda forge package coming soon*

You can install it with ``conda`` in a virtual environment.

.. code-block:: bash

    conda env create -n pymcc
    conda activate pymcc
    conda install pymccrgb -c conda-forge

The package requires several C dependencies that may not be installed on your
system. They are:

* Boost
* C++11 standard library
* Cmake
* LibLAS 

The virtual environment will include all of these when the conda-forge package is installed. 

``pymccrgb`` is developed for Linux. The package can be installed on OS X, but it and Windows are not currently supported.

Installing LibLAS
-----------------

LibLAS will be installed from conda-forge. If you need to install it manually,
there are a couple of options.

If you are on a Debian-like Linux system, the LibLAS C API is available in the
``liblas-c-dev`` package. It can be installed with ``apt-get``:

.. code-block:: bash

    sudo apt-get install liblas-c-dev

Or from source

.. code-block:: bash

    mkdir ~/liblas
    cd ~/liblas
    apt-get download liblas-c-dev  # Downloads the LibLAS .deb file
    dpkg -x <deb-file> ~/liblas
    export LD_LIBRARY_PATH=~/liblas/usr/include/:$LD_LIBRARY_PATH

On OS X, it is available as a Homebrew package.

.. code-block:: bash

    brew install liblas

For more details, including how to compile LibLAS from source, see the
`LibLAS website <https://liblas.org/start.html#installation>`_.
