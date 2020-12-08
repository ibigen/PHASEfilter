
***********************************
Installation of PHASEfilter
***********************************

Installation of PHASEfilter with virtual env:

$ virtualenv phasefilter --python=python3 --prompt "(phasefilter) "
$ source phasefilter/bin/activate
(phasefilter) $ pip3 install phasefilter
### OR if you want to run the tests
(phasefilter) $ pip3 install phasefilter --install-option test

Dependecies

* lastz >= 1.4
* minimap2 >= 2.0
* blastn >= 2.3
* samtools >= 1.3
* bcftools >= 1.3
* htslib >= 1.3
* bgzip >= 1.3

After that you have three scripts available

$ best_alignment
$ phasefilter
$ reference_statistics
$ synchronize_genomes

