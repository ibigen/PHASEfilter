'''
Created on 27/05/2020

@author: mmp
'''
import os, vcf
from PHASEfilter.lib.utils.software import Software
from PHASEfilter.lib.utils.util import Utils

class RunExtraSoftware(object):
	'''
	classdocs
	'''

	software = Software()
	utils = Utils()
	
	def __init__(self):
		'''
		Constructor
		'''
		pass
	
	def make_tabix(self, vcf_file):
		"""
		create a index for vcf.gz file
		"""
		if (vcf_file is None): return
		if (not os.path.exists(vcf_file + ".tbi")):
			cmd = "{} {} -p vcf".format(self.software.get_tabix(), vcf_file)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to run tabix.\n{}".format(cmd))
		
	def make_bgz(self, file_name, file_name_bgz):
		"""
		create a bgz file
		"""
		cmd = "{} -c {} > {}".format(self.software.get_bgzip(), file_name, file_name_bgz)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bgzip.\n{}".format(cmd))
		self.make_tabix(file_name_bgz)
	
	def make_unzip_bgz(self, file_name_bgz, file_name):
		"""
		create a bgz file
		"""
		cmd = "{} -cd {} > {}".format(self.software.get_bgzip(), file_name_bgz, file_name)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bgzip.\n{}".format(cmd))
			
	def get_vcf_with_only_chr(self, vcf_file, chr_name, temp_work_dir):
		"""
		:param vcf file in
		:param chr to filter
		:param tmp directory where is possible to create temp files, remove after
		:out return (vcf file with only this chr name, None if there's no records for this VCF chr name,
				number_of_variants -> number of variants in new file)
		"""
		
		temp_vcf_file = self.utils.get_temp_file(chr_name.replace(' ', ''), ".vcf.gz")
		
		if (vcf_file.endswith(".vcf")):
			vcf_file_temp = self.utils.get_temp_file_with_path(temp_work_dir, "tmp_vcf", ".vcf.gz")
			cmd = "{} -c {} > {}".format(self.software.get_bgzip(), vcf_file, vcf_file_temp)
			exist_status = os.system(cmd)
			if (exist_status != 0):
				raise Exception("Fail to run bgzip.\n{}".format(cmd))
			self.make_tabix(vcf_file_temp)
			vcf_file = vcf_file_temp
			
		# bcftools filter xpto.vcf.gz -r 4 | gzip -c - > 
		self.make_tabix(vcf_file)
		cmd = "{} filter {} -r {} | {} -c > {}".format(self.software.get_bcf_tools(), vcf_file,\
						chr_name, self.software.get_bgzip(), temp_vcf_file)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bcftools.\n{}".format(cmd))
		
		### test VCF if has fields
		with open(temp_vcf_file, 'rb') as handle_in:
			vcf_reader = vcf.Reader(handle_in, compressed=True)
			for _ in vcf_reader:
				## create index
				self.make_tabix(temp_vcf_file)
				
				number_of_variants = self.get_variant_number_vcf_file(temp_vcf_file)
				return (temp_vcf_file, number_of_variants)
		
		### returns empty file if there's no variants for a specific chromosome
		self.utils.remove_file(temp_vcf_file)
		return (None, 0)

				
	def get_variant_number_vcf_file(self, vcf_file):
		"""
		:out number of variations in vcf file
		"""
		temp_stats_txt = self.utils.get_temp_file("stats", ".txt")
		cmd = "{} stats {} > {}".format(self.software.get_bcf_tools(), vcf_file,\
				temp_stats_txt)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bcftools.\n{}".format(cmd))
		
		### read data
		vect_data = self.utils.read_text_file(temp_stats_txt)
		
		### remove file
		self.utils.remove_file(temp_stats_txt)
		
		for line in vect_data:
			if (line.find('number of records:') != -1):
				lst_data = line.split()
				if (self.utils.is_integer(lst_data[5])): return int(lst_data[5])
				return 0
		return 0

	
	def concat_vcf(self, temp_work_dir, prefix, extention, outfile_vcf):
		"""
		merge several output files
		/usr/bin/bcftools merge Home/data/*vcf.gz -Oz -o Merged.vcf.gz
		"""
		cmd = "{} concat -Oz -o {} {}".format(self.software.get_bcf_tools(), outfile_vcf,\
				os.path.join(temp_work_dir, "{}*{}".format(prefix, extention)))
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run bcftools.\n{}".format(cmd))


	def vcf_lines_for_position(self, vcf_file_name, chr_name, start, end, file_to_write = None):
		"""
		:param vcf source file_name 
		:param chr_name to filter 
		:param start
		:param end
		:out array with vcf output, empty value if exist file to save
		"""
		if (not file_to_write is None): temp_file = file_to_write
		else: temp_file = self.utils.get_temp_file("out_vcf", ".vcf")
		cmd = "{} {} -p vcf {}:{}-{} >> {}".format(self.software.get_tabix(),\
					vcf_file_name, chr_name, start, end, temp_file)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run tabix.\n{}".format(cmd))
		
		if (file_to_write is None):
			vect_out = self.utils.read_text_file(temp_file)
			self.utils.remove_file(temp_file)
			self.utils.remove_file(temp_file + ".tbi")
			return vect_out
		else:
			return self.utils.read_text_file(temp_file)
		return []

	def get_position_by_chain(self, chain_file, seq_name_from, seq_name_to, pos_from,
					 file_to_write = None, file_to_write_2 = None, file_to_write_3 = None):
		"""
		return position by chain name
		liftOver: liftOver oldFile map.chain newFile unMapped
		:out -1 if didn't found
		"""
		if (not file_to_write is None): temp_file = file_to_write
		else: temp_file = self.utils.get_temp_file("out_chain", ".txt")
		if (not file_to_write_2 is None): temp_file_2 = file_to_write_2
		else: temp_file_2 = self.utils.get_temp_file("out_chain", ".txt")
		if (not file_to_write_3 is None): temp_file_3 = file_to_write_3
		else: temp_file_3 = self.utils.get_temp_file("out_chain", ".txt")
		
		## create temp file
		with open(temp_file, 'w') as handle_write:
			handle_write.write("{} {} {}".format(seq_name_from, pos_from, pos_from))
			
		cmd = "{} {} {} {} {}".format(self.software.get_liftOver(),\
					temp_file, chain_file, temp_file_2, temp_file_3)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run chain.\n{}".format(cmd))
		
		vect_out = self.utils.read_text_file(temp_file_2)
		vect_out_not_mapped = self.utils.read_text_file(temp_file_3)
		if len(vect_out_not_mapped) > 0: return -1
		if len(vect_out) > 0 and vect_out[0].startswith(seq_name_to): return vect_out[0].split()[1]
		
		if (file_to_write is None): self.utils.remove_file(temp_file)
		if (file_to_write_2 is None): self.utils.remove_file(temp_file_2)
		if (file_to_write_3 is None): self.utils.remove_file(temp_file_3)

		return -1

	def get_position_by_chain_and_file(self, chain_file, file_in_bed, file_out, file_unmapped):
		"""
		return position by chain name
		liftOver: liftOver oldFile map.chain newFile unMapped
		:param file_in_bed in bed separated by spaces
		chr1 743267 743268
		chr1 766408 766409
		chr1 773885 773886
		:out file_out
		"""
		cmd = "{} {} {} {} {}".format(self.software.get_liftOver(),\
					file_in_bed, chain_file, file_out, file_unmapped)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			raise Exception("Fail to run chain.\n{}".format(cmd))
		
		return file_out

