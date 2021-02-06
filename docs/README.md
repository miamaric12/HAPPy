# Docs README #

The documentation for the HAPPY is generated using the Sphinx Python package. Documentation is written in reStructuredText format (in the source folder) and compiled by the Sphinx package into a HTML source (in the build/html folder). At compilation time Sphinx also scrapes docstrings from the Python scripts and adds these to the documentation.

Once a commit is made to the master branch, the documentation is automatically built to https://radial-hydride-code.readthedocs.io/, providing an online version of the documentation.

The following instructions are for manually compiling the documentation into html on your local machine.

Requrements to compile documentation
======================================

Install Sphinx (http://www.sphinx-doc.org/en/master/) and the theme:

`conda install sphinx sphinx-rtd-theme`

Compiling documentation
=========================

To manually build the documentation to your local machine, run the following command from the docs folder:

`make docs`

This will autogenerate the API documentation from docstrings, clean the build folder and recompile the html documentation to /build/html.
