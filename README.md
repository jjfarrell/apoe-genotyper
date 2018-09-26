# apoe-genotyper
Tool to genotype allelic variants of ApoE protein(e1,e2,e3,e4) using SNPs rs429358 and rs7412 from a phased VCF

Requirements: 
      python 3, 
      pyvcf,
      pysam 
      
      
      rs429358|rs7412|Name
      --------|------|-----
      C       |T     |ε1
      T       |T     |ε2
      T       |C     |ε3
      C       |C     |ε4

Installation

Usage

apoe-genotyper.py  -v VCF -g {GRCh37,GRCh38} -o OUT [-p PROJECT] [-h]
Args                              |Description
----------------------------------|---------------------
-v   --vcf"                       |Phased VCF with APOE snps rs429358 and rs7412" (required)
-g   --genome ["GRCh37","GRCh38"] |GRCh37 or GRCh38 reference genome" (required) 
-o   --out APOE                   |output file prefix (required)
-p   --project                    |Project Name 
-h  --help                        |Help

