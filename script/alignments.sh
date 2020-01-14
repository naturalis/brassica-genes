rm -f alignments/*
mkdir alignments
cd fasta_resultaten
fa=$( ls | wc -l )
for ((i=1;i<=${fa};i=i+1))
do
{
	file=$(ls | head -n ${i} | tail -n 1)
	file2=${file%.*}
        muscle -in ${file} -out ../alignments/$file2.al
}
done

cd ../translated_fasta

fa=$( ls | wc -l )
for ((i=1;i<=${fa};i=i+1))
do
{
        file=$(ls | head -n ${i} | tail -n 1)
        file2=${file%.*}
        muscle -in ${file} -out ../alignments_translated/$file2.al
}
done


