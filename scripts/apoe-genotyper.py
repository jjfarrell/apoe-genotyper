# APOE-genotyper
# Calls APOE genotype from Phased VCF
#
import argparse
import vcf
import sys
# import pysam

def apoeDose(a1,a2) :
      apoe_dose={"1":0,"2":0,"3":0,"4":0}
      apoe_dose[a1]=apoe_dose[a1]+1
      apoe_dose[a2]=apoe_dose[a2]+1
      return apoe_dose

def callAPOE(rs429358_gt,rs7412_gt):
# function to convert SNP genotypes to APOE Genotypes
      apoe={}
# Check if phased
      if "|" not in rs429358_gt or "|" not in rs7412_gt:
#            print("INFO: VCF File not phased.")
            apoe={'1111':'11',
                  '0111':'12',
                  '1101':'14',
                  '0011':'22',
                  '0001':'23',
                  '0101':'24',
                  '0000':'33',
                  '0100':'34',
                  '1100':'44',
                  '....':'..'}

#                 '0101':'13' ambiguous set to 24 when GT not phased
            rs429358_a=rs429358_gt.split("/")
            rs7412_a= rs7412_gt.split("/")

            gt=''.join(sorted(rs429358_a[0]+rs429358_a[1])+sorted(rs7412_a[0]+rs7412_a[1]))
            if "." in gt:
                  gt='....'
            apoe_gt=apoe[gt]
      else:
            #   rs429358/rs7412
            #      TT       CT     CT       CC
#          print("snps:",rs429358_gt,rs7412_gt)
            apoe={'11':'1','01':'2','00':'3','10':'4','..':'.'}
            rs429358_a=rs429358_gt.split("|")
            rs7412_a= rs7412_gt.split("|")
            apoe1= rs429358_a[0]+rs7412_a[0]
            apoe2= rs429358_a[1]+rs7412_a[1]
            apoe_gt=apoe[apoe1]+apoe[apoe2]
            apoe_gt=''.join(sorted(apoe_gt))
      return apoe_gt
# Parse Parameters
args_parser = argparse.ArgumentParser()
args_parser.add_argument("-v","--vcf",help="Phased VCF APOE snps rs429358 and rs7412",required=True)
args_parser.add_argument("-g","--genome",choices=["GRCh37","GRCh38"],help="GRCh37 or GRCh38 reference genome",required=True)
args_parser.add_argument("-o","--out",help="APOE output file prefix",required=True)
args_parser.add_argument("-p","--project",help="Project",default="")

args = args_parser.parse_args()

if args.project=="":
    args.project=args.vcf

f= open(args.out+".tsv","w")
log= open(args.out+".summary.tsv","w")



#set SNP postion based on reference version
genome = args.genome
if args.genome == 'GRCh37':
    chr = '19'
    rs429358_pos =  45411941
    rs7412_pos   =  45412079
elif args.genome == 'GRCh38':
    chr = 'chr19'
    rs429358_pos = 44908684
    rs7412_pos   = 44908822

#read vcf file
print("APOE genotyping VCF file   : " + args.vcf )


vcf_reader = vcf.Reader( filename=args.vcf )

samples = vcf_reader.samples
snp_missing=False
try:
      for record in vcf_reader.fetch(chr, rs429358_pos-1, rs429358_pos):
            rs429358_record = record
except ValueError:
      print("ERROR: Required SNP rs429358 is not found in vcf ")
      snp_missing=True
try:
      for record in vcf_reader.fetch(chr, rs7412_pos-1, rs7412_pos):
            rs7412_record = record
except ValueError:
      print("ERROR: Required SNP rs7412 is not found in vcf.")
      snp_missing-True
if snp_missing:
      sys.exit("ERROR: APOE-Genotyper")

# init counters
apoe_count={'1':0,'2':0,'3':0,'4':0,'.':0}
a=["1","2","3","4"]
apoe_gt_count={}
for a1 in a:
   for a2 in a:
         gt=a1+a2
         gt=''.join(sorted(gt))
         apoe_gt_count[gt]=0
