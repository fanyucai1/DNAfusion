import argparse
import os
import subprocess

docker_name="dnafusion:latest"
parser=argparse.ArgumentParser("Find DNA fusion use genefuse and factera.")
parser.add_argument("-p1","--pe1",help="pe1 fatsq",required=True)
parser.add_argument("-p2","--pe2",help="pe2 fastq",required=True)
parser.add_argument("-d","--database",help="database",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-b","--bed",help="target bed",default="")
args=parser.parse_args()

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
docker_cmd=docker_raw+"sh -c \"genefuse -r /Database/GRCh38.p13.genome.fa -f /Database/genefuse/fusion.csv " \
            "-1 /opt/%s -2 /opt/%s -t 16 -h /analysis/%s.html > /analysis/%s.result \"" %(f1,f2,args.prefix,args.prefix)
subprocess.check_call(docker_cmd,shell=True)


###############juli######################
subprocess.call('mkdir -p %s/juli/'%(out_dir),shell=True)
docker_raw="docker run -v %s:/opt/ -v %s:/Database/ -v %s/juli:/analysis/ %s "%(indir,args.database,out_dir,docker_name)
docker_cmd=docker_raw+"sh -c \'bwa mem /Database/GRCh38.p13.genome.fa /opt/%s /opt/%s |samtools sort -@16 -o /analysis/%s.bam -\'"%(f1,f2,args.prefix)
subprocess.check_call(docker_cmd,shell=True)
outfile=open("%s/juli/juli.R"%(out_dir),"w")
outfile.write("library(juliv0.1.6.2)\n"
              "callfusion(CaseBam=\'/analysis/%s.bam\',"
              "TestID=\'%s\',"
              "OutputPath=\'/analysis/\',"
              "Thread=10,"
              "Refgene=\'/Database/juliv0.1.6.2_reference_hg38/refGene_hg38.txt\',"
              "Gap=\'/Database/juliv0.1.6.2_reference_hg38/gap_hg38.txt\',"
              "Reference=\'/Database/GRCh38.p13.genome.fa\')\n"%(args.prefix,args.prefix))
outfile.close()
docker_cmd=docker_raw +"sh -c \'Rscript /analysis/juli.R\'"
print(docker_cmd)
subprocess.call(docker_cmd,shell=True)
