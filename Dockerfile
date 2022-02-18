FROM conda/miniconda3
RUN conda install -c bioconda perl-statistics-descriptive bwa samtools perl-bioperl blast genefuse ucsc-twobittofa
RUN mkdir /script/ && mkdir /Database/ && mkdir /analysis/
COPY factera.pl /script/
COPY make_fusion_genes.py /script/
