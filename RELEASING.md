# Release Checklist

* [ ] Get master to the appropriate code release state. [Travis CI](https://travis-ci.org/hugovk/osmviz) should be running cleanly for all merges to master.

* [ ] Tag with the version number:
```bash
git tag -a 3.1.1 -m "Release 3.1.1"
```

* [ ] Push tag:
 ```bash
git push --tags
```

* [ ] Create new GitHub release: https://github.com/hugovk/osmviz/releases/new
  * Tag: Pick existing tag "3.1.1"
  * Title: "Release 3.1.1"

* [ ] Check the tagged [Travis CI build](https://travis-ci.org/hugovk/osmviz) has deployed to [PyPI](https://pypi.org/project/osmviz/#history)

* [ ] Check installation:
```bash
pip3 uninstall -y osmviz && pip3 install -U osmviz
```
