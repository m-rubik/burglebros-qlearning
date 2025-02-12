from setuptools import setup, find_packages

setup(
    name='burglebros',
    version='0.0.1',
    description='Burgle Bros Simulation and Q-learning',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['networkx',
                      'numpy'
                      ]
)