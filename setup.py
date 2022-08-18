from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'app',
  ext_modules = cythonize("xxx.pyx"),
)
