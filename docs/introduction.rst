
************
Introduction
************

PHASEfilter is a bioinformatic package that allow to identify the heterozygous variants that are present in diploid species.
For that, it is necessary to have a diploid version of the reference genome and two variant files (vcf), one for each ploidy of the reference.
The software has the capability to create the synchronization between diploid chromosomes but you can use a chain if it is available. 

This package offer five tools:

-  phasefilter
-  phasefilter_single
-  reference_statistics
-  synchronize_genomes
-  make_alignment

phasefilter
+++++++++++

Identifies heterozygous variations and create three VCF files for each direction of analysis: 1) valid; 2) heterozygous variants; 3) loss of heterozygous (LOH).
Make the analysis in both directions, from reference A to reference B and vice-versa.
It accept 5 mandatory parameters and four optional parameters.
It is also possible define the threshold of Heterozygous/Homozygous variants based on Allele Count (AC) that must exist in the VCF file. These values are added by the caller, like GATK.
A threshold that allow to remove variants with low Allele Frequency values it is also possible to set, but once again, it is ncessary to have Allele Count (AC) in each variant in VCF.

phasefilter_single
++++++++++++++++++

Identifies heterozygous variations and create three VCF files: 1) valid; 2) heterozygous variants; 3) loss of heterozygous (LOH).
Only make the analysis in one direction, from reference A to reference B.
It accept 5 mandatory parameters and three optional parameters.
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