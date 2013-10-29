#!/bin/bash

#
#  Instructions:
#
#  Run this script from the top level directory of an ITK git clone.
#
#

#
#  Compute the current number of lines of code
#
echo "Number of Lines of Code"
wc -l $(git ls-files | grep -v .md5 ) | tail -n 1 | cut -f 2 -d' '

#
#  Compute the current number of third party lines of code
#
echo "Number of Third-Party Lines of Code"
wc -l $(git ls-files | grep -v .md5 | grep ThirdParty) | tail -n 1 | cut -f 2 -d' '

#
#  Compute the current number of non third party lines of code
#
echo "Number of non Third-Party Lines of Code"
wc -l $(git ls-files | grep -v .md5 | grep -v ThirdParty) | tail -n 1 | cut -f 2 -d' '


#
#  Compute the number of inserted lines
#
echo "Number of Inserted Lines of Code"
itktreeobjecthash=`git hash-object -t tree /dev/null`
itkfirstcommit=`git log  --reverse | head -n 1 | cut -d' ' -f 2`
git diff --shortstat $itkfirstcommit | cut -d' ' -f 5


#
# Compute the number of commits, excluding merges
#
echo "Number of Commits (excluding merges)"
git rev-list --no-merges --count HEAD

#
# Compute the number of authors
#
echo "Number of Authors"
git shortlog -s -n | wc | cut -d' ' -f 5

#
# Compute the ranking of authors by number of commits
#
echo "Authors ranked by number of commits"
git shortlog -s -n
