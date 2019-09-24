Installation
============

``pymccrgb`` is hosted on GitHub. You can install it with

.. code-block:: bash

    git clone https://github.com/rmsare/pymccrgb
    cd pymccrgb
    conda env create -f environment.yml
    conda activate pymcc
    py.test pymccrgb/tests

The package requires several C dependencies that may not be installed on your
system. They are:

* Boost
* C++11 standard library
* Cmake
* LibLAS 

The virtual environment will include all of these except the LibLAS bindings.

``pymccrgb`` is developed for Linux and OS X. Windows is not currently supported.

Installing LibLAS
-----------------

If you are on a Debian-like Linux system, the LibLAS C API is availablein the
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
`LibLAS website <https://liblas.org/start.html#installation>_`.
