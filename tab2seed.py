#!/usr/bin/env python
#############################################################################################
## PhiSpy is a computer program written in C++, Python and R to 
## identify prophages in a complete bacterial genome sequences.
##
## Initial versions of PhiSpy were written by
## Sajia Akhter (sajia@stanford.edu) PhD Student Edwards Bioinformatics Lab 
## (http://edwards.sdsu.edu/labsite/), Computational Science Research Center 
## (http://www.csrc.sdsu.edu/csrc/), San Diego State University (http://www.sdsu.edu/)
##
## Improvements, bug fixes, and other changes were made by
## Katelyn McNair Edwards Bioinformatics Lab (http://edwards.sdsu.edu/labsite/) 
## San Diego State University (http://www.sdsu.edu/)
## 
## The MIT License (MIT)
## Copyright (c) 2016 Rob Edwards
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
## 
## Improvements, bug fixes and other changes (2019) were made by forking the github version: 
## - Conversion from python2 -> python3
## - Add prophage.tbl
## - Simplification of code and integration into BacterialGenotyper
##
#############################################################################################
"""
Convert a tab file from PATRIC to a the SEED files that we need for PhiSpy

We need the following files:

1. assigned_functions - a tab separated list of FIG ID and function
2. contigs - the fasta DNA sequence. Note we may download this separately
3. genome - the name of the genome -- may not be required
4. taxonomy - the taxonomy of the genome -- may not be required
5. taxonomy_id - the tax id. -- also may not be required
6. Features/peg/tbl - the tbl that has id,contig_start_stop, [alt ids]
7. Features/rna/tbl - the RNA genes


The files that PhiSpy opens are:

a. dir/contigs
b. dir/Features/peg/tbl
c. dir/assigned_functions
d. dir/Features/rna/tbl


"""

import os
import sys
import argparse

#################################################
def parse_tab(filename, outputdir):
    """
    Parse a patric tab file
    :param filename: the file to parse
    :return: ummm
    """

    if not (os.path.exists(os.path.join(outputdir, "Features"))):
        os.mkdir(os.path.join(outputdir, "Features"))
    if not (os.path.exists(os.path.join(outputdir, "Features/peg"))):
        os.mkdir(os.path.join(outputdir, "Features/peg"))
    if not (os.path.exists(os.path.join(outputdir, "Features/rna"))):
        os.mkdir(os.path.join(outputdir, "Features/rna"))

    peg = open(os.path.join(outputdir, "Features/peg/tbl"), 'w')
    rna = open(os.path.join(outputdir, "Features/rna/tbl"), 'w')
    asf = open(os.path.join(outputdir, "assigned_functions"), 'w')

    wrote_genome = False

    with open(filename, 'r') as fin:
        for l in fin:
            if l.startswith('genome_id'):
                continue

            # genome_id	genome_name	accession	annotation	feature_type	patric_id	refseq_locus_tag	alt_locus_tag
            # uniprotkb_accession	start	end	strand	na_length	gene	product	figfam_id	plfam_id	pgfam_id
            # go	ec	pathway
            l = l.replace("\n", "") # this is a hack because I can't figure out how to do chomp
            p = l.split("\t")

            if not wrote_genome:
                with open(os.path.join(outputdir, "GENOME"), 'w') as gout:
                    gout.write("{}\n".format(p[1]))
                wrote_genome = True

            gid, name, acc, who, ftype, fid, refseq_locus, alt, uni, start, stop, strand, length, gene, prod, ffid, plid, pgid, go, ec, pw = p

            if start > stop:
                (start, stop) = (stop, start)

            if "CDS" in p[4]:
                peg.write("{}\t{}_{}_{}\n".format(fid, acc, start, stop))
                asf.write("{}\t{}\n".format(fid, prod))
            elif "rna" in p[4].lower():
                rna.write("{}\t{}_{}_{}\n".format(fid, acc, start, stop))
    peg.close()
    rna.close()
    asf.close()

#################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert a patric tab file to a minimal seed directory")
    parser.add_argument('-f', help='The patric tab file', required=True)
    parser.add_argument('-o', help='output directory', required=True)
    parser.add_argument('-v', help='verbose output', action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.o):
        os.mkdir(args.o)

    parse_tab(args.f, args.o)
