# Release Checklist

* [ ] Get master to the appropriate code release state. [Travis CI](https://travis-ci.org/hugovk/osmviz) should be running cleanly for all merges to master.
* [ ] Update version and commit:
```bash
git checkout master
edit setup.py
git add setup.py
git commit -m "Release 1.1.0"
```
* [ ] Tag the last commit with the version number:
```bash
git tag -a 1.1.0 -m "Release 1.1.0"
```
* [ ] Release on PyPI:
```bash
python setup.py sdist --format=gztar
twine upload dist/osmviz-1.1.0.tar.gz
```
* [ ] Check installation: `pip install -U osmviz`
* [ ] Push: `git push`
* [ ] Push tags: `git push --tags`
* [ ] Create new GitHub release: https://github.com/hugovk/osmviz/releases/new
  * Tag: Pick existing tag "1.1.0"
  * Title: "Release 1.1.0"
```
