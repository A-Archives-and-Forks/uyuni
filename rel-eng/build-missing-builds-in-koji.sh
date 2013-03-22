#!/bin/bash


pushd . >/dev/null
pushd `dirname $0`/.. >/dev/null

. rel-eng/build-missing-builds.conf

# say python to be nice to pipe
export PYTHONUNBUFFERED=1

declare -a PACKAGES

echo 'Gathering data ...'
for tag in $TAGS; do
  rel-eng/koji-missing-builds.py $KOJI_MISSING_BUILD_BREW_ARG --no-extra $tag | \
    perl -lne '/^\s+(.+)-.+-.+$/ and print $1' \
    | xargs -I replacestring awk '{print $2}' rel-eng/packages/replacestring \
    | sed "s/$/ $tag/"
done \
    | perl -lane '$X{$F[0]} .= " $F[1]"; END { for (sort keys %X) { print "$_$X{$_}" } }' \
    | while read package_dir tags ; do
      (
      echo Building package in path $package_dir for $tags
      cd $package_dir && \
          ONLY_TAGS="$tags" ${TITO_PATH}tito release $TITO_RELEASER </dev/tty
      )
    if [ "0$FEDORA_UPLOAD" -eq 1 ] ; then
      (
      echo Uploading tgz for path $package_dir
      cd $package_dir && LC_ALL=C ${TITO_PATH}tito build --tgz | \
      awk '/Wrote:.*tar.gz/ {print $2}' | \
      xargs -I packagepath scp packagepath fedorahosted.org:spacewalk
      )
    fi
    done

popd >/dev/null

