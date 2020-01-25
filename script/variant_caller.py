import os

def read_dir():
     """
     This function retrieves all the filenames out of the directory alignments.
     These file names are used in a later stadium to perform the actual variant calling process.
     The genID.txt file is used to retrieve gen names. These gen names are used in a later stadium
     of the proces to open variant files.
     """
     file_list=[]
     title_list = []
     for filename in os.listdir("alignments/"):
         if filename.endswith(".aln"): #Retrieve only alignment files.
             file_list.append(filename)
     with open ("genID.txt",'r') as x: #The genID.txt file contains relevant gene names.
          while True:
              rule = x.readline()
              if len(rule) > 0: #If the rule is empty, the program does not use it.
                 if rule[0] == "B": #Only fetch gen names.
                    title_list.append(rule) #The title_list is used to create the variant files in a later stadium
              else:
                 break
     return file_list,title_list

def file_creator(title_list):
    """
    This method creates the ouput file with tab seperated columns.
    """
    for file_name in title_list: #title names are retrieved out of genID.txt
        with open ("nuc_variant_calls/"+file_name.strip()+".var",'w') as x:
             x.write("Feature type\tAlignment length\tIdentical nucleotides\tIndel count\n") #Table headers.

def interpretor(file_list):
    """
    This method interpets the alignment files.
    The length of the alignments is determined.
    The amount of identical matches are retrieved.
    And the amount of indels are determined.
    """
    for i in range(len(file_list)):
        l_seq = 0
        l_var = 0
        l_ind = 0
        inds = 0 #This variable is used to specify wheter there are more than 1 "-" in a row.
        with open("alignments/"+file_list[i],'r') as f:
             regel = f.read().split() #Viewing each file as a whole.
             for item in regel[5:]: #Only from the 5th element there is relevant information present.
                 if item.startswith("*"):
                    l_var += (len(item))
                 elif item[0].isupper() or item[0] == "-": #only lines that starts with capital letters or - are sequence lines.
                    for char in item: #Viewing individual character in list item.
                        if char == "-" or char.isupper(): 
                           l_seq += 1
                           if char == "-":
                              inds+=1
                           elif char.isupper() and inds != 0: # if inds > 1. This means there are more than 1 "-" in a row.
                              l_ind+=1                        # This is important because the program needs to reconginze this as 1 indel.
                              inds = 0                        # Reset the indel count.

        fill_var_calls(file_list[i],l_seq,l_var,l_ind) #After each iteration the the file_var_calls method is executed.

def fill_var_calls(file,length,var,indels):
    """
    This program fills the file with the variance and indel counts.
    """ 
    titel = file[0:10] 
    with open ("nuc_variant_calls/"+titel+".var",'a')as outfile:
         outfile.write(
                    "%s\t%s\t%s\t%s\n"%(file,
                                        length/2, #Length is divided by 2 because the alignment contains 2 sequences.
                                        var,
                                        indels)
                )

if __name__ == "__main__":
     file_list,title_list = read_dir()
     file_creator(title_list)
     interpretor(file_list) 
