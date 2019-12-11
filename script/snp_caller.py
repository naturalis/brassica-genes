# Created by Rik Frijmann.
# Last edit 07-12-2019.
# A rudimentary script counting the most common types of SNPs.
# The script currently counts synonimous, non-synonimous and indels.
# Short changelog:
#
# Current issues:
#

import os
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.Alphabet import generic_protein


def find_indel(seqs):
    """
    Finds indels on any given sequence. Formatting rules mean no gap
    marker can exists opposing another gap marker. Thus, counting
    individual gaps on both strands totals the amount of indels in the
    alignment between both strands.
    :param seqs: A list containing two SeqIO objects, containing both
        sequences necessary to compare.
    :return indel_count: An integer, signifying the amount of indels
        occuring between both given sequences.
    """
    indel_count = 0
    for seq in seqs:
        gap_open = True
        for pos in range(0, len(seq)):
            if seq[pos] == "-" and gap_open is True:
                gap_open = False
                indel_count += 1
            elif seq[pos] != "-" and gap_open is False:
                gap_open = True
    return indel_count


def find_syn_nonsyn(seqs):
    """
    Finds indels on any given sequence. Formatting rules mean no gap
    marker can exists opposing another gap marker. Thus, counting
    individual gaps on both strands totals the amount of indels in the
    alignment between both strands.
    :param seqs: A list containing two SeqIO objects, containing both
        sequences necessary to compare.
    :return indel_count: An integer, signifying the amount of indels
        occuring between both given sequences.
    """
    syn_count, nonsyn_count = 0, 0
    for pos in range(0, len(seqs[0]), 3):
        codon1 = seqs[0][pos:pos+3]
        if len(codon1) == 3:
            codon2 = seqs[1][pos:pos + 3]
            if codon1 != codon2 \
                and "-" not in codon1 \
                and "-" not in codon2:
                aa1 = codon1.translate()
                aa2 = codon2.translate()
                if aa1 == aa2:
                    syn_count += 1
                elif aa1 != aa2:
                    nonsyn_count += 1
    return syn_count, nonsyn_count


if __name__ == "__main__":
    path = "feature_alignments/"

    snp_dict = {}
    for filename in os.listdir(path):
        snp_dict[filename] = {"indel":0,
                              "silent":0,
                              "syn":0,
                              "nonsyn":0}
        alignment = AlignIO.read(path+filename, "fasta")
        seq1 = alignment[0].seq
        seq2 = alignment[1].seq

        snp_dict[filename]["indel"] = find_indel([seq1, seq2])

        #seq1 = seq1.ungap("-")
        #seq2 = seq2.ungap("-")
        snp_dict[filename]["syn"], snp_dict[filename]["nonsyn"] = \
            find_syn_nonsyn([seq1, seq2])

        print(snp_dict)
