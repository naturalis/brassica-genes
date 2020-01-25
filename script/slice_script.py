# Created by Rik Frijmann and Esther Kockelmans.
# Last edit 12-JAN-2020
# Short changelog:
# 12-JAN-2020: added more information to header and ID line of output
#   fasta files. Adding contig identifier to fasta header was
#   required in particular.
# 08-JAN-2020: removed functionality to slice on both reference and
#   target at the same time. Instead split the script's function into
#   two parts. It now slices from a genome, gff3 and geneid file; or
#   from a genome, and a file with filenames and locations.
# 14-OCT-2019: changed header for output fasta file to the information
#   line of the GFF3 file, making it more informative and a unique
#   identifier.
# 10-OCT-2019: added support for multi-line fasta-files.
# 30-SEP-2019: added predicted framework and documentation.

from Bio import SeqIO
from Bio.Seq import Seq
from os import path
import os
import glob


def input_file_location(message):
    """
    This function performs basic quality control of user input. It
    calls for a filepath with a pre-specified message. The function
    then checks if the given filepath leads to an actual existing
    file. If no file exists at the given location, the function will
    throw an error message and ask for a new file location.
    :param message: String. Contains the message asking for a filepath
    :return filepath: String. Contains a filepath leading to the file.
    """
    filepath = input(message)
    flag = path.isfile(filepath)
    while not flag:
        filepath = input("Error: file not found! \n"
                         "Please specify full relative filepath leading to the required file")
        flag = path.isfile(filepath)
    print("%s succesfully located"%(filepath))
    return filepath


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
    # Create clean output folder
    try:
        os.mkdir("fasta_resultaten")
    except FileExistsError:
        tempfiles = glob.glob("fasta_resulaten/*")
        for file in tempfiles:
            print(file)
            if path.isfile(file):
                os.remove(file)

    while True:
        mode = input("### Bpexa slice script\n"
                     "Choose the mode to run this slicing programm in by entering one of the following numbers:\n"
                     "1) Input is a genome in fasta format and a related GFF3-file.\n"
                     "2) Input is a genome in fasta format and a list of start- and stop locations.\n"
                     "3) Quit without running.\n"
                     "Mode: ")
        if mode == "1":
            # Fetch input file location
            genome_file = input_file_location("Specify the location of the genome fasta file: ")
            gff3_file = input_file_location("Specify the location of the related GFF3 file: ")
            goi_file = input_file_location("Specify the location of the file with gene IDs of interest: ")

            # Fetch and modify input
            with open(genome_file, "rU") as handle:
                genome = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
            feature_list = import_gff3(gff3_file)
            with open(goi_file, 'r') as handle:
                goi = []
                for record in handle.readlines():
                    goi.append(record.rstrip("\n"))

            # Slice sequences
            exon_counter = {}
            for feature in feature_list:
                sequence = fetch_strand(feature, genome[feature[0]])
                # Write output file name
                out_gene = "unknown"
                for gene_id in goi:
                    if gene_id in feature[-1]:
                        out_gene = gene_id
                if feature[1] == "exon":
                    try:
                        exon_counter[out_gene] += 1
                    except KeyError:
                        exon_counter[out_gene] = 1
                    feature[1] = "exon"+str(exon_counter[out_gene])
                outfilename = "fasta_resultaten/%s_%s.fa"%(out_gene, feature[1])
                # Write output file
                with open(outfilename, 'w') as outfile:
                    outfile.write(">geneid:%s;contig:%s;feature:%s;seqstart:%i;seqstop:%i\n"%(
                        out_gene,
                        feature[0],
                        feature[1],
                        feature[2],
                        feature[3]
                    ))
                    outfile.write(str(sequence.seq) + "\n")
            quit()
        if mode == "2":
            # Fetch input file location
            genome_file = input_file_location("Specify the location of the genome fasta file: ")
            locations_file = input_file_location("Specify the filename of the target sequence locations: ")

            # Fetch input
            with open(genome_file, "rU") as handle:
                genome = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
            locations = []
            with open(locations_file, 'r') as handle:
                record_list = iter(handle.readlines())
                next(record_list)
                for record in record_list:
                    # a record should be:
                    # filename \t contig \t start \t end \n
                    record = record.rstrip("\n").split("\t")
                    record[2] = int(record[2])
                    record[3] = int(record[3])
                    locations.append(record)

            # Gather parameters for slicing in a mock feature list.
            for location in locations:
                mock_feature = [location[1], "",
                                min(location[2], location[3]),
                                max(location[2], location[3]),
                                "", "+", ""]
                if location[2] > location[3]:
                    mock_feature[5] = "-"

                # Slice sequence using mock feature list
                sequence = fetch_strand(mock_feature, genome[mock_feature[0]])

                # Write sequence away to appropriate file
                location[0] = location[0].split(".")[0]+".fa"
                with open("fasta_resultaten/"+location[0], 'a') as outfile:
                    outfile.write(">seqstart:%i;seqstop%i+\n"%(mock_feature[2],
                                                               mock_feature[3]))
                    outfile.write(str(sequence.seq) + "\n")
            quit()
        if mode == "3":
            quit()
