#!/bin/bash
set -e

### remove possible remain files
remove_file () {
        if [[ -f "$1" ]]; then
                rm -rf $1
        fi
}
remove_file "minimap2"
remove_file "k8"
remove_file "libhts.so.3"


#### MINIMAP2
echo "Install minimap2"
mkdir -p external_software/minimap2; cd external_software/minimap2
wget https://github.com/lh3/minimap2/releases/download/v2.24/minimap2-2.24_x64-linux.tar.bz2
tar -jxvf minimap2-2.24_x64-linux.tar.bz2; rm minimap2-2.24_x64-linux.tar.bz2

## make links
cd ../..
ln -s external_software/minimap2/minimap2-2.24_x64-linux/minimap2 minimap2
ln -s external_software/minimap2/minimap2-2.24_x64-linux/k8 k8

#### SAMTOOLS
echo "Install samtools"
cd external_software
wget https://github.com/samtools/samtools/releases/download/1.14/samtools-1.14.tar.bz2
tar -xjvf samtools-1.14.tar.bz2 
cd samtools-1.14/
./configure; make
cp samtools ../..
cd ..
rm -r samtools-1.14*

#### BCFTOOLS
echo "Install bcftools"
wget https://github.com/samtools/bcftools/releases/download/1.14/bcftools-1.14.tar.bz2
tar -xjvf bcftools-1.14.tar.bz2 
cd bcftools-1.14/
./configure; make
cp bcftools ../..
cd ..
rm -r bcftools-1.14*

#### HTSLIB
echo "Install htslib"
wget https://github.com/samtools/htslib/releases/download/1.14/htslib-1.14.tar.bz2
tar -xjvf htslib-1.14.tar.bz2 
cd htslib-1.14/
./configure; make
cp tabix ../..
cp htsfile ../..
cp bgzip ../..
cp libhts.so ../..
cd ..
rm -r htslib-1.14*
cd ..
ln -s libhts.so libhts.so.3

## All done
echo "All done"

