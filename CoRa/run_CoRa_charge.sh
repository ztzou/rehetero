# Assumes LSF environment with Anaconda (w. Python 3.6, BioPython),
# Bio++ v. 2.4.0, and ModelOMatic v. 1.04 (development branch) installed.
# Folder must contain Radical.mat

# Notes on defining amino acid partitions in bppml: 
# https://github.com/BioPP/bpp-phyl/blob/master/src/Bpp/Phyl/Model/Codon/AbstractCodonClusterAASubstitutionModel.h
# Amino acids are in alphabetical order (ARNDCQEGHILKMFPSTWYV)
# The default partition (i.e. "partition" parameter not explicitly set) corresponds to the one used in this study.

bpp_basedir=/home/ztzou/.local/bin/

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/ztzou/.local/lib/

#Translate
mkdir -p ./data/cleaned_fasta_AA/
for i in ./data/cleaned_fasta/*.fasta; do f=$(basename $i .fasta); ${bpp_basedir}/bppseqman params=SeqMan.bpp DATA=./data/cleaned_fasta/${f}; done

mv ./data/cleaned_fasta/*.AA.fasta ./data/cleaned_fasta_AA/

#Generate bionj trees from AA sequence
mkdir -p ./data/bionj/
for i in ./data/cleaned_fasta_AA/*.fasta; do f=$(basename $i .fasta); ${bpp_basedir}/bppdist params=Bionj.bpp DATA=${f}; done

#Declutter
mv *.AA.mat ./data/bionj/; mv *.AA.messages ./data/bionj/; mv *.AA.profile ./data/bionj/

mkdir -p ./data/output/

#Run CoRa_charge
for i in ./data/cleaned_fasta/*.fasta; do
  f=$(basename $i .fasta);
  if [ ! -f ./data/output/${f}.CoRa_charge.params.txt ]; then
    ${bpp_basedir}/bppml params=ML.CoRa.iter.charge.bpp DATA=${f}
  fi
done

#Run M0
for i in ./data/cleaned_fasta/*.fasta; do
  f=$(basename $i .fasta);
  if [ ! -f ./data/output/${f}.M0.params.txt ]; then
    ${bpp_basedir}/bppml params=ML.M0.iter.bpp DATA=${f}
  fi
done

#parse output
python parse_CoRa.py