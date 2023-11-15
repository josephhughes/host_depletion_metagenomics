import argparse
import statistics
import csv
from ete3 import NCBITaxa

# python3 combine_mappedreads_hit.py -s viral_mapped_reads/V_17_0451122_A_S11_viral_bowtie2_stats.txt -t diamond/V_17_0451122_A_S11_contig_acc_taxid.txt

parser = argparse.ArgumentParser(description='Combined the information on contig hits, with the species information and the mapping statistics.')
parser.add_argument('-s', '--stats', help='The read mapping stats from weeSAM')
parser.add_argument('-o', '--output', help='The output file with the combined data')
parser.add_argument('-t', '--tax', help='the file with the taxonomy information')
args = parser.parse_args()

ncbi = NCBITaxa()
#ncbi.update_taxonomy_database()

def get_desired_ranks(taxid, desired_ranks):
    lineage = ncbi.get_lineage(taxid)
    #names = ncbi.get_taxid_translator(lineage)
    #print(lineage)
    #print(names)
    lineage2ranks = ncbi.get_rank(lineage)
    ranks2lineage = dict((rank, taxid) for (taxid, rank) in lineage2ranks.items())
    #print(ranks2lineage)
    return {'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}

# viral_mapped_reads/V_17_0451122_A_S11_viral_bowtie2_stats.txt

label=args.stats.strip('_viral_bowtie2_stats.txt')
label=label.lstrip('viral_mapped_reads/')
stats = {}
statfile = open(args.stats, "r")
with statfile as f:
  for line in f:
    line=line.rstrip()
    str = line.split("\t")
    stats[str[0]]=line

taxid = {}
taxfile = open(args.tax, "r")
with taxfile as f:
  for line in f:
    #print(line.rstrip())
    line=line.rstrip()
    str = line.split("\t")
    print(str[0])
    if str[0] in taxid and str[2] in taxid[str[0]]:
      taxid[str[0]][str[2]] += 1
      print(str[0],str[2])
    elif str[0] in taxid:
      taxid[str[0]][str[2]] = 1
    else:
      taxid[str[0]]={}
      taxid[str[0]][str[2]] = 1
      print(str[0],str[2])

of = open(args.output, "w")
of.write("Filename\tContig_Name\tRef_Len\tMapped_Reads\tBreadth\t%_Covered\tMin_Depth\tMax_Depth\tAvg_Depth\tStd_Dev\tAbove_0.2_Depth\tAbove_1_Depth\tAbove_1.8_Depth\tVariation_Coefficient\tOrder\tFamily\tGenus\tSpecies\n")
for contig_id, tax in taxid.items():
    #print("\nContig ID:", contig_id)
  if contig_id in stats:
    print(stats[contig_id], end = '')
    of.write(label+"\t"+stats[contig_id])
    #print(list(tax.values()))
    #print(statistics.median(list(tax.values())))
    #print(statistics.mean(list(tax.values())))
    for key in tax:
      if max(list(tax.values())) == tax[key]:
        #print(key + ':', tax[key])
        desired_ranks = ['order', 'family', 'genus', 'species']
        #print(get_desired_ranks(key, desired_ranks))
        tax_info=get_desired_ranks(key, desired_ranks)
        for (rank, taxid) in tax_info.items():
          #print(rank)
          #print(taxid)
          print("\t", end = '')
          of.write("\t")
          if isinstance(taxid, int):
            taxid2name = ncbi.get_taxid_translator([taxid])
            for (id, name) in taxid2name.items():
              print(name, end = '')
              of.write(name)
          else:
            print(taxid, end = '')
            of.write(taxid)
    print()
    of.write("\n")
  else:
    of.write(label+"\t"+contig_id+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n")
of.close()

