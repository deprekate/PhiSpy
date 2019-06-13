# INTRODUCTION

PhiSpy is a computer program written in C++, Python and R to identify prophages in a complete bacterial genome sequences.

Initial versions of PhiSpy were written by 

Sajia Akhter (sajia@stanford.edu)
PhD Student
Edwards Bioinformatics Lab (http://edwards.sdsu.edu/labsite/)
Computational Science Research Center (http://www.csrc.sdsu.edu/csrc/)
San Diego State University (http://www.sdsu.edu/)


Improvements, bug fixes, and other changes were made by

Katelyn McNair
Edwards Bioinformatics Lab (http://edwards.sdsu.edu/labsite/)
San Diego State University (http://www.sdsu.edu/)

Recently, translation from python2 to python3 and implementation as a module was made by

Jose F. Sanchez Herrero, Bioinformatics Unit IGTP, Hospital German Trias i Pujol (http://www.germanstrias.org/technology-services/genomica-bioinformatica/)


# SYSTEM REQUIREMENTS

The program should run on all Unix platforms, although it was not tested in all platforms.


# SOFTWARE REQUIREMENTS

PhiSpy requires following programs to be installed in the system. NOTE: You can ignore this if you're using the singularity container method of installation.

1. Python - version 2.7.2 or later
2. Biopython - version 1.58 or later 
3. gcc - GNU project C and C++ compiler - version 4.4.1 or later
4. The R Project for Statistical Computing - version 2.9.2 or later
5. Package randomForest in R - version 4.5-36 or later
 

# INSTALLATION

1. Clone this repository
2. `% cd PhiSpy`
3. `% make`
4. For ease of use, add the location of PhiSpy.py to your $PATH.

TO TEST THE PROGRAM

1. `% cd PhiSpy`
2. `% ./PhiSpy.py -i Test_Organism/160490.1/ -o output_directory -t 25`

Test_Organism/160490.1/ is a seed annotation directory for genome 'Streptococcus pyogenes M1 GAS'. 
You will find the output files of this genome at output_directory.

# TO RUN PHISPY

`% ./PhiSpy.py -i organism_directory -o output_directory -c`

where:
'output directory': Output directory is the directory where the final output file will be created.

'organism directory': The seed annotation directory for the input bacterial organism whose prophage(s) need to be identified. 

You can download the SEED genomes from the [PhAnToMe database](http://www.phantome.org/Downloads/genomes/seed/)

Or, 
If you have new genome, you can annotate it using the [RAST server](http://rast.nmpdr.org/rast.cgi). 
After annotation, you can download the genome directory from the server.

Or, 
If you have the GenBank file (containing sequence) of the genome, you can convert it using the following command:
`% python genbank_to_seed.py GenBank_file.gb organism_directory`

Now to run PhiSpy, use organism_directory as 'organism directory'. 
 

The program will access the following files in the organism_directory:
i.   contig file: organism_directory/contigs
ii.  tbl file for peg: organism_directory/Features/peg/tbl
iii. assigned_functions file: organism_directory/assigned_functions or organism_directory/proposed_functions or organism_directory/proposed_non_ff_functions  
iv.  tbl file for rna: organism_directory/Features/rna/tbl


_Note:_
The assigned functions file may not be in the RAST genome directory. You can create it from proposed_functions and proposed_non_ff_functions or you can use [this perl script](/home/redwards/Dropbox/GitHubs/EdwardsLab/RAST/make_assigned_functions.pl) to create an assigned_functions file for you.

# REQUIRED INPUT OPTIONS

The program will take 1 command line input.

It shows a list (run with -c option) and asks for a number from the list. 
In the list, there are several organisms and each organism is associated by a number. 
If you find a closely related genome of your interested organism enter the number. PhiSpy will consider that genome as training genome.
Otherwise, enter 0 to run with generic training set.


# HELP

For the help menu use the -h option:
% python PhiSpy.py -h


# OUTPUT FILES

There are 3 output files, located in output directory.

1. prophage.tbl: This file has two columns separated by tabs [id, location]. 
The id is in the format: pp_number, where number is a sequential number of the prophage (starting at 1). 
Location is be in the format: contig_start_stop that encompasses the prophage.
 
2. prophage_tbl.tsv: This is a tab seperated file. The file contains all the genes of the genome. The tenth colum represents the status of a gene. If this column is 1 then the gene is a phage like gene; otherwise it is a bacterial gene. 

This file has 16 columns:(i) fig_no: the id of each gene; (ii) function: function of the gene;	(iii) contig; (iv) start: start location of the gene; (v) stop: end location of the gene; (vi) position: a sequential number of the gene (starting at 1); (vii)	rank: rank of each gene provided by random forest; (viii) my_status: status of each gene based on random forest; (ix) pp: classification of each gene based on their function; (x) Final_status: the status of each gene. For prophages, this column has the number of the prophage as listed in prophage.tbl above; If the column contains a 0 we believe that it is a bacterial gene. If we can detect the _att_ sites, the additional columns will be: (xi) start of _attL_; (xii) end of _attL_; (xiii) start of _attR_; (xiv) end of _attR_; (xv) sequence of _attL_; (xvi) sequence of _attR_.

3. prophage_coordinates.tsv: This file has the prophage ID, contig, start, stop, and potential _att_ sites identified for the phages.


# EXAMPLE DATA

We have provided two different example data sets.

* _Streptococcus pyogenes_ M1 GAS which has a single genome contig. The genome contains four prophages.

To analyse this data, you can use:

```
python2.7 PhiSpy.py -t 25 -i Test_Organism/160490.1/ -o Test_Organism/160490.1.output
```

And you should get a prophage table that has this information:

| Prophage number | Contig | Start | Stop |
| --- | --- | --- | --- | 
pp_1 | NC_002737 | 529631 | 604720
pp_2 | NC_002737 | 778642 | 846824
pp_3 | NC_002737 | 1191309 | 1255536
pp_4 | NC_002737 | 1607352 | 1637214

* _Salmonella enterica_ serovar Enteritidis LK5

This is an early draft of the genome (the published sequence has a single contig), but this draft has 1,410 contigs and some phage like regions.

If you run PhiSpy on this draft genome with the default parameters you will not find any prophage because they are all filtered out for not having enough genes. By default, PhiSpy requires 30 genes in a prophage. You can alter that stringency on the command line, and for example reducing the phage gene window size to 10 results in 3 prophage regions being identified.

```
python2.7 PhiSpy.py -t 21 -w 10 -i Test_Organism/272989.13/ -o Test_Organism/272989.13.output
```

You should get a prophage table that has this information:

| Prophage number | Contig | Start | Stop |
| --- | --- | --- | --- | 
pp_1 | Contig_2300_10.15 | 1630 | 10400
pp_2 | Contig_2294_10.15 | 175 | 11290
pp_3 | Contig_2077_10.15 | 318 | 12625


# LICENSE

This is a modified version of the original code. No further developments were made, only conversion from python2 to python3 and small bug fixes were done. Please refer to the original version for further details and cited them accordingly.

The MIT License (MIT)

Copyright (c) 2016 Rob Edwards

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

