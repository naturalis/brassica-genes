import os
from Bio.Seq import Seq

def read_dir():
     file_list=[]
     file_listaa=[]
     for filename in os.listdir("fasta_resultaten/"):
    	 if filename.endswith(".fa"):
             file_list.append(filename)
             base = os.path.splitext(filename)[0]
             file_listaa.append(base+".aa")
     return (file_list,file_listaa)

def translator(file_list,aa):
     for i in range(len(file_list)):
         with open ("fasta_resultaten/"+file_list[i],'r') as f:
              header1 = f.readline().strip()
              sequence1 = f.readline().strip()
              header2 = f.readline().strip()
              sequence2 = f.readline().strip()
              seq1 = Seq(sequence1)
              seq2 = Seq(sequence2)
              seq_trans1=seq1.translate()
              seq_trans2=seq2.translate()
         with open("translated_fasta/"+aa[i],'w') as x:
              x.write(header1+"\n")
              x.write(str(seq_trans1)+"\n") 
              x.write(header2+"\n") 
              x.write(str(seq_trans2)+"\n") 

if __name__ == "__main__":
     file_list,file_listaa = read_dir()
     print (file_list[5])
     print (file_listaa[5]) 
     translator(file_list,file_listaa)
