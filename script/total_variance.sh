###Documentation
#This script adds more rules to the variance files.
#First it calculates a total of each column
#Second it retrieves total observations out of the snpEff table.

cd nuc_variant_calls #change directory

fa=$(ls | wc -l)     #Determine how many files are present in that directory
for ((i=1;i<=${fa};i=i+1)) #Loop over x amount of files.
do
{
	file=$(ls | head -n ${i} | tail -n 1) #Fetch file name
	total_alignment=$(cat ${file} | awk '{SUM += $2} END {print SUM}') #Calculate total alignment length.
	total_id=$(cat ${file} | awk '{SUM += $3} END {print SUM}')        #Calculate total identical nucleotides.
	total_indel=$(cat ${file} | awk '{SUM += $4} END {print SUM}')     #Calculate total amount of indels.
	printf "Total\t${total_alignment}\t${total_id}\t${total_indel}\n" >> ${file} #Append the observations to filename.
	file2=${file%.*}                                                   #Remove file extension of gene name.The program is able to grep this gene out of snpEff file.
	snpEff_indel_gene=$(cat ../snpEff_goi.txt | awk '{print $2,$9+$10+$11+$12}' | grep "${file2}.*" | grep "gene") #Retrieve specific gene out of snpEff file. 
                                                                                                                       #Calculate total amount of indels on gene feature
        snpEff_indel_exon=$(cat ../snpEff_goi.txt | awk '{print $2,$9+$10+$11+$12}' | grep "${file2}.*" | grep "exon") 
                                                                                                                       #Calculate total amount of indels on exon feature 
	snpEff_tv_gene=$(cat ../snpEff_goi.txt | awk '{print $2, $8}' | grep "${file2}.*" | grep "gene")
        snpEff_tv_exon=$(cat ../snpEff_goi.txt | awk '{print $2, $8}' | grep "${file2}.*" | grep "exon")
        printf "${file}: Exon variant:\t${snpEff_tv_exon}\tExon indels${snpEff_indel_exon}\n"  >> ${file}
	printf "${file}: Gene variant:\t${snpEff_tv_gene}\tGene indels${snpEff_indel_gene}\n"  >> ${file}
}
done
cd .. #Change back to main directory.
