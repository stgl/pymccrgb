Installation
============

``pymccrgb`` is hosted on GitHub and PyPI. You can install it with ``conda`` 
 in a virtual environment.

.. code-block:: bash

    conda env create -n pymcc
    conda install pymccrgb -c conda-forge

The package requires several C dependencies that may not be installed on your
system. They are:

* Boost
* C++11 standard library
* Cmake
* LibLAS 

The virtual environment will include all of these whe nthe conda-forge package is installed. 

``pymccrgb`` is developed for Linux. OS X and Windows are not currently supported.

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
