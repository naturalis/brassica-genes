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
   for i in range (2):
        if i == 0 :
             gff3_file = raw_input("Specifiy the filename of the reference GFF3 file. ")
             genome_pathway = raw_input("Specify the name of the Brassica  fasta file. ")
        else:
             gff3_file = raw_input("Specifiy the filename of the Jersey Kale GFF3 file. ")
             genome_pathway = raw_input("Specify the name of the Jersey Kale fasta file. ")
        output = raw_input("Specify the name of the output fasta file. ")

        with open(output, 'w') as outfile:
             pass  # wipes output file.

        with open(genome_pathway, "rU") as handle:
             genome = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))

        feature_list = import_gff3(gff3_file)

        with open(output, 'a') as outfile:
            teller = 0
            for feature in feature_list:
                sequence = fetch_strand(feature, genome[feature[0]])
                outfile.write(">Feature:"+str(teller)+"\t%s\n"%(feature[-1]))
                outfile.write(str(sequence.seq)+"\n")
                teller+=1
