'''
Created on 16/12/2019

@author: mmp
'''
import sys, os
from PHASEfilter.lib.utils.util import Utils, Cigar
from PHASEfilter.lib.utils.blast_two_sequences import BlastTwoSequences
from PHASEfilter.lib.utils.lastz_two_sequences import LastzTwoSequences
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from PHASEfilter.lib.utils.software import Software
from typing import Union

class SliceDimention(object):
	
	TAG_BEGIN = 0
	TAG_EQUAL = 1
	TAG_NOT_EQUAL = 2
	TAG_GAP_ON_A = 3
	TAG_GAP_ON_B = 4
	
	def __init__(self, pos_a_begin: int, pos_a_end: int, pos_b_begin: int, pos_b_end: int, tag: int):
		"""
		each block has a begin and a end for A and a begin and a end for B marked with a TAG
		Possible TAGs:
			1) TAG_EQUAL
			2) TAG_NOT_EQUAL
			3) TAG_GAP_ON_A
			4) TAG_GAP_ON_B
		"""
		self.pos_a_begin = pos_a_begin
		self.pos_a_end = pos_a_end
		self.pos_b_begin = pos_b_begin
		self.pos_b_end = pos_b_end
		self.tag = tag

class SliceSynchronize(object):
	
	def __init__(self, start_position):
		self.start_position = start_position
		self.vect_positions = []
		
	def add_position(self, pos_a_begin: int, pos_a_end: int, pos_b_begin: int, pos_b_end: int, tag_item):
		self.vect_positions.append(SliceDimention(pos_a_begin, pos_a_end, pos_b_begin, pos_b_end, tag_item))
	
	def get_pos_in_target(self, pos_from):
		"""
		Target is the chromosome A, the position is A to B 
		position in this slice,
		returns NONE if GAP
		"""
		for slice_dim in self.vect_positions:
			
#			position_fit = slice_dim.get
			return pos_from
		return None

	def get_pos_in_source(self, pos_to):
		"""
		Source is the chromosome B, the position is B to A 
		position in this slice,
		returns NONE if GAP
		"""
		for slice_dim in self.vect_positions:
			
#			position_fit = slice_dim.get
			return pos_to
		return None

class SynchronizaValues(object):
	
	### set limit seq to sync
	LIMIT_SEQ_SYNC = -20

	def __init__(self):
		"""
		One base position, like VCF specifications
		"""
		self.tag_process = None
		self.pos_a = 1
		self.pos_b = 1
		
		### sync seqs
		self.seq_to_sync_a = ""
		self.seq_to_sync_b = ""
		
	def add_seq_to_sync(self, base_a, base_b):
		"""
		create the sequence to synchronizes tail and heads of different sequences
		"""
		self.seq_to_sync_a = self.seq_to_sync_a[SynchronizaValues.LIMIT_SEQ_SYNC:] + base_a
		self.seq_to_sync_b = self.seq_to_sync_b[SynchronizaValues.LIMIT_SEQ_SYNC:] + base_b

	def clean_seq_to_sync(self):
		"""
		clean seq to sync
		"""
		self.seq_to_sync_a = ""
		self.seq_to_sync_b = ""


