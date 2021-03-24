#Author: Habibi Husain Arifin
#Created Date: 15 January 2019
#Last Updated Date: 24 March 2020
#Version: 1.0

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

import xlrd
import pandas as PD

from API.Instance import Instance

class ExcelManager():
 
    #Documentation: https://xlsxwriter.readthedocs.io/example_pandas_simple.html
    @staticmethod
    def writeExcelFile(name, dataFrame):
        writer = PD.ExcelWriter(name, engine='xlsxwriter')
        dataFrame.to_excel(writer, sheet_name='Sheet1')
        writer.save()
       
    #Documentation: https://www.dataquest.io/blog/excel-and-pandas/
    @staticmethod
    def readExcelFile(name):
        maxRowSize = maxColSize = 0
        all_data = PD.DataFrame()
        xlsx = xlrd.open_workbook(name, on_demand=True)
        tab_list = xlsx.sheet_names()

        instances = []
        for insType in tab_list:
            #Create the DataFrame without removing or skipping any row
            df = PD.read_excel(name, sheet_name=insType, index_col=0)
            
            #To check and show Top 5 rows
            #df.head()
            
            #To append the data
            data = all_data.append(df, ignore_index=True)

            #Check if the data is NaN and remove it
            new_data = data.dropna(axis=0, how="all")
            clean_data = new_data.dropna(axis=1, how="all")
            
            #To check how many records/rows of the catalog sheet and find the maximum row and column size
            rowSize = clean_data.shape[0]
            colSize = clean_data.shape[1]  
            if rowSize > maxRowSize:maxRowSize = rowSize
            if colSize > maxColSize:maxColSize = colSize
            
            #Get the row and columns
            cols = clean_data.columns
            
            #Assign the Instance Parameters
            tempInstParams = {}
            for rowIndex in range(rowSize):
                for col in cols:
                    tempInstParams[col] = clean_data.loc[rowIndex, col]
                    #print(tempInstParams) 
                
                #Store the normalize data into the array of Catalog List
                newInst = Instance.createNewInstance(insType, None, tempInstParams)
                instances.append(newInst)
                tempInstParams = {} #Empty the temporary InstanceParameters
 
        if instances == []:return None
        else:return instances, maxRowSize, maxColSize

########################################################################################################################
#Below this line is test area
"""
#Test read ExcelFile
CATALOG_FILE_PATH = "Input/BOM/Catalogs.xlsx"

instances, maxRowSize, maxColSize = ExcelReader.readExcelFile(CATALOG_FILE_PATH)
instances = Instance.generateGeneSequentially(instances, maxRowSize)

print("MaxRowSize:", maxRowSize, "MaxColSize:", maxColSize)
for instance in instances:
    print(instance.insType, instance.gaGene, instance.parameters)
    
#Test get instance by InstanceType and Gene
inst = Instance.getInstanceByTypeAndGene("Bicycle", "G", instances)
print("Get instance:", inst.insType, inst.gaGene, inst.parameters)
"""
