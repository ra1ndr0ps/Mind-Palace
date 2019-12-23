from setuptools import setup, find_packages


setup(
    name = 'foobar',
    version = '0.1.0',
    author = 'Ran Dvir',
    description = 'Mind Palace - A client-server application.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)
