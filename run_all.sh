#!/usr/bin/env bash

set -e

# Detect homework number
BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [[ "$BRANCH" =~ hw([0-9]+) || "$BRANCH" =~ homework([0-9]+) ]]; then
  HW_NUM="${BASH_REMATCH[1]}"
  echo "Detected Homework #: $HW_NUM"
else
  echo "Error: Could not detect HW number from branch '$BRANCH'"
  echo "How to solve: Use branch names like 'hw5' or 'homework7'"
  exit 1
fi

HW_FOLDER="homeworks/hw${HW_NUM}"
TEST_FILE="tests/test_hw${HW_NUM}.py"
TARGETS=""

# Collect targets
if [ -d "$HW_FOLDER" ]; then
  for d in "$HW_FOLDER"/*; do
    [ -d "$d" ] && TARGETS="$TARGETS $d"
  done
  TARGETS="$TARGETS $HW_FOLDER"
fi

if [ -f "$TEST_FILE" ]; then
  TARGETS="$TARGETS $TEST_FILE"
else
  echo "Test file not found: $TEST_FILE"
  echo "Aborting tests."
  exit 1
fi

echo -e "\nFiles and directories selected for checks:"
echo "$TARGETS"

# Linters
echo -e "\nRunning linters..."

echo -e "\n- flake8"
flake8 .

echo -e "\n- mypy"
mypy .

echo -e "\n- pylint"
pylint . || true

echo -e "\n- ruff"
ruff check .

# Tests
echo -e "\n- Running pytest..."
pytest "$TEST_FILE" -v --tb=short --disable-warnings

echo -e "\nDone! Linters and tests passed (if no errors above)."