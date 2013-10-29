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
wc -l $(git ls-files | grep -v .md5 ) | tail -n 1


#
#  Compute the number of inserted lines
#
echo "Number of Inserted Lines of Code"
itkfirstcommit=`git hash-object -t tree /dev/null`
git diff --shortstat $itkfirstcommit

