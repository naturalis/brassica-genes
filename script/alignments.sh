##Documentation
#This program automatically performs all alignments. Nucleotide and Amino acids alingments need to be performed.

rm -f alignments/*
rm -f alignments_translated/*
mkdir alignments
mkdir alignments_translated

cd fasta_resultaten
fa=$( ls | wc -l ) #Determine how many files are present in the file.
for ((i=1;i<=${fa};i=i+1)) #Loop over all files.
do
{
	file=$(ls | head -n ${i} | tail -n 1) #Fetching filename
	file2=${file%.*} #Remove the original extension. 
        muscle -in ${file} -clwout ../alignments/$file2.aln #Performing the actual alignment. Creating .aln files.
}
done

cd ../translated_fasta #Switch to correct directory
fa=$( ls | wc -l )
for ((i=1;i<=${fa};i=i+1))
do
{
        file=$(ls | head -n ${i} | tail -n 1)
        file2=${file%.*}
        muscle -in ${file} -clwout ../alignments_translated/$file2.aln
}
done

cd ..
