#!/usr/bin/env python3
# encoding: utf-8
'''
synchronize_genomes.py -- shortdesc

Synchronize annotations genomes adapting the annotations that are in reference 1 to the reference 2, 
adding the tags 'StartHit' and 'EndHit' to the result file. In VCF type files only add 'StartHit' 
tag in Info. The annotations, input file, need to be in VCF or GFF3, and belong to the reference 1.

@author:	 mmp

@copyright:  2019 iBiMED. All rights reserved.

@license:	license

@contact:	monsanto@ua.pt

@deffield	updated: Updated
'''
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.read_gff import ReadGFF
from PHASEfilter.lib.process.process_references import ProcessTwoReferences
from PHASEfilter.lib.utils.software import Software
from PHASEfilter.lib.constants import version
import os, re, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# export PYTHONPATH='/home/mmp/git/PHASEfilter'
# python3 synchronize_genomes.py
#	--ref1 /usr/local/databases/references/yeast/S288C/S288C_reference_chr_names_cleaned.fna
#	--ref2 /home/projects/ua/rita_guimaraes/syncronizationSacharo/S01.assembly.final.fa 
#	--gff /home/projects/ua/rita_guimaraes/syncronizationSacharo/S01.TE.gff3 
#	--out /home/projects/ua/rita_guimaraes/syncronizationSacharo/result.gff
#   --pass_chr chrmt

# python3 synchronize_genomes.py
#	--ref1 /home/projects/ua/rita_guimaraes/syncronizationSacharo/S01.chrI_0_100000.fasta
#	--ref2 /home/projects/ua/rita_guimaraes/syncronizationSacharo/S288C.chrI_0_100000.fasta
#	--gff /home/projects/ua/rita_guimaraes/syncronizationSacharo/S01.TE_chrI_till_100000.gff3 
#	--out /home/projects/ua/rita_guimaraes/syncronizationSacharo/result.gff
#   --pass_chr chrI

# ./synchronize_genomes.py --ref1 /home/projects/ua/candida/compare_A_vs_B/ref/genomeA/C_albicans_SC5314_chrA_A22_chromosomes.fasta --ref2 /home/projects/ua/candida/compare_A_vs_B/ref/genomeB/C_albicans_SC5314_chrB_A22_chromosomes.fasta --vcf /home/projects/ua/candida/compare_A_vs_B/vcf/A-M_S4/A-M_S4_chrA_filtered_snps.vcf --out data.vcf
# ./synchronize_genomes.py --ref1 /usr/local/databases/references/yeast/S288C/S288C_reference_chr_names_cleaned.fna --ref2 /home/projects/ua/rita_guimaraes/syncronizationSacharo/S01.assembly.final.fa --gff /home/projects/ua/rita_guimaraes/syncronizationSacharo/S01.TE.gff3 --out /home/projects/ua/rita_guimaraes/syncronizationSacharo/result.gff --pass_chr chrmt
from optparse import OptionParser

__all__ = []
__version__ = version.VERSION_synchronize_genomes
__date__ = '2020-05-01'
__updated__ = '2021-09-06'

def checkRequiredArguments(opts, parser):
	missing_options = []
	for option in parser.option_list:
		if re.match(r'^\[REQUIRED\]', option.help) and eval('opts.' + option.dest) == None:
			missing_options.extend(option._long_opts)
	if len(missing_options) > 0:
		parser.error('Missing REQUIRED parameters: ' + str(missing_options))


def main(argv=None):
	'''Command line options.'''
	utils = Utils()
	
	program_name = os.path.basename(sys.argv[0])
	program_version = "{}".format(__version__)
	program_build_date = "%s" % __updated__

	program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
	#program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
	program_longdesc = '''
	Synchronize two references and add two new fields (StartHit;EndHit) to the VCF/GFF with the positions on hit reference.
	It accept 4 mandatory parameters and one optional parameters. It is necessary to pass a VCF or a GFF file.
	''' # optional - give further explanation about what the program does
	program_license = "Copyright 2020 (iBiMED)											\
				Licensed under the MIT\nhttps://spdx.org/licenses/MIT.html"

	if argv is None:
		argv = sys.argv[1:]
	
		# setup option parser
		parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
		parser.add_option("--ref1", dest="reference_1", help="[REQUIRED] reference for genome 1", metavar="FILE")
		parser.add_option("--ref2", dest="reference_2", help="[REQUIRED] reference for genome 2", metavar="FILE")
		parser.add_option("--gff", dest="gff", help="[Optional] GFF3 file to set new positions of hit genome (gff3)", metavar="FILE")
		parser.add_option("--vcf", dest="vcf", help="[Optional] VCF file to set new positions of hit genome (vcf)", metavar="FILE")
		parser.add_option("--pass_chr", dest="pass_chr", help="[Optional] name of chromosomes to not processed. More than one chr split by comma, example 'chrI,chrII'")
		parser.add_option("--out", dest="out", help="[REQUIRED] report in tab separated value (tsv)")

		# process options
		(opts, args) = parser.parse_args(argv)
		checkRequiredArguments(opts, parser)
		
		if not opts.gff is None and not opts.vcf is None:
			print("Only one type of file is allowed. You can pass one VCF or one GFF3")
			sys.exit(1)
		if opts.gff is None and opts.vcf is None:
			print("You must pass one file, a VCF or a GFF3 reference, that belongs to the reference 1")
			sys.exit(1)
				
		if opts.reference_1: print("reference 1         = %s" % opts.reference_1)
		if opts.reference_2: print("reference 2         = %s" % opts.reference_2)
		if opts.gff:         print("gff3                = %s" % opts.gff)
		if opts.vcf:         print("vcf                 = %s" % opts.vcf)
		if opts.out:         print("out                 = %s" % opts.out)
		if opts.pass_chr:    print("not processed chr.  = %s" % opts.pass_chr)

		if (opts.reference_1 == opts.reference_2): sys.exit("Error: you have the same reference file")

		utils.test_file_exists(opts.reference_1)
		utils.test_file_exists(opts.reference_2)
		if opts.gff: utils.test_file_exists(opts.gff)
		if opts.vcf: utils.test_file_exists(opts.vcf)
		process_two_references = ProcessTwoReferences(opts.reference_1, opts.reference_2, opts.out)

		### test all software needed to run this script
		software = Software()
		software.test_softwares()

		### parse pass ref
		if (opts.pass_chr): opts.pass_chr = [_.lower() for _ in opts.pass_chr.split(',')]
		else: opts.pass_chr = []
		
		### test output file
		if (os.path.exists(opts.out)):
			read_input = input("Output file '{}' already exist, do you want to replace it? [y|Y] ".format(opts.out))
			if (len(read_input.strip()) > 0 and read_input.upper() != 'Y'): sys.exit("Exit by the user.")

		## make dir if does not exist
		utils.make_path(os.path.dirname(opts.out))
		VECT_TYPE = [ReadGFF.PROCESS_TYPE_all]
		if opts.gff: process_two_references.parse_gff(opts.gff, opts.pass_chr, VECT_TYPE)
		if opts.vcf: process_two_references.parse_vcf(opts.vcf, opts.pass_chr)

		print("File created: {}".format(opts.out))


if __name__ == "__main__":

	sys.exit(main())


