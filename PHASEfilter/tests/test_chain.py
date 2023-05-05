'''
Created on 06/07/2022

@author: mmp
'''
import unittest, os

from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.chain import Chain
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.lift_over_simple import LiftOverLight

class Test(unittest.TestCase):

    utils = Utils()
    
    def test_get_position_by_chain(self):
        """
        test by position
        """
        chain_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/chain/chain_chrA_to_chrB_1")
        self.assertTrue(os.path.exists(chain_file))

        chain_instance = Chain(chain_file)
        
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 100000)
        self.assertEqual(100003, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 1000000)
        self.assertEqual(1000031, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 200000)
        self.assertEqual(200008, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 2000000)
        self.assertEqual(2000026, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 2000000)
        self.assertEqual(2000026, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC534", 2000000)
        self.assertEqual(-1, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 98912)
        self.assertEqual(-1, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 98922)
        self.assertEqual(-1, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 98932)
        self.assertEqual(-1, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 98942)
        self.assertEqual(98945, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 98992)
        self.assertEqual(98995, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 99892)
        self.assertEqual(99895, position_to)
        position_to = chain_instance.get_position_by_chain("Ca22chr1A_C_albicans_SC5314",
                    "Ca22chr1B_C_albicans_SC5314", 200000000)
        self.assertEqual(-1, position_to)

    def test_get_position_by_chain2(self):
        """
        test by position
        """
        utils = Utils("synchronize")
        
        chain_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/chain/chain_chrA_to_chrB_2")
        self.assertTrue(os.path.exists(chain_file))
        seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr2A_C_albicans_SC5314.fasta.gz")
        seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr2B_C_albicans_SC5314.fasta.gz")
        self.assertTrue(os.path.exists(seq_file_name_a))
        self.assertTrue(os.path.exists(seq_file_name_b))
        reference_a = Reference(seq_file_name_a)
        reference_b = Reference(seq_file_name_b)
        
        temp_file = utils.get_temp_file("align", ".aln")
        chain_instance = Chain(chain_file)
        position_to = chain_instance.get_position_by_chain("Ca22chr2A_C_albicans_SC5314",
                    "Ca22chr2B_C_albicans_SC5314", 18242)
        self.assertEqual(18240, position_to)
        self.assertEqual(reference_a.get_base_in_position("Ca22chr2A_C_albicans_SC5314", 18242,
                    18242, temp_file),
                    reference_b.get_base_in_position("Ca22chr2B_C_albicans_SC5314", 18240,
                    18240, temp_file))
        
        position_to = chain_instance.get_position_by_chain("Ca22chr2A_C_albicans_SC5314",
                    "Ca22chr2B_C_albicans_SC5314", 18252)
        self.assertEqual(18250, position_to)
        self.assertEqual(reference_a.get_base_in_position("Ca22chr2A_C_albicans_SC5314", 18252,
                    18252, temp_file),
                    reference_b.get_base_in_position("Ca22chr2B_C_albicans_SC5314", 18250,
                    18250, temp_file))
        
        position_to = chain_instance.get_position_by_chain("Ca22chr2A_C_albicans_SC5314",
                    "Ca22chr2B_C_albicans_SC5314", 18253)
        self.assertEqual(18251, position_to)
        self.assertEqual(reference_a.get_base_in_position("Ca22chr2A_C_albicans_SC5314", 18253,
                    18253, temp_file),
                    reference_b.get_base_in_position("Ca22chr2B_C_albicans_SC5314", 18251,
                    18251, temp_file))
        self.utils.remove_file(temp_file)


    def test_alignment_file(self):
        """
        create an alignment file
        """
        
        chain_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/chain/chain_chrA_to_chrB_2")
        self.assertTrue(os.path.exists(chain_file))
        
        utils = Utils("synchronize")
        temp_work_dir = utils.get_temp_dir()
    
        seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr2A_C_albicans_SC5314.fasta.gz")
        seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/ref/Ca22chr2B_C_albicans_SC5314.fasta.gz")
        self.assertTrue(os.path.exists(seq_file_name_a))
        self.assertTrue(os.path.exists(seq_file_name_b))
    
        reference_a = Reference(seq_file_name_a)
        reference_b = Reference(seq_file_name_b)
        lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, chain_file)
        
        ### save alignment
        seq_name_a = reference_a.get_first_seq()
        self.assertEqual("Ca22chr2A_C_albicans_SC5314", seq_name_a)
        seq_name_b = reference_b.get_chr_in_genome(seq_name_a)
        self.assertEqual("Ca22chr2B_C_albicans_SC5314", seq_name_b)

        temp_out_file = utils.get_temp_file_with_path(temp_work_dir, "align", ".aln")
        b_test = True
        temp_out_file = lift_over_ligth.create_alignment_file_chain(temp_out_file, seq_name_a, seq_name_b, b_test)
        self.assertFalse(temp_out_file is None)
        self.assertTrue(os.path.exists(temp_out_file))
        
        out_result_expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/chain/alignment_out_2.aln')
        self.assertTrue(os.path.exists(out_result_expected))
        temp_diff = utils.get_temp_file_with_path(temp_work_dir, "diff", ".txt")        
        cmd = "diff {} {} > {}".format(out_result_expected, temp_out_file, temp_diff)
        os.system(cmd)
        vect_result = utils.read_text_file(temp_diff)
        self.assertEqual(0, len(vect_result))
        
        #####
        percentage_mapped = lift_over_ligth.get_percent_alignment_chain(seq_name_a, seq_name_b)
        self.assertAlmostEqual(99.954, percentage_mapped, places=3)
        self.utils.remove_dir(temp_work_dir)
        
        
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()