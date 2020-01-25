### Documentation
#This program filters the gff3 of the whole genome into a smaller list. The shortlist contains the gene of interest.
gunzip -c /home/bpexa/data/Brassica_oleracea.v2.1.39.chr.gff3.gz | more | awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9}' > comparison.txt #Saves necessary columns in vergelijk_lijst.txt
cat BPEXA_genes.tsv | awk {'print $2'} | sed '$d' > genID.txt #Saves only the gene names into genID.txt
egrep -f genID.txt comparison.txt > gff3_shortlist.txt #Genenames are used as a search query in comparison.txt and saves the filtered shortlist in gff3_shortlist.txt


##Additional validation steps
#1. Invertarisation of the shortlist
#cat ~/script/github/resultaten_project/shortlist/gff3_shortlist.txt | awk '{print $2}' | sort | uniq -c

#2. Duplicate check
#cat ~/script/github/resultaten_project/shortlist/gff3_shortlist.txt | sort | uniq -c

#3. Amount of unique genes present in the shortlist. Does this corresponds with step 1?
#cat ~/script/github/resultaten_project/shortlist/genID.txt | sort | uniq | wc -l
