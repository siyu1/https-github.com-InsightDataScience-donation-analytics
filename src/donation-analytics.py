# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:24:40 2018

@author: Siyu Guo
"""
del A
del C
del chunk

import pandas as pd
import numpy as np
import math

f = open('out.txt', 'w')
f.close()

percentile=50
calendar_year='2017'
A = df = pd.DataFrame(columns=['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID'])



for chunk in pd.read_csv("itcont_2018_20171118_20180113.txt",sep="|", header=None, chunksize=10000):
    
    chunk = chunk.iloc[:,[0,7,10,13,14,15]]
    chunk.columns=['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']
    chunk['TRANSACTION_DT'] = chunk['TRANSACTION_DT'].astype(object)
    chunk = chunk[pd.isnull(chunk['OTHER_ID'])]
    chunk = chunk[pd.notnull(chunk['CMTE_ID'])] # drop rows with NAN values for the column
    chunk = chunk[pd.notnull(chunk['NAME'])]
    
    chunk = chunk[pd.notnull(chunk['TRANSACTION_AMT'])]
    chunk['ZIP_CODE'] = chunk['ZIP_CODE'].astype('str').str[0:5] # get the first 6 digits
    chunk['TRANSACTION_DT']=chunk['TRANSACTION_DT'].astype('str').str[-4:]
    chunk['ZIP_CODE']=chunk['ZIP_CODE'].str.extract('^(\d{5})$', expand=False) # only keep rows with 6 digits
    chunk = chunk[pd.notnull(chunk['ZIP_CODE'])]
    
    
    
    C=pd.concat([A,chunk])
    A=C.drop_duplicates() 

B=A.groupby(['NAME','ZIP_CODE']).size() # identify doners by name and zipcode
B1=pd.Series.to_frame(B)
Group=A.groupby(['NAME','ZIP_CODE'])
B1.columns=['repeat_number'] 
Repeat_doner=B1.loc[B1['repeat_number']!=1] #get repeat doners
Identities=Repeat_doner.index.tolist() # get identities of repeat doners (name+zipcode)
Repeat_number=np.r_[0,len(Repeat_doner)] # get total number of repeat doner

for j in Repeat_number:
    Individual_doner=Group.get_group(Identities[j])
    donation_calendar=Individual_doner.loc[Individual_doner['TRANSACTION_DT']==calendar_year] # get the total transactions in 2018
    donation_calendar=Individual_doner.loc[Individual_doner['TRANSACTION_DT']==calendar_year] # get the total transactions in 2018
    donation_calendar =donation_calendar[donation_calendar['TRANSACTION_AMT'] > 0.5] # drop values less than 0.5


    Receipt_group=Individual_doner.groupby('CMTE_ID')



    for x in Receipt_group.groups:
          Individual_receipt=Receipt_group.get_group(x)
          Individual_receipt.reset_index()
      
          Zipcode=Individual_receipt.iloc[0,2]
          Totalamount=Individual_receipt['TRANSACTION_AMT'].sum() # valvulate total transaction amount
      
      #percentile_value=Individual_receipt['TRANSACTION_AMT'].quantile(percentile)
          Number_contribution=len(Individual_receipt)# get the number of contributions
          Transactions=np.ceil(Individual_receipt['TRANSACTION_AMT'].values) # round the transaction amount
          Transaction_rank=np.sort(Transactions)
      #Individual_receipt['RANK_AMT']=Individual_receipt['TRANSACTION_AMT'].rank(ascending=1)
          rank=math.ceil(percentile/100*N) # calculate the nearest rank
          Value_percentile=Transaction_rank[rank-1] # get value of the rank
      
     # write to txt file
          f = open('out.txt', 'w+')
          f.write(x)
          f.write('|')
          f.write(Zipcode)
          f.write('|')
          f.write(calendar_year)
          f.write('|')
          f.write(str(Value_percentile))
          f.write('|')
          f.write(str(Totalamount))
          f.write('|')
          f.write(str(Number_contribution))
          f.write('\n')
          f.close()