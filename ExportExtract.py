import pandas as pd 
import matplotlib.pyplot as plt

class Vantage:
    
    annual_start_year = 2000
    annual_end_year = 2020
    
    def __init__(self, filename):
        self.filename = filename
        self.Overview = self.table_extract()[0]
        self.Annual = self.table_extract()[1]

    def table_extract(self):
        '''
        Extract the two dataframes from the exported exel files,
        and create two DFs named Overview & Annual
        
        '''
        
        # Overview = pd.read_excel(FileName, sheet_name = 'Overview')
        xlsx = pd.ExcelFile(self.filename)
        Overview = pd.read_excel(xlsx, sheet_name='Overview')
        Overview.columns = Overview.iloc[0]
        Overview = Overview.drop(0, axis=0)
        Overview = pd.DataFrame(Overview)
        Annual = pd.read_excel(xlsx, sheet_name='Annual')
        Annual = pd.DataFrame(Annual)
        return Overview, Annual

    def production_profile(self, HCType ='oil', category = 'Region'):
        '''
        HCType = oil or gas
        category = 
        'Asset Name', 
        'Status', 
        'Primary Product',
        'Country/Area', 
        'Region', 
        'Basin Name',
        'Terrain',
        'FID Status
        ----------
        category : TYPE
            DESCRIPTION.

        Returns
        ------
        Parameters
        

        None.

        '''
        if HCType =='oil':
            metric = 'Production Oil Rate (Mbbl/d)'
        elif HCType == 'gas':
            metric = 'Production Gas Rate (MMcf/d)'
        else:
            pass
        
        prod = pd.merge(self.Annual[self.Annual['Metric'] == metric].iloc[:,[0,1]], self.Annual[self.Annual['Metric'] == metric].loc[:,'2000':'2020'],how='inner',left_index=True, right_index=True)
        prod.rename(columns = {' ':'Asset Name'}, inplace=True)
        prod = pd.merge(prod,self.Overview[['Asset Name','Status','Primary Product','Country/Area','Region','Basin Name','Terrain','FID Status']],how='inner', left_on= 'Asset Name', right_on='Asset Name')
        
        prod_pivot = pd.pivot_table(prod, index = category)
        # prod_pivot.T.plot(kind='bar',)
        return prod_pivot
        
        
    def DiscYearChart(self):  
        '''
        create a chart showing the count of discoveries by year

        Returns
        -------
        None.

        '''    
        
        # chart of when the existing fields were discovered
        DiscYear = self.Overview.pivot_table(
            columns='Year Discovered',  values='Asset Name', aggfunc='count')
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(DiscYear.columns, DiscYear.iloc[0], color='darkgreen')
        ax.set(xlabel='Year', ylabel='Count of discoveries',
               title='Field Discoveries by Year', xlim=[1950, 2020])
        
        
    def test(self):
        print(self.Annual)

def main():
    pass


#Get the data from standard Vantage exported data, of the two tabs: Overview & annual
# def VantageFunc(FileName):
#     '''
#     Get the data from standard Vantage exported excel data, 
#     for the two tabs: 
#     Overview & annual
#     '''
#     # Overview = pd.read_excel(FileName, sheet_name = 'Overview')
#     xlsx = pd.ExcelFile(FileName)
#     Overview = pd.read_excel(xlsx, sheet_name='Overview')
#     Overview.columns = Overview.iloc[0]
#     Overview = Overview.drop(0, axis=0)
#     Overview = pd.DataFrame(Overview)
#     Annual = pd.read_excel(xlsx, sheet_name='Annual')
#     Annual = pd.DataFrame(Annual)
#     return Overview, Annual


def test():
    print('This is a test function')


class EDIN():
        
    
    def __init__(self, filename):
        self.filename = filename 
        self.EDINData = self.table_extract()        
    
    def table_extract(self):
        xlsx = pd.ExcelFile(self.filename)
        EDINData = pd.read_excel(xlsx,sheet_name='China Resources Data Pull')
        return EDINData


    def remaining_reserve(self):
        Remaining_by_country = pd.pivot_table(EDIN, values = 'Tot Remaining PP MMboe', columns = 'Country Names').T.sort_values(by = 'Tot Remaining PP MMboe')
        return Remaining_by_country



if __name__ == '__main__':
    main()   