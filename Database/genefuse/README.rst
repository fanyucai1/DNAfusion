prepare genefuse file
#########################

step1:Download gene fusion from cosmic (https://cancer.sanger.ac.uk/cosmic/fusion) named(cosmic_genelist.txt) as following:
::

    ACBD6_ENST00000367595-RRP15
    ACSL3-ETV1
    ACTB-GLI1

step2:Download gtf from gencode
::

    https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/

step3:output file fusion.csv
::

    python3 pre_genefuse.py