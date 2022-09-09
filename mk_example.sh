#!/usr/bin/env bash

set -ex

EXAMPLE_DIR="static/images/examples"

NAME=${1:?"Name is not set"}
IN_FILE=${2:?"input file is not set"}
OUT_FILE=${3:?"output file is not set"}

DIR="${EXAMPLE_DIR}/${NAME}"
mkdir "$DIR"

cp "$IN_FILE" "${DIR}/in.png"
cp "$OUT_FILE" "${DIR}/out.gif"

git add "${DIR}"
