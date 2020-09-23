import glob
import io
import re
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

with open('README.md') as rm:
    long_description=rm.read()

setup(
    name="BasicHTTPServer",
    version="0.0.1",
    license="GPLv3",
    description="A pretty simple HTTP server to help you build a website fast",
    long_description=long_description,
    author="Eddie Breeg",
    author_email="eddiebreeg0@protonmail.com",
    url="https://github.com/EddieBreeg/BasicHTTPServer",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/BasicHTTPServer/*.py")] + 
    [splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: https://pypi.org/classifiers/
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords=[
        "web", "webdev", "http", "server"
    ],
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
    ],
    extras_require={
        # eg: 'rst': ["docutils>=0.11"],
    },

)
