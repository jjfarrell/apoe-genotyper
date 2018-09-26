# apoe-genotyper
Utility to genotype allelic variants of ApoE protein(e1,e2,e3,e4) using two SNPs rs429358 and rs7412 from a phased VCF.
      
rs429358|rs7412|ApoE
--------|------|-----
C       |T     |ε1
T       |T     |ε2
T       |C     |ε3
C       |C     |ε4

# Installation

Requirements: 
      python 3, 
      pyvcf,
      pysam 
# Preparation

For accurate genotyping of the APOE,
# Usage

apoe-genotyper.py  -v VCF -g {GRCh37,GRCh38} -o OUT [-p PROJECT] [-h]

Args                              |Description
----------------------------------|---------------------------------------------------------
-v   --vcf                       |Phased VCF with APOE snps rs429358 and rs7412" (required)
-g   --genome ["GRCh37","GRCh38"] |GRCh37 or GRCh38 reference genome" (required) 
-o   --out                        |APOE output file prefix (required)
-p   --project                    |Project Name (replaces VCF filename in output)
-h  --help                        |Help

Two output files are generated:

{output_prefix}.tsv This file contains the sample genotypes in a tab delimited file.

Column|Description
------|-----------
Column 1 |project
Column 2 |Sample 
Column 3 |rs429358 GT
Column 4 |rs7412 GT
Column 5 |APOE GT

output_prefix.log

Column|Description
------|---------------------------
project|Project or VCF name
NSamples|Number of Samples
ApoE1_N|Number of alleles with ApoE-1 (very rare)
ApoE1_pct|Per Cent of alleles with APOE-1
ApoE2_N| Number of alleles with ApoE-2
ApoE2_pct|Per Cent of alleles with APOE-1
ApoE3_N| Number of alleles with ApoE-3
ApoE3_pct|Per Cent of alleles with APOE-1
ApoE4_N| Number of alleles with ApoE-4
ApoE4_pct|Per Cent of alleles with APOE-1
e11_n|Number of samples with ApoE Genotype ε1ε1
e11_pct
e12_n|Number of samples with ApoE Genotype ε1ε2
e12_pct
e13_n|Number of samples with ApoE Genotype ε1ε3
e13_pct
e14_n|Number of samples with ApoE Genotype ε1ε4
e14_pct
e22_n|Number of samples with ApoE Genotype ε2ε2
e22_pct
e23_n|Number of samples with ApoE Genotype ε2ε3
e23_pct
e24_n|Number of samples with ApoE Genotype ε2ε4
e24_pct
e33_n|Number of samples with ApoE Genotype ε3ε3
e33_pct
e34_n|Number of samples with ApoE Genotype ε3ε4
e34_pct
e44_n|Number of Samples with ApoE Genotype ε4ε4
e44_pct



#Examples
