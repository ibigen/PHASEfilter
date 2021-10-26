
************
Installation
************

Regular Install
+++++++++++++++

Install directly with pip:

.. code-block:: shell
   :linenos:
   
   $ pip3 install phasefilter

.. important::
   When install 'pyvcf', dependent package, and if your setuptools>=58 it goes to throw an error: "error in PyVCF setup command: use_2to3 is invalid."
   Please, use setuptools<58.
   Setuptools>=58 breaks support for use_2to3 thats why you are facing this error for the package 'pyvcf'.
   
   
PHASEfilter in a virtual environment
++++++++++++++++++++++++++++++++++++

Install with virtual environment:

.. code-block:: shell
   :linenos:

   $ virtualenv phasefilter --python=python3 --prompt "(phasefilter) "
   $ source phasefilter/bin/activate
   (phasefilter) $ pip3 install phasefilter
   ### OR if you want to run the tests
   (phasefilter) $ pip3 install phasefilter --install-option test

.. important::
   When install 'pyvcf', dependent package, and if your setuptools>=58 if goes to throw an error: "error in PyVCF setup command: use_2to3 is invalid."
   Please, use setuptools<58.
   Setuptools>=58 breaks support for use_2to3 thats why you are facing this error.

After that you have five scripts available:

.. code-block:: shell
   :linenos:

   $ phasefilter
   $ phasefilter_single
   $ make_alignment
   $ reference_statistics
   $ synchronize_genomes
   $ copy_raw_data_example_phasefilter
   
Dependecies
+++++++++++

PHASEfilter relies on several bioinformatic software to run:

-  minimap2 >= 2.22
-  samtools >= 1.3
-  bcftools >= 1.3
-  htslib >= 1.3
-  bgzip >= 1.3


