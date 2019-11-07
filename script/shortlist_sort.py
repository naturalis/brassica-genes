#!/usr/bin/python3
# Created by Rik Frijmann.
# Last edit: 05/11/2019.
# Short changelog:
# 29/10/2019:   Added output method to write new/updated GFF3.
# 28/10/2019:   Continued building on outline.
# 27/10/2019:   Created outline and infrastructure for the script.
# 04/11/2019:   Added functionality to add NonCoding Region to
#   cluster variables.
# 05/11/2019:   Added functionality to resort cluster elements to
#   include the NCR, properly outputs gffex-file with all gff3 records.
#
# Current issues:
# 1. Script is not particularly memory friendly. Consider use on GFF3-
# files of <1000 records.
# 2. Script contains a way to determine gene IDs that may not be
# universally applicable to all GFF3-format files. It does apply for
# the project this script was originally written for.
# 3. Function add_ncs() does not meet PEP-8 standards.
# 4. Temporarily creates duplicate dictionary when resorting clusters.
#   which may cause unnecessary memory issues with larger tasks.

from itertools import islice


def add_ncs(cluster, strand):
    """
    NCS (Non Coding Sequences) are the parts of a gene not covered by
    other elements on a gene. Meaning from the start of the gene, to
    the end of the gene, all parts not covered by exon elements
    are to be considered NCS. All instances of NCS of a gene
    are added to the id_record_cluster list as a new record.
    :param cluster: A 2D list containing all cluster elements.
    :param strand: A string indicating the strand the cluster is on.
    :return cluster: A 2D list containing all cluster elements,
        including records for noncoding region elements.
    """
    exons, ncr = [], []
    for record in cluster:
        if record[1] == "gene":
            gene_range = [record[2], record[3], abs(record[3]-record[2]+1)]
        if record[1] == "exon":
            exons.append([record[2], record[3]])
    if strand == "+":
        pass
        exons.append([gene_range[1]+1, gene_range[1]+1])  # Sets end range
        ncr_start = gene_range[0]
        while ncr_start < gene_range[1] and len(exons) > 0:
            ncr_end = exons[0][0]-1  # first exon start
            if ncr_start < ncr_end:
                ncr.append([ncr_start, ncr_end])
            ncr_start = exons[0][-1]+1  # Skip to end current exon
            del exons[0]  # Remove current exon
    elif strand == "-":
        exons.append([gene_range[0]-1, gene_range[0]-1])  # Sets end range
        ncr_start = gene_range[1]
        while ncr_start > gene_range[0] and len(exons) >0:
            ncr_end = exons[0][-1]+1  # first exon start
            if ncr_start > ncr_end:
                ncr.append([ncr_end, ncr_start])
            ncr_start = exons[0][0]-1  # Skip to end current exon
            del exons[0]  # Remove current exon
    cluster = make_records(cluster, ncr, "ncr")
    return cluster


def check_for_exon(cluster, type):
    """
    This function checks a 2D list for the presence of a record type as
    specified in the paramater 'type'. If the type of record is present
    in the cluster, the function returns the boolean value 'True'. If
    the record type is not found in the cluster, the boolean value
    'False' is returned instead.
    :param cluster: A 2D list containing all GFF3 records belonging to
        one gene parent.
    :param type: String containing the type of record the function checks
        the cluster for.
    :return Boolean: Return is true if the record type is present, return
        is false if the record type is not present.
    """
    for record in cluster:
        for field in record:
            if field == type:
                return "True"
    return False


def cluster_gene_elements(gff3_list):
    """
    Accepts a 2D list of GFF3-file records. Pops the last record and
    fetches the ID of the gene the gene product relates to (either from
    the ID field, or the extra information field). The record is saved
    in a new list. Then loops through all records, popping all elements
    with the same ID, saving all in the new list.
    The list of all records sharing a common ID is saved in the dict
    cluster_dict, using the ID as key and the 2D list as value.
    :param gff3_list: 2D list, containing all records of a GFF3
        formatted file.
    :return cluster_dict: dictionary, using gene identifier as key, and
        a 2D list of all records related to that gene identifier as
        value.
    """
    cluster_dict = {}
    for record in gff3_list:
        if record[1] == "gene":
            id = record[-1].split(";")[0].split(":")[-1]  # may be
            # project specific
            cluster_dict[id] = []
    for id in cluster_dict.keys():
        for record in gff3_list:
            if id in record[-1]:
                cluster_dict[id].append(record)
    return cluster_dict


def read_shortlist(filepath):
    """
    Opens a shortlist in GFF3 format (or plain GFF3-file) at the
    location specified in filepath. This shortlist is stored in a list,
    consisting of list elements, containing all the fields for each
    record. This 2D list is then returned.
    :param filepath: String containing the location of the GFF3-file
        or shortlist in GFF3-format.
    :return shortlist: 2D list containing all records and fields of
        the shortlist or GFF3-file.
    """
    feature_list = []
    with open(filepath, 'r') as infile:
        iterdata = infile.readlines()
        for line in islice(iterdata, 1, None):
            line = line.strip("\n").split("\t")
            feature_list.append([line[0], line[2], int(line[3]), int(line[4]), line[5], line[6], line[7], line[8]])
    return feature_list


