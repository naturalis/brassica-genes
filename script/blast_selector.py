# Created by Rik Frijmann
# Last edit 12-JAN-2020

from os import listdir
from os.path import isfile
from os import remove


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
    """

    :param location: String containing the exact relative filepath to
        the BLAST file to be read.
    :return blast_result: A 2D-list; contains lists with a variety of
        Int, float and string elements detailing all results of a
        single BLAST result record.
    """
    with open(location, 'r') as infile:
        content = infile.readlines()
    blast_result = []
    for line in content:
        if line[0] != "#":
            line = line.rstrip("\n").split("\t")
            # temporarily commented out for testing!
            # line[2] = float(line[2])
            # for pos in range(3, 10):
            #    line[pos] = int(line[pos])
            # line[11] = int(line[11])
        blast_result.append(line)
    return blast_result


def select_chrom(results):
    query = results[0]
    blast_results = []
    for record in results:
        if query[2] == record[2]:
            blast_results.append(record)
    return results


if __name__ == "__main__":
    # Make it easier for the argument parsing
    blast_dr = "blast_resultaten/"

    # Prepare output file. Clear if exists; add header
    if isfile(dir+"target_gene_locations.txt"):
        remove(dir+"target_gene_locations.txt")
    with open(dir+"target_gene_locations.txt", 'a') as outfile:
        outfile.write("filename\tcontig\tstart\tend\n")

    # List all subject BLAST files
    blast_files = list_blast_files(blast_dr)

    # Loop over BLAST files
    for file in blast_files:
        # Open the current BLAST file
        blast_results = read_blast_file(dir+file)
        # If there is a BLAST result, start filtering
        if blast_results != []:
            blast_results = select_chrom(blast_results)
        if blast_results != []:
            # BLAST sorting guarantees highest bit-score comes first
            final_result = blast_results[0]
            with open(dir+"target_gene_locations.txt" 'a') as outfile:
                outfile.write(
                    "%s\t%s\t%s\t%s\n"%(file,
                                        blast_results[1],
                                        blast_results[8],
                                        blast_results[9],)
                )
        if blast_results == []:
            print("No BLAST results found for file: %s"%(file))
