from setuptools import find_packages, setup

# read the contents of the README file
from os import path

thisDirectory = path.abspath(path.dirname(__file__))
with open(path.join(thisDirectory, "README.md"), encoding="utf-8") as f:
    longDescription = f.read()

setup(
    name="automathon",
    packages=find_packages(
        include=[
            "automathon",
            "automathon.finite_automata",
            "automathon.errors",
            "automathon.utils",
        ]
    ),
    include_package_data=True,
    version="{{VERSION_PLACEHOLDER}}",
    description="A Python library for simulating and visualizing finite automata",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    author="Robin Hafid Quintero Lopez",
    license="MIT",
    install_requires=["graphviz==0.16"],
    tests_require=["graphviz==0.16"],
    test_suite="tests",
    author_email="rohaquinlop301@gmail.com",
    url="https://github.com/rohaquinlop/automathon",
    download_url="https://github.com/rohaquinlop/automathon/archive/refs/tags/{{VERSION_PLACEHOLDER}}.tar.gz",
    keywords=["python", "automata", "automata", "automathon"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Retrieval",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
