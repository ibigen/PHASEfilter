'''
Created on 01/06/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.run_extra_software import RunExtraSoftware
from PHASEfilter.lib.utils.util import Utils

### run command line
# export PYTHONPATH='/home/mmp/git/PHASEfilter'
# python3 -m unittest -v tests.test_run_extra_software
class Test(unittest.TestCase):

	utils = Utils()
	run_extra_software = RunExtraSoftware()
	
	def test_vcf_empty_name(self):
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_dir = self.utils.get_temp_dir()
		chr_name = 'Chr Not found'
		(temp_out_vcf, number_of_records) = self.run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		self.assertEqual(0, number_of_records)
		self.assertTrue(temp_out_vcf is None)
		
	def test_run_extra_software(self):
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_file_name_bgz = self.utils.get_temp_file("temp_file_", ".vcf.gz")
		self.run_extra_software.make_bgz(vcf_file_name, temp_file_name_bgz)
		self.assertTrue(os.path.exists(temp_file_name_bgz))
		self.assertTrue(os.path.getsize(temp_file_name_bgz) > 200)
		
		temp_file_name = self.utils.get_temp_file("temp_file_", ".vcf")
		self.run_extra_software.make_unzip_bgz(temp_file_name_bgz, temp_file_name)
		self.assertTrue(os.path.exists(temp_file_name))
		self.assertTrue(os.path.getsize(vcf_file_name) == os.path.getsize(temp_file_name))
		
		self.utils.remove_file(temp_file_name_bgz)
		self.utils.remove_file(temp_file_name)


"""
	def test_get_position_by_chain(self):
		## test positions by chain
		chain_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/chain/chain_chrA_to_chrB")
		self.assertTrue(os.path.exists(chain_file))
		
		position_to = self.run_extra_software.get_position_by_chain(chain_file, "Ca22chr1A_C_albicans_SC5314",
					"Ca22chr1B_C_albicans_SC5314", 100000)
		self.assertEqual("100003", position_to)
		position_to = self.run_extra_software.get_position_by_chain(chain_file, "Ca22chr1A_C_albicans_SC5314",
					"Ca22chr1B_C_albicans_SC5314", 1000000)
		self.assertEqual("1000031", position_to)
		position_to = self.run_extra_software.get_position_by_chain(chain_file, "Ca22chr1A_C_albicans_SC5314",
					"Ca22chr1B_C_albicans_SC5314", 200000)
		self.assertEqual("200008", position_to)


	def test_get_position_by_chain_file(self):
		## test positions by chain
		chain_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/chain/chain_chrA_to_chrB")
		self.assertTrue(os.path.exists(chain_file))
		
		temp_file = self.utils.get_temp_file("out_chain", ".txt")
		temp_file_2 = self.utils.get_temp_file("out_chain", ".txt")
		temp_file_3 = self.utils.get_temp_file("out_chain", ".txt")
		
		vect_positions = [
			['Ca22chr1A_C_albicans_SC5314', 100000],
			['Ca22chr1A_C_albicans_SC5314', 1000000],
			['Ca22chr1A_C_albicans_SC5314', 200000],
			['Ca22chr1A_C_albicans_SC5314', 200000000],
		]
		### create out file
		with open(temp_file, 'w') as handle_write:
			for data_ in vect_positions:
				handle_write.write("{} {} {}\n".format(data_[0], data_[1], data_[1]))
		
		###  run chain
		self.run_extra_software.get_position_by_chain_and_file(chain_file, temp_file,
					temp_file_2, temp_file_3)
		
		vect_parsed = self.utils.read_text_file(temp_file_2)
		vect_not_parsed = self.utils.read_text_file(temp_file_3)
		
		self.assertEqual(len(vect_positions) - 1, len(vect_parsed))
		for pos, line in enumerate(vect_parsed):
			self.assertTrue(line.split()[0].startswith('Ca22chr1B_C_albicans_SC5314'))
			if pos == 0: self.assertEqual("100003", line.split()[1])
			if pos == 1: self.assertEqual("1000031", line.split()[1])
			if pos == 2: self.assertEqual("200008", line.split()[1])
		self.assertEqual(2, len(vect_not_parsed))
		self.assertTrue(vect_not_parsed[0].startswith('#Deleted in new'))
		
		self.utils.remove_file(temp_file)
		self.utils.remove_file(temp_file_2)
		self.utils.remove_file(temp_file_3)
"""


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_run_extra_software']
	unittest.main()

