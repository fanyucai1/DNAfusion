import re

infile=open("hgnc.txt","r")
gene=[]
for line in infile:
    gene.append(line.strip())
infile.close()

infile=open("gencode.v39.annotation.gtf","r")
outfile=open("exon.bed","w")
outfile2=open("target.bed","w")
gencode=[]
for line in infile:
    line=line.strip()
    array=line.split("\t")
    if not line.startswith("#"):
        genename = line.split("gene_name \"")[1].split("\"")[0]
        if genename in gene and array[2] == "gene":
            outfile2.write("%s\t%s\t%s\t%s\n" % (array[0], array[3], array[4], genename))
        if re.search('Ensembl_canonical',line):
            if array[2]=="exon":
                outfile.write("%s\t%s\t%s\t%s\n"%(array[0],array[3],array[4],genename))
infile.close()

