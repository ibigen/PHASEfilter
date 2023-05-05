'''
Created on 23/05/2022

@author: mmp
'''
from PHASEfilter.lib.utils.util import Utils
from pyliftover import LiftOver

class Chain(object):
    '''
    classdocs
    '''
    utils = Utils()

    def __init__(self, chain_file):
        '''
        Constructor
        '''
        self.chain_file = chain_file
        if not chain_file is None:
            self.lift_over = LiftOver(self.chain_file)


    def has_chain(self):
        """ return true if there is chain """
        return not self.chain_file is None and self.utils.test_file_exists(self.chain_file)

    def has_chain_name(self, seq_name_from, seq_name_to):
        """ return true if there is chain """
        for chain in self.lift_over.chain_file.chains:
            if chain.source_name == seq_name_from and chain.target_name == seq_name_to:
                return True
        return False
    
    def get_position_by_chain(self, seq_name_from, seq_name_to, pos_from):
        """
        :param seq_name_from chr name from
        :param seq_name_to chr name top
        :param pos_from position from
        """
        if self.chain_file is None: return -1
        covert_data = self.lift_over.convert_coordinate(seq_name_from, pos_from)
        if len(covert_data) == 1 and covert_data[0][0].startswith(seq_name_to): return covert_data[0][1]
        return -1
    
    def get_chains(self, seq_name_from, seq_name_to):
        """
        return chains that belong to this chr names
        """
        vect_chains = []
        for chain in self.lift_over.chain_file.chains:
            if chain.source_name == seq_name_from and chain.target_name == seq_name_to:
                vect_chains.append(chain)
        return vect_chains
    
    
