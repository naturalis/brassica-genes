#Het maken van de shortlist.

gunzip -c /home/bpexa/data/Brassica_oleracea.v2.1.39.chr.gff3.gz | more | awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9}' >> vergelijk_lijst.txt

egrep -f id_lijst.txt vergelijk_lijst.txt  >> gff3_short_list.txt

##Validatie stappen
#1. Invertarisatie van de shortlist
cat gff3_short_list.xt | awk '{print $2}' | sort | uniq -c

#2. Duplicaten check
cat gff3_short_list.txt | sort | uniq -c

#3. Checken of alle genen in de aangeleverde ID_lijst ook in de shortlist vertegenwoordigd zijn.
cat id_lijst.txt | egrep -vf gegenereerde_79_genen.txt

#4. Hoeveel unieke genen zitten er in de aangeleverde genen lijst. En komt dit aantal overeen met wat in stap 1 is geconstateerd?
cat id)lijst.txt | sort | uniq | wc -l
