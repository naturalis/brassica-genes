 #### SnpEff Documentation

SnpEff is a tool used to annotate and predict the effect of genetic variants.

 #### Input
SnpEff takes a VCF (variant call format) file as input (usually obtained after a sequencing experiment) . This file contains the predicted variants like SNPs, insertions, deletions and MNPs.
The location of the variant is discribed by the chromosome name and position.

 #### Processing
The effect impact is used to determine the impact the variant has on the genes. The main difference between a HIGH and a LOW impact is that a HIGH impact means that, according tot he SnpEff program, the variant results in damaging effects on the gene, while a LOW impact means that the variant has no damaging effects on the gene. A MODERATE impact has a more harmful effect on the gene than the LOW impact, but not as high as the HIGH impact.

The effects and annotations that SnpEff can calculate are listed in Tabel 1 below.

 #### Tabel 1 Effect types SnpEff can calculate and their meanings
|Effect type  | Meaning                          | Example                              |
|-------------|----------------------------------|--------------------------------------|
|SNP 	      | Single-Nucleotide Polymorphism   | Reference = 'A', Sample = 'C'        |
|Ins          | Insertion                        | Reference = 'A', Sample = 'AGT'      |
|Del          | Deletion                         | Reference = 'AC', Sample = 'C'       |
|MNP          | Multiple-nucleotide polymorphism | Reference = 'ATA', Sample = 'GTC'    |
|MIXED        | Multiple-nucleotide and an InDel | Reference = 'ATA', Sample = 'GTCAGT' |


Variants are the differences between a genome and a reference genome1. The places in the genome where the sample differs from the reference genome are called “genomic variants” or “variants”. Variants can be categorized as shown in Table 1.

 #### Output
SnpEff examines the input variants and returns the variants after annotating and calculating the effects on (known) genes1. The output of SnpEff is a huge file, it contains the differences between the used sample and the reference genome. The output is a bit similar to the VCF file used as input, the main difference is that the INFO-section is added to it. This section tells a bit more about the effect of the variant.


 #### Output headers explained
GeneName: Common gene name (HGNC). Optional: use closest gene when the variant is “intergenic”.
GeneId: GeneID
TranscriptId: Transcript's ID
BioType: Transcript's Biotype (if available)
variants_impact_HIGH : Count number of variants for HIGH impact				
variants_impact_LOW : Count number of variants for LOW impact
variants_impact_MODERATE : Count number of variants for MODERATE impact
variants_impact_MODIFIER : Count number of variants for MODIFIER impact
variants_effect_conservative_inframe_deletion :	Count number of variants for each effect type
variants_effect_conservative_inframe_insertion : X	
variants_effect_disruptive_inframe_deletion : One codon is changed and one or more codons are deleted
e.g.: A deletion of size multiple of three, not at codon boundary MODERATE

variants_effect_disruptive_inframe_insertion : One codon is changed and one or many codons are inserted
e.g.: An insert of size multiple of three, not at codon boundary MODERATE

variants_effect_downstream_gene_variant : Downstream of a gene (default length: 5K bases)  MODERATE
	
variants_effect_exon_loss_variant : A deletion removes the whole exon.  HIGH
variants_effect_frameshift_variant : Insertion or deletion causes a frame shift
e.g.: An indel size is not multple of 3 HIGH
	
variants_effect_initiator_codon_variant : Variant causes start codon to be mutated into another start codon (the new codon produces a different AA).
e.g.: Atg/Ctg, M/L (ATG and CTG can be START codons) LOW

variants_effect_intron_variant 	: Variant hits and intron. Technically, hits no exon in the transcript.	MODIFIER
		
variants_effect_missense_variant : Variant causes a codon that produces a different amino acid
e.g.: Tgg/Cgg, W/R 	MODERATE

variants_effect_non_canonical_start_codon : X	
variants_effect_non_coding_transcript_exon_variant : X
variants_effect_splice_acceptor_variant : The variant hits a splice acceptor site (defined as two bases before exon start, except for the first exon). 	HIGH
	
variants_effect_splice_donor_variant : The variant hits a Splice donor site (defined as two bases after coding exon end, except for the last exon). 	HIGH

variants_effect_splice_region_variant : A sequence variant in which a change has occurred within the region of the splice site, either within 1-3 bases of the exon or 3-8 bases of the intron. 	LOW 	
variants_effect_start_lost : Variant causes start codon to be mutated into a non-start codon.
e.g.: aTg/aGg, M/R 	HIGH

variants_effect_stop_gained : Variant causes a STOP codon
e.g.: Cag/Tag, Q/* 	HIGH

variants_effect_stop_lost : Variant causes stop codon to be mutated into a non-stop codon
e.g.: Tga/Cga, */R 	HIGH

variants_effect_stop_retained_variant : Variant causes stop codon to be mutated into another stop codon.
e.g.: taA/taG, */* 	LOW

variants_effect_synonymous_variant : Variant causes a codon that produces the same amino acid
e.g.: Ttg/Ctg, L/L 	LOW
	
variants_effect_upstream_gene_variant : Upstream of a gene (default length: 5K bases) 	MODIFIER

 #### Source: http://snpeff.sourceforge.net/SnpEff_manual.html