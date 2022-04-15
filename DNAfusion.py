#version 1.0 2022.04.08
#Email:yucai.fan@illumina.com
import argparse
import os
import subprocess
from multiprocessing import Process

docker_name="dnafusion:latest"
parser=argparse.ArgumentParser("\n\nDetect dna fusion use genefuse,svict and JuLI.\n\n")
parser.add_argument("-p1","--pe1",help="pe1 fatsq",required=True)
parser.add_argument("-p2","--pe2",help="pe2 fastq",required=True)
parser.add_argument("-d","--database",help="database",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-b","--bed",help="target bed",default="")
args=parser.parse_args()

def shell_run(x):
    subprocess.check_call(x, shell=True)
def shell_run2(a,b):
    subprocess.check_call(a,shell=True)
    subprocess.check_call(b,shell=True)

docker_cmd=""
a=os.path.abspath(args.pe1)
b=os.path.abspath(args.pe2)
if os.path.dirname(a)!=os.path.dirname(b):
    print("%s and %s must be the same directory"%(args.pe1,args.pe2))
indir=os.path.dirname(a)
out_dir=os.path.abspath(args.outdir)
f1=a.split("/")[-1]
f2=b.split("/")[-1]
args.database=os.path.abspath(args.database)
###############genefuse######################
subprocess.call('mkdir -p %s/genefuse/'%(out_dir),shell=True)
docker_raw="docker run -v %s:/opt/ -v %s:/Database/ -v %s/genefuse:/analysis/ %s "%(indir,args.database,out_dir,docker_name)
genefuse=docker_raw+"sh -c \"genefuse -r /Database/GRCh38.p13.genome.fa -f /Database/genefuse/fusion.csv " \
            "-1 /opt/%s -2 /opt/%s -t 24 -h /analysis/%s.html > /analysis/%s.final.txt \"" %(f1,f2,args.prefix,args.prefix)
###############juli######################
subprocess.call('mkdir -p %s/juli/'%(out_dir),shell=True)
docker_raw="docker run -v %s:/opt/ -v %s:/Database/ -v %s/juli:/analysis/ %s "%(indir,args.database,out_dir,docker_name)
mapping=open("%s/juli/mapping.sh"%(out_dir),"w")
mapping.write("bwa mem -t 24 /Database/GRCh38.p13.genome.fa /opt/%s /opt/%s |samtools view -@24 -q20 -b -o /analysis/%s.bam\n"%(f1,f2,args.prefix))
mapping.write("java -Xmx10g -jar /software/picard.jar SortSam INPUT=/analysis/%s.bam OUTPUT=/analysis/%s.sorted.bam SORT_ORDER=coordinate\n"%(args.prefix,args.prefix))
mapping.write("java -Xmx10g -jar /software/picard.jar MarkDuplicates I=/analysis/%s.sorted.bam O=/analysis/%s.marked_duplicates.bam M=/analysis/marked_dup_metrics.txt\n"%(args.prefix,args.prefix))
mapping.write("rm -rf /analysis/%s.bam /analysis/%s.sorted.bam /analysis/marked_dup_metrics.txt /analysis/mapping.sh /analysis/%s.BamStat.txt\n" % ((args.prefix,args.prefix,args.prefix)))
mapping.close()
Juli_a=docker_raw+"sh -c \'sh /analysis/mapping.sh\'"
outfile=open("%s/juli/juli.R"%(out_dir),"w")
outfile.write("library(juliv0.1.6.2)\n"
              "callfusion(CaseBam=\'/analysis/%s.marked_duplicates.bam\',"
              "TestID=\'%s\',"
              "OutputPath=\'/analysis/\',"
              "Thread=48,"
              "Refgene=\'/Database/juliv0.1.6.2_reference_hg38/refGene_hg38.txt\',"
              "Gap=\'/Database/juliv0.1.6.2_reference_hg38/gap_hg38.txt\',"
              "Reference=\'/Database/GRCh38.p13.genome.fa\')\n"%(args.prefix,args.prefix))
outfile.close()
Juli_b=docker_raw +"sh -c \'Rscript /analysis/juli.R\'"
###############svict######################
subprocess.call('mkdir -p %s/svict/'%(out_dir),shell=True)
docker_raw="docker run -v %s/juli/:/opt/ -v %s:/Database/ -v %s/svict/:/analysis/ %s "%(out_dir,args.database,out_dir,docker_name)
svict=docker_raw+" sh -c \'svict -r /Database/GRCh38.p13.genome.fa " \
                      "-i /opt/%s.marked_duplicates.bam -o /analysis/%s -g /Database/genefuse/gencode.v39.annotation.gtf \'"%(args.prefix,args.prefix)
subprocess.check_call(docker_cmd,shell=True)
#####################################
if not os.path.exists ("%s/genefuse/%s.final.txt"%(out_dir,args.prefix)) or not os.path.exists("%s/juli/%s.marked_duplicates.bam"%(out_dir,args.prefix)):
    p1 = Process(target=shell_run, args=(genefuse,))
    p2 = Process(target=shell_run, args=(Juli_a,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
print("\n\nGenefuse and mapping finished\n\n")
if not os.path.exists ("%s/svict/%s.vcf"%(out_dir,args.prefix)) or not os.path.exists("%s/juli/%s.txt"%(out_dir,args.prefix)):
    p3 = Process(target=shell_run, args=(svict,))
    p4 = Process(target=shell_run, args=(Juli_b,))
    p3.start()
    p4.start()
    p3.join()
    p4.join()

print("\n\nJuli and svict has done.\n\n")

######################################################genelist from cosmic genefusion
gene_lit=[]
hgnc=open("%s/svict/hgnc.txt"%(args.database),"r")
for line in hgnc:
    gene_lit.append(line.strip())
hgnc.close()
######################################################output final svict result
infile=open("%s/svict/%s.vcf"%(out_dir,args.prefix),"r")
outfile=open("%s/svict/%s.final.vcf"%(out_dir,args.prefix),"w")
for line in infile:
    if not line.startswith("#"):
        array=line.strip().split("\t")[-1].split(";")
        gene_a, gene_b = "", ""
        for i in array:
            if i.startswith("ANNOL"):
                gene_a=i.split(",")[-1]
            if i.startswith("ANNOR="):
                gene_b = i.split(",")[-1]
        if gene_a in gene_lit and gene_b in gene_lit and gene_b!=gene_a:
            outfile.write("%s\n"%(line.strip()))
infile.close()
outfile.close()
######################################################output final Juli result the gene must from cosmic gene list
infile=open("%s/juli/%s.txt"%(out_dir,args.prefix),"r")
outfile=open("%s/juli/%s.final.txt"%(out_dir,args.prefix),"w")
for line in infile:
    array=line.strip().split("\t")
    if line.strip().startswith("ChrA"):
        outfile.write("%s\n" % (line.strip()))
    if array[-2]!=array[-4] and array[-2] in gene_lit and array[-4] in gene_lit:
        outfile.write("%s\n"%(line.strip()))
infile.close()
outfile.close()
######################################################delete tmp file
subprocess.call("rm -rf %s/juli/juli.R"%(out_dir),shell=True)










