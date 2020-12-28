# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
# import matplotlib.pyplot as plt
import camelot
from tools import WriteToExcel, WriteToExcel_df
import numpy as np

# from secedgar.filings import Filing, FilingType


# df = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/mpg_ggplot2.csv")
# df_select = df.loc[df.cyl.isin([4,8]),:]

# CNOOC_folder = r'C:\Users\Kunfeng.Zhu\OneDrive - IHS Markit\01_Key Research Topics\06_NOCs\CNOOC\Annual Reports'
# file = r'\2019 annual report CNOOC ltd.pdf'
# file2 = r'\gst-revenue-collection-march2020.pdf'
# file3 = r'\2019 CNOOC 20-F.pdf'
# table = camelot.read_pdf(CNOOC_folder+file3, pages = '15', password = None,flaver = 'stream',process_background=True)

# CNOOC_SEC_2019 = r'https://www.sec.gov/Archives/edgar/data/0001095595/000095010320007907/dp124679_20f.htm'

# SEC_ticker ={
#     'CNOOC Limited':'CEO',
#     'PetroChina':'PTR',
#     'Sinopec':'SNP'
#     }

# CNPC_filings = Filing(cik_lookup='PTR',filing_type=FilingType.FILING_20F)
# CNPC_filings.save(r'C:\Users\Kunfeng.Zhu\OneDrive - IHS Markit\01_Key Research Topics\06_NOCs\CNPC\Annual Reports\PetroChina\SEC filings')


CNOOC_links ={
        'CNOOC SEC 2019':r'https://www.sec.gov/Archives/edgar/data/0001095595/000095010320007907/dp124679_20f.htm',
        'CNOOC SEC 2018':r'https://www.sec.gov/Archives/edgar/data/0001095595/000095010319005015/dp105023_20f.htm',
        'CNOOC SEC 2017':r'https://www.sec.gov/Archives/edgar/data/0001095595/000095010318004976/dp89764_20fa.htm',
        'CNOOC SEC 2016':r'https://www.sec.gov/Archives/edgar/data/0001095595/000095010317003701/dp75013_20f.htm',
        'CNOOC SEC 2015':r'https://www.sec.gov/Archives/edgar/data/0001095595/000095010316012730/dp64914_20f.htm'
        }

items_to_extract_for_CNOOC =[
        'Operating revenue',
        'Net Production',
        'Total Developed',
        'Total Undeveloped',
        'North America (excluding Canada)',
        'East South China Sea',
        'Exploration and production',
        'Total oil and gas sales',
        'Oil and gas sales',
        'Overseas',
        'Exploration',
        'Development',
        ]
    

CNPC_links ={
        'CNPC SEC 2019':r'https://www.sec.gov/Archives/edgar/data/1108329/000119312520125304/d836220d20f.htm',
        'CNPC SEC 2018':r'https://www.sec.gov/Archives/edgar/data/1108329/000119312519123907/d676237d20f.htm',
        'CNPC SEC 2017':r'https://www.sec.gov/Archives/edgar/data/1108329/000119312518137017/d482381d20f.htm',
        'CNPC SEC 2016':r'https://www.sec.gov/Archives/edgar/data/1108329/000119312517141187/d369285d20f.htm',
        'CNPC SEC 2015':r'https://www.sec.gov/Archives/edgar/data/1108329/000119312516561899/d264935d20f.htm'
        }




items_to_extract_for_CNPC =[
        'Consolidated Statement of Comprehensive Income Data',
        'Proved developed and undeveloped reserves On a consolidated basis',
        'Changqing',
        'Net exploratory wells drilled',
        'Exploration and production',
        'OPERATING EXPENSES',
        'Type of goods and services',
        'Exploration expenses', 
        'Exploration',
        'Development',
        'Production'        
        ]

Sinopec_links = {
    'Sinopec SEC 2019':r'https://www.sec.gov/Archives/edgar/data/1123658/000110465920045548/a19-28355_120f.htm',
    'Sinopec SEC 2018':r'https://www.sec.gov/Archives/edgar/data/1123658/000110465919024232/a18-41808_120f.htm',
    'Sinopec SEC 2017':r'https://www.sec.gov/Archives/edgar/data/1123658/000110465918027339/a18-6011_120f.htm',
    'Sinopec SEC 2016':r'https://www.sec.gov/Archives/edgar/data/1123658/000134100417000262/form20-f.htm',
    'Sinopec SEC 2015':r'https://www.sec.gov/Archives/edgar/data/1123658/000134100416001318/form20-f.htm',
    }

items_to_extract_for_Sinopec =[
        'Operating revenues',
        'Consolidated Balance Sheet Data',
        'Statement of Cash Flow and Other Financial Data',
        'Total Proved Developed',
        'Average Daily Crude Oil Production',
        'Average Daily Natural Gas Production',
        'Average petroleum lifting cost per BOE',
        'Shengli',
        'Puguang',
        'Exploration and production',
        'Crude oil',
        'Current assets',        
        'Exploration expenses', 
        'Exploration',
        'Development',
        'Production'        
        ]

def table_extractor(link, items_to_extract):
# =============================================================================
#     link can be found in the SEC website
    # excel_filename is used for name the exported excel files
# =============================================================================
    
    
    tables = pd.read_html(link)
    
 
    #Select the tables that contains the key words in items_to_extract_for CNOOC
    #and store it into talbe_extracted
    
    tables_extracted = []
    for i in range(0,len(tables)):
        string =''
        for j in tables[i][0]:
            string +=str(j)
        for k in items_to_extract:
            if k in string:
                tables_extracted.append(tables[i])
                break
            else:
                pass
    return tables_extracted

def table_cleaning(tables_extracted,company):
    CNPC_CNOOC = [0,3,7,11,15,19,23,27,31,35,39]
    Sinopec = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
    if company == 'CNPC' or company == 'CNOOC':
        columns_to_use = CNPC_CNOOC
    elif company == 'Sinopec':
        columns_to_use = Sinopec
    else:
        print('Wrong company name inputed')
    tables_cleaned =[]
    for table in tables_extracted:
        new_table =pd.DataFrame(index = list(table.index))
        columns_len=len(table.columns)
        for i in columns_to_use:
           if i<columns_len:
               new_table = new_table.merge(table[i],how='outer', left_index = True, right_index = True)
        tables_cleaned.append(new_table)
    return tables_cleaned


# for i in links:
#     table_extractor(links[i],i,items_to_extract_for_CNOOC)
def SaveToExcel(links, items_to_extract, company):
    for i in links:
        tables_extracted = table_extractor(links[i],items_to_extract)
        tables_cleaned = table_cleaning(tables_extracted, company)
        WriteToExcel_df(i,tables_cleaned)



# SaveToExcel(CNPC_links, items_to_extract_for_CNPC,'CNPC')
SaveToExcel(Sinopec_links, items_to_extract_for_Sinopec,'Sinopec')
# SaveToExcel(CNOOC_links, items_to_extract_for_CNOOC,'CNOOC')