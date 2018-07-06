import os, operator, tkFileDialog, Tkinter, textwrap, time, sys, pdb

os.system("title IndexMi")
print ("IndexMi")
print("Please Select a FASTQ File")
time.sleep(1)

#Originally used sys.argv to provide file name from CMD, but GUI of Tkinter is easier for other users
rootwindow = Tkinter.Tk()
rootwindow.withdraw()
fastq_file = tkFileDialog.askopenfilename(parent=rootwindow,
                                          filetypes=[("fastq", "*.fastq")],
                                          title="IndexMi")

if fastq_file=="":
    print ("No File Selected")
    raw_input("Press Enter to Quit: ")
    sys.exit()
    
os.chdir(os.path.dirname(fastq_file))
fastq=open(fastq_file,'r')

#empty dict of all index combinations in fastq to add to later
indexes={}

#Dict of i5 indexes
i5={'TGAACCTT':'A501',
    'TGCTAAGT':'A502',
    'TGTTCTCT':'A503',
    'TAAGACAC':'A504',
    'CTAATCGA':'A505',
    'CTAGAACA':'A506',
    'TAAGTTCC':'A507',
    'TAGACCTA':'A508',
    }
#Dict of i7 indexes
i7={'ATCACGAC':'A701',
    'ACAGTGGT':'A702',
    'CAGATCCA':'A703',
    'ACAAACGG':'A704',
    'ACCCAGCA':'A705',
    'AACCCCTC':'A706',
    'CCCAACCT':'A707',
    'CACCACAC':'A708',
    'GAAACCCA':'A709',
    'TGTGACCA':'A710',
    'AGGGTCAA':'A711',
    'AGGAGTGG':'A712',
    }

print textwrap.fill("Collecting All Index Combinations in: " + fastq_file)
#goes through each line and skips unless starts with "@M0" (ID line, where indexes are)
#Indexes are at the end of the ID line, after the final ":"
#creates new entry if index combination not in indexes dict, else increase count
#of existing entry
for line in fastq:
    if line[:3]=="@M0":
        index=((line.split(":")[-1]).strip('\n'))
        if index not in indexes:
                indexes[index]=1
        elif index in indexes:
                indexes[index]+=1

#makes nested tuples, sorted by most common count e.g
#((COMBO1,COUNT1),(COMBO2,COUNT2)...)
sorted_indexes=sorted(indexes.items(), key=operator.itemgetter(1), reverse=True)

Report=open("IndexMi_Report.txt",'w')

#Writes sorted tuple pairs into a tab seperated text doc.
for i in range(len(sorted_indexes)):
    #saves the Index combination as i7xx+i50x if valid, if not a valid index (dict KeyError): NO MATCH
    try:
        Combo=i7[sorted_indexes[i][0].split("+")[0]] + "+" + i5[sorted_indexes[i][0].split("+")[1]]
        #Prints a notificiation for combinations that are found more than 1,000 times
        if sorted_indexes[i][1]>1000:
            print
            print ("FOUND!")
            time.sleep(2)
            print textwrap.fill("THE INDEX COMBINATION {} WAS FOUND {:,} TIMES".format(Combo, sorted_indexes[i][1]))
            time.sleep(3)                                              
    except (KeyError):
        Combo = "NO MATCH"                                                    
    Report.write(("{0}\t{1}\t{2}\t{3}\n".format(i+1,sorted_indexes[i][1], sorted_indexes[i][0],Combo)))

Report.close()
print
print
print textwrap.fill("Full Index Report Saved as: " +os.path.join(os.path.dirname(fastq_file),"IndexMi_Report.txt"))
print
print
raw_input("Press Enter to Quit: ")
