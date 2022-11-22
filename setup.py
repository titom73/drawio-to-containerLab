import os
import sys
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="drawio-to-clab",
    version="0.1",
    python_requires=">=3.6",
    scripts=["bin/drawio-to-containerlab"],
    install_requires=required,
    # packages=find_packages(),
    packages=find_packages(exclude=['data','ez_setup', 'tests', 'tests.*']),
    # package_data={'': ['templates/CLAB_TEMPLATE.j2']},
    include_package_data=True,
    url="https://github.com/dwarf-fr/drawio-to-containerLab",
    license="APACHE2",
    author="Arista EMEA",
    author_email="",
    description="Script to build containerlab topology from draw.io",
)
