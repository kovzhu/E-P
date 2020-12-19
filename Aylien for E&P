import aylien_news_api
from aylien_news_api.rest import ApiException
from pprint import pprint as pp
import pandas as pd
import time
# import json

## Configure your connection to the API
configuration = aylien_news_api.Configuration()
configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'xxx'
configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'xxx'
configuration.host = "https://api.aylien.com/news"
api_instance = aylien_news_api.DefaultApi(aylien_news_api.ApiClient(configuration))

## List our parameters as search operators
opts_energy= {
    # 'title': '"energy transition" OR "climate change"',
    'title': '"energy transition',
    'body': '"oil company" OR "oil companies"',
    'language': ['en'],
    'published_at_start': 'NOW-30DAYS',
    'published_at_end': 'NOW',
    'per_page': 100,
    'sort_by': 'relevance'
}

opts_digital_twin= {
    # 'title': '"energy transition" OR "climate change"',
    'title': '"digital twin',
    'body': 'upstream E&P',
    'language': ['en'],
    'published_at_start': 'NOW-30DAYS',
    'published_at_end': 'NOW',
    'per_page': 100,
    'sort_by': 'relevance'
}

try:
    ## Make a call to the Stories endpoint for stories that meet the criteria of the search operators
    api_response = api_instance.list_stories(**opts_digital_twin)
    ## Print the returned story
    pp(api_response.stories)
except ApiException as e:
    print('Exception when calling DefaultApi->list_stories: %s\n' % e)
    

data = api_response.to_dict()

title = []
source = []
summary = []
homepage = []
links = []
PublishAt = []

for i in range(0,len(data['stories'])):
    title.append(data['stories'][i]['title'])
    source.append(data['stories'][i]['source']['name'])
    homepage.append(data['stories'][i]['source']['home_page_url'])
    summary.append(data['stories'][i]['summary']['sentences'])
    links.append(data['stories'][i]['links']['permalink'])
    PublishAt.append(data['stories'][i]['published_at'].strftime('%Y-%m-%d %H:%M:%S'))

summary = pd.DataFrame({'title':title, 'source':source, 'publish time':PublishAt, 'link':links,'summary':summary})


def WriteToExcel(name, dataframe):
    '''
    Parameters:
    name = name of the spreadsheet
    dataframe = dataframe to be written into the excel spreadsheet
    Write dataframes into excel
    '''
    filename = name+' '+ time.ctime().replace(':','_')
    # filename = name
    with pd.ExcelWriter(filename+'.xlsx') as writer:
        dataframe.to_excel(writer, sheet_name = name)

WriteToExcel('Aylien summary',summary)
