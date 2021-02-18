# pypi-hogger

Typosquat PyPi package names based on a YAML file.

# Normal build and upload of packages


```bash
# Build package
python setup.py -q sdist bdist_wheel

# Use Twine to upload wheel and tarball
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

```

# References

* [Packaging Tutorial](https://packaging.python.org/tutorials/packaging-projects/)
* [SetupTools source code](https://github.com/pypa/setuptools/tree/main/setuptools)
* [Twine source code](https://github.com/pypa/twine/)
