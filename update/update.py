import random

import pandas as pd

from OntologyNode import findNodes, getDescendantNodes, getUpper
from utility.ReadFD import reFD
from utility.ReadJson import reJson


path='../data/test1/1000gdb.csv'
df=pd.read_csv(path,header=0)
df=pd.DataFrame(df,columns=['PID','GEN','AGE','SYMP','DRUG','ILLNESS'])


print(df)


age=reJson('../data/test1/age.json')
symp=reJson('../data/test1/symp.json')
gen={1:'male',2:'female'}
drug={}
illness={}
fd=reFD('../data/test1/fd.csv')

'''

单独存一个fd集，只存fd所在的列数

'''

fdcolumns=[3,4,5]

'''
不在fdcolumns的才存domain

'''

domain=[{0:{'number':'1,1000'}},
        {1:{'value':gen}},
        {2:{'ontology':age}},
       ]



def update(amount,df,domain,fdcolumns):

    update=[]

    for i in range(0,amount):

        randomrow=random.randint(0,len(df))

        # tag=random.randint(0,1)
        tag=0


        if tag==0:  ##更改非fd列

            max=len(domain)-1

            rand=random.randint(0,max)

            randomcol=domain[rand]

            for c in randomcol:

                col=c
                coldom=randomcol[c]

            print(col,coldom)

            for d in coldom:



                if d=='ontology':

                    root=coldom[d]
                    print(root)
                    print('write a function generate node value randomly')

                if d=='value':

                    dd=coldom[d]
                    print(dd)
                    max=0
                    for i in dd:
                        max=max+1
                    choice=dd[random.randint(1,2)]

                    record=[randomrow,col,choice]
                    update.append(record)

                if d=='number':
                    dd = coldom[d]
                    print(dd)
                    rg=dd.split(',')
                    min=int(rg[0])
                    max=int(rg[1])
                    print(min)
                    print(max)

                    choice=random.randint(min,max)
                    record=[randomrow,col,choice]
                    update.append(record)

    return update

update(1,df,domain,fdcolumns)

# print(df.ix[2][3])