import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymccrgb",
    version="0.1.1",
    author=["Robert Sare", "George Hilley"],
    author_email="rmsare@stanford.edu",
    description="A Python package for point cloud classification using color and curvature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/rmsare/pymccrgb",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_require=">=3.6",
    install_requires=[
        "cmake",
        "cython",
        "fiona",
        "numpy",
        "matplotlib",
        "pdal",
        "scipy",
        "scikit-image",
        "scikit-learn",
    ],
    dependency_links=["https://github.com/stgl/pymcc/tarball/master#egg=pymcc"],
)
