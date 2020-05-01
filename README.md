# Bank-Statement-OCR
Optical Character Recognition for Bank Statements using python and tabula.  
This is a python code for Bank Statement OCR which can extract all the information (like account details and transaction history) from the bank statement in a structured format. 
The bank statements are taken as input in the form of pdf files. 
Here i have used ICICI bank as an example but one can create an OCR for any bank just by making some necessary edits(mainly in the column header part as they are different for various banks).
I have used open source library 'Tabula' to read the data from pdf. 
Proper and sufficient comments are added for the reader to understand the code and logic.
Task:-
1)Pull out all the transactions from bank statements. -> 
2)Put it a dataframe. -> 
3)Clean the data so we can play around with data. ->
4)Categorize into credit and debit.
