FROM fanyucai1/biobase
RUN mkdir /script/ && mkdir /Database/ && mkdir /analysis/
COPY make_fusion_genes.py /script/
COPY genefuse /usr/bin/
COPY JuLI-v0.1.6.2.zip /opt/
RUN cd /opt/ && unzip JuLI-v0.1.6.2.zip
RUN R -e "install.packages('devtools')"
RUN R -e "install.packages('ellipsis')"
RUN R -e "install.packages('vctrs')"
RUN R -e "install.packages('usethis')"
RUN cd /opt/JuLI-v0.1.6.2/ && R -e "library(devtools)" -e "install('juliv0.1.6.2')"
COPY samtools-1.15.tar.bz2 /software/
COPY svict-master.zip /software/
COPY bwa-0.7.17.tar.bz2 /software/
RUN cd /software/ && tar xjvf samtools-1.15.tar.bz2 && tar xjvf bwa-0.7.17.tar.bz2 && cd samtools-1.15 && ./configure && make install
RUN cd /software/bwa-0.7.17/ && make
RUN cd /software/ && unzip svict-master.zip && cd svict-master && make && ln -s /software/svict-master/svict /usr/bin/
RUN ln -s /software/bwa-0.7.17/bwa /usr/bin
COPY picard.jar /software/
