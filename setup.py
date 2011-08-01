from distutils.core import setup

setup(
    name = 'cmdlnui',
    packages = ['cmdlnui'],
    version='0.1',
    description = "Command Line UI Builder",
    author = "Philip Graham",
    author_email = "philip@zeptech.ca",
    url = "https://github.com/pgraham/cmdlnui",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces"
    ],
    long_description = """\
Command Line UI Utility
-----------------------

Aids in building command line interfaces for Python programs.
"""
)
