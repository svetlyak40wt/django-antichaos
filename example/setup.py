from setuptools import setup, find_packages

setup(
    name = 'antichaos-example',
    version = '0.1.0',
    description = 'Example application for django-antichaos application.',
    author = 'Alexander Artemenko',
    install_requires = ['setuptools'],
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    include_package_data = True,
    zip_safe = False,
)

