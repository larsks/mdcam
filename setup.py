from setuptools import setup, find_packages
from mdcam import __version__

with open('requirements.txt') as fd:
    requires = fd.read().splitlines()

setup(name='mdcam',
      author='Lars Kellogg-Stedman',
      author_email='lars@oddbit.com',
      url='https://github.com/larsks/mdcam',
      version=__version__,
      packages=find_packages(),
      install_requires=requires,
      entry_points={'console_scripts': ['mdcam = mdcam.main:cli']})
