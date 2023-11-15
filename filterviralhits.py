# input the combined file and create bed files for each virus species
# use the bed file to count the number of unique reads mapping to each species
# samtools view -b -L test.bed viral_mapped_reads/V_18_0403076_E_S3_viral_bowtie2.bam
# samtools view -F 260 -L V_18_Influenza_A_virus.bed viral_mapped_reads/V_18_0403076_E_S3_viral_bowtie2.bam | cut -f 1 | sort |  uniq | wc -l
# python3 filterviralhits.py -c viral_mapped_reads/V_18_0403076_E_S3_summary.txt -o test -s V_18 -b viral_mapped_reads/V_18_0403076_E_S3_viral_bowtie2.bam
# python3 filterviralhits.py -c viral_mapped_reads/V_18_0403076_E_S3_summary.txt -o viral_mapped_reads/V_18_0403076_E_S3_per_virus.txt -s viral_mapped_reads/V_18_0403076_E_S3 -b viral_mapped_reads/V_18_0403076_E_S3_viral_bowtie2.bam

import argparse
import os

parser = argparse.ArgumentParser(description='Script to produce bed file for each file-species and count the uniquely mapping reads.')
parser.add_argument('-c', '--combined', help='The read mapping and species stats combined file')
parser.add_argument('-o', '--output', help='The output file with the combined data')
parser.add_argument('-s', '--stub', help='Stub for the output bed file, species name will be appended')
parser.add_argument('-b', '--bam', help='BAM file with the mapped viral reads')
args = parser.parse_args()

combinedfile = open(args.combined, "r")
species={}
with combinedfile as f:
  next(f)
  for line in f:
    line=line.rstrip()
    str = line.split("\t")
    #print(str)
    if len(str)>17:
      if str[17] in species:
        #print(str[17]) 
        species[str[17]][str[1]]=str[2]
      else:
        species[str[17]] = {}
        #print(str[17]) 
        species[str[17]][str[1]]=str[2]
        
#     else:
#       print("No mapped reads for ",str[1])

summary = open(args.output,"w+")
for species, value in species.items():
    #print(key, '->', value)
    filename=species+".bed"
    filename=filename.replace(" ", "_")
    filename=filename.replace("/", "_")
    filename=args.stub+"_"+filename
    print(filename)
    f= open(filename,"w+")
    for contig in value:
      f.write(contig+"\t1\t"+value[contig]+"\n" )
    f.close()
    cmd="samtools view -F 260 -L "+filename+" "+args.bam+" | cut -f 1 | sort |  uniq | wc -l"
    cnt=os.popen(cmd).read()
    #print(cnt)
    summary.write(species+"\t"+cnt)
summary.close()