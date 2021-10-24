# Release Checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/hugovk/osmviz/actions) should be running
      cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/hugovk/osmviz/workflows/Test/badge.svg)](https://github.com/hugovk/osmviz/actions)

- [ ] Edit release draft, adjust text if needed:
      https://github.com/hugovk/osmviz/releases

- [ ] Check next tag is correct, amend if needed

- [ ] Publish release

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/hugovk/osmviz/actions?query=workflow%3ADeploy)
      has deployed to [PyPI](https://pypi.org/project/osmviz/#history)

- [ ] Check installation:

```bash
pip3 uninstall -y osmviz && pip3 install -U osmviz
```
