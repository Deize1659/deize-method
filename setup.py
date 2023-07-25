from setuptools import find_packages, setup

import src

NAME = "my-method"
AUTHOR = "ymorishima030"
AUTHOR_EMAIL = "ymorishima@hochiki.co.jp"
DESCRIPTION = "my-method"
VERSION = src.__version__
PACKAGES = find_packages()
PY_REQUIRES = ">=3.11"

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    version=VERSION,
    packages=PACKAGES,
    python_requires=PY_REQUIRES,
)
