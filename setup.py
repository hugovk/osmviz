from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name='osmviz',
    version='1.1.0',
    description='OSMViz is a small set of Python tools for retrieving '
                'and using Mapnik tiles from a Slippy Map server '
                '(you may know these as OpenStreetMap images).',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Documentation'],
    keywords='osm openstreetmap tiles visualization',
    author='Colin Bick',
    author_email='colin.bick@gmail.com',
    url='https://hugovk.github.io/osmviz',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    # osmviz actually only requires either PyGame or PIL, not necessarily both
    requires=(
       'PyGame',
       'PIL',
    )
)
