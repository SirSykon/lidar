from setuptools import setup

setup(
    name='lidar_processing_utils',
    version='0.1.0',
    author='Jorge García',
    author_email='jrggcgz@gmail.com',
    scripts=['bin/script1','bin/script2'],
    url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE.txt',
    description='LIDAR processing related code.',
    long_description=open('README.txt').read(),
    install_requires=[
        "bagpy",
        "pandas",
        "numpy",
    ],
)