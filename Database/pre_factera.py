import re

infile=open("gencode.v39.annotation.gtf","r")
outfile=open("exon.bed","w")
gencode={}
for line in infile:
    line=line.strip()
    array=line.split("\t")
    if not line.startswith("#") and re.search('Ensembl_canonical', line):
        genename = line.split("gene_name \"")[1].split("\"")[0]
        trans = line.split("transcript_id \"")[1].split(("\""))[0]
        if array[2]=="exon":
            outfile.write("%s\t%s\t%s\t%s\n"%(array[0],array[3],array[4],genename))
infile.close()

