git clone git@github.com:python/mypy
cd mypy
git submodule update --init typeshed
PYTHONPATH=`pwd`
scripts/mypy
