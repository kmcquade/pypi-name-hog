#!/usr/bin/env python
import os
import sys
import logging
import shutil
import yaml
import setuptools
import requests
import click
from twine import cli as twine_cli
from random_word import RandomWords

logger = logging.getLogger(__name__)
here = os.path.dirname(__file__)
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def read_yaml_file(filename):
    """Reads a YAML file, safe loads, and returns the dictionary"""
    with open(filename, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            logger.critical(exc)
    return cfg


def change_log_level(log_level):
    """"Change log level of module logger"""
    logger.setLevel(log_level)


def clean_folder(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


def create_file(path: str, content: str = None):
    with open(path, "w") as file:
        if content:
            file.write(content)


class Package:
    def __init__(self, name: str, version: str = "0.0.0"):
        self.name = self._name(name)
        self.version = version
        self.setup_params = self._setup_params()
        if not os.path.exists(os.path.join(here, "packages", name)):
            os.makedirs(os.path.join(here, "packages", name))
        self.target_directory = os.path.join(here, "packages", name)
        print(f"Target directory: {self.target_directory}")
        self.readme = self._readme()

    def _name(self, name) -> str:
        if name:
            return name
        # If name is not provided, return a random name
        else:
            r = RandomWords()
            words = r.get_random_words(minLength=8, limit=3)
            random_package_name = "_".join(words).lower()
            return random_package_name

    def _setup_params(self) -> dict:
        setup_params = dict(
            name=self.name,
            version=self.version,
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

    def _readme(self) -> str:
        readme_content = f"""{self.name.capitalize()}
        Hogging this space for future use.
        """
        return readme_content

    def build_and_upload(
        self,
        twine_password: str,
        clean: bool = True,
        repository_url: str = "https://test.pypi.org/legacy/",
    ):

        # Create the __init__ file if it does not exist
        create_file(
            path=os.path.join(self.target_directory, "__init__.py"), content=None
        )
        # Create the README file if it does not exist
        create_file(
            path=os.path.join(self.target_directory, "README.md"), content=self.readme
        )
        # Change to the target directory and generate the build artifacts
        os.chdir(self.target_directory)
        print(f"Changing directory to {self.target_directory}")
        print("Abspath: ")
        print(f"{str(os.path.abspath(self.target_directory))}/dist/*")
        dist = setuptools.setup(**self.setup_params)
        command = [
            "upload",
            "--repository-url",
            repository_url,
            "--username",
            "__token__",
            "--password",
            twine_password,
            f"./dist/*",
        ]
        try:
            twine_cli.dispatch(command)
        except requests.exceptions.HTTPError as error:
            logger.info(error)


class Packages:
    def __init__(self, file):
        self.file = os.path.abspath(file)
        self.package_names = self._package_names()
        self.packages = self._packages()

    def _package_names(self) -> list:
        cfg = read_yaml_file(self.file)
        package_names = cfg.get("names")
        return package_names

    def _packages(self) -> [Package]:
        packages = []
        for package_name in self.package_names:
            package = Package(name=package_name)
            packages.append(package)
        return packages

    def build_and_upload(
        self,
        twine_password: str,
        clean: bool,
        repository_url: str = "https://test.pypi.org/legacy/",
    ):
        for package in self.packages:
            # setuptools reads directly from sys.argv so we need to manipulate it
            sys.argv.clear()
            sys.argv.extend(["-q", "sdist", "bdist_wheel"])
            package.build_and_upload(
                twine_password=twine_password,
                clean=clean,
                repository_url=repository_url,
            )


@click.command(short_help="Typosquat PyPi package names based on a YAML file.")
@click.option(
    "--input-file",
    type=click.Path(exists=True),
    default=os.path.join(os.getcwd(), "package_names.yml"),
    help="Path to the file containing the packages.",
)
@click.option(
    "--password",
    "-p",
    type=str,
    required=False,
    help="The password to upload to PyPi",
    envvar="TWINE_PASSWORD",
)
@click.option(
    "--server",
    "-s",
    default="https://test.pypi.org/legacy/",
    type=str,
    required=True,
    help="The PyPi server to push artifacts to. Defaults to 'https://test.pypi.org/legacy/'",
    envvar="PYPI_SERVER",
)
@click.option(
    "--clean",
    "-c",
    is_flag=True,
    default=False,
    help="Clean the path",
)
def pypi_squat(input_file, password, server, clean):
    packages = Packages(input_file)
    packages.build_and_upload(
        twine_password=password, clean=clean, repository_url=server
    )


if __name__ == "__main__":
    pypi_squat()
