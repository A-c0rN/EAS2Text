from os import path, pardir, chdir
from setuptools import setup

with open(path.join(path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
chdir(path.normpath(path.join(path.abspath(__file__), pardir)))

setup(
    name="EAS2Text",
    packages=["EAS2Text"],
    version="0.1.7",
    description="A Python library to convert raw EAS header data to a human readable text",
    author="A-c0rN",
    author_email="acrn@gwes-eas.network",
    license="ODbL-1.0",
    install_requires=[],
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/A-c0rN/EAS2Text",
    keywords="eas alerting emergency-alert-system",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
