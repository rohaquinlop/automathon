from setuptools import find_packages, setup
setup(
    name="pythomata",
    packages=find_packages(include=['pythomata']),
    version='0.0.0',
    description="A Python library for simulating finite automata",
    author="Robin Hafid Quintero Lopez",
    license="GNU General Public License v2.0",
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)