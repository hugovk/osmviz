# Release Checklist

* [ ] Get master to the appropriate code release state. [Travis CI](https://travis-ci.org/hugovk/osmviz) should be running cleanly for all merges to master.
* [ ] Remove `.dev0` suffix from version in `setup.py`:
```bash
git checkout master
edit setup.py
```
* [ ] Commit and tag with the version number:
```bash
git add setup.py
git commit -m "Release 2.0.0"
git tag -a 2.0.0 -m "Release 2.0.0"
```
* [ ] Create a distribution and release on PyPI:
```bash
pip install -U pip setuptools wheel twine keyring
rm -rf build
python setup.py sdist --format=gztar bdist_wheel
twine upload -r pypi dist/osmviz-2.0.0*

```
* [ ] Check installation: `pip install -U osmviz`
* [ ] Push commits and tags:
 ```bash
git push
git push --tags
```
* [ ] Create new GitHub release: https://github.com/hugovk/osmviz/releases/new
  * Tag: Pick existing tag "2.0.0"
  * Title: "Release 2.0.0"
* [ ] Increment version and append `.dev0` in `setup.py`:
```bash
git checkout master
edit setup.py
```
* [ ] Commit and push:
```bash
git add setup.py
git commit -m "Start new release cycle"
git push
```
