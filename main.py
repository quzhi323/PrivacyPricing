import pandas as pd
path='data/test1/1000gdb.csv'
df=pd.read_csv(path,header=0)
df=pd.DataFrame(df,columns=['PID','GEN','AGE','SYMP','DRUG','ILLNESS'])

df.ix[0,0]='test'
print(df)