class ResultSynchronize(object):

	def __init__(self):
		self.dt_position_chain = {}
		self.vect_start_cut = []


	def process_file(self, start_cut_position_from, result_file_name, sync_values, sync_previous_values):
		"""
		process single file
		"""
		
		## position where starts 
		self.vect_start_cut.append(int(start_cut_position_from))
		
		### read sequences
		seq_from_first = None
		seq_to_first = None
		for record in SeqIO.parse(result_file_name, "fasta"):
			if (record.id.startswith(LiftOverLight.PREFIX_SEQ_NAME_FROM)): seq_from_first = str(record.seq)
			if (record.id.startswith(LiftOverLight.PREFIX_SEQ_NAME_TO)): seq_to_first = str(record.seq)
		
		if (seq_from_first is None): sys.exit("Error: 'from' without sequence alignment. File: {}".format(result_file_name))
		if (seq_to_first is None): sys.exit("Error: 'to' without sequence alignment. File: {}".format(result_file_name))
		
		(self.dt_position_chain[start_cut_position_from], sync_values, sync_previous_values) = self.syncronize_sequences(start_cut_position_from,\
											seq_from_first, seq_to_first, sync_values, sync_previous_values)
		return sync_values, sync_previous_values
	
	
	def syncronize_sequences(self, start_cut_position_from, seq_from, seq_to, sync_values, sync_previous_values):
		"""
		synchronize a slice 
		"""
		## create class
		slice_synchronize = SliceSynchronize(start_cut_position_from)
		
		### new values for this slice
		sync_previous_values.seq_to_sync_a = sync_values.seq_to_sync_a
		sync_previous_values.seq_to_sync_b = sync_values.seq_to_sync_b
		sync_values.clean_seq_to_sync()
		if (len(sync_previous_values.seq_to_sync_a) == 0): b_sync_already = True	## first time that is call
		else: b_sync_already = False
		
		position = 0	## real position in the slice seqeunce
		while position < len(seq_from):
			
			### to search the sync position in next slice
			sync_values.add_seq_to_sync(seq_from[position], seq_to[position])
			
			if (not b_sync_already):
				if (sync_values.seq_to_sync_a == sync_previous_values.seq_to_sync_a and sync_values.seq_to_sync_b == sync_previous_values.seq_to_sync_b):
					b_sync_already = True
				position += 1
				continue
				
			if (sync_values.tag_process is None):		# interaction start
				if (seq_from[position] == "-"): 
					sync_values.tag_process = SliceDimention.TAG_GAP_ON_A
					sync_values.pos_a = 0		## because is one base, need to be put zero in gap a
					sync_previous_values.pos_a = 0
					sync_values.pos_b = 1
				elif (seq_from[sync_values.pos_a] == seq_to[sync_values.pos_b]):
					sync_values.tag_process = SliceDimention.TAG_EQUAL
					sync_values.pos_a = 1
					sync_values.pos_b = 1
				elif (seq_to[position] == "-"): 
					sync_values.tag_process = SliceDimention.TAG_GAP_ON_B
					sync_values.pos_a = 1
					sync_values.pos_b = 0		## because is one base, need to be put zero in gap b
					sync_previous_values.pos_b = 0
				else:
					sync_values.tag_process = SliceDimention.TAG_NOT_EQUAL
					sync_values.pos_a = 1
					sync_values.pos_b = 1
				position += 1
			else:
			## gap
				b_change = False
				if (seq_from[position] == "-" or seq_to[position] == "-"):
					if (seq_from[position] == "-"):
						if (sync_values.tag_process != SliceDimention.TAG_GAP_ON_A):		### change state
							b_change = True
							slice_synchronize.add_position(sync_previous_values.pos_a, sync_values.pos_a,\
										sync_previous_values.pos_b, sync_values.pos_b, sync_values.tag_process)
							sync_previous_values.tag_process = sync_values.tag_process
							sync_values.tag_process = SliceDimention.TAG_GAP_ON_A
						sync_values.pos_b += 1
					elif (seq_to[position] == "-"):
						if (sync_values.tag_process != SliceDimention.TAG_GAP_ON_B):		### change state
							b_change = True
							slice_synchronize.add_position(sync_previous_values.pos_a, sync_values.pos_a,\
										sync_previous_values.pos_b, sync_values.pos_b, sync_values.tag_process)
							sync_previous_values.tag_process = sync_values.tag_process
							sync_values.tag_process = SliceDimention.TAG_GAP_ON_B
						sync_values.pos_a += 1
	
				## equal bases
				elif seq_from[position] == seq_to[position]:
					if (sync_values.tag_process != SliceDimention.TAG_EQUAL):
						b_change = True
						slice_synchronize.add_position(sync_previous_values.pos_a, sync_values.pos_a,\
									sync_previous_values.pos_b, sync_values.pos_b, sync_values.tag_process)
						sync_previous_values.tag_process = sync_values.tag_process						
						sync_values.tag_process = SliceDimention.TAG_EQUAL
					sync_values.pos_a += 1
					sync_values.pos_b += 1
				else:	## different bases
					if (sync_values.tag_process != SliceDimention.TAG_NOT_EQUAL):
						b_change = True 
						slice_synchronize.add_position(sync_previous_values.pos_a, sync_values.pos_a,\
									sync_previous_values.pos_b, sync_values.pos_b, sync_values.tag_process)
						sync_previous_values.tag_process = sync_values.tag_process
						sync_values.tag_process = SliceDimention.TAG_NOT_EQUAL
					sync_values.pos_a += 1
					sync_values.pos_b += 1

				if (b_change):
					sync_previous_values.pos_a = sync_values.pos_a
					sync_previous_values.pos_b = sync_values.pos_b
				position += 1

		return (slice_synchronize, sync_values, sync_previous_values)

	def _get_index_position(self, pos_from, overlap_slice):
		"""
		try to find best index
		need to improve
		"""
		## test the first position
		if (len(self.vect_start_cut) == 1 or (self.vect_start_cut[0] >= pos_from or self.vect_start_cut[1] <= (pos_from - overlap_slice))): return 0	## first
		## test last index
		if ((pos_from + overlap_slice) > self.vect_start_cut[-1]): return len(self.vect_start_cut) -1		## last
		
		## test other ones, the first is never ever
		half_index = (len(self.vect_start_cut) >> 1)
		split_index = half_index
		while True:
			split_index >>= 1
			print("{} <= {}  ---- {} >= {}".format(self.vect_start_cut[half_index], pos_from, self.vect_start_cut[half_index + 1], pos_from))
			if (self.vect_start_cut[half_index] <= pos_from and self.vect_start_cut[half_index + 1] >= pos_from): return half_index
			elif (self.vect_start_cut[half_index] > pos_from):
				if (split_index == 0): half_index -= 1
				half_index -= split_index
			elif (self.vect_start_cut[half_index] < pos_from):
				if (split_index == 0): half_index += 1
				half_index += split_index
				
			if (half_index < 0): half_index = 0
			if (half_index >= len(self.vect_start_cut)): half_index = len(self.vect_start_cut) - 1
		return None
		
		
	def get_pos_in_target(self, pos_from: int, overlap_slice: int) -> Union[int, None]:
		"""
		:param pos_from -> position from seq to convert in target 
		"""
		index = self._get_index_position(pos_from, overlap_slice)
		position = self.dt_position_chain[self.vect_start_cut[index]].get_pos_in_target(pos_from)
		if (not position is None): return position
		
		## try the next one
		if ((index + 1) < len(self.vect_start_cut)):
			return self.dt_position_chain[self.vect_start_cut[index + 1]].get_pos_in_target(pos_from)
		return None

