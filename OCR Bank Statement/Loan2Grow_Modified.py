#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tabula
import pandas as pd
from tabula import read_pdf
import os
import re
#import pyPdf
#import spacy


# In[2]:


# Creating a dictionary with keys as bank names and assigning indexes to each column
Bank_statement_features = {
    'HDFC': 
    {
        'Date': 0,           
        'Narration': 1,    
        'Chq.': 2,
        'Value Dt': 3,
        'Withdrawal Amt.': 4,     
        'Deposit Amt.': 5,        
        'Closing Balance': 6,        
   },
   'ICICI':
   {
       'Date':0,
       'Particulars':1,
       'Chq.No.':2,
       'Withdrawals':3,
       'Deposits':4,
       'Auto Sweep':5,
       'Reverse Sweep':6,
       'Balance(INR)':7,
   },#can further add features according to "bank name as keys" of the dictionary
}


# In[3]:


# Using Tabula(an open source library) to extract tables from a pdf with much accuracy
# here using tabula-py(Python wrapper of tabula)
#setting the values of various parameters 
filepath = r"D:\Dataset\Loan2Grow\Pdf format\ICICI_Bank_Statement_New.pdf" 
rows_list = tabula.read_pdf(filepath,pages='1',silent=True,stream=True,lattice=True,guess=False,
                            area = (320.0,9.0,743.81,601.11),encoding='utf-8')
                            #area refers to the Portion of the page to analyze(top,left,bottom,right).
                            # calulated using tabula script exporter
                                
                            #pandas_options={'header': None,'error_bad_lines': False,'warn_bad_lines': False}
                            #pandas_options not needed when multiple_tabels=True

                    
#converting the lists together into a dataFrame 
rows_df = pd.DataFrame(rows_list,
                       columns = ['Date','Particulars','Chq.No.','Withdrawals','Deposits',
                                  'Auto Sweep','Reverse Sweep','Balance(INR)','Credit','Debit'])         

#Removing unnecessary columns and rows
rows_df.drop(['Auto Sweep','Reverse Sweep'],axis=1,inplace=True)
rows_df.drop([0],inplace=True)

# tackling those entries which contain delimeter like ','
for i in range(1,len(rows_df)+1):
    rows_df['Withdrawals'][i] = rows_df['Withdrawals'][i].replace(',','')
    rows_df['Deposits'][i] = rows_df['Deposits'][i].replace(',','')

#converting string values to float so that airthmetic analysis can be made 
rows_df["Withdrawals"] = pd.to_numeric(rows_df["Withdrawals"], downcast="float",errors='ignore')
rows_df["Deposits"] = pd.to_numeric(rows_df["Deposits"], downcast="float",errors='ignore')

rows_df


# In[4]:


#same code when all the pages are need to be covered
aux_list = tabula.read_pdf(filepath, 
                     guess=False, pages='all', stream=False ,silent=True ,encoding="utf-8",multiple_tabels=True,
                     area = ( 320.0,9.0,743.81,601.11 ))   
                     #columns = (65.3,196.86,294.96,351.81,388.21,429.77))
                           
aux_df = pd.DataFrame(aux_list,
                      columns = ['Date','Particulars','Chq.No.','Withdrawals','Deposits',
                                 'Auto Sweep','Reverse Sweep','Balance(INR)','Credit','Debit'])

aux_df.drop(['Auto Sweep','Reverse Sweep'],axis=1,inplace=True)
aux_df.drop([0],inplace=True)

for i in range(1,len(aux_df)):
    aux_df['Withdrawals'][i] = aux_df['Withdrawals'][i].replace(',','')
    aux_df['Deposits'][i] = aux_df['Deposits'][i].replace(',','')

aux_df["Withdrawals"] = pd.to_numeric(aux_df["Withdrawals"], downcast="float",errors='ignore')
aux_df["Deposits"] = pd.to_numeric(aux_df["Deposits"], downcast="float",errors='ignore')

aux_df


# In[5]:


b_i = Bank_statement_features['ICICI']['Balance(INR)']  
d_i = Bank_statement_features['ICICI']['Withdrawals']     
w_i = Bank_statement_features['ICICI']['Deposits'] 

for i in range(1,len(rows_df)):
    if(rows_df['Withdrawals'][i]>rows_df['Deposits'][i]):
        rows_df['Credit'][i] = "No"
        rows_df['Debit'][i] = "Yes"
        
    if(rows_df['Withdrawals'][i]<rows_df['Deposits'][i]):
        rows_df['Credit'][i] = "Yes"
        rows_df['Debit'][i] = "No"

rows_df


# In[ ]:


# the following functions are basically to handel side cases and were not of use on the pdf which I used.


# In[ ]:


## these two methods needed in case we have pdf containing multiple pages ##

#to count the no. of pages in a pdf
def count_pdf_pages(file_path):
    rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
    with open(file_path, "rb") as temp_file:
        return len(rxcountpages.findall(temp_file.read()))
    
n = count_pdf_pages("D:\Dataset\Loan2Grow\Pdf format\ICICI_Bank_Statement_New_1.pdf")
reader = pyPdf.PdfFileReader(open(filepath, mode='rb' ))
n = reader.getNumPages() 

# if different pages have different areas from which data is to be extracted
df = []
for page in [str(i+1) for i in range(n)]:
    if page == "1":
            df.append(read_pdf(filepath, area=(320.0,9.0,743.81,601.11), pages=page))
    else:
            df.append(read_pdf(filepath, pages=page))


# In[ ]:


## in case of ICICI bank not needed as they don't have unique headers on each page ##

# to remove the header from the list of transaction in case pdf have multiple pages
#(as bank statement have same header on each page)
# not of use in case of icici

Headers = []
# iterating over all rows extracted from the pdf
for i in rows_list:
    if if type(rows_list['Deposits'][i])==float:
        Headers.append(rows_list[i:i+1])
    else:
        break

# creating a list containing only valid transactions(removing the header rows from the extracted rows)
Valid_transactions = []  
# iterating over all rows extracted from the pdf
for row in rows_lost:
    if row not in Headers:
        Valid_transactions.append(row)        


# In[ ]:


## here our code is already ignoring those rows which don't have dates therefore not needed ## 

# To deal with those transactions which aquire multiple rows
#(when tabula is not able to differentiate whether multiple lines in a row belong to the same row 
# and therfore would have created multiple rows for a single transaction) 
# and these multiple lines is only because of narration/transaction_remarks column

single_row_transactions = []
#use the bank name according to pdf
index_date = Bank_statement_features['ICICI']['Date']          
particulars_index = Bank_statement_features['ICICI']['Particulars'] 

for row in Valid_transactions:
    if row[index_date] is not None:                 #checking if the date exist in the row
        single_row_transactions.append(row)

    else:
        # adding the narration part of those rows as the last entry in single_row_transaction
        single_row_transactions[-1][narration_index] += row[narration_index]


# In[ ]:


#can be used if needed
#categorizing transactions

def categorize(Particulars):
    word_list = tokenize(Particulars)
    
    if keyword in word_list:
        return category

    for rows in rows_list:
    rows_df['category'] = categorize(rows_df['Particulars'])

