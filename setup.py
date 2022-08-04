# from distutils.core import setup
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding='utf-8') as fh:
    long_desc = fh.read()

setup(
  name = 'matrix_calculus',
  packages = find_packages(),
  version = '0.0.4',
  description = 'Use python to take derivative of matrix equations!',
  long_description_content_type="text/markdown",
  long_description=long_desc,
  author = 'Ray Hou (Songlin Hou)',
  author_email = 'songlinhou1993@gmail.com',
  url = 'https://github.com/songlinhou/matrix_calculus', # use the URL to the github repo
  keywords = ['matrix','calculus'],
  classifiers = [],
  install_requires=['requests']
)