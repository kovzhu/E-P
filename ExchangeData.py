import time
import requests
import json
import pandas as pd
import sys

def gettime():
    return int(round(time.time()*1000))


def getResponse(url, headers, params):
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        reqIsJson = False

        if "application/json" in response.headers.get('content-type'):
            reqIsJson = True

        if response.status_code == 200 and reqIsJson == True:
            return response

        if response.status_code == 200 and reqIsJson == False:
            print("Unsupported content type received : ", response.headers.get('content-type'))
            return response

        print('Status Code: ' + str(response.status_code))

        if response.status_code == 400:
            print("The server could not understand your request, check the syntax for your query.")
            print('Error Message: ' + str(response.json()))
        elif response.status_code == 401:
            print("Login failed, please check your user name and password.")
        elif response.status_code == 403:
            print("You are not entitled to this data.")
        elif response.status_code == 404:
            print("The URL you requested could not be found or you have an invalid view name.")
        elif response.status_code == 500:
            print("The server encountered an unexpected condition which prevented it from fulfilling the request.")
            print("Error Message: " + str(response.json()))
            print("If this persists, please contact customer care.")
        else:
            print("Error Message: " + str(response.json()))
    except:
        sys.exit()


def get_data(pages):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Referer': r'https://www.shpgx.com/html/gdtrqsj.html',
        'Connection': r'keep-alive',
        'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8'}
    s = requests.session()
    table = pd.DataFrame()
    for i in range(pages):
        params =    {
            'wareid': 6,
            'cd':None,
            'starttime':None,
            'endtime':None,
            'start': 0 + 25*i,
            'length': 25,
            'ts': str(gettime()) }

        payload =    {
            'wareid': 6,
            'cd':None,
            'starttime':None,
            'endtime':None,
            'start': 0,
            'length': 25,
            'ts': str(gettime()) }

        # url = r'https://www.shpgx.com/html/gdtrqsj.html'
        url = r'https://www.shpgx.com/marketstock/dataList'
        response = s.get(url,headers=headers, params = params).text.encode('utf-8')
        # data = getResponse(url,headers, params).text.encode('utf8')
        data = pd.DataFrame(json.loads(response)['root'])
        rows = len(data.index)
        for i in range(rows):
            df = pd.DataFrame.from_dict(
                {'挂牌价': data.iloc[i]['basename'],
                '成交价（元/立方米）' : data.iloc[i]['contprice'],
                '挂牌量（立方米）' : data.iloc[i]['basenum'],
                '成交量（立方米)' : data.iloc[i]['dealnum'],
                '交收截至日' : data.iloc[i]['enddate'],
                '交收地' : data.iloc[i]['jsd'],
                '挂牌日期' : data.iloc[i]['orderdate']}, orient = 'index')
            table = pd.merge(table, df, how='outer', left_index=True, right_index=True)
    return table.T
