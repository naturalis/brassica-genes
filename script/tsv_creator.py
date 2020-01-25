import os

def read_dir():
     """
     This method iterates over the directory and retrieves the present filenames.
     """
     file_list=[]
     for filename in os.listdir("nuc_variant_calls/"):
         if filename.endswith(".var"):
            file_list.append(filename)
     return file_list

def create_vsf():
    """
    This method creates the .tsv file with correct column headers.
    """
    with open("slice_vs_snpEff.tsv",'w') as x:
         x.write("Slice script\t\t\tsnpEff\n")
         x.write("feature\tindels\tvariance count\tindels\tvariance count\n")

def interpretor(file_list):
    """"
    This method is used to proces the summary variance files.
    To achieve this goal the parameter file_list contains each indivdual summary file name.
    Each seperate feature present in this file gets filtered out using elaborate if/else statements.
    """
    for i in range(len(file_list)):
          title = file_list[i].split(".") 
          #Defining counters for relevant information
          exon_indels = 0
          gene_indels = 0
          exon_var = 0
          gene_var = 0
          snpEff_exon_var = 0 
          snpEff_indels_exon = 0
          snpEff_gene_var = 0
          snpEff_gene_ind = 0
          with open("nuc_variant_calls/"+file_list[i],'r') as file:
               content = file.readlines()
               for y in content:
                   rules=y.split("\t") #Splits the lines into seperate items.
                   if len(rules[0]) > 11 and rules[0][0] == "B" and rules[0][11] == "e": #Retrieving alignment exon features
                      exon_indels += int(rules[3])                                       # Collecting indel count
                      exon_var+= (int(rules[1].split(".")[0])-int(rules[2].split(".")[0])) #Collecting exon variant count. Splitting creates correct indexing for retrieval 
                   elif len(rules[0]) > 11 and rules[0][0] == "B" and rules[0][11] == "g" and len(rules) > 2 : #This step filters out remaining feature lines.
                        gene_indels += int(rules[3])
                        gene_var += (int(rules[1].split(".")[0])-int(rules[2].split(".")[0]))
                   if len(rules) == 3 and rules[1][0] == "g": #retrieve gene features out of snpEff file
                       snpEff_gene_var  += int(rules[1].split(" ")[1]) #SnpEff gene feature variant count .
                       snpEff_gene_ind += int(rules[2].split(" ")[2])  #Splitting " " creates correct indexes for retrieval
                   elif len(rules) == 3 and rules[1][0] == "G": #Retrieves exon features out of snpEff file.
                        snpEff_exon_var += int(rules[1].split(" ")[1])
                        snpEff_indels_exon += int(rules[2].split(" ")[2])
          filling_tsv(title,exon_indels,exon_var,gene_indels,gene_var,snpEff_exon_var,snpEff_indels_exon,snpEff_gene_var,snpEff_gene_ind) #After each seperate file the tsv file gets elongated.

def filling_tsv(title,exon_indels,exon_var,gene_indels,gene_var,snpEff_exon_var,snpEff_indels_exon,snpEff_gene_var,snpEff_gene_ind):
    """
    This method adds to the tsv format table with all the generated count information.
    To resemble the snpEff count table, for each gene name there are 2 seperate lines.
    One line contains all the observed indels and variations on the exons
    The other line contains all the observed indels and variations on other feature types.
    """
    with open( "slice_vs_snpEff.tsv",'a') as x:
         x.write(title[0]+".exon"+"\t"+str(exon_indels)+"\t"+str(exon_var)+"\t"+"\t"+str(snpEff_indels_exon)+"\t"+str(snpEff_exon_var)+"\n") #exon line.
         x.write(title[0]+".gene"+"\t"+str(gene_indels)+"\t"+str(gene_var)+"\t"+"\t"+str(snpEff_gene_ind)+"\t"+str(snpEff_gene_var)+"\n")    #Remaining feature line.

if __name__ == "__main__":
   file_list = read_dir()
   create_vsf()
   interpretor(file_list)
