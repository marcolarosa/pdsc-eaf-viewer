#!/bin/bash

if [ -z $GH_TOKEN ] ; then
    echo 'A github personal access token is not set in the environment.'
    read -p 'Please enter one so that the release can be pushed. > ' token

    if [ -z $token ] ; then
        echo "A token was not provided. Exiting."
        exit -1
    fi
fi

export GH_TOKEN="${token}"


read -p 'Should I bump the minor version number? [y/N] ' resp
if [ "$resp" == 'y'] ; then
    npm version minor
    git commit -m "minor version bump" -a
fi
PACKAGE_VERSION=$(awk '/version/{gsub(/("|",)/,"",$2);print $2};' package.json)
git tab -a "v${PACKAGE_VERSION}"
  
npm run publish

cat <<EOF

    You can now go to https://github.com/marcolarosa/pdsc-eaf-viewer/releases
    to verify the draft and release it.

EOF