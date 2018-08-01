#!/usr/bin/env bash
set -e

function main() {
  if [ $# -lt 1 ] ; then
    echo "No destination directory provided"
    exit 1
  fi

  echo `pwd`

  # Create the directory, then do dirname on a non-existent file inside it to give us an absolute paths with tilde
  # characters resolved to the destination directory. Readlink -f is a cleaner way of doing this but is not available
  # on a fresh macOS install.
  DEST="$(realpath "${1}")"
  mkdir -p "$DEST"
  echo "=== destination directory: ${DEST}"

  TMPDIR=$(mktemp -d -t tmp.XXXXXXXXXX)
  echo $(date) : "=== Using temporary directory: ${TMPDIR}"

  echo "=== Copy source files"
  # Here are bazel-bin/pip_package/pip_package.runfiles directory structure.
  # |- tfunicode
  #   |- tfunicode (needed)
  #   |- pip_pkg
  #   |- pip_pkg.sh
  # |- MANIFEST
  # |- <maybe other directories generated by bazel build>
  #
  # To build wheel, we only need setup.py, MANIFEST.in, python and .so files under tfunicode/tfunicode.
  # So we extract those to ${TMPDIR}.
  cp -LR bazel-bin/pip_package/pip_package.runfiles/tfunicode/tfunicode ${TMPDIR}
  find ${TMPDIR}/tfunicode/cc/ -name '__init__.py'  -type f -delete
  cp pip_package/LICENSE ${TMPDIR}
  cp pip_package/MANIFEST.in ${TMPDIR}
  cp pip_package/README.md ${TMPDIR}
  cp pip_package/setup.cfg ${TMPDIR}
  cp pip_package/setup.py ${TMPDIR}

  pushd ${TMPDIR}

  echo $(date) : "=== Building wheel"
  PY_BIN=${PYTHON_BIN_PATH:-python}
  $PY_BIN setup.py bdist_wheel

  if [[ $(uname) == "Linux" ]]; then
    mkdir repaired
    for WHL in dist/*.whl
    do
      auditwheel repair -w repaired $WHL
    done

    rm dist/*
    mv repaired/* dist/
  fi

  cp dist/* ${DEST}

  popd

  rm -rf ${TMPDIR}
  echo $(date) : "=== Output wheel is in: ${DEST}"
}

main "$@"
