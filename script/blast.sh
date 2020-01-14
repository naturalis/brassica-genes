#Documentation
#This program uses FASTA formatted sequences originated from the slice script earlier in the pipeline.
#First of all a nucleotide database is created of the target genome.
#A loop is created over the directory that contains these FASTA files.
#Each individual FASTA file is used by the BLAST algorithm to detect the most similar sequences.

#makeblastdb -in jerseykale_consensus.fa -dbtype nucl

rm -f blast_resultaten/*
mkdir -p  blast_resultaten

fa=$( ls fasta_resultaten | wc -l )
for ((i=1;i<=${fa};i=i+1))
do
{
        file=$(ls fasta_resultaten | head -n ${i} | tail -n 1)
        file2=${file%.*}
        blastn -query fasta_resultaten/${file} -db jerseykale_consensus.fa -out blast_resultaten/${file2}.blast -outfmt 7
}
done

#Het verwerken van een output file. We hebben nodig: GenID, op welk chromosoom ligt het, en waar op dat chromosoom.
# cat output.txt | egrep -v [#] | awk {'print $1"\t"$2"\t"$9"\t"$10'} > output_gefilterd.txt #Alle bruikbare informatie is nu verzameld vanuit de output file
