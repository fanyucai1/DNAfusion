import re

'''
#### following genes were replaced from HGNC database
s/SEPT2/SEPTIN2/
s/SEPT5/SEPTIN5/
s/SEPT6/SEPTIN6/
s/SEPT8/SEPTIN8/
s/SEPT9/SEPTIN9/
s/CXorf67/EZHIP/
'''
hgnc=['SEPTIN2','SEPTIN5','SEPTIN6','SEPTIN8','SEPTIN9','EZHIP','CARS1']
gene=[]
infile=open("cosmic_genelist.txt","r")#download https://cancer.sanger.ac.uk/cosmic/fusion 第一列
outfile=open("fusion.csv","w")
gene.append('ROS1')
gene.append('HLA-A')
for line in infile:
    line=line.strip()
    array=line.split("-")
    if not re.search('HLA-A',line):
        if not array[0].split("_")[0] in gene:
            gene.append(array[0].split("_")[0])
        if not array[1].split("_")[0] in gene:
            gene.append(array[1].split("_")[0])
infile.close()
print ("Gene total number is %s"%(len(gene)))

infile=open("gencode.v39.annotation.gtf","r")
gencode=[]
for line in infile:
    line=line.strip()
    array=line.split("\t")
    if not line.startswith("#") and re.search('Ensembl_canonical',line):
        genename = line.split("gene_name \"")[1].split("\"")[0]
        trans = line.split("transcript_id \"")[1].split(("\""))[0]
        if genename in gene or genename in hgnc:
            if array[2]=="transcript":
                gencode.append(genename)
                outfile.write(">%s_%s,%s:%s-%s\n"%(genename,trans,array[0],array[3],array[4]))
            if array[2]=="exon":
                exon_number=line.split("exon_number ")[1].split((";"))[0]
                outfile.write("%s,%s,%s\n" % (exon_number, array[3], array[4]))
infile.close()

for name in gene:
    if name not in gencode:
        print ("%s not find in gencode datasebase"%(name))
outfile.close()