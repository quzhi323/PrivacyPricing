import random

import pandas as pd

from OntologyNode import findNodes, getDescendantNodes, getUpper, getRandom
from query.gequery import gequerry
from utility.ReadFD import reFD
from utility.ReadJson import reJson

def findFdPatterns(df,fdcolumns):
    patternlist=[]
    length=len(df)
    for l in range(0,length):
        t=[]
        for c in fdcolumns:
            t.append(df.ix[l][c])
        if t not in patternlist:
            patternlist.append(t)
    return patternlist

class UpdateValue():
    def __init__(self,row,column,value):
        self.row=row
        self.column=column,
        self.value=value

    def setRow(self,row):
        self.row=row

    def getRow(self):
        return self.row

    def setColumn(self, column):
        self.column = column

    def getColumn(self):
        return self.column

    def setValue(self, value):
        self.row = value

    def getValue(self):
        return self.value

class UpdateFD():
    def __init__(self,UpdateValueList):
        self.updates=UpdateValueList

    def getUpdates(self):
        return updates

    def setUpdates(self,UpdateValueList):
        self.updates=UpdateValueList

def createUpdate(amount,df,domain,fdcolumns,pattern):
    '''
    :param amount:
    :param df:
    :param domain:
    :param fdcolumns:
    :param pattern:
    :return:
    '''
    updatelist=[]
    for i in range(0,amount):
        randomrow=random.randint(0,len(df)-1)
        tag=random.randint(0,1)
        if tag==0:  ##更改非fd列
            max=len(domain)-1
            rand=random.randint(0,max)
            randomcol=domain[rand]

            for c in randomcol:
                col=c
                coldom=randomcol[c]

            for d in coldom:
                if d=='ontology':
                    root=coldom[d]
                    oldvalue=str(df.ix[randomrow][col])
                    choice=getRandom(root, oldvalue)
                    print(col)
                    upd=UpdateValue(randomrow,int(col),choice)
                    print(upd.column)
                    updatelist.append(upd)

                if d=='value':
                    dd=coldom[d]
                    choice=dd[random.randint(1,2)]
                    print(col)
                    upd = UpdateValue(randomrow, int(col), choice)
                    print(upd.column)
                    updatelist.append(upd)

                if d=='number':
                    dd = coldom[d]
                    rg=dd.split(',')
                    min=int(rg[0])
                    max=int(rg[1])
                    choice=random.randint(min,max)
                    print(col)
                    upd = UpdateValue(randomrow,int(col), choice)
                    print(upd.column)
                    updatelist.append(upd)

        if tag==1:
            pat = random.sample(pattern, 1)[0]
            updatevaluelist=[]
            for i in range(0,len(pat)):
                upd = UpdateValue(randomrow, fdcolumns[i], pat[i])
                updatevaluelist.append(upd)
            updfd=UpdateFD(updatevaluelist)
            updatelist.append(updfd)

    return updatelist
# def createUpdatesCoverEveryRow(amount,df,domain,fdcolumns,pattern):
#
#     updates=[]
#
#     for i in range(0,amount):
#         for randomrow in range(0,len(df)-1):
#             tag=random.randint(0,1)
#             if tag==0:  ##更改非fd列
#                 update = []
#                 max=len(domain)-1
#                 rand=random.randint(0,max)
#                 randomcol=domain[rand]
#
#                 for c in randomcol:
#                     col=c
#                     coldom=randomcol[c]
#
#                 for d in coldom:
#                     if d=='ontology':
#                         root=coldom[d]
#                         oldvalue=str(df.ix[randomrow][col])
#                         choice=getRandom(root, oldvalue)
#                         record=[randomrow,col,choice]
#                         update.append(record)
#
#                     if d=='value':
#                         dd=coldom[d]
#                         max=0
#                         for i in dd:
#                             max=max+1
#                         choice=dd[random.randint(1,2)]
#                         record=[randomrow,col,choice]
#                         update.append(record)
#
#                     if d=='number':
#                         dd = coldom[d]
#                         rg=dd.split(',')
#                         min=int(rg[0])
#                         max=int(rg[1])
#                         choice=random.randint(min,max)
#                         record=[randomrow,col,choice]
#                         update.append(record)
#
#                 updates.append(update)
#
#             if tag == 1:
#                 update = []
#                 pat = random.sample(pattern, 1)[0]
#                 l=len(pat)
#                 for t in range(0, len(pat)):
#                     record = [randomrow, fdcolumns[t], pat[t]]
#                     # print(record)
#                     update.append(record)
#
#                 updates.append(update)
#
#     return updates
def createUpdatesCoverEveryRow(df,domain,fdcolumns,pattern):
    '''
    :param amount:
    :param df:
    :param domain:
    :param fdcolumns:
    :param pattern:
    :return:
    '''
    updatelist=[]
    for i in range(0,len(df)-1):
        randomrow=i
        tag=random.randint(0,1)
        if tag==0:
            max=len(domain)-1
            rand=random.randint(0,max)
            randomcol=domain[rand]

            for c in randomcol:
                col=c
                coldom=randomcol[c]

            for d in coldom:
                if d=='ontology':
                    root=coldom[d]
                    oldvalue=str(df.ix[randomrow][col])
                    choice=getRandom(root, oldvalue)
                    print(col)
                    upd=UpdateValue(randomrow,int(col),choice)
                    print(upd.column)
                    updatelist.append(upd)

                if d=='value':
                    dd=coldom[d]
                    choice=dd[random.randint(1,2)]
                    print(col)
                    upd = UpdateValue(randomrow, int(col), choice)
                    print(upd.column)
                    updatelist.append(upd)

                if d=='number':
                    dd = coldom[d]
                    rg=dd.split(',')
                    min=int(rg[0])
                    max=int(rg[1])
                    choice=random.randint(min,max)
                    print(col)
                    upd = UpdateValue(randomrow, int(col), choice)
                    print(upd.column)
                    updatelist.append(upd)

        if tag==1:
            pat = random.sample(pattern, 1)[0]
            updatevaluelist=[]
            for index in range(0,len(pat)):
                upd = UpdateValue(randomrow, fdcolumns[index], pattern[index])
                updatevaluelist.append(upd)
            updfd = UpdateFD(updatevaluelist)
            updatelist.append(updfd)

    return updatelist

