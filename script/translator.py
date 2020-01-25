import shutil
import os
from Bio.Seq import Seq

def read_dir():
     """
     This function loops over all the files that are present in the directory "fasta_resultaten".
     The file names are retrieved and get stored in file_list.
     file_listaa contains the same filenames with a different extension. Instead of .fa it now has .aa
     """

     file_list=[]
     file_listaa=[]
     for filename in os.listdir("fasta_resultaten/"):
    	 if filename.endswith(".fa"):  #Only fetch fasta files.
             file_list.append(filename) 
             base = os.path.splitext(filename)[0] #Remove the .fa extension.
             file_listaa.append(base+".aa")       #Place new aa extension to filename.
     return (file_list,file_listaa)               #file_listaa contains file names with .aa extension.

def translator(file_list,aa):
     """
     This function receives the file_names from the read_dir function.
     These extention .fa files are being opened and the sequences that are present get translated.
     The extention .aa filenames are used to create new files.
     The translated sequences get saved into these files.
     """
     for i in range(len(file_list)):
         with open ("fasta_resultaten/"+file_list[i],'r') as f:
              header1 = f.readline().strip()
              sequence1 = f.readline().strip()
              header2 = f.readline().strip()
              sequence2 = f.readline().strip()
              seq1 = Seq(sequence1) #Without this step the bio.python module wont recognize it as a sequence.
              seq2 = Seq(sequence2)
              seq_trans1=seq1.translate() #The actual translation step.
              seq_trans2=seq2.translate()
         with open("translated_fasta/"+aa[i],'w') as x:
              x.write(header1+"\n")
              x.write(str(seq_trans1)+"\n") 
              x.write(header2+"\n") 
              x.write(str(seq_trans2)+"\n") 

if __name__ == "__main__":
     try:
        os.mkdir("translated_fasta") #Creating directory.
     except FileExistsError:         
        shutil.rmtree("translated_fasta") #Remove directory.
        os.mkdir("translated_fasta")      #Create new one.
     file_list,file_listaa = read_dir()
     translator(file_list,file_listaa)
