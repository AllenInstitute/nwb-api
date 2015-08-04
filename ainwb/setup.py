from setuptools import setup, find_packages
import io
#import nwb

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')

setup(
    name='nwb',
    version="1.0.0",#nwb.__version__,
    url='https://github.com/AllenInstitute/nwb-api',
    author='Keith Godfrey',
    author_email='keithg@alleninstitute.org',
    description='Allen Institute API for the NWB format',
    long_description = long_description,

    install_requires=['h5py>=2.2.1'],
    platforms=["any"],
    #packages=find_packages('nwb'),
    packages=['nwb'],
    include_package_data=True,
    package_data={'': ['spec*.json']}
)

