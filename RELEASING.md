# Release Checklist

* [ ] Get master to the appropriate code release state. [Travis CI](https://travis-ci.org/hugovk/osmviz) should be running cleanly for all merges to master.

* [ ] Tag with the version number:
```bash
git tag -a 2.0.0 -m "Release 2.0.0"
```
* [ ] Create a distribution and release on PyPI:
```bash
pip3 install -U pip setuptools wheel twine keyring
rm -rf build
python3 setup.py sdist --format=gztar bdist_wheel
twine check dist/*
twine upload -r pypi dist/osmviz-2.0.0*
```
* [ ] Check installation: `pip3 uninstall -y osmviz && pip3 install -U osmviz`
* [ ] Push tag:
 ```bash
git push --tags
```

* [ ] Create new GitHub release: https://github.com/hugovk/osmviz/releases/new
  * Tag: Pick existing tag "2.0.0"
  * Title: "Release 2.0.0"
