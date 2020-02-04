# OSMViz

[![PyPI version](https://img.shields.io/pypi/v/osmviz.svg?logo=pypi&logoColor=FFE873)](https://pypi.python.org/pypi/osmviz/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/osmviz.svg?logo=python&logoColor=FFE873)](https://pypi.python.org/pypi/osmviz/)
[![PyPI downloads](https://img.shields.io/pypi/dm/osmviz.svg)](https://pypistats.org/packages/pypistats)
[![Travis CI status](https://img.shields.io/travis/hugovk/osmviz/master?label=Travis%20CI&logo=travis)](https://travis-ci.org/hugovk/osmviz)
[![GitHub Actions status](https://github.com/hugovk/osmviz/workflows/Test/badge.svg)](https://github.com/hugovk/osmviz/actions)
[![codecov](https://codecov.io/gh/hugovk/osmviz/branch/master/graph/badge.svg)](https://codecov.io/gh/hugovk/osmviz)
[![GitHub](https://img.shields.io/github/license/hugovk/osmviz.svg)](LICENSE)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

An OpenStreetMap Visualization Toolkit for Python

## OSMViz License

OSMViz is released under the MIT license.
See LICENSE in this directory.


# OpenStreetMap License

Tiles taken from the openstreetmap.org server
have a usage policy as outlined here:

https://operations.osmfoundation.org/policies/tiles/

These tiles are (c) OpenStreetMap & contributors, CC-BY-SA.
OpenStreetMap: https://www.openstreetmap.org
CC-BY-SA: https://creativecommons.org/licenses/by-sa/2.0/

You can tell OSMViz to use any slippymap server provided
tiles that you wish, which may have its own usage policy.

## About

OSMViz is a small set of Python tools for retrieving
and using Mapnik tiles from a Slippy Map server
(you may know these as OpenStreetMap images).

## Requirements

* Python 3.6+
* Pillow and/or Pygame 

## Installation

Either:

    pip install osmviz

Or just add the src directory to your PYTHONPATH.

## Help

See [html/doc.html](https://hugovk.github.io/osmviz/html/doc.html)
