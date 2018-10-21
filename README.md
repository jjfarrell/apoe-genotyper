# apoe-genotyper
Utility to genotype allelic variants of ApoE protein(e1,e2,e3,e4) using two SNPs rs429358 and rs7412 from a phased or unphased VCF.
      
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

For the most accurate genotyping of all the APOE genotypes, the VCF should be phased (eg: eagle or SHAPEI2). This will help distinquish between the ambigous genotypes(e2e4 and e1e3). Without phasing, the e1e3 will default to the more probable e2e4 as e1 is very rare.

# Usage

apoe-genotyper.py  -v VCF -g [GRCh37,GRCh38] -o OUT [-p PROJECT] [-h]

Args                              |Description
----------------------------------|---------------------------------------------------------
-v   --vcf                        |VCF with APOE snps rs429358 and rs7412" (required)
-g   --genome ["GRCh37","GRCh38"] |GRCh37 or GRCh38 reference genome" (required) 
-o   --out                        |APOE output file prefix (required)
-p   --project                    |Project name (replaces VCF filename in output)
-h  --help                        |Help

Two output files are generated:

[output_prefix].tsv This file contains each sample's genotypes in a tab delimited file. Missing is specified with "."


Column|Heading
------|-----------
Column 1 |project
Column 2 |sample 
Column 3 |rs429358_T_C
Column 4 |rs7412_C_T
Column 5 |APOE
Column 6 |e1_dose
Column 7 |e2_dose
Column 8 |e3_dose
Column 9 |e4_dose

[output_prefix].summary.tsv contains tab delimited list of summary information


Column|Description
------|---------------------------
project|Project or VCF name
NSamples|Number of Samples
APOE_MISS_N|Samples missing APOE
APOE_MISS|Samples Missing APOE Frequency
ApoE1_N|Number of alleles with ApoE-1 (very rare)
ApoE1_pct|Per Cent of alleles with APOE-1
ApoE2_N| Number of alleles with ApoE-2
ApoE2_pct|Per Cent of alleles with APOE-1
ApoE3_N| Number of alleles with ApoE-3
ApoE3_pct|Per Cent of alleles with APOE-1
ApoE4_N| Number of alleles with ApoE-4
ApoE4_pct|Per Cent of alleles with APOE-1
eMISSING_n|Number of samples with ApoE Missing Genotype
eMISSING_freq|Frequency of samples with ApoE Missing Genotype
e11_n|Number of samples with ApoE Genotype ε1ε1
e11_freq|Frequency of ε1ε1
e12_n|Number of samples with ApoE Genotype ε1ε2
e12_freq|Frequency of ε1ε2
e13_n|Number of samples with ApoE Genotype ε1ε3
e13_freq|Frequency of ε1ε3
e14_n|Number of samples with ApoE Genotype ε1ε4
e14_freq|Frequency of ε1ε4
e22_n|Number of samples with ApoE Genotype ε2ε2
e22_freq|Frequency of ε2ε2
e23_n|Number of samples with ApoE Genotype ε2ε3
e23_freq|Frequency of ε2ε3
e24_n|Number of samples with ApoE Genotype ε2ε4
e24_freq|Frequency of ε2ε4
e33_n|Number of samples with ApoE Genotype ε3ε3
e33_freq|Frequency of ε3ε3
e34_n|Number of samples with ApoE Genotype ε3ε4
e34_freq|Frequency of ε3ε4
e44_n|Number of Samples with ApoE Genotype ε4ε4
e44_freq|Frequency of ε4ε4
rs429358_R2|rs429358_R2 (If Available from Imputed VCF)
rs7412_R2|rs7412_R2 (If Available from Imputed VCF)

#Examples
python apoe-genotyper --project ADSP --vcf adsp_5k_phased.vcf.gz --out adsp_apoe_5k -g GRCh38 >adsp_apoe_5k.log

Will produce two files:
   adsp_apoe_5k.tsv
   adsp_apoe_5k.summary.tsv
   adsp_apoe_5k.log

