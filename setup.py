from setuptools import setup, find_packages

setup(
    name='osmviz',
    version='1.0',
    long_description=open('README.md', 'r').read(),
    packages= find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe=False,
    requires = (
       'PyGame',
       'PIL',
    )
)