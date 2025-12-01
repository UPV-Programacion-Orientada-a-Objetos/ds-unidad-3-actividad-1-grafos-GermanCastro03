from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import sys

# Force MinGW on Windows
if sys.platform == 'win32':
    # Tell distutils to use mingw32
    import distutils.cygwinccompiler
    distutils.cygwinccompiler.get_msvcr = lambda: []

# Define the extension module
extensions = [
    Extension(
        name="neuronet",
        sources=["src/cython/neuronet.pyx", "src/cpp/GrafoDisperso.cpp"],
        include_dirs=["src/cpp"],
        language="c++",
        extra_compile_args=["-std=c++17", "-O2"],
        extra_link_args=[],
    )
]

setup(
    name="neuronet",
    ext_modules=cythonize(extensions, language_level="3"),
)
