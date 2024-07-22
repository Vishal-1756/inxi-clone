
from setuptools import setup, find_packages

setup(
    name='inxi_clone',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'stats=inxi_clone.main:main',
        ],
    },
)
