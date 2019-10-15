from setuptools import find_packages, setup


with open("README.md") as f:
    long_description = f.read()


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="osmviz",
    description="OSMViz is a small set of Python tools for retrieving "
    "and using Mapnik tiles from a Slippy Map server "
    "(you may know these as OpenStreetMap images).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=["setuptools_scm"],
    extras_require={"tests": ["coverage", "pillow", "pytest", "pytest-cov"]},
    python_requires=">=3.5",
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
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