def make_records(cluster, locations, type):
    """
    Creates record-like lists to add to clusters, to create uniform
    output of newly added records later in the script.
    :param cluster: Contains a 2D list with records of gene elements.
    :param locations: a 2D list with start and stop position of
        elements to be added to the cluster.
    :param type: Type of elements to be added.
    :return cluster: A 2D list with records of gene elements,
        including newly added records of the pre-specified type.
    """
    id = cluster[0][-1].split(";")[0].split(":")[-1]  # may be project specific
    ncr_count = 1
    for element in locations:
        if element[0] > element[1]:
            element = [element[1], element[0]]
        cluster.append([cluster[0][0],
                       type,
                       element[0],
                       element[1],
                       ".",
                       cluster[0][5],
                       ".",
                       "parent_gene=%s;ncr=%i"%(id, ncr_count)])
        ncr_count += 1
    return cluster


def sort_cluster_dict(cluster_dict):
    """
    For every list of DNA features sharing a parent gene, the group
    will be sorted as such that they are in order of transcription.
    This is 5' to 3', or start to end, for the + strand, and 3' to 5',
    or end to start, for the - strand. A starting position of the
    gene feature in the relevant frame is added to the list in
    position 0. The sorted cluster dictionary is then returned.
    :param cluster_dict: dictionary with gene IDs as keys and a 2D
        list of gene related elements as values.
    :return cluster_dict: Start position of cluster, then the ID of
        the gene the list's elements are related to, then 2D list,
        containing lists of GFF3 records, sorted by order of
        transcription.
    """
    for cluster_id in cluster_dict.keys():
        if cluster_dict[cluster_id][0][5] == "+":
            cluster_dict[cluster_id].sort(key=lambda x: int(x[2]))
            cluster_dict[cluster_id] = [cluster_dict[cluster_id][0][2],  # Start position of first transcribed element
                                        cluster_dict[cluster_id][0][0],  # Chromosome elements are lcoated on
                                        cluster_dict[cluster_id]]  # sorted cluster elements
        elif cluster_dict[cluster_id][0][5] == "-":
            cluster_dict[cluster_id].sort(reverse=True, key=lambda x: int(x[3]))
            cluster_dict[cluster_id] = [cluster_dict[cluster_id][-1][3],  # Start position of first transcribed element
                                        cluster_dict[cluster_id][0][0],   # Chromosome elements are located on
                                        cluster_dict[cluster_id]]  # sorted cluster elements
    return cluster_dict


if __name__ == "__main__":
    path_shortlist = "testgff3_01.txt"  # in absence of an arg parser
    path_outfile = "shortlist.gffex"

    #  read shortlist
    feature_list = read_shortlist(path_shortlist)

    #  cluster gene elements
    #  start at element 0 of 2D shortlist list, grab all elements
    #  with same ID. Write out to global dict with key==ID, element
    #  == 2D list
    cluster_dict = cluster_gene_elements(feature_list)

    #  for every cluster of elements
    #  if + strand: sort elements by start pos.
    #  if - strand: sort elements by stop pos (- strand reads from end
    #  to start, so that is how GFF3 and fasta file should store them.
    #  loop through all elements:
    #  in pos 0, insert the position of the first element in the
    #  relevant reading frame. Meaning the lowest start pos in + frame,
    #  and the highest end pos in - frame. This is done for easier
    #  sorting output later on
    cluster_dict = sort_cluster_dict(cluster_dict)

    #  Sort elements by first base (reading each strand from left to
    #  right). Stable sort is used to sort this order for every
    #  chromosome.
    cluster_list = []
    for key in cluster_dict.keys():
        cluster_list.append(cluster_dict[key])
    cluster_list.sort(key=lambda x: int(x[0]))
    cluster_list.sort(key=lambda x: x[1])  # Use stable sorting.

    #  add non coding regions
    for cluster_no in range(len(cluster_list)):
        if check_for_exon(cluster_list[cluster_no][-1], "exon"):
            cluster_list[cluster_no][-1] = add_ncs(cluster_list[cluster_no][-1],  # Cluster
                                                   cluster_list[cluster_no][-1][0][5])  # Strand cluster is on

    #  Sort noncoding regions into the clusters
    temp_dict = {}
    for i, cluster_id in enumerate(cluster_dict.keys(), 1):
        temp_dict[i] = cluster_dict[cluster_id][-1]
    cluster_dict = sort_cluster_dict(temp_dict)
    del temp_dict

    #  Write output to .gffex file.
    with open(path_outfile, 'w') as outfile:
        for cluster in cluster_dict.keys():
            for record in cluster_dict[cluster][-1]:
                record = "\t".join(
                    [str(field) for field in record]
                )
                outfile.write(record+"\n")
