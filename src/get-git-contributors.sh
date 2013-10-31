#!/bin/bash

#
#  Instructions:
#
#  Run this script from the top level directory of an ITK git clone.
#
#

#
# Compute the ranking of authors by number of commits
#
echo "Authors ranked by number of commits"
git shortlog -s -n | tee /tmp/itk_git_contributors.dat
