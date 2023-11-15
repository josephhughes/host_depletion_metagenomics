# based on the diamond taxids that match viruses - map reads to those contigs using bwa
# see how many map to each virus
# viruses is superkingdom with taxid 10239
# efetch -db protein -id "AFG70522.1" -format docsum | xtract -pattern DocumentSummary -element TaxId
# cat diamond/V_18_0421327_A_S12.m8 | cut -f 1,2 | sort | uniq > test_S12.txt
# cut -f2 test_S12.txt | sort | uniq > test_S12_acconly.txt
# first occurrence with -m1 
# fgrep -m1 "AFG70522.1" prot.accession2taxid 
# fgrep --color=auto -w -f ~/Documents/ToniRespiratory/test_S12_acconly.txt prot.accession2taxid > test_taxids.txt
# fgrep a bit slow so how about filtering acc2taxid beforehand for the viral
# get all taxon ids below viruses: taxonkit list --ids 10239 --indent "" > 10239.taxid.txt
# filter prot.accession2taxid for viral protein accessions
# awk 'FNR==NR{a[$0]; next} ($3 in a){print $0}' 10239.taxid.txt dead_prot.accession2taxid > viral_dead_prot.accession2taxid
# awk 'FNR==NR{a[$0]; next} ($3 in a){print $0}' 10239.taxid.txt prot.accession2taxid > viral_prot.accession2taxid 
# now searching agst this filtered set
# fgrep -w -f ~/Documents/ToniRespiratory/test_S12_acconly.txt viral_prot.accession2taxid > test_taxids.txt
# join -1 2 -2 2 <(sort -k 2 test_S12.txt ) <(sort -k 2 test_taxids.txt )

diamond=$1
#stub=$(basename $diamond)
#stub=${stub%.*}
stub=${diamond%.*}
#echo $stub
cat $diamond | cut -f 1,2 | sort | uniq > ${stub}_contig_acc.txt
cut -f2 ${stub}_contig_acc.txt | sort | uniq > ${stub}_acc.txt
fgrep -w -f ${stub}_acc.txt ~/mydbs/viral_prot.accession2taxid > ${stub}_acc_taxid.txt
fgrep -w -f ${stub}_acc.txt ~/mydbs/viral_dead_prot.accession2taxid >> ${stub}_acc_taxid.txt
#join -t $'\t' -1 2 -2 1 <(sort -k 2 ${stub}_contig_acc.txt ) <(sort -k 1 ${stub}_acc_taxid.txt ) > ${stub}_contig_acc_taxid.txt
python ~/bin/generic_pipes/metagenomic_with_host_depletion/join_tables_by_col.py --file1 ${stub}_contig_acc.txt --file2 ${stub}_acc_taxid.txt -s ${stub} --col1 2 --col2 1
cut -f1,2,4 ${stub}_joined.tsv | sort | uniq > ${stub}_contig_acc_taxid.tsv
cut -f1 ${stub}_joined.tsv | sort | uniq > ${stub}_viral_contig.txt

