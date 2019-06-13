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
import re
import string
import os

#################################################
def unknown_func(x):

    x_lower = x.lower()

    if (
       (len(x) == 0) or
       #('hypoth' in x_lower) or
       ('conserved protein' in x_lower) or
       ('gene product' in x_lower) or
       ('interpro' in x_lower) or
       ('uncharacterized' in x_lower) or
       ('pseudogene' in x_lower) or
       ('similar to' in x_lower) or
       ('similarity' in x_lower) or
       ('glimmer' in x_lower) or
       ('unknown' in x_lower) or
       ('complete' in x_lower) or
       ('ensang' in x_lower) or
       ('unnamed' in x_lower) or
       ('Expressed' in x_lower) or
       ('similar to' in x_lower) or
       (' identi' in x_lower) or
       ('ortholog of' in x_lower) or
       ('structural feature' in x_lower) or
       ('cds_' in x_lower) or
       ('predicted by Psort' in x) or
       ('AGR_' in x) or
       ('EG:' in x) or
       ('RIKEN' in x) or
       re.search('lmo\d+ protein', x_lower) or
       re.search('lmo\d+protein', x_lower) or
       re.search('B[sl][lr]\d', x_lower) or
       re.search('^U\d', x) or
       re.search('[a-zA-Z]{2,3}\|', x) or
       re.search('orf\d+', x_lower) or
       re.match('orf[^_]', x_lower) or
       re.match('predicted', x_lower) or
       re.match('bh\d+', x_lower) or
       re.match('y[a-z]{2,4}\\b', x) or
       re.match('[a-z]{2,3}\d+[^:\+\-0-9]', x_lower) ):
        
        return 1
    else:
        return 0

#################################################
def add_unknown_function_initial_tbl(infile,outfile):
    try:
        f = open(infile,'r')
        fw = open(outfile,'w')
    except:
        return 0
    
    flag = 0
    for line in f:
        if flag == 0:
            fw.write(line)
            flag = 1
            continue

        line = line.strip()
        temp = re.split('\t',line)
        i = 0
        while i<8:
            fw.write(temp[i]+'\t')
            i = i + 1

        x = unknown_func(temp[1])
        if x == 0:
            fw.write(temp[8]+'\n')
        else:
            fw.write('0.5\n')
 
    f.close()
    fw.close()
    return 1

#################################################
def consider_unknown(output_dir):
    x = add_unknown_function_initial_tbl(output_dir+'initial_tbl.txt',output_dir+'initial_tbl_2.txt')
    if (x == 1):
        cmd2 = "rm " + output_dir+'initial_tbl.txt'
        os.system(cmd2)

        cmd2 = "mv "+output_dir+'initial_tbl_2.txt '+output_dir+'initial_tbl.txt'
        os.system(cmd2)
