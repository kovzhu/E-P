import pandas as pd 
# import numpy as np 
import matplotlib.pyplot as plt 
import requests
import re
import time
from bs4 import BeautifulSoup as soup


class MNRLicenses():
    '''
    Parameters:
    Exp_PageNo = 6,
    Prd_PageNo = 6,
    Get the data of licenses from MNR website

    '''
    

    def __init__(self,Exp_PageNo =6, Prd_PageNo =6):
        self.Exp_PageNo = Exp_PageNo
        self.Prd_PageNo = Prd_PageNo


    def LicenseDataDataframe(self):
        '''
        Get the data from the website in the format of dataframe
        '''
        df_exp = self.DataCleaning(self.ExtractExpTable())
        df_prd = self.DataCleaning(self.ExtractPrdTable())
        exp_year = df_exp.pivot_table(
            index='Project Type', columns='Start Year', aggfunc='count', values='License No')
        prd_year = df_prd.pivot_table(
            index='Project Type', columns='Start Year', aggfunc='count', values='License No')
        # print(df_exp)
        # print(df_prd)

        LicenseData = pd.concat([df_exp, df_prd])

        # Date conversion
        LicenseData['Announcement Date'] =pd.to_datetime(LicenseData['Announcement Date'], format = '%Y-%m-%d')
        LicenseData["Start Time"]=pd.to_datetime(LicenseData['Valid Time'].str[0:10], format = '%Y-%m-%d')
        LicenseData["End Time"]=pd.to_datetime(LicenseData['Valid Time'].str[-10:], format = '%Y-%m-%d')
        LicenseData['Coord1']=[i[0] for i in LicenseData['Coordinates'].str.split('～')]
        LicenseData['Coord2']=[i[1][:-9] for i in LicenseData['Coordinates'].str.split('～')]
        LicenseData['Coord3']=[i[1][-9:] for i in LicenseData['Coordinates'].str.split('～')]
        LicenseData['Coord4']=[i[2] for i in LicenseData['Coordinates'].str.split('～')]

    # Drop the unnecessary columns 
        LicenseData.drop(['Valid Time','Coordinates'], axis = 1 )
        return LicenseData

    def WriteToExcel(self):
        filename = 'license '+ time.ctime().replace(':',' ')
        with pd.ExcelWriter(filename+'.xlsx') as writer:
            self.LicenseDataDataframe().to_excel(writer, sheet_name = 'License Data')
        # df_exp.to_excel(writer, sheet_name='Exploration Licenses')
        # df_prd.to_excel(writer, sheet_name='Production Licenses')
        # exp_year.to_excel(writer, sheet_name='New Exp')
        # prd_year.to_excel(writer, sheet_name='New Prd')


    def ExtractExpTable(self):
        Exp_url = "http://ky.mnr.gov.cn/dj/yqtkq/"
        df1 = self.ReadPage(Exp_url)
        for i in range(1, self.Exp_PageNo):
            df2 = self.ReadPage(Exp_url+'index_'+str(i)+'.htm')
            df1 = pd.concat([df1, df2], ignore_index=True)
            df1['License Type']='Exploration'
        return df1


    def ExtractPrdTable(self):
        Prd_url = "http://ky.mnr.gov.cn/dj/yqckq/"
        df1 = self.ReadPage(Prd_url)
        for i in range(1, self.Prd_PageNo):
            df2 = self.ReadPage(Prd_url+'index_'+str(i)+'.htm')
            df1 = pd.concat([df1, df2], ignore_index=True)
            df1['License Type']='Production'
        return df1


    def ReadPage(self,url):

        # set the random time interval for data extract
        # rand = random.randint(4, 20)
        # ua = UserAgent()
        
        
        headers = {
            # "User-Agent": ua.random, "X-Requested-With": "XMLHttpRequest", "Referer":"http://ky.mnr.gov.cn/dj/yqtkq/index_1.htm"}
            # "User-Agent": ua.random, "Referer":"http://ky.mnr.gov.cn/dj/yqtkq/index_1.htm"}
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1", "Referer": "http://ky.mnr.gov.cn/dj/yqtkq/index_1.htm", "Cookie": "_Jo0OQK=3C01DE15F3212B3ACBD300D618C87D562D8258144E80E799FCFA26878EB1E19B720EF126526FB18527A491844DBD754CB50AF207CC9293F94B8646416F148903D42AEC72B56FA616F6836B5670FF571807A36B5670FF571807A2AC3ECBB3D71FAFA86B20968A7766A04GJ1Z1ZA==",
            "Referer":"http://ky.mnr.gov.cn/"}
        
        reg_url = url
        req = requests.get(url=reg_url, headers=headers)
        req.encoding = 'UTF-8'
        d = pd.read_html(req.text)
        df = d[1]
        return df


    def DataCleaning(self,df):
        # df1 = pd.read_excel(
            # r'C:\Users\onc54085\Documents\Python Scripts\Development Licences backup.xlsx', sheet_name='Development')
        # df2 = df1.drop('Unnamed: 0', axis=1)
        HeadersInEnglish = {'许可证号': 'License No',
                            '油气田名称': 'Feild Name',
                            '项目类型': 'Project Type',
                            '采矿权人': 'License Owner',
                            '有效期': 'Valid Time',
                            '极值坐标': 'Coordinates',
                            '面积(km²)': 'Area',
                            '地理位置': 'Location',
                            '公告日期': 'Announcement Date',
                            '项目名称': 'Project Name',
                            '探矿权人': 'License Owner'}
        df2 = df.rename(columns=HeadersInEnglish)
        ProjectType = {'变更': 'Change',
                    '延续': 'Extend',
                    '新立': 'New',
                    '注销': 'Relinguish'}
        df2 = df2.replace({'Project Type': ProjectType})
        df2['Start Year'] = df2['Valid Time'].str[0:4].apply(int)
        df2['Start Month'] = df2['Valid Time'].str[5:7].apply(int)
        df2['End Year'] = df2['Valid Time'].str[-10:-6].apply(int)
        df2['End Month'] = df2['Valid Time'].str[-5:-3].apply(int)
        df2['License Length'] = df2['End Year'] - df2['Start Year']

        # df2.pivot_table(index = 'Project Type', columns= 'Start Year', aggfunc= 'count', values= 'License No')
        return df2

