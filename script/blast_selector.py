# Created by Rik Frijmann
# Last edit 12-JAN-2020

from os import listdir
from os.path import isfile


def list_blast_files(dir):
    """This function lists all directories and files in a given
    directory, filters out only the files, and returns a list
    containing the filenames.
    :param dir: String containing the path towards the directory
        to be checked.
    :return blast_files: List, contains one string for every filename
        in the 'dir' directory.
    """
    dir_content = listdir(dir)
    blast_files = []
    for file in dir_content:
        if file.isfile():
            blast_files.append(file)
    return blast_files


def read_blast_file(location):
    with open(location, 'r') as infile:
        content = infile.readlines()
    blast_result = []
    for line in content:
        if line[0] != "#":
            line = line.rstrip("\n").split("\t")
            line[2] = float(line[2])
            for pos in range(3, 10):
                line[pos] = int(line[pos])
            line[11] = int(line[11])
        blast_result.append(line)
    return blast_result


if __name__ == "__main__":
    # Make it easier for the argument parsing
    blast_dr = "blast_resultaten/"

    # List all subject BLAST files
    blast_files = list_blast_files(blast_dr)

    # Loop over BLAST files
    for file in blast_files:
        # Open the current BLAST file:
        result = read_blast_file(dir+file)


