import argparse
import csv

# script to join two tables based on values in a certain column
# specify the name of file1, file2, col1, col2

parser = argparse.ArgumentParser(description='Join two tables based on values in columns.')
parser.add_argument('--file1', help='The name of the first file')
parser.add_argument('--file2', help='The name of the second file')
parser.add_argument('--col1', help='The column in file1 to join on')
parser.add_argument('--col2', help='The column in file2 to join on')
parser.add_argument('-s', '--stub', help='The output file with the combined data')
args = parser.parse_args()

col1=int(args.col1)-1
col2=int(args.col2)-1
file1=args.file1
file2=args.file2

f1_dictionary = {}
f1_file = open(file1)
for line in f1_file:
    line=line.rstrip()
    values = line.split()
    if values:
      f1_dictionary[values[col1]] = line
f2_dictionary = {}
f2_file = open(file2)
for line in f2_file:
    line=line.rstrip()
    values = line.split()
    if values:
      f2_dictionary[values[col2]] = line

out=args.stub+"_joined.tsv"
out1=args.stub+"_onlyfile1.tsv"
out2=args.stub+"_onlyfile2.tsv"
o = open(out, "w")
o1 = open(out1, "w")
o2 = open(out2, "w")

for key in f1_dictionary:
  if key in f2_dictionary:
    #print(f1_dictionary[key],"\t",f2_dictionary[key])
    o.write(f1_dictionary[key]+"\t"+f2_dictionary[key]+"\n")
  else:
    #print("Not in f2",f1_dictionary[key])
    o1.write(f1_dictionary[key]+"\n")

for key in f2_dictionary:
  if key not in f1_dictionary:
    #print("Not in f1",f2_dictionary[key])
    o2.write(f2_dictionary[key]+"\n")
o.close()
o1.close()
o2.close()