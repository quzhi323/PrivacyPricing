import pandas as pd

from OntologyNode import findNodes, getLeaves
from utility.ReadJson import reJson

def geselect(root,value,exp_level):
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

def gequerry(query,exp_level,rootdic):
    from pandasql import sqldf
    pysqldf = lambda q: sqldf(q, globals())
    rsl=pysqldf(query)
    columns=[]
    for c in rsl.columns:
        columns.append(str(c))
    for col in columns:
        a=rsl[col]
        gersl=[]
        for i in a:
            gersl.append(geselect(rootdic[col],i,exp_level))
    return gersl