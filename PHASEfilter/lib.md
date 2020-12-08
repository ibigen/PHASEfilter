## Internal Dependencies of PHASEfilter/lib
### Desciprtion of Functions
* [lib/constants](lib/constants)/
    - Basic data structure used for nesting the information of genome annotations in GFF3 format. 
    - Some of the error checking functions listed in [lib/ERROR](lib/ERROR)
* [lib/process](lib/process)/
    - Extract specific sequences from genome sequences according to the GFF3 file.
* [lib/utils](lib/utils)
    - Contains the full list of Error codes and the corresponding Error tag

### Functions used by each program (GFF3toolkit/bin/*.py)
* [bin/best_alignment.py](bin/best_alignment.py)/
    - [lib/gff3_/gff3_.py](lib/gff3/gff3.py)
* [bin/phasefilter.py](bin/phasefilter.py)
    - [lib/gff3_/gff3_.py](lib/gff3/gff3.py)
        - Note: If a error type cannot be found in the following four directories, you shall find it here
    - [lib/function4gff](lib/function4gff)/
    - [lib/inter_model](lib/inter_model)/
    - [lib/intra_model](lib/intra_model)/
    - [lib/single_feature](lib/single_feature)/
    - [lib/ERROR](lib/ERROR)
* [bin/reference_statistics.py](bin/reference_statistics.py)
     - [lib/function4gff](lib/function4gff)/
* [bin/synchronize_genomes.py](bin/synchronize_genomes.py)
     - [lib/function4gff](lib/function4gff)/