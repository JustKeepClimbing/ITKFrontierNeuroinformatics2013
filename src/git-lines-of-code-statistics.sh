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

