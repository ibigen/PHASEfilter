'''
Created on 20/05/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.lastz_two_sequences import LastzTwoSequences, LastzAlignments
from PHASEfilter.lib.utils.util import CountLength

class Test(unittest.TestCase):

	def test_parse_lastz(self):
		
		use_multithreading = False
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1A.fasta")
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/ref_ca22_1B.fasta")
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
		
		debug = True
		lastz_two_sequences = LastzTwoSequences(seq_file_name_a, seq_file_name_b, debug, use_multithreading)
		lastz_alignments = lastz_two_sequences.align_data()
		self.assertEqual(["35769M1I9181M1I1214M1I23763M"], lastz_alignments.get_cigar(0).get_vect_cigar_string())
		self.assertEqual(1, lastz_alignments.get_number_alignments())
		self.assertEqual("69927\t69930\t0\t69927\t0\t3\t100.0", str(lastz_alignments.get_cigar_count_elements()))

	def test_lastz_overlap(self):
		
		use_multithreading = False
		debug = True
		lastz_alignments = LastzAlignments(debug, use_multithreading)
		
		# name1,start1,end1,name2,start2,end2,strand2,cigar
		line_to_add = "seq1 1 233013 seq2 1 232981 + 7052M1I21591M1D67M2I172M3I1116M1I1521M1I312M1I17M1D510M1I88" +\
			"M2I6154M1I34M1I847M1D125M2D3401M2D11050M1D26M1D213M1I6020M1I428M1I2730M1I782M1D390M3D1603M1I7569M1D" +\
			"2367M1D5871M2D1241M1I3128M1I679M1D2216M2I890M1D123M2D1855M1D221M1D13838M1I5038M1D46M1I354M1I431M1D1" +\
			"4256M1D2209M1D3166M1I119M1D1488M1D491M1I3178M1I7691M1D44M3D421M1I886M1D105M1D437M1I819M1D943M1I2326" +\
			"M1D310M1I432M1D600M1I1914M1I429M1D385M1D1666M3D476M2D623M1I2177M2I2005M2I2807M2D958M1D1413M1D34M1I8" +\
			"5M2D840M1D1997M3I1808M3D490M1I22M2D5645M2D170M3I4234M1D166M1I154M1D6572M1D45M2D912M1D51M1D272M2D338" +\
			"M1I107M2D53M1D25M1D1793M2D31M1D6327M1D9393M1I523M1D1384M1I306M1I2275M1D1343M1I93M1I2552M2D3650M1D54" +\
			"6M3D1843M3D773M1D2451M1I1710M1I2857M1D2164M"
		lastz_alignments.add_new_alignment(line_to_add)
		line_to_add = "seq1 232541 414294 seq2 232512 414247 + 21M11I16M7I16M14I14M2I11M4D22M2I11M8I16M4D9M18D5M" +\
			"3D11M3I24M3D10M2D13M13D21M2I13M2D37M2I29M12I23M8D20M6I7M4D9M4D16M6D28M1D16850M3D591M1D16144M2I546M1" +\
			"D1155M3I1647M3D317M2I933M1D129M2D207M1I490M1I1040M3D70M1I93M1D177M1D347M1I219M1I19M1D31M1D3678M3I22" +\
			"8M3I155M1I365M2D90M1D110M3D3872M2I1418M1I2098M2D768M3I1377M3I791M2D216M1D1213M3I845M2I117M3I693M1D5" +\
			"98M1I1935M1D348M3D1496M1I55M1I7942M1D1808M1D2546M1D426M1D2778M3I544M1I5569M1I1265M2D144M1D466M3D114" +\
			"4M1D3490M1I381M1D291M1I81M1D1822M3D464M2D211M2D38M1D489M2I2320M2D155M1I121M2I21M1D79M1I81M1I97M1D17" +\
			"8M1I160M1I111M1D2174M1D80M2D111M1I640M1D591M3I1130M3D187M1I25M3D374M2D1612M1I271M1D297M1D8967M1I89M" +\
			"1D75M1I1348M3D380M1I7943M1I2770M1I561M1D883M1I1529M1D43M1I126M3D1174M2I136M2D4384M1I5945M1I2697M1D5" +\
			"240M1I2677M3D400M1D1818M1D379M1I211M2I112M1I88M1I2573M1I42M1D1642M2D105M1I2765M1I1883M2I7071M1D124M" +\
			"1I367M1I2318M1I418M1I5554M3D9M3D7M10D4M2I34M8I18M5I13M4D3M2D53M"
		lastz_alignments.add_new_alignment(line_to_add)
		line_to_add = "seq1 414132 860563 seq2 414092 860521 + 13013M3I3061M1I285M2I1904M2D1261M1D2585M1I1426M2I" +\
			"5444M1D1328M1I4633M2D3771M1D171M1I1174M1D2527M1I690M2D36M1D330M1I1094M1I1875M1D391M1D40M1I90M2D6416" +\
			"M3D5265M2D448M3D174M2D100M1D15M2I69M1I35M1I35M3D161M2D60M3I1284M2I4024M1I1863M1D1286M3I92M3I414M2I1" +\
			"6M2I38M1D1947M1I53M1D359M3D439M3D1324M1D248M1D403M3D374M3I1092M3D1837M2D1794M1I430M1D2431M1I2034M1I" +\
			"75M1I1087M1I1600M2I471M1I1728M1I135M1I289M1D75M1D2027M21D668M6I43M3I210M3D30M3I1787M1I734M1I1993M1I" +\
			"2814M2I238M1D210M1I21M1I2309M1I130M1D776M1I48M1I11989M2D25M1I26M1D2713M1I409M3D2337M1D2469M2I7522M1" +\
			"I996M3D1072M1I697M3D3613M2D258M1I295M1D269M1I29M2I347M1D1268M2I1836M3I943M1I4713M1I3036M1D2186M1D36" +\
			"38M2D6003M1D684M2D9377M1I76M2I2445M1D1566M3I3820M1I1804M1I474M3I3168M2D8903M1D1605M1D80M1D1521M1I26" +\
			"M2I1259M3I440M2I102M1I95M2I185M2D409M2D2031M1D107M3I106M2D67M1I4478M1D82M1I21024M1I17M1D445M1D165M1" +\
			"I271M1I2932M1I508M1I1915M1D2417M1I647M3D385M1I3316M1I3888M1D27M1I13479M1I1460M1D145M1D8104M1I3051M1" +\
			"D368M1I1135M1D982M1D174M1D82M1D1091M1I53M2I4022M1D1084M3D1690M2D4037M1D3685M3I1036M3I64M2I547M3D351" +\
			"M3D558M1I740M3D80M1D152M1I276M1D52M3I101M1D480M1I22M3I105M2I206M2I74M1D1354M1D1475M2I26M3I416M1I56M" +\
			"1I45M1D236M1I1188M1D615M3D373M1I242M1D1903M1D2191M3D1386M3D10581M2D47M1D75M2D3826M1I76M3I1814M1D634" +\
			"M1D29M1I143M1I2609M3D108M1D4620M1I6361M1D1216M2D3701M2D310M1I187M1D6436M2I304M1I1777M3I125M3I738M1D" +\
			"121M1I1259M1I170M1D6837M3I7418M1I154M1I6737M1D795M1I5968M2D605M1I93M1I8188M1D5335M2D1144M1I1591M1I4" +\
			"9M1D93M1D72M2I508M1D297M1I3786M1D47M1I3866M1I10M3I870M1I2840M1D476M1D1715M3D1284M1I1268M1D263M1D165" +\
			"M1D49M1D29M1I7978M1I1767M3I79M1D523M1D583M1D5225M1I30M2D3530M1I31M1I1511M1I6044M2D3367M"
		lastz_alignments.add_new_alignment(line_to_add)
		line_to_add = "seq1 860441 1033292 seq2 860410 1033212 + 31M5D75M2D7M4D780M2D10755M1I12759M3I999M1D793M3" +\
			"I1232M2I284M2D184M1D844M1D384M3D152M1I178M3I404M2D1900M2D190M2I3442M18D10186M2I63M1I41M3D67M1I1098M" +\
			"1D505M2I62M1I300M3D1179M3I164M3I1795M4I303M1I439M1I213M2I377M1D384M1I65M3D1418M3I489M3D1138M3D30M2I" +\
			"147M1I3008M2I381M1D325M1D1336M3D1078M3D2438M1D801M1I1154M3D442M1D4290M1I854M2I64M1I201M2D589M2I3305" +\
			"M2I1616M1I8008M1D32M2D1357M1D107M1D26M1D124M3I161M1D1481M3I668M1D33M1I617M3I2116M2I142M1D1747M1D117" +\
			"6M3I25M12D98M6I492M3D456M3D120M2I1271M3D826M1I158M1I1307M3D303M3D1418M1I721M1D24M1I840M1D225M2D1309" +\
			"M3D53M1D3190M1D232M1D519M1D177M1I43M1D822M1D11955M1D4890M1I4995M1D244M1I6372M1D4358M3D8174M3D3889M1" +\
			"D1076M1D2494M1D2643M1I3254M2I8209M"
		lastz_alignments.add_new_alignment(line_to_add)
		line_to_add = "seq1 860449 861929 seq2 860424 862076 + 35769M1I9181"
		lastz_alignments.add_new_alignment(line_to_add)
		line_to_add = "seq1 860452 862120 seq2 860399 861885 + 35769M1I9181"
		lastz_alignments.add_new_alignment(line_to_add)
		line_to_add = "seq1 860452 1033292 seq2 860399 1033212 + 35769M1I9181"
		lastz_alignments.add_new_alignment(line_to_add)
		
		line_to_add = "seq1 860449 861929 seq2 860424 862076 + 35769M1I9181"
		lastz_alignments.add_new_alignment(line_to_add)

#		lastz_alignments.print_all_alignments()
		lastz_alignments.sort_all_alignments()
		self.assertEqual(860449, lastz_alignments.vect_alignments[-3].start_query)
		self.assertEqual(860452, lastz_alignments.vect_alignments[-2].start_query)
		self.assertEqual(1033292, lastz_alignments.vect_alignments[-2].end_query)
		self.assertEqual(860452, lastz_alignments.vect_alignments[-1].start_query)
		self.assertEqual(862120, lastz_alignments.vect_alignments[-1].end_query)
#		lastz_alignments.print_all_alignments()
		
		###		remove overlap alignments
#		lastz_alignments.print_all_alignments()
		lastz_alignments.remove_overlap_alignments()
#		lastz_alignments.print_all_alignments()
		
		self.assertEqual("Make cigar, Query: 1-233013  len(233012)    Subject: 1-232981  len(232980)", str(lastz_alignments.vect_alignments[0]))
		self.assertEqual("50M1D546M3D1843M3D773M1D2451M1I1710M1I2857M1D2164M", lastz_alignments.vect_alignments[0].get_cigar_string()[len(lastz_alignments.vect_alignments[0].get_cigar_string()) - 50:])
		self.assertEqual("M -> 7052", str(lastz_alignments.vect_alignments[0].cigar.vect_positions[0][0]))
		self.assertEqual("I -> 1", str(lastz_alignments.vect_alignments[0].cigar.vect_positions[0][1]))
		self.assertEqual("Make cigar, Query: 233015-414131  len(181116)    Subject: 232983-414091  len(181108)", str(lastz_alignments.vect_alignments[1]))
		self.assertEqual("16850M3D591M1D16144M2I546M1D1155M3I1647M3D317M2I93", lastz_alignments.vect_alignments[1].get_cigar_string()[:50])
		self.assertEqual("M -> 16850", str(lastz_alignments.vect_alignments[1].cigar.vect_positions[0][0]))
		self.assertEqual("D -> 3", str(lastz_alignments.vect_alignments[1].cigar.vect_positions[0][1]))
		self.assertEqual("Make cigar, Query: 414132-860563  len(446431)    Subject: 414092-860521  len(446429)", str(lastz_alignments.vect_alignments[2]))
		self.assertEqual("Make cigar, Query: 860565-1033292  len(172727)    Subject: 860523-1033212  len(172689)", str(lastz_alignments.vect_alignments[3]))

		count_element = CountLength()
		self.assertEqual("Query length	Subject length	missmatch	Match length	Del length	Ins length	% Match VS Del+Ins", str(count_element.get_header()))
		self.assertEqual("1033290\t1033210\t0\t1032770\t520\t440\t99.9", str(lastz_alignments.get_cigar_count_elements()))
		
	def test_lastz_remove_overlap_2(self):
	
		use_multithreading = False
		debug = True
		lastz_alignments = LastzAlignments(debug, use_multithreading)
	
		aln_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/lastz/lastz_result.aln")
		self.assertTrue(os.path.exists(aln_file_name))
	
		### parse file
		## <name1> <start1> <end1> <name2> <start2> <end2> <strand2> [<score>] [#<comment>]
		## where <name1>, etc. correspond to the target sequence and <name2>, etc. correspond to the query. Fields are delimited by whitespace. 
		with open(aln_file_name) as handle:
			for line in handle:
				sz_temp = line.strip()
				if (len(sz_temp) == 0 or sz_temp.startswith('#')): continue
				### add new alignments
				lastz_alignments.add_new_alignment(sz_temp)
	
		### sort alignments
#		lastz_alignments.print_all_alignments()
		lastz_alignments.remove_overlap_alignments()
#		lastz_alignments.print_all_alignments()

		self.assertEqual("Make cigar, Query: 1286540-1733200  len(446660)    Subject: 1286558-1733218  len(446660)", str(lastz_alignments.vect_alignments[5]))
		self.assertEqual("Make cigar, Query: 1733204-2007383  len(274179)    Subject: 1733222-2007299  len(274077)", str(lastz_alignments.vect_alignments[6]))
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_parse_blast']
	unittest.main()