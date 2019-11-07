# Created by Rik Frijmann and Esther Kockelmans.
# Last edit 14-OCT-2019.
# Short changelog:
# 14-OCT-2019: changed header for output fasta file to the information
#   line of the GFF3 file, making it more informative and a unique
#   identifier.
# 10-OCT-2019: added support for multi-line fasta-files.
# 30-SEP-2019: added predicted framework and documentation.
#
#28-10-2019 Changes that need to be made:
#To slice the consensus sequence there will be another file deliverd.
#This file contains locations in which deletions or insertions have ocurred.
#This location has to be accounted for in the slicing method.

# Current issues:
# Script can not accept external variables for genome filepath, GFF3-
# filepath and output filepath. A argument parser will have to be
# added at a later date.

from Bio import SeqIO


def fetch_strand(feature_list, in_sequence):
    """
    This function takes paramaters from the 'feature_list' variable
    and slices the corresponding positions from the sequence of the
    genome it is located on.
    :param feature_list: list containing start, end, and strand of the
        DNA feature.
    :param in_sequence: genome sequence is SeqIO's seq format.
    :return sequence: sequence of DNA feature in Seq format.
    """
    sequence = in_sequence[feature_list[2]-1:feature_list[3]]  # start-1
    if feature_list[5] == "-":
        sequence = sequence.reverse_complement()
    return sequence


def import_gff3(filepath):
    """
    This function opens a GFF3-file in the location specified by the
    variable 'filepath'. Looping over the file, the list variable
    'feature_list' will be used to store short lists of DNA features.
    This 2D list is returned.
    :param filepath: string containing the location of the GFF3-file.
    :return feature_list: a 2D list containing DNA features, their
        type, start position, end position, coding strand and
        translation frame.
    """
    feature_list = []
    with open(filepath, 'r') as infile:
        iterdata = iter(infile.readlines())
        next(iterdata)
        for line in iterdata:
            line = line.strip("\n").split("\t")
            feature_list.append([line[0], line[2], int(line[3]), int(line[4]), line[5], line[6], line[-1]])
    return feature_list


if __name__ == "__main__":
    testgff3 = "../shortlist/tussenproduct/gff3_short_list.txt"  # variable used to test code
    testfasta = "../data/jerseykale_consensus.fa"  # variable used to test code
    outfasta = "jk_sequences_output.fasta" # variable used to test code
    with open(outfasta, 'w') as outfile:
        pass  # wipes output file.

    with open(testfasta, "rU") as handle:
        genome = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))

    feature_list = import_gff3(testgff3)
    # print(feature_list)  # debug

    with open(outfasta, 'a') as outfile:
        for feature in feature_list:
            # print(feature)  # debug
            sequence = fetch_strand(feature, genome[feature[0]])
            outfile.write(">%s\n"%(feature[-1]))
            outfile.write(str(sequence.seq)+"\n")
            # print(sequence.seq)  # debug
