Change log
==========

This tab includes a list (chronologically ordered) of notable changes in PHASEfilter.

2021
----

December 7, 2022
................

Improve "synchronize_genomes" tool

-  It is possible to load "gff3.gz" and write output in "gz" too;

December 30, 2021
.................

Add script to install all software dependencies

-  Add the shell script "install_phasefilter_dependencies.sh" to install all dependencies automatically;


October 26, 2021
................

Add new tool

-  Create a tool to copy some data to test the some tools;
-  Add the possibility of creation a reference with degenerated bases for heterozygous positions. IUPAC codes will be applied. It is only available for SNPs;


September 17, 2021
..................

Add new tool 

-  Change name phasefilter to phasefilter_single;
-  Add phasefilter script to the package. Can make both directions in a single run. Make RefA to RefB and RefB to RefA. The output will be saved in a directory;

September 16, 2021
..................

Add all documentation to the project 

-  Change command line frm make_alignment to make_alignment;

July 1, 2021
............

First launch of PHASEfilter, Version 0.2.0.

-  Four command lines available: 1) best_alignment; 2) phasefilter; 3) reference_statistics; 4) synchronize_genomes
