#!/bin/bash
set -uo pipefail
set +e

FAILURE=false

echo "safety (failure is tolerated)"
poetry run pip freeze | poetry run safety check --stdin

echo "pylint"
PYTHONPATH=. pylint src || FAILURE=true

echo "pycodestyle"
pycodestyle src || FAILURE=true

echo "pydocstyle"
pydocstyle src || FAILURE=true

echo "mypy"
mypy src || FAILURE=true

echo "bandit"
bandit -ll -r src || FAILURE=true

echo "shellcheck"
# .venv dir present in github workflow but not locally
find . -name "*.sh" -not -path "./.venv/*" -print0 | xargs -0 shellcheck || FAILURE=true

if [ "$FAILURE" = true ]; then
  echo "Linting failed"
  exit 1
fi
echo "Linting passed"
exit 0