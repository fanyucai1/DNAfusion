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



#prepare Juli

stp1:HGNC2UniProtID

    https://www.genenames.org/download/custom/

    select:
    HGNC ID
    Approved symbol
    Approved name
    Approved

step2:gap_hg38.txt

    http://genome.ucsc.edu/cgi-bin/hgTables?db=hg38
    select:gap

step3: refGene_hg38.txt

    https://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz

step4:CosmicFusionExport_V95.tsv

    https://cancer.sanger.ac.uk/cosmic/

# analysis dnafusion

    python3 script/DNAfusion.py -p1 test_data/R1.fq -p2 test_data/R2.fq -d Database/ -o output/ -p test

# output file

    test.html
    test_dnafuse.result
    test.txt