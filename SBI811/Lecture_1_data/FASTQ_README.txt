Synthetic paired-end FASTQ files
================================

Files
-----
data/raw/sample01_R1.fastq
data/raw/sample01_R2.fastq
data/raw/sample01_R1.fastq.gz
data/raw/sample01_R2.fastq.gz

Design
------
Read length: 75 bp
Read pairs: 300
Insert size: 180-260 bp

Read-pair distribution
----------------------
chr1: 140 pairs
chr2: 105 pairs
plasmidA: 55 pairs

The reads were sampled directly from the synthetic genome and contain no
introduced sequencing errors. This makes them useful for introductory teaching
because alignment results are easy to interpret.

The paired reads follow the normal orientation:
R1 = sequence from the left end of the fragment
R2 = reverse complement of the right end of the same fragment

metadata/sample01_read_origins.tsv
contains the true origin of every read pair. This is intended as a validation/
teaching key and is not required for basic student exercises.

Useful commands
---------------
head -n 8 data/raw/sample01_R1.fastq
wc -l data/raw/sample01_R1.fastq
expr $(wc -l < data/raw/sample01_R1.fastq) / 4
zcat data/raw/sample01_R1.fastq.gz | head
