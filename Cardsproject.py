import pandas as pd
import numpy as np
from datetime import datetime


#Function Description
def StandardizeStatement(inputFile,outputFile):
    df=pd.read_csv(str(inputFile))
    list=df.values.tolist()

    #Formating Columns as Headers
    for idx in range(len(list)):
        for j in list[idx]:
            if(str(j).rstrip()=='Date'):
                break
        else:
            df = df.drop(idx)
            continue
        break
    df.columns = df.iloc[0]
    df.head(40)

    #Adding Debit and Credit where there is Amount 
    flag=0
    idx=0
    for (ColumnName,Debit) in df.iteritems():
        ColumnName=str(ColumnName)
        df = df.rename(columns = {ColumnName:ColumnName.rstrip()})
        if(ColumnName=='Transaction Details'):
            flag=1
        if(ColumnName == 'Amount'):
            Credit=Debit
            for item in Debit:
                parse=str(item)
                if(parse[:-3:-1]=='rc' or parse[:-3:-1]=='rC'):
                    Debit=Debit.replace(to_replace= item, value=np.nan)
                else:
                    Credit=Credit.replace(to_replace= item, value=np.nan)
            df['Debit'] = pd.Series(Debit, index=df1.index)
            df['Credit'] = pd.Series(Credit, index=df1.index)
            del df['Amount']    
    df=df[['Date', 'Transaction Description' if flag==0 else 'Transaction Details', 'Debit', 'Credit']]
    list=df.values.tolist()
    list.pop(0)

    #printing new DataFrame....................

    CardName=""
    flag=0
    trans=[]
    for i in list:
        if(str(i[0]) != "nan" and str(i[0]).rstrip() != "Date" and str(i[0]) != "Rahul" and str(i[0]) != "Rajat" and str(i[0]) != "International Transactions"):
            date=i[0]
            tdesc=i[1].rstrip()
            loc=tdesc.split()
            Location=loc[-1] if flag==0 else loc[-2]
            Currency="INR" if flag==0 else loc[-1]
            debit=i[2]
            credit=i[3]
            Transaction="Domestic" if flag==0 else "International"
            trans.append([date,tdesc,debit,credit,Currency,CardName,Transaction,Location]) 

        else:
            for data in i:
                if(str(data) != "nan" and data !="International Transactions"):
                    CardName=data
                if(data == "International Transactions" or data == "International Transaction"):
                    flag=1
    newdf=pd.DataFrame(trans,columns= ['Date','Transcation Description','Debit','Credit','Currency','CardName','Transaction','Location'])
    newdf['Date'] = pd.to_datetime(newdf['Date'])
    newdf = newdf.sort_values(by="Date")
    newdf.to_csv(outputFile, index=False)

if __name__ == "__main__":
    
    #reading csv files and calling the function
    #case1
    inputFile= "HDFC-Input-Case1.csv"
    outputFile ="HDFC-Output-Case1.csv"
    StandardizeStatement(inputFile,outputFile)
    
    #case2
    inputFile= "ICICI-Input-Case2.csv"
    outputFile ="ICICI-Output-Case2.csv"
    StandardizeStatement(inputFile,outputFile)

    #case3
    inputFile= "Axis-Input-Case3.csv"
    outputFile ="Axis-Output-Case3.csv"
    StandardizeStatement(inputFile,outputFile)
    
    #case4
    inputFile= "IDFC-Input-Case4.csv"
    outputFile ="IDFC-Output-Case4.csv"
    StandardizeStatement(inputFile,outputFile)
    