apoe_gt_count['..']=0
apoe_label=['ApoE1','ApoE2','ApoE3','ApoE4','NA   ']
n=len(samples)
if n== 0:
      sys.exit("ERROR: No Samples! Is it a sites only vcf?")
# Print out samples with genotypes
# Header
f.write("project\tsample" +"\t"+ "rs429358_T_C"  +"\t"+ "rs7412_C_T"  +"\t"+ "apoe" + "\te1_dose\te2_dose\te3_dose\te4_dose\n" )
for sample in samples:
    rs429358_GT=rs429358_record.genotype(sample)['GT']
    if "R2" in rs429358_record.INFO.keys():
          rs429358_R2=rs429358_record.INFO['R2']
    else:
          rs429358_R2="NA"
    rs7412_GT  =rs7412_record.genotype(sample)['GT']
    if "R2" in rs7412_record.INFO.keys():
          rs7412_R2  =rs7412_record.INFO['R2']
    else:
          rs7412_R2  = "NA"
    APOE=callAPOE(rs429358_GT,rs7412_GT)
    a1,a2=APOE
    dose=apoeDose(a1,a2)
    apoe_count[a1]= apoe_count[a1]+1
    apoe_count[a2]= apoe_count[a2]+1
    apoe_gt_count[APOE]= apoe_gt_count[APOE]+1
    f.write(args.project+"\t"+sample +"\t"+ rs429358_GT  +"\t"+ rs7412_GT  +"\t"+ APOE + "\t" + str(dose["1"]) + "\t" + str(dose["2"]) + "\t" + str(dose["3"])+ "\t" + str(dose["4"]) + "\n" )
# write out summary
line=args.project+"\t"+str(n)
# print(apoe_count.keys())
for k in sorted(apoe_count.keys()):
    value=apoe_count[k]
    freq=value/(2.0*n)
    line=line+"\t"+str(value)
    line=line+"\t"+"{0:.4}".format(freq)
for k in sorted(apoe_gt_count.keys()):
        freq=apoe_gt_count[k]/(n*1.0)
        line=line+"\t"+str(apoe_gt_count[k])
        line=line+"\t"+"{0:.4}".format(freq)
line=line+"\t"+ str(rs429358_R2)+"\t"+ str(rs7412_R2)
# write out summary
header="project\tNSamples\tAPOE_MISS_N\tAPOE_MISS\tApoE1_N\tApoE1_AF\tApoE2_N\tApoE2_AF\tApoE3_N\tApoE3_AF\tApoE4_N\tApoE4_AF"
# if imputed VCF, INCLUDE R2 Values
for gt in sorted(apoe_gt_count.keys()):
    label="e"+gt
#     print(gt,apoe_label)
    label=label.replace("..","MISSING")
    header=header+"\t"+label+"_n"
    header=header+"\t"+label+"_freq"
header=header+"\trs429358_R2\trs7412_R2"
log.write(header+"\n")
log.write(line+"\n")
f.close()
log.close()

print("APOE genotypes written to: "+args.out+".tsv")
print("Summary counts written to: "+args.out+".summary.tsv")
print("Number of samples        : "+str(n)+" samples")
print("\nAPOE Allele Summary")
for k in sorted(apoe_count.keys()):
    line="ApoE"+k+"\t"
    value=apoe_count[k]
    freq=value/(2.0*n)
    line=line+"\t"+str(value)
    line=line+"\t"+"{0:.4%}".format(freq)
    print(line)
print("\nAPOE Genotype Summary")
for k in sorted(apoe_gt_count.keys()):
        line="ApoE"+k+"\t"
        freq=apoe_gt_count[k]/(1.0*n)
        line=line+"\t"+str(apoe_gt_count[k])
        line=line+"\t"+"{0:.4%}".format(freq)
        print(line)
