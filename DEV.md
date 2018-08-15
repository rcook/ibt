# Developer guide

## Building and publishing

```
pip install --user twine
pip install --user setuptools-markdown
pip install --user -r requirements.txt
python setup.py sdist
twine upload dist/*
```
