Change log
==========

This tab includes a list (chronologically ordered) of notable changes in PHASEfilter.

2020
----

December 20, 2020
.......................

First launch of PHASEfilter.

- Add a new button to delete fastq.gz files that are not attached to any sample ("Remove not processed files") 
- Add a new button to unlock sample metadata tables ("Unlock last file").
- As for nucleotide alignments (see update 30 Oct 2020), amino acid alignments now also include samples with incomplete locus, i.e., undefined amino acids (“X”) are automatically introduced in low coverage regions at a user-selected coverage thresholds. This update will be applied to all novel Projects. Samples within old projects (before this update) will remain unchanged unless any parameter is altered. In that case, the updated samples will be included in the amino acid alignments following the new criteria.
