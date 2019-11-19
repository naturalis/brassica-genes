def import_indels(indel_file):
    indel_list = []

    with open(indel_file, "r") as f:
        while True:
            line = f.readline().strip("\n").split(" ")
            if len(line) > 1:
                indel_list.append([line[0:len(line)]])
            else:
                break
    return indel_list

def gff3(indel_lijst,input_file):
    pl = []
    with open(input_file, "r") as x, open("updated_gff3.txt","w") as updated_gff3:
        while True:
            line = x.readline().split("\t")
            if len(line) > 1:
                for y in indel_lijst:
                    if line[0] == y[0][0] and y[0][1] >= line[3] and y[0][1] < line[4] and not line in pl:
                        if y[0][2] == 'ins':
                            end_position = int(line[4]) + int(y[0][3])
                        elif y[0][2] == 'del':
                            end_position = int(line[4]) - int(y[0][3])
                        new_line = updating_gff3(line,str(end_position))
                        pl.append(line)
                    elif line[0] == y[0][0] and y[0][1] >= line[3] and y[0][1] < line[4]and line in pl:
                        if y[0][2] == 'ins':
                            end_position= end_position+int(y[0][3])
                            new_line = updating_gff3(line,str(end_position))
                        elif y[0][2] == 'del':
                            end_position = end_position - int(y[0][3])
                            new_line = updating_gff3(line, str(end_position))

                #Hier worden de lines weggeschreven die niet muteren!
                if not line in pl:
                    updated_gff3.write(line[0] + '\t' + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\t" +
                            line[
                                5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8])
                elif line in pl:
                    updated_gff3.write(new_line)
            else:
                break

def updating_gff3(line,end_pos):
     new_line=(
        line[0] + '\t' + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + end_pos + "\t" +
        line[
            5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8])
     return new_line

if __name__ == "__main__":
    indel_file = raw_input("Specifiy the indel file name. ")
    input_file = raw_input("Specifiy the original GFF3 filename. ")
    indel_lijst = import_indels(indel_file)
    gff3(indel_lijst,input_file)
