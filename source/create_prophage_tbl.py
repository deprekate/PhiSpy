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
Create a prophage.tbl file from a phispy directory that does not contain one.
"""

import os
import sys
import argparse
from evaluation import  make_prophage_tbl

#################################################
def make_new_prophage_tbl(phispydir):
	"""
	Make a new prophage table
	:param phispydir: the directory to read the input and create the output
	:return: nothing
	"""
	make_prophage_tbl(os.path.join(phispydir, 'prophage_tbl.txt'), os.path.join(phispydir, 'prophage.tbl'))

#################################################
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="create a prophage.tbl file for a PhiSpy directory")
	parser.add_argument('-d', help='phispy directory')
	parser.add_argument('-v', help='verbose output', action="store_true")
	args = parser.parse_args()

	make_new_prophage_tbl(args.d)