def CNPCCountryInfo():
    '''
    Get the information of each country from CNPC website
    '''

    url = r'http://www.cnpc.com.cn/cnpc/Algeria/country_index.shtml'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

    page = requests.get(url)
    sp = soup(page.text)
    Countries = [i[0] for i in [re.findall('''<a href="/cnpc/(.*?)/country_index''', str(i)) for i in sp.div.findAll(name='li', attrs={'class':'on_list'})]]
    link = ['http://www.cnpc.com.cn/' +i[0] for i in [re.findall('''<a href="(.*?)" target="''', str(i)) for i in sp.div.findAll(name='li', attrs={'class':'on_list'})]]
    CountryDescrip=[]
    for i in link:
        response = requests.get(i)
        countrysp = soup(response.text)
        CountryDescrip.append(countrysp.find_all(name = 'div', attrs={'id':'country_ul_c'})[0].text)
    CountryInfo = pd.DataFrame({'Country' : Countries, 'Link' : link, 'Description': CountryDescrip})
    return CountryInfo


def WriteToExcel(name, dataframe):
    '''
    name = name of the spreadsheet
    dataframe = dataframe to be written into the excel spreadsheet
    Write dataframes into excel
    '''
        filename = name+ time.ctime().replace(':',' ')
        with pd.ExcelWriter(filename+'.xlsx') as writer:
            dataframe.to_excel(writer, sheet_name = name)

def main():
    pass 

if __name__ == '__main__':
    main()