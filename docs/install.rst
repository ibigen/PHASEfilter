
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

   $ virtualenv phasefilter --python=python3 --prompt "(phasefilter 0.3.7) "
   $ source phasefilter/bin/activate
   (phasefilter 0.3.7) $ pip install phasefilter
   
   ### To install all software dependencies of PHASEfilter 
   (phasefilter 0.3.7) $ cd phasefilter/bin/
   (phasefilter 0.3.7) $ ./install_phasefilter_dependencies.sh


.. important::
   When install 'pyvcf', dependent package, and if your setuptools>=58 if goes to throw an error: "error in PyVCF setup command: use_2to3 is invalid."
   Please, use setuptools<58.
   Setuptools>=58 breaks support for use_2to3 thats why you are facing this error.
   
PHASEfilter with conda
++++++++++++++++++++++

Install with conda:

.. code-block:: shell
   :linenos:

   $ wget https://raw.githubusercontent.com/ibigen/PHASEfilter/main/conda/conda_phasefilter_env.yml -O conda_phasefilter_env.yml
   $ conda env create -f conda_phasefilter_env.yml
   $ conda activate PHASEfilter
   $ python -m pip install PHASEfilter
 

After that you have six scripts available:

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


