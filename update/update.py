import random

import pandas as pd

from OntologyNode import findNodes, getDescendantNodes, getUpper, getRandom
from utility.ReadFD import reFD
from utility.ReadJson import reJson

def findFdPatterns(df,fdcolumns):
    '''
    Find the Value Patterns according to FD
    :param df: dataframe
    :param fdcolumns: list of all fd columns, [3,4,5]
    :return: pattern list
    '''
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
    '''
    Obj UpdateValue represents the basic tupple in the dataframe.
    '''
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
    '''
    Obj UpdateFD represents the update for FD columns, including several UpdateValues according to the FD columns
    '''
    def __init__(self,UpdateValueList):
        self.updates=UpdateValueList

    def getUpdates(self):
        return self.updates

    def setUpdates(self,UpdateValueList):
        self.updates=UpdateValueList

def createUpdate(amount,df,domain,fdcolumns,pattern):

    '''
    Create UpdateValue or UpdateFD randomly
    :param amount: an argument controling the number of updates
    :param df: dataframe
    :param domain: 1.saving the information of NonFD-columns' value domain, there are three kinds of domain: number,value,ontology
                   domain=[{0:{'number':'1,1000'}},
                         {1:{'value':gen}},
                         {2:{'ontology':age}}]
                   2.for value domain, you have to have a pre definded value dict like,
                   gen={1:'male',2:'female'}
                   3.for ontology domain, you have to have a pre definded root like,
                   age=reJson('../data/test1/age.json')
                   function reJson() can resolve the ontology file in the format of json
    :param fdcolumns: list of all fd columns, [3,4,5]
    :param pattern: FD patterns, got from function findFdPatterns()
    :return: a list of all Updates
    '''
    updatelist=[]
    for i in range(0,amount):
        randomrow=random.randint(0,len(df)-1)
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
                    upd=UpdateValue(randomrow,int(col),choice)
                    updatelist.append(upd)

                if d=='value':
                    dd=coldom[d]
                    choice=dd[random.randint(1,2)]
                    upd = UpdateValue(randomrow, int(col), choice)
                    updatelist.append(upd)

                if d=='number':
                    dd = coldom[d]
                    rg=dd.split(',')
                    min=int(rg[0])
                    max=int(rg[1])
                    choice=random.randint(min,max)
                    upd = UpdateValue(randomrow,int(col), choice)
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

def createUpdatesCoverEveryRow(df,domain,fdcolumns,pattern):
    '''
    A specific method to create updates covering every row, based on createUpdate()
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
                    upd=UpdateValue(randomrow,int(col),choice)
                    updatelist.append(upd)

                if d=='value':
                    dd=coldom[d]
                    choice=dd[random.randint(1,2)]
                    upd = UpdateValue(randomrow, int(col), choice)
                    updatelist.append(upd)

                if d=='number':
                    dd = coldom[d]
                    rg=dd.split(',')
                    min=int(rg[0])
                    max=int(rg[1])
                    choice=random.randint(min,max)
                    upd = UpdateValue(randomrow, int(col), choice)
                    updatelist.append(upd)

        if tag==1:
            pat = random.sample(pattern, 1)[0]
            updatevaluelist=[]
            for index in range(0,len(pat)):
                upd = UpdateValue(randomrow, fdcolumns[index], pat[index])
                updatevaluelist.append(upd)
            updfd = UpdateFD(updatevaluelist)

            updatelist.append(updfd)
    return updatelist

def createUpdates(amount,df,domain,fdcolumns,pattern):
    '''
    A specific method to create updates at least cover every row, based on createUpdate() and createUpdatesCoverEveryRow()
    '''
    updates=createUpdatesCoverEveryRow(df,domain,fdcolumns,pattern)
    max=random.randint(100,1000)
    for t in range(0,max):
        updates.append(createUpdate(amount,df,domain,fdcolumns,pattern)[0])
    return updates

def select(root,value,exp_level):
    '''
    According to the 3 arguments, we can find the specific Value in OntologyTree
    :param root:
    :param value:
    :param exp_level:
    :return:
    '''
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
    '''
    Using pandasql to do query job. Before the final result, the output of query have to call select()
    to change to one expected value
    :param qry:
    :param exp_level:
    :param rootdic:
    :return:
    '''
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
    '''
    Apply update on DF
    :param df:
    :param Update:
    :return:
    '''
    master=[]
    update=Update
    if isinstance(update,UpdateValue) is True:

        row=update.row
        col=update.column[0]
        value=update.value
        original=UpdateValue(row,col,df.ix[row][col])
        df.ix[row, col] = value
        master.append(original)

    if isinstance(update,UpdateFD) is True:
        updfd=update.getUpdates()
        for u in updfd:
            row=u.row
            col=u.column[0]
            original=UpdateValue(row,col,df.ix[row, col])
            value=u.value
            df.ix[row, col] = value
            master.append(original)

    return df,master

def filter(df,updates,qry,exp_level,rootdic):
    '''
    Using specific query to check those updates applied on the dataframe.
    If the result of query is the same between the original dataframe and the dataframe with update, then the update can be
    append to the return result list.
    :param df:
    :param updates:
    :param qry:
    :param exp_level:
    :param rootdic:
    :return:
    '''
    rsl=[]
    correct=query(qry,exp_level,rootdic)

    for update in updates:
        df, maintain = apply(df, update)
        te=query(qry,exp_level,rootdic)
        if te==correct:
            rsl.append(update)
            print('true')
        else:
            print('false')
        size=len(maintain)

        if size==1:
            df=apply(df,maintain[0])[0]
        else:
            for mt in maintain:
                df=apply(df,mt)[0]

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
pattern=findFdPatterns(df,fdcolumns)
updates=createUpdates(1,df,domain,fdcolumns,pattern)
rootdic={'AGE':age,'SYMP':symp}
# print('---------TEST UPDATE----------')
# for z in updates:
#      print('=============================')
#      if isinstance(z,UpdateFD) is True:
#
#          print(':Update for FD')
#          print(z)
#          a=z.getUpdates()
#          print(a)
#          for zf in a:
#              print(zf)
#              print(zf.row,zf.column[0],zf.value)
#
#
#      if isinstance(z,UpdateValue) is True:
#          print(':Update for Value')
#          print(z)
#          print(z.row)
#          print(z.column[0])
#          print(z.value)
#
#
#      print('---------')

# print('*******')
# print('')
# print('*******')
#
# print('---------TEST QUERY----------')
qry="select SYMP from df where GEN='female' ;"
exp_level=2
# print(query(qry,exp_level,rootdic))
# print('*******')
# print('')
# print('*******')
# print('--------Test APPLY and Filter------------')
# UpdateList=createUpdate(1,df,domain,fdcolumns,pattern)
# apply(df,UpdateList[0])
#
print('original number of updates:'+str(len(updates)))
rsl=filter(df,updates,qry,exp_level,rootdic)
print('after filtering:'+str(len(rsl)))