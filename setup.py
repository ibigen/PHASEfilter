import setuptools
from constants.constants import Constants
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

## python setup.py sdist bdist_wheel
## python3 -m twine upload dist/*
## to test in virtual env
## python3 -m pip install dist/PHASEfilter-0.1-py3-none-any.whl --install-option test


with open("README.md", 'r') as fh:
	long_description = fh.read()

class bdist_wheel(_bdist_wheel):
	def finalize_options(self):
		_bdist_wheel.finalize_options(self)
		# Mark us as not a pure python package
		self.root_is_pure = False
		
setuptools.setup(
	name='PHASEfilter',
	version=Constants.VERSION_package,
	scripts=['phasefilter.py', 'best_alignment.py', 'reference_statistics.py', 'synchronize_genomes.py'],
	author="Miguel Pinheiro",
	author_email="monsanto@ua.pt",
	description="Software package to filter variants, SNPs and INDELs, that are present in heterozygous form, in phased genomes.",
	long_description_content_type="text/markdown",
	url="https://github.com/ibigen/PHASEfilter",
	packages=setuptools.find_packages(),
	license='MIT',
	include_package_data=True, # include other files
	classifiers=[
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 3 - Alpha',
		
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Operating System :: MacOS :: MacOS X",
		"Intended Audience :: Science/Research",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
	],
	install_requires=[
		"pyvcf==0.6.8",
		"pysam==0.15.2",
		"biopython==1.78",
		"gff3tool==2.0.1",
		"wheel",
	],
	entry_points={
		'console_scripts': [
			'best_alignment = best_alignment.__main__:main',
			'reference_statistics = reference_statistics.__main__:main',
			'phasefilter = phasefilter.__main__:main',
			'synchronize_genomes = synchronize_genomes.__main__:main',
		],
	},
	tests_require=['tox'],
	
	# Note that this is a string of words separated by whitespace, not a list.
	keywords='filtering synchronize genome bioinformatics ',  # Optional
	
	project_urls={  # Optional
		'Bug Reports': 'https://github.com/ibigen/PHASEfilter/issues',
		'Source': 'https://github.com/ibigen/PHASEfilter',
	},
	
)