#!/usr/bin/env python
import os
import sys
import subprocess

from Bio import SeqIO

INSTALLATION_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
sys.path.append(INSTALLATION_DIR)

from modules import makeTrain
from modules import makeTest
from modules import classification
from modules import evaluation
from modules import unknownFunction
import modules.helper_functions as helpers

class SeqioFilter( object ):
    """This is class to allow filtering of the Biopython SeqIO record

    SeqIO returns a generator object so anytime you want to perform
    an action on it, you must iterate through the entire list. This
    class add the ability to filter and return only a subset of the
    features.

    Note:
        To use simply pass a SeqIO.parse object to it and then when
        the object is called a keyword is passed to it and only those
        features matching the keyword are returned.
    Example:
        record = SeqioFilter(SeqIO.parse(infile)):
        #no change to standard SeqIO calls
        for entry in record:
            print(entry.id, entry.seq)
        #now we can get only certain features
        for cds in record.get_feature('CDS'):
            print(cds)

    """
    def __init__( self, content ):
        self.__content = content
    def __iter__(self):
        for item in self.__content:
            yield item
    def __call__( self, keyword='' ):
        pass
    #def get_features( self, keyword='' ):
    #    for item in self.__content:
    #        for line in item.features:
    #            if not keyword or line.type == keyword:
    #                line.id = item.id
    #                yield line


def main(argv):  #organismPath, output_dir, trainingFlag, INSTALLATION_DIR, evaluateOnly, threshold_for_FN, phageWindowSize, quietMode, keep):
    ######################################
    #         check R install            #
    ######################################
    try:
        subprocess.call("type Rscript", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
    except OSError:
        sys.exit("The R programming language is not installed")

    ######################################
    #         parse the options          #
    ######################################
    args_parser = helpers.get_args()
    # in future support other types
    input_file = SeqIO.parse(args_parser.infile, "genbank")
    args_parser.record = input_file
    os.makedirs(args_parser.output_dir, exist_ok=True)

    ######################################
    #         make training set          #
    ######################################
    if args_parser.make_training_data:
        print('Making Train Set... (need couple of minutes)')
        my_make_train_flag = makeTrain.make_set_train(**vars(args_parser))
        exit()

    ######################################
    #         make testing set           #
    ######################################
    print('Making Test Set... (need couple of minutes)')
    my_make_test_flag = makeTest.make_test_set(**vars(args_parser))
    # check file im,plement later
    #if (my_make_test_flag == 0):
    #    print('The input organism is too small to predict prophages. Please consider large contig (having at least 40 genes) to use PhiSpy.')
    #    return

    ######################################
    #         do classification          #
    ######################################
    print('Start Classification Algorithm')
    classification.call_randomforest(**vars(args_parser))
    classification.make_initial_tbl(**vars(args_parser))

    ######################################
    #         i dont know what           #
    ######################################
    ###### added in this version 2.2 #####
    if (args_parser.training_set == 'data/genericAll.txt'):
        print('As training flag is zero, considering unknown functions')
        unknownFunction.consider_unknown(args_parser.output_dir)

    ######################################
    #         do evaluation              #
    ######################################
    print('Start evaluation...')
    evaluation.fixing_start_end(**vars(args_parser))
    print('Done!!!')

    ######################################
    #                                    #
    ######################################

if __name__== "__main__":
    main(sys.argv)
