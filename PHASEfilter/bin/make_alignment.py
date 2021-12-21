#!/usr/bin/env python3
# encoding: utf-8
'''
best_alignment -- shortdesc

Create a list with the best algorithm to make the alignment between chromosomes.

@author:	 mmp

@copyright:  2019 iBiMED. All rights reserved.

@license:	license

@contact:	monsanto@ua.pt

@deffield	updated: Updated
'''
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.process.process_references import ProcessTwoReferences
from PHASEfilter.lib.utils.software import Software
from PHASEfilter.lib.constants import version
import os, re, sys

# export PYTHONPATH='/home/mmp/git/PHASEfilter'
# python3 /home/mmp/git/PHASEfilter/PHASEfilter/bin/make_alignment.py 
#   --ref1 /home/projects/ua/candida/compare_A_vs_B/ref/genomeA/Ca22chr1A_C_albicans_SC5314.fasta 
#	--ref2 /home/projects/ua/candida/compare_A_vs_B/ref/genomeB/Ca22chr1B_C_albicans_SC5314.fasta
#	--out report.txt

# python3 /home/mmp/git/PHASEfilter/PHASEfilter/bin/make_alignment.py 
#   --ref1 /home/projects/ua/candida/compare_A_vs_B/ref/genomeA/C_albicans_SC5314_chrA_A22_chromosomes.fasta
#	--ref2 /home/projects/ua/candida/compare_A_vs_B/ref/genomeB/C_albicans_SC5314_chrB_A22_chromosomes.fasta
#	--out_alignment /home/projects/ua/candida/compare_A_vs_B/ref/syncronization
#	--out report.txt

# python3 /home/mmp/git/PHASEfilter/PHASEfilter/bin/make_alignment.py
# 	--ref1 /usr/local/databases/references/yeast/S288C/S288C_reference_chr_names_cleaned.fna
# 	--ref2 /home/projects/ua/rita_guimaraes/syncronizationSacharo/S01.assembly.final.fa
# 	--pass_chr chrmt
# 	--out report.txt
# 	--out_alignment /home/projects/ua/rita_guimaraes/syncronizationSacharo

## --ref1 /home/projects/ua/candida/compare_A_vs_B/ref/genomeA/Ca22chr2A_C_albicans_SC5314.fasta --ref2 /home/projects/ua/candida/compare_A_vs_B/ref/genomeB/Ca22chr2B_C_albicans_SC5314.fasta --out /home/projects/ua/candida/compare_A_vs_B/out_lignment/report.txt --out_alignment /home/projects/ua/candida/compare_A_vs_B/out_lignment
## --ref1 /home/projects/ua/candida/compare_A_vs_B/ref/genomeA/C_albicans_SC5314_chrA_A22_chromosomes.fasta --ref2 /home/projects/ua/candida/compare_A_vs_B/ref/genomeB/C_albicans_SC5314_chrB_A22_chromosomes.fasta --out /home/projects/ua/candida/compare_A_vs_B/out_lignment/report.txt --out_alignment /home/projects/ua/candida/compare_A_vs_B/out_lignment

from optparse import OptionParser

__all__ = []
__version__ = version.VERSION_make_alignement
__date__ = '2020-05-01'
__updated__ = '2021-10-26'

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
	Make the align of two nucleotide sequences. It accept 3 mandatory parameters and two optional parameters.
	Creates a report to identify the percentage of alignment.
	Has optional can save the alignments between chromossomes and create new references based on bases that are ambiguous between synchronized positions in chromosomes.
	''' # optional - give further explanation about what the program does
	program_license = "Copyright 2020 (iBiMED)											\
				Licensed under the MIT\nhttps://spdx.org/licenses/MIT.html"

	if argv is None:
		argv = sys.argv[1:]

		# setup option parser
		parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
		parser.add_option("--ref1", dest="reference_1", help="[REQUIRED] reference for genome 1", metavar="FILE")
		parser.add_option("--ref2", dest="reference_2", help="[REQUIRED] reference for genome 2", metavar="FILE")
		parser.add_option("--out", dest="outfile", help="[REQUIRED] report in tab separated value (tsv)", metavar="FILE")
		parser.add_option("--pass_chr", dest="pass_chr", help="[Optional] name of chromosomes to not processed. More than one chr splitted by comma, example 'chrI,chrII'")
		parser.add_option("--out_alignment", dest="out_alignment", help="[Optional] save the aligments, one for each synchronized chromosome.'", metavar="PATH")
		parser.add_option("--out_new_reference", dest="out_new_reference", help="[Optional] create new reference for ref1 that has IUPAC codes for bases that are ambiguous between synchronized positions in chromosomes.'", metavar="FILE")

		# process options
		(opts, args) = parser.parse_args(argv)
		checkRequiredArguments(opts, parser)
			
		if opts.reference_1:       print("reference 1          = %s" % opts.reference_1)
		if opts.reference_2:       print("reference 2          = %s" % opts.reference_2)
		if opts.outfile:           print("out file             = %s" % opts.outfile)
		if opts.pass_chr:          print("not processed chr.   = %s" % opts.pass_chr)
		if opts.out_alignment:     print("out path alignments  = %s" % opts.out_alignment)
		if opts.out_new_reference:  print("out file new ref.   = %s" % opts.out_new_reference)

		if (opts.reference_1 == opts.reference_2): sys.exit("Error: you have the same reference file")
		
		utils.test_file_exists(opts.reference_1)
		utils.test_file_exists(opts.reference_2)

		### create path for out alignments
		if (opts.out_alignment and not os.path.exists(opts.out_alignment)):
			os.makedirs(opts.out_alignment, exist_ok=True)
			
		process_two_references = ProcessTwoReferences(opts.reference_1, opts.reference_2, 
					opts.outfile, opts.out_alignment, opts.out_new_reference)
		
		### test all software needed to run this script
		software = Software()
		software.test_softwares()
		
		### parse pass ref
		if (opts.pass_chr): vect_pass_chr = [_.lower() for _ in opts.pass_chr.split(',')]
		else: vect_pass_chr = []
		
		### test output file
		if (os.path.exists(opts.outfile)):
			read_input = input("Output file '{}' already exist, do you want to replace it? [y|Y] ".format(opts.outfile))
			if (len(read_input.strip()) > 0 and read_input.upper() != 'Y'): sys.exit("Exit by the user.")
			
		## make dir if does not exist
		utils.make_path(os.path.dirname(opts.outfile))
		if opts.out_new_reference: utils.make_path(os.path.dirname(opts.out_new_reference))
		
		## process
		process_two_references.process(vect_pass_chr)

if __name__ == "__main__":

	sys.exit(main())


