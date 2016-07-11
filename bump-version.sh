#!/bin/sh

echo "Generating new version identifier..."

VERSION=`git describe 2>/dev/null || git rev-parse --short HEAD`
echo -e "nodenator_version = '${VERSION}'\n" > nodenator/version.py && git add nodenator/version.py

echo "New version is '${VERSION}'"

