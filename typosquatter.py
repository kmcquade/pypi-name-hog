#!/usr/bin/env python
import os
import argparse
import setuptools
import twine
import json
from random_word import RandomWords

here = os.path.dirname(__file__)


def get_setup_params(package_name):
    setup_params = dict(
        name=package_name,
        # include_package_data=True,
        version="0.0.0",
        author="null",
        author_email="null@example.com",
        description="null",
        long_description="null",
        long_description_content_type="text/markdown",
        url="http://www.example.com/",
        zip_safe=True,
        python_requires=">=3.7",
    )
    return setup_params


def get_name_idea():
    r = RandomWords()
    words = r.get_random_words(minLength=8, limit=3)
    idea = '_'.join(words)
    print(words)
    print(idea)


def squat(name):
    print(f"name: {name}")
    setup_params = get_setup_params(name)
    print("Setup params:")
    print(json.dumps(setup_params, indent=4))
    # here and os.chdir(here)
    os.chdir(os.path.join(here, "packages"))
    print(here)
    dist = setuptools.setup(**setup_params)
    print(dist)


def typosquatter(arguments):
    if arguments.idea:
        get_name_idea()
    if arguments.name:
        squat(arguments.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Typosquat a Python package name")
    parser.add_argument(
        "--name",
        "-n",
        dest="name",
        default=None,
        # TODO: Name validation?
        help="Name of the python package",
    )
    parser.add_argument(
        "--idea",
        action="store_true",
        dest="idea",
        help="Get a name idea"
    )
    args = parser.parse_args()
    typosquatter(arguments=args)
