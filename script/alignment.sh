
#Dit programma aligned alles automatisch met elkaar.





#muslce -in Feature\:452.fa -out Feature\:452.afa
for ((i=0;i<910;i=i+1))
do
{
	muscle -in Feature\:$i.fa -out alignments/Feature\:$i.afa 
}
done
