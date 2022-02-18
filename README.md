
# genefuse file

### step1:Download gene fusion from cosmic (https://cancer.sanger.ac.uk/cosmic/fusion) named(cosmic_genelist.txt) as following:

    ACBD6_ENST00000367595-RRP15
    ACSL3-ETV1
    ACTB-GLI1

### step2:Download gtf and genome fasta file from gencode:

    https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/

### step3:output file fusion.csv

    python3 pre_genefuse.py

#### step4:run genefuse 

# factera file:

#### step1:download hg38.2bit file

    https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/

#### step2：output exon bed

    python3 pre_factera.py

