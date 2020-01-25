###Documentation
#This program uses FASTA formatted sequences originated from the slice script earlier in the pipeline.
#Each individual FASTA file is used by the BLAST algorithm to detect the most similar sequences.

#A nucleotide database for the target genome is created.
makeblastdb -in jerseykale_consensus.fa -dbtype nucl

#If the directory already exists, it gets removed. 
rm -f blast_resultaten/*
mkdir -p  blast_resultaten


fa=$( ls fasta_resultaten | wc -l ) #Determine the amount of files present in the directory
for ((i=1;i<=${fa};i=i+1))          #A loop is created in the directory that contains these FASTA files.
do
{
        file=$(ls fasta_resultaten | head -n ${i} | tail -n 1) #Method to select 1 file at the time
        file2=${file%.*}
        blastn -query fasta_resultaten/${file} -db jerseykale_consensus.fa -out blast_resultaten/${file2}.blast -outfmt 7  #Each individual FASTA file is used by
                                                                                                                           #the BLAST algorithm to detect the most similar sequences.
}
done


