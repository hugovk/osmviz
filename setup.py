import sys

from setuptools import find_packages, setup

if sys.version_info < (3,):
    error = """You are running OSMViz 3.0 on Python 2.

OSMViz 3.0 and above are no longer compatible with Python 2.
Make sure you have pip >= 9.0 and setuptools >= 24.2:

 $ pip install pip setuptools --upgrade

Your choices:

- Upgrade to Python 3.

- Install an older version of OSMViz:

 $ pip install 'osmviz<3.0'

See the following for more up-to-date information:

https://github.com/hugovk/osmviz/issues/18
    """

    print(error, file=sys.stderr)
    sys.exit(1)

with open("README.md") as f:
    long_description = f.read()

setup(
    name="osmviz",
    version="3.2.0.dev0",
    description="OSMViz is a small set of Python tools for retrieving "
    "and using Mapnik tiles from a Slippy Map server "
    "(you may know these as OpenStreetMap images).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Documentation",
    ],
    keywords="osm openstreetmap tiles visualization",
    author="Colin Bick and Contributors",
    author_email="colin.bick@gmail.com",
    url="https://hugovk.github.io/osmviz",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    # osmviz actually only requires either PyGame or PIL, not necessarily both
    requires=("PyGame", "PIL"),
)
