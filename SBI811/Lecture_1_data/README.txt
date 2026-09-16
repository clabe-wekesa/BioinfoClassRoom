SBI 811 - Multi-replicon synthetic bacterial reference
======================================================

Purpose
-------
This is a fully synthetic and internally consistent teaching reference for Linux
and introductory bioinformatics exercises.

Genome organization
-------------------
chr1      chromosome   12000 bp
chr2      chromosome   9000 bp
plasmidA  plasmid       5000 bp

The dataset deliberately contains TWO chromosomes plus ONE plasmid. This is useful
for showing that a bacterial genome is not always represented by a single sequence.
Many bacteria have one chromosome, but some have multiple chromosomes and/or
additional plasmids.

Reference files
---------------
reference/genome.fasta
    Complete synthetic genome with three replicons.

reference/annotation.gff
    GFF3 annotation for protein-coding genes, CDS features, tRNA/rRNA/ncRNA
    features and both + and - strands.

reference/genes.fasta
    Nucleotide sequences of all protein-coding genes in 5'->3' coding orientation.
    For genes on the negative strand, these are the reverse-complemented gene
    sequences relative to the genome.

reference/proteins.fasta
    Protein translations of all protein-coding genes.

reference/replicons.tsv
    Simple table describing the three replicons.

reference/validation.tsv
    Internal consistency check showing that GFF coordinates, gene nucleotide
    lengths and protein translations agree.

Useful Linux questions
----------------------
How many replicons are in the genome?
    grep -c "^>" reference/genome.fasta

What are their names?
    grep "^>" reference/genome.fasta

How many gene features occur on each replicon?
    awk '$3=="gene" {print $1}' reference/annotation.gff | sort | uniq -c

Which genes are on chr2?
    awk '$1=="chr2" && $3=="gene"' reference/annotation.gff

Which genes are on the negative strand?
    awk '$3=="gene" && $7=="-"' reference/annotation.gff

How many feature types occur?
    grep -v "^#" reference/annotation.gff | awk '{print $3}' | sort | uniq -c

Which sequence headers contain "transporter"?
    grep "transporter" reference/genes.fasta

How many protein sequences are present?
    grep -c "^>" reference/proteins.fasta

All sequences are artificial and intended only for teaching.
