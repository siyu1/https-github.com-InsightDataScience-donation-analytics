# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:24:40 2018

@author: Siyu Guo
"""


import pandas as pd
import numpy as np
import math

f = open('repeat_donors.txt', 'w')
f.close()
f1 = open('percentile.txt', 'r')
percentile=int(f1.read())

calendar_year='2018'

C = pd.DataFrame(columns=['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID'])



for chunk in pd.read_csv("itcont.txt",sep="|", header=None, converters={10: lambda x: str(x)}, chunksize=1):
    if len(chunk)>0:
        chunk = chunk.iloc[:,[0,7,10,13,14,15]]
        chunk.columns=['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']
        chunk['TRANSACTION_DT'] = chunk['TRANSACTION_DT'].astype(object)
        chunk = chunk[pd.isnull(chunk['OTHER_ID'])]
        chunk = chunk[pd.notnull(chunk['CMTE_ID'])] # drop rows with NAN values for the column
        chunk = chunk[pd.notnull(chunk['NAME'])]
        chunk = chunk[pd.notnull(chunk['ZIP_CODE'])]
    
        chunk = chunk[pd.notnull(chunk['TRANSACTION_AMT'])]
    
        if len(chunk)>0:
            
            chunk['ZIP_CODE'] = chunk['ZIP_CODE'].astype('str').str[0:5] # get the first 6 digits
            chunk['TRANSACTION_DT']=chunk['TRANSACTION_DT'].astype('str').str[-4:]
            chunk['ZIP_CODE']=chunk['ZIP_CODE'].str.extract('^(\d{5})$', expand=False) # only keep rows with 6 digits
            
            C=pd.concat([C,chunk])
            Name=chunk.iloc[0,1]
            ZIP=chunk.iloc[0,2]
            ID=chunk.iloc[0,0]
            Repeat_doner=C[(C.ZIP_CODE == ZIP) & (C.NAME ==Name)] #get repeat doners
        
            if len(Repeat_doner)>1:

                receipt_calendar=C[(C.ZIP_CODE == ZIP) & (C.CMTE_ID ==ID)& (C.TRANSACTION_DT ==calendar_year)]
            
           
                receipt_calendar =receipt_calendar[receipt_calendar['TRANSACTION_AMT'] > 0.5] # drop values less than 0.5
            
                if len(receipt_calendar)>0:

                    receipt_calendar.reset_index()
      
          
                    #Totalamount=receipt_calendar['TRANSACTION_AMT'].sum() # valvulate total transaction amount
      
      
                    Number_contribution=len(receipt_calendar)# get the number of contributions
                    Transactions=np.int_(np.ceil(receipt_calendar['TRANSACTION_AMT'].values)) # round the transaction amount
                    Totalamount=np.sum(Transactions)
                    Transaction_rank=np.sort(Transactions)
                    rank=math.ceil(percentile/100*Number_contribution) # calculate the nearest rank
                    Value_percentile=Transaction_rank[rank-1] # get value of the rank
      
                    # write to txt file
                    f = open('repeat_donors.txt', 'a')
                    f.write(ID)
                    f.write('|')
                    f.write(ZIP)
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