def createUpdates(amount,df,domain,fdcolumns,pattern):
    updates=createUpdatesCoverEveryRow(df,domain,fdcolumns,pattern)
    max=random.randint(100,1000)
    for t in range(0,max):
        updates.append(createUpdate(amount,df,domain,fdcolumns,pattern)[0])
    return updates

def select(root,value,exp_level):
    node=findNodes(root,value)
    if node is not None:
        level=node.getHeight()
        diff=exp_level-level
        if diff==0:
            return value
        if diff<0:
            diff=-diff
            temp=node
            for i in range(0,diff):
                temp=temp.getParent()
                va=temp.value
            return temp.value
        if diff>0:
            temp=node.getChildren()
            for i in range(1,diff):
                temp2=[]
                for c in temp:
                    temp2=temp2+c.getChildren()
                temp=temp2
            rsl=[]
            for node in temp:
                rsl.append(node.value)
            return rsl

def query(qry,exp_level,rootdic):
    from pandasql import sqldf
    pysqldf = lambda q: sqldf(q, globals())
    rsl=pysqldf(qry)
    columns=[]
    for c in rsl.columns:
        columns.append(str(c))
    for col in columns:
        a=rsl[col]
        gersl=[]
        for i in a:
            gersl.append(select(rootdic[col],i,exp_level))
    return gersl

def apply(df,Update):

    master=[]
    for u in update:
        row=u[0]
        col=df.columns[u[1]]
        original=[row,u[1],df.ix[row, col]]
        value=u[2]
        df.ix[row, col] = value
        master.append(original)

    return df,master

def filter(df,updates,qry,exp_level,rootdic):

    rsl=[]
    correct=query(qry,exp_level,rootdic)
    for update in updates:
        df,maintain=apply(df,update)
        te=query(qry,exp_level,rootdic)
        if te==correct:
            rsl.append(update)
        df=apply(df,maintain)[0]

    return rsl







path='../data/test1/1000gdb.csv'
df=pd.read_csv(path,header=0)
df=pd.DataFrame(df,columns=['PID','GEN','AGE','SYMP','DRUG','ILLNESS'])
age=reJson('../data/test1/age.json')
symp=reJson('../data/test1/symp.json')
gen={1:'male',2:'female'}
drug={}
illness={}
fd=reFD('../data/test1/fd.csv')
fdcolumns=[3,4,5]
domain=[{0:{'number':'1,1000'}},
        {1:{'value':gen}},
        {2:{'ontology':age}},
       ]
print('---------TEST UPDATE----------')

pattern=findFdPatterns(df,fdcolumns)
updates=createUpdates(1,df,domain,fdcolumns,pattern)

#
# for r in updates:
#      # print(r)
#      # if isinstance(r,UpdateFD) is True:
#      #     print(':Update for FD')
#      #     upd=r.getUpdates()
#      #     print(upd)
#      #     for u in upd:
#      #         print(u)
#      #
#      # print(r)
#      if isinstance(r,UpdateValue) is True:
#          print('value')
#          print(r.row)
#          print(r.column)
#          print(r.value)
#
#
#      print('---------')







# print('*******')
# print('')
# print('*******')
#
# print('---------TEST QUERY----------')
# qry="select SYMP from df where GEN='female' ;"
# exp_level=2
# rootdic={'AGE':age,'SYMP':symp}
# print(query(qry,exp_level,rootdic))

# print('*******')
# print('')
# print('*******')
# print('--------Test APPLY and Filter------------')
# update=createUpdate(1,df,domain,fdcolumns,pattern)
# apply(df,update)
#
# print('original number of updates:'+str(len(updates)))
# rsl=filter(df,updates,qry,exp_level,rootdic)
# print('after filtering:'+str(len(rsl)))