
***************************
Introduction of PHASEfilter
***************************

PHASEfilter is a bioinformatic package that allow to identify the heterozygous variants that are present in diploid species.
For that, it is necessary to have a diploid version of the reference genome and two variant files (vcf), one for each ploidy of the reference. 

This package offer four tools:

* phasefilter
* reference_statistics
* synchronize_genomes
* make_alignment

phasefilter
+++++++++++

Identifies heterozygous variations and create three VCF files: 1) valid; 2) heterozygous variants; 3) loss of heterozygous (LOH).
It accept 5 mandatory parameters and two optional parameters.
It is also possible define the threshold of Heterozygous/Homozygous variants based on Allele Count (AC) that must exist in the VCF file. These values are added by the caller, like GATK.
A threshold that allow to remove variants with low Allele Frequency values it is also possible.

reference_statistics
++++++++++++++++++++

Creates a report based on the number of bases that exists in the chromosomes.
It accept 2 mandatory parameters.

synchronize_genomes
+++++++++++++++++++

Synchronize two references and add two new fields (StartHit;EndHit) GFF with the positions on hit reference. If you you a VCF file only adds (start_hit) tag to the VCF INFO.
It accept 4 mandatory parameters and one optional parameter. It is necessary to pass a VCF or a GFF file.

make_alignment
++++++++++++++

Obtain the percentage of the minimap2 alignment between chromosomes and create an output in Clustal X format. It accept 3 mandatory parameters and two optional parameters.