class LiftOverLight(object):
	'''
	This is one base, starts on ONE position
	'''
	SPLIT_SEQUENCES_SIZE_test = 250
	SPLIT_SEQUENCES_SIZE_real = 25000
	OVERLAP_SEQUENCE_SIZE_test = 80
	OVERLAP_SEQUENCE_SIZE_real = 1000
	
	PREFIX_SEQ_NAME_FROM = "from_"
	PREFIX_SEQ_NAME_TO = "to_"
	
	software = Software()

	def __init__(self, reference_from, reference_to, work_directory, impose_minimap2_only = False, b_test_mode = False):
		'''
		Constructor
		'''
		self.utils = Utils("synchronize")
		
		self.reference_from = reference_from
		self.reference_to = reference_to
		self.b_test_mode = b_test_mode
		self.impose_minimap2_only = impose_minimap2_only
		self.work_directory = work_directory
		self.dt_chain = {}
		self.dt_chain_best_method = {}
	
	def _get_temp_files(self, seq_name_from, seq_name_to, star_pos_from, star_pos_to):
		"""
		get temp files
		"""
		return (self._get_temp_file(seq_name_from, self.reference_from, star_pos_from),
			self._get_temp_file(seq_name_to, self.reference_to, star_pos_to))
	
	
	def _get_temp_file(self, seq_name, reference, star_pos):
		"""
		return one file with one sequence
		"""
		
		temp_file = self.utils.get_temp_file("split_file_{}".format(seq_name), ".fasta")
		with open(temp_file, 'w') as handle_write:
			records = []
			records.append(SeqRecord(Seq(str(reference.reference_dict[seq_name].seq)[star_pos : \
					star_pos + (LiftOverLight.SPLIT_SEQUENCES_SIZE_test if self.b_test_mode else LiftOverLight.SPLIT_SEQUENCES_SIZE_real)]), \
					id = seq_name, description=""))
			SeqIO.write(records, handle_write, "fasta")
		return temp_file


	def _get_chr_file(self, reference, seq_name):
		"""
		save a chr from a reference in a file
		"""
		temp_file = self.utils.get_temp_file("chr_file_{}".format(seq_name), ".fasta")
		with open(temp_file, 'w') as handle_write:
			records = []
			records.append(reference.reference_dict[seq_name])
			SeqIO.write(records, handle_write, "fasta")
		return temp_file
		
	
	def _run_mafft(self, number_temp_file, file_from, file_to):

		temp_file_in = self.utils.get_temp_file("join_mafft_o_file", ".fasta")
		temp_file_out = self.utils.get_temp_file("{}_join_mafft_o_file".format(number_temp_file + 1), ".fasta")
		cmd = "cat {} {} > {}".format(file_from, file_to, temp_file_in)
		os.system(cmd)

		cmd = "mafft --maxiterate 1000 --localpair --preservecase --leavegappyregion --thread 3 {} > {}".format(temp_file_in, temp_file_out)
		exist_status = os.system(cmd)
		os.unlink(temp_file_in)
		if (exist_status != 0):
			os.unlink(temp_file_out)
			raise Exception("Fail to run mafft")
		return temp_file_out


	def _get_key_chain_name(self, seq_name_from, seq_name_to):
		"""
		:param seq_name_from
		:param seq_name_to
		:out key name for these two sequences
		"""
		return "{}_{}".format(seq_name_from, seq_name_to)

	
	def get_best_algorithm(self, seq_name_from, seq_name_to):
		"""
		:param seq_name_from
		:param seq_name_to
		:out best software for this chromosomes
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		if key_chain_name in self.dt_chain_best_method: return self.dt_chain_best_method[key_chain_name]
		return None

	def get_pos_in_target(self, seq_name_from: str, seq_name_to: str, pos_from: int) -> Union[int, None]:
		"""
		:param pos_from -> position from seq to convert in target
		:out (position in to ref, if does not have position return left most position)
			-1 to no position  
		IMPORTANT - don't give the best
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		if (Software.SOFTWARE_minimap2_name in self.dt_chain and key_chain_name in self.dt_chain[Software.SOFTWARE_minimap2_name]):
			return self.dt_chain[Software.SOFTWARE_minimap2_name][key_chain_name].get_position_from_2_to(pos_from)
		if (Software.SOFTWARE_blast_name in self.dt_chain and key_chain_name in self.dt_chain[Software.SOFTWARE_blast_name]):
			return self.dt_chain[Software.SOFTWARE_blast_name][key_chain_name].get_position_from_2_to(pos_from)
		if (Software.SOFTWARE_lastz_name in self.dt_chain and key_chain_name in self.dt_chain[Software.SOFTWARE_lastz_name]):
			return self.dt_chain[Software.SOFTWARE_lastz_name][key_chain_name].get_position_from_2_to(pos_from)
		return (-1, -1)

	def get_best_pos_in_target(self, seq_name_from: str, seq_name_to: str, pos_from: int) -> Union[int, None]:
		"""
		:param pos_from -> position from seq to convert in target
		:out (position in to ref, if does not have position return left most position)
			-1 to no position 
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		
		if (self.dt_chain_best_method[key_chain_name] in self.dt_chain and 
				key_chain_name in self.dt_chain[self.dt_chain_best_method[key_chain_name]]):
			return self.dt_chain[self.dt_chain_best_method[key_chain_name]][key_chain_name].get_position_from_2_to(pos_from)
		return (-1, -1)

	def _run_minimap2(self, file_from, file_to):
		"""
		Create a SAM file to get the compare
		"""

		### out file
		temp_file_out = self.utils.get_temp_file("minimap_o_file", ".sam")
		temp_file_out_2 = self.utils.get_temp_file("minimap_o_file_2", ".sam")

		### minimap2 -L ca22_1A.fasta ca22_1B.fasta -a -o temp.sam
		cmd = "{} -L {} {} -a -o {}; awk '{{ print $6 }}' {} > {}".format(\
			self.software.get_minimap2(), \
			file_from, file_to, temp_file_out_2, temp_file_out_2, temp_file_out)
		exist_status = os.system(cmd)
		if (exist_status != 0):
			os.unlink(temp_file_out)
			raise Exception("Fail to run minimap2")
		self.utils.remove_file(temp_file_out_2)
		return temp_file_out


	def get_cigar_sequence(self, sam_file_from_minimap):
		"""
		:out return last line of the output file from minimap2 
		"""
		### open the output file and
		vect_cigar_string = []
		with open(sam_file_from_minimap) as handle_in:
			for line in handle_in:
				temp_line = line.strip()
				if len(temp_line) == 0 or temp_line.startswith("-L"): continue
				vect_cigar_string.append(temp_line)
		return vect_cigar_string


	def _get_path_chain(self, key_chain_name):
		"""
		:out path to a specific chain 
		"""
		return os.path.join(self.work_directory, 'chains', key_chain_name)

	def get_cigar_string(self, method, seq_name_from, seq_name_to):
		"""
		:param software used
		:param seq_name_from
		:param seq_name_to
		:out return cigar for a two references 
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		if (method == Software.SOFTWARE_minimap2_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].vect_cigar_string
		if (method == Software.SOFTWARE_blast_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_cigar_strings()
		if (method == Software.SOFTWARE_lastz_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_cigar_strings()
		return None
	
	def get_count_cigar_length(self, method, seq_name_from, seq_name_to):
		"""
		:param software used
		:param seq_name_from
		:param seq_name_to
		:out return the length match of query, subject and un-match length.
			We don't have the length of the areas that don't match 
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		if (method == Software.SOFTWARE_minimap2_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_count_element()
		if (method == Software.SOFTWARE_blast_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_cigar_count_elements()
		if (method == Software.SOFTWARE_lastz_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_cigar_count_elements()
		return None

	def get_number_cigar_string(self, method, seq_name_from, seq_name_to):
		"""
		:param software used
		:param seq_name_from
		:param seq_name_to
		:out return the number of cigar strings created by the alignment
		
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		if (method == Software.SOFTWARE_minimap2_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_number_cigar_string()
		if (method == Software.SOFTWARE_blast_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_number_alignments()
		if (method == Software.SOFTWARE_lastz_name and method in self.dt_chain and key_chain_name in self.dt_chain[method]):
			return self.dt_chain[method][key_chain_name].get_number_alignments()
		return None
	
	def is_100_percent(self, method, seq_name_from, seq_name_to):
		"""
		:out true if specific method is 100%
		"""
		count_length = self.get_count_cigar_length(method, seq_name_from, seq_name_to)
		if count_length is None: return False
		return count_length.is_100_percent(self.reference_from.get_chr_length(seq_name_from),\
								self.reference_to.get_chr_length(seq_name_to))

	def get_percent_alignment(self, method, seq_name_from, seq_name_to):
		"""
		:out percentage of alignment
		"""
		count_length = self.get_count_cigar_length(method, seq_name_from, seq_name_to)
		if count_length is None: return False
		return count_length.get_percentage_coverage(self.reference_from.get_chr_length(seq_name_from),\
								self.reference_to.get_chr_length(seq_name_to))
				
	def get_method(self, seq_name_from, seq_name_to):
		"""
		:out method used to synchronize
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		vect_methods_out = []
		for soft_name in Software.VECT_SOFTWARE_DO_ALIGNMENT:
			if (soft_name in self.dt_chain and key_chain_name in self.dt_chain[soft_name]):
				vect_methods_out.append(soft_name)
				
		return ",".join(vect_methods_out)

	def get_method_best_method(self, seq_name_from, seq_name_to):
		"""
		get best method
		"""
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		return self.dt_chain_best_method[key_chain_name] if key_chain_name in self.dt_chain_best_method else ""
	
	def synchronize_sequences(self, seq_name_from, seq_name_to):
		"""
		:param seq_from -> name of sequence from 
		:param seq_to -> name of sequence to, target 
		:param work_directory place to save the chain, next run test if exist to read it instead fo run it 
		:out { '<seq_name_from>_<seq_name_to>' : }
		"""

		### get key chan name		
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		if key_chain_name in self.dt_chain: return True				## already in memory
		
		### get match positions to cut
		try:
			temp_file_from = self._get_chr_file(self.reference_from, seq_name_from)
			temp_file_to = self._get_chr_file(self.reference_to, seq_name_to)
		except KeyError:
			return False
		
		print("*" * 50 + "\nMaking minimap2 on {}->{}".format(seq_name_from, seq_name_to))
		result_file_name = self._run_minimap2(temp_file_from, temp_file_to)
		vect_cigar_string = self.get_cigar_sequence(result_file_name)
		
		### process cigar string
		keep_best = True
		if (Software.SOFTWARE_minimap2_name in self.dt_chain):
			self.dt_chain[Software.SOFTWARE_minimap2_name][key_chain_name] = Cigar(vect_cigar_string, keep_best)
		else:
			dt_chain_temp = { key_chain_name : Cigar(vect_cigar_string, keep_best) }
			self.dt_chain[Software.SOFTWARE_minimap2_name] = dt_chain_temp
		
		### do the others, if needed
		if (not self.impose_minimap2_only and not self.is_100_percent(\
					Software.SOFTWARE_minimap2_name, seq_name_from, seq_name_to)):

			### lastz
			lastz_two_sequences = LastzTwoSequences(temp_file_from, temp_file_to)
			print("*" * 50 + "\nMaking lastz on {}->{}".format(seq_name_from, seq_name_to))
			### process cigar string
			if (Software.SOFTWARE_lastz_name in self.dt_chain):
				self.dt_chain[Software.SOFTWARE_lastz_name][key_chain_name] = lastz_two_sequences.align_data()
			else:
				dt_chain_temp = { key_chain_name : lastz_two_sequences.align_data() } 
				self.dt_chain[Software.SOFTWARE_lastz_name] = dt_chain_temp
			
			if not self.is_100_percent(Software.SOFTWARE_lastz_name,\
					seq_name_from, seq_name_to):
				### blastn
				print("*" * 50 + "\nMaking blast on {}->{}".format(seq_name_from, seq_name_to))
				use_multithreading = False
				blast_two_sequences = BlastTwoSequences(temp_file_from, temp_file_to, use_multithreading)
				if (Software.SOFTWARE_blast_name in self.dt_chain):
					self.dt_chain[Software.SOFTWARE_blast_name][key_chain_name] = blast_two_sequences.align_data()
				else:
					dt_chain_temp = { key_chain_name : blast_two_sequences.align_data() } 
					self.dt_chain[Software.SOFTWARE_blast_name] = dt_chain_temp
					
				### get best algignment
				vect_percentage_alignment = []
				vect_percentage_alignment.append([Software.SOFTWARE_minimap2_name,\
					self.get_percent_alignment(Software.SOFTWARE_minimap2_name, seq_name_from, seq_name_to)])
				vect_percentage_alignment.append([Software.SOFTWARE_lastz_name,\
					self.get_percent_alignment(Software.SOFTWARE_lastz_name, seq_name_from, seq_name_to)])
				vect_percentage_alignment.append([Software.SOFTWARE_blast_name,\
					self.get_percent_alignment(Software.SOFTWARE_blast_name, seq_name_from, seq_name_to)])
				vect_percentage_alignment = sorted(vect_percentage_alignment, key=lambda x : x[1], reverse=True)
				self.dt_chain_best_method[key_chain_name] = vect_percentage_alignment[0][0]
			else:
				self.dt_chain_best_method[key_chain_name] = Software.SOFTWARE_lastz_name
		else:		### set best alignment method
			self.dt_chain_best_method[key_chain_name] = Software.SOFTWARE_minimap2_name

		self.utils.remove_file(temp_file_from)
		self.utils.remove_file(temp_file_to)
		self.utils.remove_file(result_file_name)
					
		print("Synchronize chromosome {} -> {} done".format(seq_name_from, seq_name_to))
		return True

	def synchronize_sequences_all_methods(self, seq_name_from, seq_name_to):
		"""
		:param seq_from -> name of sequence from 
		:param seq_to -> name of sequence to, target 
		:param work_directory place to save the chain, next run test if exist to read it instead fo run it 
		:out { '<seq_name_from>_<seq_name_to>' : }
		"""

		### get key chan name		
		key_chain_name = self._get_key_chain_name(seq_name_from, seq_name_to)
		if key_chain_name in self.dt_chain: return True				## already in memory
		
		### get match positions to cut
		temp_file_from = self._get_chr_file(self.reference_from, seq_name_from)
		temp_file_to = self._get_chr_file(self.reference_to, seq_name_to)
		
		result_file_name = self._run_minimap2(temp_file_from, temp_file_to)
		vect_cigar_string = self.get_cigar_sequence(result_file_name)
		
		### minimap2		
		if (not vect_cigar_string is None and len(vect_cigar_string) > 0):
			print("Passed: minimap2 alignment on {}->{}".format(seq_name_from, seq_name_to))

			keep_best = True
			### process cigar string
			if (Software.SOFTWARE_minimap2_name in self.dt_chain):
				self.dt_chain[Software.SOFTWARE_minimap2_name][key_chain_name] = Cigar(vect_cigar_string, keep_best)
			else:
				dt_chain_temp = { key_chain_name : Cigar(vect_cigar_string, keep_best) }
				self.dt_chain[Software.SOFTWARE_minimap2_name] = dt_chain_temp
		
		### lastz
		lastz_two_sequences = LastzTwoSequences(temp_file_from, temp_file_to)
		print("Making lastz on {}->{}".format(seq_name_from, seq_name_to))
		### process cigar string
		if (Software.SOFTWARE_lastz_name in self.dt_chain):
			self.dt_chain[Software.SOFTWARE_lastz_name][key_chain_name] = lastz_two_sequences.align_data()
		else:
			dt_chain_temp = { key_chain_name : lastz_two_sequences.align_data() } 
			self.dt_chain[Software.SOFTWARE_lastz_name] = dt_chain_temp
			
		### blastn
		blast_two_sequences = BlastTwoSequences(temp_file_from, temp_file_to)
		print("Making blast on {}->{}".format(seq_name_from, seq_name_to))
		### process cigar string
		if (Software.SOFTWARE_blast_name in self.dt_chain):
			self.dt_chain[Software.SOFTWARE_blast_name][key_chain_name] = blast_two_sequences.align_data()
		else:
			dt_chain_temp = { key_chain_name : blast_two_sequences.align_data() } 
			self.dt_chain[Software.SOFTWARE_blast_name] = dt_chain_temp
			
		self.utils.remove_file(temp_file_from)
		self.utils.remove_file(temp_file_to)
		self.utils.remove_file(result_file_name)
					
		print("Synchronize chromosome {} -> {} done".format(seq_name_from, seq_name_to))
		return True
