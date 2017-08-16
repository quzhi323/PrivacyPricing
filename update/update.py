import random

import pandas as pd

from OntologyNode import findNodes, getDescendantNodes, getUpper, getRandom
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


def fdpattern(df,fdcolumns):
    patternlist=[]
    length=len(df)
    for l in range(0,length):
        t=[]
        for c in fdcolumns:
            t.append(df.ix[l][c])
        if t not in patternlist:
            patternlist.append(t)
    return patternlist

def update(amount,df,domain,fdcolumns,pattern):

    update=[]

    for i in range(0,amount):

        randomrow=random.randint(0,len(df)-1)     #### next version, every row at least one tupple has to be updated
        tag=random.randint(0,1)

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
                    oldvalue=str(df.ix[randomrow][col])
                    choice=getRandom(root, oldvalue)
                    record=[randomrow,col,choice]
                    print(record)
                    update.append(record)

                if d=='value':
                    dd=coldom[d]
                    max=0
                    for i in dd:
                        max=max+1
                    choice=dd[random.randint(1,2)]
                    record=[randomrow,col,choice]
                    print(record)
                    update.append(record)

                if d=='number':
                    dd = coldom[d]
                    rg=dd.split(',')
                    min=int(rg[0])
                    max=int(rg[1])
                    choice=random.randint(min,max)
                    record=[randomrow,col,choice]
                    print(record)
                    update.append(record)

        if tag==1:
            pattern = random.sample(pattern, 1)[0]
            for i in range(0,len(pattern)):
                record=[randomrow,fdcolumns[i],pattern[i]]
                print(record)
                update.append(record)

    return update

pattern=fdpattern(df,fdcolumns)
update(1,df,domain,fdcolumns,pattern)

# print(df.ix[2][3])


#### generate a new set :   apply()

