#Het maken van de shortlist.
gunzip -c /home/bpexa/data/Brassica_oleracea.v2.1.39.chr.gff3.gz | more | awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9}' > vergelijk_lijst.txt
cat BPEXA_genes.tsv | awk {'print $2'} | sed '$d' > genID.txt
egrep -f vergelijk_lijst.txt > gff3_shortlist.txt

##Validatie stappen
#1. Invertarisatie van de shortlist
#cat ~/script/github/resultaten_project/shortlist/gff3_shortlist.txt | awk '{print $2}' | sort | uniq -c

#2. Duplicaten check
#cat ~/script/github/resultaten_project/shortlist/gff3_shortlist.txt | sort | uniq -c

#3. Hoeveel unieke genen zitten er in de aangeleverde genen lijst. En komt dit aantal overeen met wat in stap 1 is geconstateerd?
#cat ~/script/github/resultaten_project/shortlist/genID.txt | sort | uniq | wc -l

