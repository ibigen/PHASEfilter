
[![License: MIT](https://img.shields.io/badge/License-MIT%20-blue.svg)](https://www.mit.edu/~amini/LICENSE.md)


# PHASEfilter
PHASEfilter is a software package to filter variants, SNPs and INDELs, that are present in heterozygous form in phased genomes.

# Installation

This installation is oriented for Linux distributions.

### Install directly

```
$ pip3 install PHASEfilter
```

### Install with virtualenv

```
$ virtualenv PHASEfilter --python=python3 --prompt "(PHASEfilter version) "
$ . PHASEfilter/bin/activate
$ pip install PHASEfilter
OR
$ pip3 install PHASEfilter
```


The follow software must be available in your computer:
* [minimpa2](https://github.com/lh3/minimap2) v2.22 or up
* [bcftools](http://www.htslib.org/download/) v1.3 or up
* [samtools](http://www.htslib.org/download/) v1.3 or up
* [htslib](http://www.htslib.org/download/) v1.3 or up


# All software available

## Filter variants in phased genomes

This software that can identify heterozygosity positions between two phased references.
The software starts by aligning pairs of diploid chromosomes, based on Minimap2 aligner. With synchronization done it is possible to identify the position of a variation, in both pair of chromosomes, allowing variants to be removed if they meets some established criterias.
To classify variants it is necessary to pass two VCF files, one for each reference phase. After that, the PHASEfilter will go through the variants called in reference A and check if there are any homologous in the variants called in reference B. For each variant called in the reference A it can happen three situations: 1) both references, for the position in analysis, are equal and the variant is valid; 2) the position is heterozygous in the references and the variant reflects it, so the variant is removed; 3) the position is heterozygous in the references and the variant is homozygous. It goes to the valid variants file but it also go to the Loss Of Heterozygous (LOH) file.
The variant file in analysis it is always the one passed in parameter '--vcf1'.

```
$ phasefilter --help
$ phasefilter --ref1 Ca22chr1A_C_albicans_SC5314.fasta --ref2 Ca22chr1B_C_albicans_SC5314.fasta --vcf1 A-M_S4_chrA_filtered_snps.vcf.gz --vcf2 A-M_S4_chrB_filtered_snps.vcf.gz --out output_dir
```

Eighth possible files will be created after the commands ends. The outputs are from refrence A (ref1) to reference B (ref2), and from reference B (ref2) to reference A (ref1).

-  report_[A]_to_[B].txt - has the statistics about the analysis;
-  valid_[A]_to_[B].vcf.gz - has all variants that are not heterozygous between two references;
-  removed_[A]_to_[B].vcf.gz - has all heterozygous variants;
-  LOH_[A]_to_[B].vcf.gz - has all variants that are loss of heterozygous between two references. This variants are also in 'out_file.vcf.gz' file.

-  report_[B]_to_[A].txt - has the statistics about the analysis from ;
-  valid_[B]_to_[A].vcf.gz - has all variants that are not heterozygous between two references;
-  removed_[B]_to_[A].vcf.gz - has all heterozygous variants;
-  LOH_[B]_to_[A].vcf.gz - has all variants that are loss of heterozygous between two references. This variants are also in 'out_file.vcf.gz' file.

Headings description in report files:

-  **Heterozygous (Removed)**  Heterozygous identified and they go the re remove_[YYY]_to[XXX].vcf.gz file
-  **Keep alleles**   Alleles present in valid_[YYY]_to[XXX].vcf.gz file
-  **LOH alleles Loss of Heterozygous** They are in valid_[YYY]_to[XXX].vcf.gz and LOH_[YYY]_to[XXX].vcf.gz file.
-  **Other than SNP** Other variants thar are not SNPs and INDELs and they go to valid_[YYY]_to[XXX].vcf.gz file
-  **Don't have hit position** Variants that don’t have position in hit (ref B) genome and they go to valid_[YYY]_to[XXX].vcf.gz file
-  **Could Not Fetch VCF Record on Hit**   Variants that are present in source file but not in hit VCF file. They go to valid_[YYY]_to[XXX].vcf.gz file
-  **Total alleles**  All the alleles present in the source vcf file. Analyzed alleles.
-  **Total Alleles new Source VCF**  Total alleles that are in valid_[YYY]_to[XXX].vcf.gz file
-  **Method**   Alignment method.
-  **Alignment %** Percentage of alignment.


## Filter variants in phased genomes but only one direction

This tool do as the same of the previous script but only analysis from Reference A (ref1) to Reference B (ref2)

```
$ phasefilter_single --help
$ phasefilter_single --ref1 Ca22chr1A_C_albicans_SC5314.fasta --ref2 Ca22chr1B_C_albicans_SC5314.fasta --vcf1 A-M_S4_chrA_filtered_snps.vcf.gz --vcf2 A-M_S4_chrB_filtered_snps.vcf.gz --out_vcf out_result.vcf.gz
```

## Synchronize annotation genomes

Synchronize annotations genomes adapting the annotations that are in reference 1 to the reference 2, adding the tags 'StartHit' and 'EndHit' to the result file. In VCF type files only add 'StartHit' tag in Info. The annotations (input file need to be in VCF or GFF3 and belong to the reference 1.

```
$ synchronize_genomes --help
$ synchronize_genomes --ref1 S288C_reference.fna --ref2 S01.assembly.final.fa --gff S288C_reference.gff3 --out result.gff3 --pass_chr chrmt
$ synchronize_genomes --ref1 S288C_reference.fna --ref2 S01.assembly.final.fa --vcf S288C_reference.vcf.gz --out result.vcf.gz
```

## Make alignments

Obtain the percentage of the minimap2 alignment between chromosomes and create an output in ClustalX format.

```
$ make_alignment --help
$ make_alignment --ref1 Ca22chr1A_C_albicans_SC5314.fasta --ref2 Ca22chr1B_C_albicans_SC5314.fasta --out report.txt
$ make_alignment --ref1 Ca22chr1A_C_albicans_SC5314.fasta --ref2 Ca22chr1B_C_albicans_SC5314.fasta --out report.txt --pass_chr chrmt --out_alignment syncronizationSacharo
```

## Reference Statistics

With this application it is possible to obtain the number of nucleotides by chromosome.

```
$ reference_statistics --help
$ reference_statistics --ref some_fasta_file.fasta --out retport.txt
$ reference_statistics --ref Ca22chr1A_C_albicans_SC5314.fasta --out retport.txt
```

## Copy some example data to test all tools

It is possible to copy some example data and test the tools available

```
$ copy_raw_data_example_phasefilter --help
$ copy_raw_data_example_phasefilter --out temp_dir
```

# Documentation

PHASEfilter documentation is available in [ReadTheDocs: PHASEfilter](https://phasefilter.readthedocs.io/en/latest/)
