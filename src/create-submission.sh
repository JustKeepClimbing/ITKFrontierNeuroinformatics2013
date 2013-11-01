#!/bin/sh

# Run to create the submission.

dexy

out=output/submission
doc=output/doc
width=2000

mkdir -p $out
rm $out/*

cp output/doc/frontiers.pdf $out/ITKEnablingReproducibleResearchAndOpenScience.pdf

# EPS or covert to tiff?
cpconvert="cp"

convert -resize ${width}x $doc/itk_module_dependency.png $out/figure_1_itk_module_dependency.tiff
convert -resize ${width}x $doc/itk_code_contribution.png $out/figure_2_itk_code_contribution.tiff
$cpconvert $doc/itk_git_contributors.eps $out/figure_3_itk_git_contributors.eps
$cpconvert $doc/gerrit_patch_set_histogram.eps $out/figure_4_gerrit_patch_set_histogram.eps
$cpconvert $doc/gerrit_fix_ups.eps $out/figure_5_gerrit_fix_ups.eps
convert -resize ${width}x $doc/GerritGraphRender.png $out/figure_6_gerrit_graph_render.tiff
$cpconvert $doc/gerrit_closeness.eps $out/figure_7_gerrit_closeness.eps
$cpconvert $doc/insight_journal_submissions.eps $out/figure_8_insight_journal_submissions.eps

