#!/usr/bin/env python
import os
import sys
import shutil

## unzip data
print ("##############################")
print ("Unzipping test data...")
print ("##############################")


if (os.path.isdir("./Test_Organism") ):
	print ("Removing previous data test...")	
	shutil.rmtree("./Test_Organism")

cmd = 'unzip Test_Organism.zip'
os.system(cmd)
print ("Done...")
print ("##############################\n\n")

## call PhiSpy on example data 1
print ("##############################")
print ("Call PhiSpy for example dataset1...")
print ("##############################")
ex1 = "Test_Organism/160490.1"
ex1_out = ex1 + "_out"
cmd1 = "python ../PhiSpy.py -i " + ex1 + " -o " + ex1_out
print ("## Command:")
print (cmd1)
os.system(cmd1)
print ("Done...")
print ("##############################\n\n")

## call PhiSpy on example data 2
print ("##############################")
print ("Call PhiSpy for example dataset2...")
print ("##############################")
ex2 = "Test_Organism/272989.13"
ex2_out = ex2 + "_out"
cmd2 = "python ../PhiSpy.py -i " + ex2 + " -o " + ex2_out
print ("## Command:")
print (cmd2)
os.system(cmd2)
print ("Done...")
print ("##############################\n\n")

print ("Testing PhiSpy finished....\n\n")
