#!/bin/bash

#
#  Instructions:
#
#  Run this script from any directory
#
#

#
#  Get statistics from the last line of the first page in the Insight Journal site.
#
echo "Insight Journal Statistics"
curl -i http://www.insight-journal.org  2>&1 | grep publications | grep users | grep reviews

echo "Most Downloaded Publications"
curl -i http://www.insight-journal.org/browse/publications/dl      2>&1 | grep downloaded | grep times

echo "Highest Rated Publications"
curl -i http://www.insight-journal.org/browse/publications/rating  2>&1 | grep downloaded | grep times
