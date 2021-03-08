from setuptools import find_packages, setup

#read the contents of the README file
from os import path
thisDirectory = path.abspath(path.dirname(__file__))
with open(path.join(thisDirectory, 'README.md'), encoding='utf-8') as f:
  longDescription = f.read()

setup(
    name="automathon",
    packages=find_packages(include=['automathon']),
    version='0.0.1',
    description="A Python library for simulating finite automata",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    author="Robin Hafid Quintero Lopez",
    license="GNU General Public License v2.0",
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    author_email='rohaquinlop301@gmail.com',
    url='https://github.com/rohaquinlop/automathon',
    download_url="https://github.com/rohaquinlop/automathon/archive/v_000.tar.gz",
    keywords=["python", "automata", "automata", "automathon"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3'
    ]
)

