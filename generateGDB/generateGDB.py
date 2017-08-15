import csv
import random

list=[]

fd={1:['fever','Advil','incluenza'],
    2:['fatigue','Penicillin','scarlatin'],
    3:['fever','Metformin','type 2 diabetes'],
    4:['fatigue','Advil','cold'],
    5:['fatigue','Clofarabine','leukemia'],
    6:['itchiness','Aldara','common wart'],
    7:['itchiness','Clobex','dermatits']}

gen={1:'male',2:'female'}

for i in range (0,1000):

    tupple=[]
    #
    # tid='m'+str(i)
    # tupple.append(tid)

    PID=random.randint(1, 1000)
    tupple.append(PID)

    randomG=random.randint(1,2)
    GEN=gen[randomG]
    tupple.append(GEN)

    AGE=random.randint(1,100)
    tupple.append(AGE)

    randomFD=random.randint(1,7)
    SDI=fd[randomFD]

    for element in SDI:
        tupple.append(element)

    print(tupple)
    list.append(tupple)

with open("../data/test1/1000gdb.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    #先写入columns_name
    writer.writerow(["PID","GEN","AGE","SYMP","DRUG","ILLNESS"])
    #写入多行用writerows
    writer.writerows(list)