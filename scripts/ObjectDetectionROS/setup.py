from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = []

setup(
    name="my-package",
    version="0.1",
    author="Cornell Electric Vehicles",
    author_email="electricvehiclescornell@gmail.com",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description="An example package for training on Cloud ML Engine.",
)
