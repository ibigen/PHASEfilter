
***************************
Installation of PHASEfilter
***************************

Installation of PHASEfilter
+++++++++++++++++++++++++++

.. code-block::
   $ pip3 install phasefilter

Installation of PHASEfilter in a virtual environment
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block::
   $ virtualenv phasefilter --python=python3 --prompt "(phasefilter) "
   $ source phasefilter/bin/activate
   (phasefilter) $ pip3 install phasefilter
   ### OR if you want to run the tests
   (phasefilter) $ pip3 install phasefilter --install-option test


After that you have four scripts available:

.. code-block::
   $ phasefilter
   $ make_alignment
   $ reference_statistics
   $ synchronize_genomes
   
Dependecies
+++++++++++

PHASEfilter relies on several bioinformatic software to run:

-  minimap2 >= 2.2
-  samtools >= 1.3
-  bcftools >= 1.3
-  htslib >= 1.3
-  bgzip >= 1.3


