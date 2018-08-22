========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-efs/badge/?style=flat
    :target: https://readthedocs.org/projects/python-efs
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/eatfirst/python-efs.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/eatfirst/python-efs

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/eatfirst/python-efs?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/eatfirst/python-efs

.. |landscape| image:: https://landscape.io/github/eatfirst/python-efs/master/landscape.svg?style=flat
    :target: https://landscape.io/github/eatfirst/python-efs/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/efs.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/efs

.. |commits-since| image:: https://img.shields.io/github/commits-since/eatfirst/python-efs/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/eatfirst/python-efs/compare/v0.2.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/efs.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/efs

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/efs.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/efs

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/efs.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/efs


.. end-badges

A simple wrapper around fs to work with flask and switch between local and s3fs

* Free software: MIT license

Installation
============

::

    pip install efs

Documentation
=============

https://python-efs.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
