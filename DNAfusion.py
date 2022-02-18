import argparse
import os
import subprocess

docker_name="fanyucai1/dnafusion:latest"
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
if a!=b:
    print("%s and %s must be the same directory"%(args.pe1,args.pe2))
indir=os.path.dirname(a)
out_dir=os.path.abspath(args.outdir)
f1=a.split("/")[-1]
f2=b.split("/")[-1]

###############factera######################
subprocess.call('mkdir -p %s/factera/'%(out_dir),shell=True)
docker_raw="docker run -v %s:/opt/ -v %s:/Database/ -v %s/factera:/analysis/ %s "%(indir,args.datase,out_dir,docker_name)
#step1:first mapping
docker_cmd=docker_raw+" bwa mem /Database/GRCh38.p13.genome.fa /opt/%s /opt/%s |samtools view -bS -@8 -o /analysis/%s.bam" %(f1,f2,args.prefix)
subprocess.check_call(docker_cmd,shell=True)
#step2:run factera
docker_cmd=docker_raw+" perl /script/factera.pl /analysis/%s.bam /Database/exon.bed /Database/hg38.2bit "
if args.bed!="":
    if os.path.dirname(args.bed)!=indir:
        subprocess.check_call('cp %s %s'%(args.bed,indir),shell=True)
        bedname=args.bed.split("/")[-1]
        docker_cmd+="/opt/%s "%(bedname)
docker_cmd+="-o /analysis/"
subprocess.check_call(docker_cmd,shell=True)
###############genefuse######################
subprocess.call('mkdir -p %s/genefuse/'%(out_dir),shell=True)
docker_raw="docker run -v %s:/opt/ -v %s:/Database/ -v %s/genefuse:/analysis/ %s "%(indir,args.datase,out_dir,docker_name)
docker_name="genefuse -r /Database/GRCh38.p13.genome.fa -f /Database/fusion.csv " \
            "-1 /opt/%s -2 /opt/%s -t 4 -h /analysis/%s.html > /analysis/%s.result" %(f1,f2,args.prefix,args.prefix)
subprocess.check_call(docker_cmd,shell=True)