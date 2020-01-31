# import numpy as np
import pandas as pd
# import urllib
from urllib.request import urlopen, Request
import requests
# import time
# import random


def main():
    Exp_PageNo = 2  # Number of exploration licese pages, check in MNR's website
    Prd_PageNo = 2  # Production page numbers,  check in MNR's website
    df_exp = DataCleaning(ExtractExpTable(Exp_PageNo=Exp_PageNo))
    df_prd = DataCleaning(ExtractPrdTable(Prd_PageNo=Prd_PageNo))
    exp_year = df_exp.pivot_table(
        index='Project Type', columns='Start Year', aggfunc='count', values='License No')
    prd_year = df_prd.pivot_table(
        index='Project Type', columns='Start Year', aggfunc='count', values='License No')
    # print(df_exp)
    # print(df_prd)
    with pd.ExcelWriter('temp2.xlsx') as writer:
        df_exp.to_excel(writer, sheet_name='Exploration Licenses')
        df_prd.to_excel(writer, sheet_name='Production Licenses')
        exp_year.to_excel(writer, sheet_name='New Exp')
        prd_year.to_excel(writer, sheet_name='New Prd')


def ExtractExpTable(Exp_PageNo):
    Exp_url = "http://ky.mnr.gov.cn/dj/yqtkq/"
    df1 = ReadPage(Exp_url)
    for i in range(1, Exp_PageNo):
        df2 = ReadPage(Exp_url+'index_'+str(i)+'.htm')
        df1 = pd.concat([df1, df2])
    return df1


def ExtractPrdTable(Prd_PageNo):
    Prd_url = "http://ky.mnr.gov.cn/dj/yqckq/"
    df1 = ReadPage(Prd_url)
    for i in range(1, Prd_PageNo):
        df2 = ReadPage(Prd_url+'index_'+str(i)+'.htm')
        df1 = pd.concat([df1, df2])
    return df1


def ReadPage(url):

    # set the random time interval for data extract
    # rand = random.randint(4, 20)
    # ua = UserAgent()

    headers = {
        # "User-Agent": ua.random, "X-Requested-With": "XMLHttpRequest", "Referer":"http://ky.mnr.gov.cn/dj/yqtkq/index_1.htm"}
        # "User-Agent": ua.random, "Referer":"http://ky.mnr.gov.cn/dj/yqtkq/index_1.htm"}
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1", "Referer": "http://ky.mnr.gov.cn/dj/yqtkq/index_1.htm", "Cookie": "_Jo0OQK=3C01DE15F3212B3ACBD300D618C87D562D8258144E80E799FCFA26878EB1E19B720EF126526FB18527A491844DBD754CB50AF207CC9293F94B8646416F148903D42AEC72B56FA616F6836B5670FF571807A36B5670FF571807A2AC3ECBB3D71FAFA86B20968A7766A04GJ1Z1ZA=="}
    reg_url = url
    req = Request(url=reg_url, headers=headers)
    html = urlopen(req).read()
    d = pd.read_html(html)
    df = d[1]
    return df


def DataCleaning(df):
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


if __name__ == '__main__':
    main()
