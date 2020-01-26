 #### SnpEff Documentation
 ##### Summary

SnpEff is a tool used in order to annotate and predict the effects of genetic variants and explains the differences between the genome and the reference genome.
SnpEff takes predicted variants, usually a VCF (Variant Call Format) file, as input and generates a VCF file as output. 
This tool does not only tell you the differences between the genome and the reference genome but also gives a lot more information about these variants because of the annotation step.

SnpEff is an open source tool and can be installed on local computers as well as servers. The tool is written in Java and runs on Unix/Limnux, OS.X and Windows [1]. 


 #### Download and install
Downloading and installing is very simple and can be done using/via the next URL: http://snpeff.sourceforge.net/download.html
Follow these simple steps (just a double click on a ZIP file) and you can start using SnpEff.

 #### Usage
SnpEff requires a database for the annotation step. The user can choose to use a built-in database or to create their own database by following a few steps. The last case can be useful when using an organism which is not currently supported. If you want to know whether you need to built your own database or if the database you need is supported by SnpEff, just type in the following database command[1]:

$ java -jar snpEff.jar databases | less

This will show the name of the database and some info about it.

When the database is not available, you can build your own database (from reference genome files) with the next commandline:
$ java -jar snpEff.jar build -gff3 -v own_data


 #### Input
SnpEff takes a VCF (variant call format) file as input (created after a sequencing experiment). This file contains the predicted variants like SNPs, insertions, deletions and MNPs. 

Annotating the VCF file is done by running the next command line:
$ java -Xmx4g -jar snpEff.jar GRCh37.75 examples/test.chr22.vcf > test.chr22.ann.vcf

The verbose (-v option) can be useful for debugging since it shows a lot information, if you would like to use this mode, your input will look a bit like this:
$ java -Xmx4g -jar snpEff.jar -v GRCh37.75 examples/test.chr22.vcf > test.chr22.ann.vcf
[ This mode will also create a .html page containing the basic statistics about the analyzed variants ]


 #### Processing
SnpEff generates a tab separated file (“snpEff_genes.txt”) with the variants which have an effect on each transcript and gene. The file name can be changed with the -stats command line option.  The effect types that SnpEff can predict are SNPs, insertions, deletions, MNPs (Multiple Nucleotide Polymorphisms) and MIXED (multiple-nucleotide and an indel)[1].

SnpEff calculates the effect and returns an indication of how damaging the variant is to the gene (LOW, MEDIUM, HIGH, MODERATE). The main difference between a HIGH and a LOW impact is that a HIGH impact means that, according to the SnpEff program, the variant results in damaging effects on the gene, probably resulting in a shorter protein or  a loss of function, while a LOW impact means that the variant has no damaging effects on the gene, and does not change the protein at all. A MODERATE impact has a more harmful effect on the gene than the LOW impact, but not as high as the HIGH impact, it might result in a non-disruptive variant, changing the effect of the protein. A MODIFIER impact includes non-coding variants or variants which have an effect on non-coding genes[1].

 #### Output
The tab separated file (“snpEff_genes.txt”) contains 31 columns with info about the gene and 23 columns describing the effect of the variants found in the genome with the ‘variants_impact_*’ and ‘variants_effect_*’ columns.

SnpEff examines the input variants and returns the variants after annotating and calculating the effects on (known) genes[1]. SnpEff generates a VCF file similar to the input file but the main difference is that the eight column is added to it, this is the INFO section with all the annotation information.


 #### Output headers explained
|Column name						| Meaning								  |
| ----------------------------------------------------- | ----------------------------------------------------------------------- |
|GeneName						| Common gene name (HGNC). Optional: use closest gene when the variant is “intergenic”. |
|GeneId 						| GeneID
|TranscriptId 						| Transcript's ID
|BioType						| Transcript's Biotype (if available)
|variants_impact_HIGH					| Number of variants for high impact				
|variants_impact_LOW 					| Number of variants for low impact
|variants_impact_MODERATE 				| Number of variants for moderate impact
|variants_impact_MODIFIER 				| Number of variants for modifier impact
|variants_effect_conservative_inframe_deletion	 	| Number of variants for each effect type
|variants_effect_conservative_inframe_insertion		| X	
|variants_effect_disruptive_inframe_deletion 		| One codon is changed and one or more codons are deleted e.g.: A deletion of size multiple of three, not at codon boundary = *moderate*
|variants_effect_disruptive_inframe_insertion 		| One codon is changed and one or many codons are inserted e.g.: An insert of size multiple of three, not at codon boundary = *moderate* |
|variants_effect_downstream_gene_variant 		| Downstream of a gene (default length: 5K bases)  = *moderate* |
|variants_effect_exon_loss_variant 			| A deletion removes the whole exon  = *high*
|variants_effect_frameshift_variant 			| Insertion or deletion causes a frame shift e.g.: An indel size is not multple of 3 = *high* |
|variants_effect_initiator_codon_variant 		| Variant causes start codon to be mutated into another start codon (the new codon produces a different AA). e.g.: Atg/Ctg, M/L (ATG and CTG can be START codons) = *low* |
|variants_effect_intron_variant 			| Variant hits and intron. Technically, hits no exon in the transcript = *modifier* |	
|variants_effect_missense_variant 			| Variant causes a codon that produces a different amino acid e.g.: Tgg/Cgg, W/R 	= *moderate*  |
|variants_effect_non_canonical_start_codon 		| X	
|variants_effect_non_coding_transcript_exon_variant 	| X
|variants_effect_splice_acceptor_variant 		| The variant hits a splice acceptor site (defined as two bases before exon start, except for the first exon) = *high* |	
|variants_effect_splice_donor_variant 			| The variant hits a Splice donor site (defined as two bases after coding exon end, except for the last exon) = *high* |
|variants_effect_splice_region_variant 			| A sequence variant in which a change has occurred within the region of the splice site, either within 1-3 bases of the exon or 3-8 bases of the intron = *low* |	
|variants_effect_start_lost 				| Variant causes start codon to be mutated into a non-start codon. e.g.: aTg/aGg, M/R 	= *high* |
|variants_effect_stop_gained 				| Variant causes a STOP codon e.g.: Cag/Tag, Q/* 	= *high* |
|variants_effect_stop_lost 				| Variant causes stop codon to be mutated into a non-stop codon e.g.: Tga/Cga, */R 	= *high* |
|variants_effect_stop_retained_variant 			| Variant causes stop codon to be mutated into another stop codon. e.g.: taA/taG, */* 	= *low* |
|variants_effect_synonymous_variant 			| Variant causes a codon that produces the same amino acid e.g.: Ttg/Ctg, L/L 	= *low* |	
|variants_effect_upstream_gene_variant 			| Upstream of a gene (default length: 5K bases) 	= *modifier* |
 #### Source: http://snpeff.sourceforge.net/SnpEff_manual.html

