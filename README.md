# Software docker

    docker pull fanyucai1/dnafusion:latest

# prepare genefuse file

step1:Download gene fusion from cosmic (https://cancer.sanger.ac.uk/cosmic/fusion) named(cosmic_genelist.txt) as following:

    ACBD6_ENST00000367595-RRP15
    ACSL3-ETV1
    ACTB-GLI1

step2:Download gtf and genome fasta file from gencode:

    https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/

step3:output file fusion.csv

    python3 pre_genefuse.py

# analysis dnafusion

    python3 script/DNAfusion.py -p1 test_data/R1.fq -p2 test_data/R2.fq -d Database/ -o output/ -p test

# output file

    test.html
    test_dnafuse.result
    test.txt