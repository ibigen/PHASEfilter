
***************************
Installation of PHASEfilter
***************************

Installation of PHASEfilter:
++++++++++++++++++++++++++++

.. code-block:: shell
   $ pip3 install phasefilter

Installation of PHASEfilter in a virtual environment:
+++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: shell
   $ virtualenv phasefilter --python=python3 --prompt "(phasefilter) "
   $ source phasefilter/bin/activate
   (phasefilter) $ pip3 install phasefilter
   ### OR if you want to run the tests
   (phasefilter) $ pip3 install phasefilter --install-option test

Dependecies
+++++++++++

PHASEfilter relies on several bioinformatic software to run:

* lastz >= 1.4
* minimap2 >= 2.0
* blastn >= 2.3   [Optional]
* samtools >= 1.3
* bcftools >= 1.3
* htslib >= 1.3
* bgzip >= 1.3

After that you have three scripts available
+++++++++++++++++++++++++++++++++++++++++++

.. code-block:: shell
   $ best_alignment
   $ phasefilter
   $ reference_statistics
   $ synchronize_genomes
