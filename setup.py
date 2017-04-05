from setuptools import setup, find_packages

setup(
    name='osmviz',
    version='1.0.1',
    description=
        'OSMViz is a small set of Python tools for retrieving '
        'and using Mapnik tiles from a Slippy Map server '
        '(you may know these as OpenStreetMap images).',
    long_description=open('README.md', 'r').read(),
    classifiers=[
        #'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Documentation'],
    keywords='osm openstreetmap tiles visualization',
    author='Colin Bick',
    author_email='colin.bick@gmail.com',
    url='http://cbick.github.com/osmviz',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    use_2to3=True,
    # osmviz actually only requires either PyGame or PIL, not necessarily both
    requires=(
       'PyGame',
       'PIL',
    )
)
