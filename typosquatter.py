#!/usr/bin/env python
import os
import argparse
import setuptools
import sys
import json
from random_word import RandomWords
import shutil
from twine import cli as twine_cli
import logging

logger = logging.getLogger(__name__)
here = os.path.dirname(__file__)
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_name_idea():
    r = RandomWords()
    words = r.get_random_words(minLength=8, limit=3)
    idea = '_'.join(words).lower()
    print(words)
    print(idea)
    return idea


def change_log_level(log_level):
    """"Change log level of module logger"""
    logger.setLevel(log_level)


def get_setup_params(package_name):
    setup_params = dict(
        name=package_name,
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


def get_readme(name: str):
    readme_content = f"""{name.capitalize()}
Hogging this space for future use.
"""
    return readme_content


def create_file(path: str, content: str = None):
    # if not os.path.exists(path):
    with open(path, 'w') as file:
        if content:
            file.write(content)


def clean_folder(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


def upload_with_twine(folder: str, twine_password: str, repository_url: str = "https://test.pypi.org/legacy/"):
    logger.debug("repository_url: %s" % repository_url)
    logger.debug("folder: %s" % folder)
    command = [
        "upload",
        "--repository-url",
        "https://test.pypi.org/legacy/",
        "--username",
        "__token__",
        "--password",
        twine_password,
        f"{str(folder)}/dist/*",
    ]
    twine_cli.dispatch(command)


def typosquatter(name: str, clean: bool, twine_password: str):
    logger.debug(f"name: {name}")
    target_directory = os.path.join(here, "packages", name)
    if clean:
        clean_folder(target_directory)
    setup_params = get_setup_params(name)
    # print("Setup params:")
    logger.debug(json.dumps(setup_params))
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)
    # Create the __init__ file if it does not exist
    create_file(path=os.path.join(target_directory, "__init__.py"), content=None)
    # Create the README file if it does not exist
    create_file(path=os.path.join(target_directory, "README.md"), content=get_readme(name=name))
    # Change to the target directory and generate the build artifacts
    os.chdir(target_directory)
    logger.debug(here)
    dist = setuptools.setup(**setup_params)
    logger.debug(dist)
    upload_with_twine(folder=target_directory, twine_password=twine_password)


# def typosquatter(name: str, clean: bool, twine_password: str):
#     if name:
#         squat(name, clean, twine_password)


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
        "--clean",
        "-c",
        dest="clean",
        action="store_true",
        default=None,
        # TODO: Name validation?
        help="Clean the directory",
    )
    # Not using try/except because I am yoloing this and because os.getenv returns none
    if os.getenv("TWINE_PASSWORD"):
        twine_pass = os.getenv("TWINE_PASSWORD")
    else:
        raise Exception("TWINE_PASSWORD not provided.")
    change_log_level("DEBUG")
    args = parser.parse_args()
    # name_arg = args.name
    clean_arg = args.clean
    sys.argv.clear()
    logger.debug("Initial arguments")
    logger.debug(sys.argv)
    sys.argv.extend(["-q", "sdist", "bdist_wheel"])
    logger.debug("Extended arguments")
    logger.debug(sys.argv)
    name_arg = get_name_idea()
    typosquatter(name=name_arg, clean=clean_arg, twine_password=twine_pass)
