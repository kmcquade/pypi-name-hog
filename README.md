# pypi-hogger

~~Hog all the good PyPi package names~~ Get first dibs on PyPi package names by uploading dummy packages to the desired package namespaces  specified in a YAML file.

The following package_names.yml will create two packages in pypi.org's Python Package Index, so you get first dibs on the names. The names of the packages will be `tralala` and `tralala2`.

```yaml
names:
  - tralala
  - tralala2
```

## Overview

The typical process of taking up space on PyPi (the Python package server) is as follows (generally speaking):

* Create a file called `setup.py`
* Fill it with contents like this:

<p align="center">
  <img src="docs/images/dynamic-setuptools.png">
</p>

* Install `twine`, `setuptools`, and `wheel`
* Run this command to build the package: `python setup.py -q sdist bdist_wheel`
* Use Twine to upload the wheel and tarball to the PyPi server: `python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

If you write python packages regularly - or if you just want to claim a name on the server to get first dibs on a potential sweet name - then you might be discouraged from doing that because you need to check your notes and follow this process.

Since we are all Senior YAML engineers at this point, I thought it would be great to skip this process by ~~hogging all the good names~~ noting my name ideas in a YAML file (called `package_names.yml`, and then have GitHub actions take care of the rest for me.

If I feel like using one of the names, then I can remove it from the `package_names.yml` file (to avoid duplicate uploads and failed upload events) and then automate the package upload process from wherever my new tool lives.


# References

* [Packaging Tutorial](https://packaging.python.org/tutorials/packaging-projects/)
* [SetupTools source code](https://github.com/pypa/setuptools/tree/main/setuptools)
* [Twine source code](https://github.com/pypa/twine/)
