#!/bin/bash

if test -z "$HOST" ; then
  HOST=10.0.0.155
fi
if test -z "$REMOTE_USER" ; then
  REMOTE_USER=pi
fi
if test -z "$DIR" ; then
  DIR='hydropwnics-raspi-server'
fi
if test -z "$BRANCH" ; then
  BRANCH='master'
fi

echo "Deploying $DIR to ${REMOTE_USER}@${HOST} on branch $BRANCH"

ssh ${REMOTE_USER}@${HOST} bash <<EOF
set -e
cd "$DIR"
git fetch
git reset --hard origin/master
source bin/activate
OUT="\$(pip install -r requirements.txt)"
if [ \$? -ne 0 ] ; then
  echo "Pip install failed for requirements!"
  echo "\$OUT"
fi
echo "Deploy complete. Have a nice day."
EOF
