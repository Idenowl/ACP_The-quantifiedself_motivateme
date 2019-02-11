import os
import sys, getopt
import requests
import  urllib.request #replace this line by urllib2 if you use python 2
import datetime
from datetime import date

def readAPIkey(key_path) :
    '''
    :param key_path: path of file contains the API key
    :return: string of API key
    '''
    file = open(key_path, 'r')
    if file.mode == 'r':
        return file.read()

def extract (date,API):
    '''
    Make the extraction of rescue time data, create csv and json file
    :param date: string year-month-day
    :param API : string of the API key
    :return: None
    '''

    print('Extraction data of :', str(date))

    path='data/rescuetime/'
    filename_csv= path+'csv/'+str(date)+'.csv'
    filename_json=path+'json/'+str(date)+'.json'
    option='overview'

    url='https://www.rescuetime.com/anapi/data?key='+API+'&perspective=rank&restrict_kind='+option+'&restrict_begin='+str(date)+'&restrict_end='+str(date)+'&format=csv'
    url2='https://www.rescuetime.com/anapi/data?key='+API+'&perspective=rank&restrict_kind='+option+'&restrict_begin='+str(date)+'&restrict_end='+str(date)+'&format=json'

    urllib.request.urlretrieve(url,filename_csv )
    r=requests.get(url)
    if r :
        print(filename_csv)

    urllib.request.urlretrieve(url2, filename_json)
    r2 = requests.get(url2)
    if r2 :
        print(filename_json)

if __name__ == '__main__':
    key_path = 'key/APIkey.txt'
    API = readAPIkey(key_path)

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hd:", "idate=")
    except getopt.GetoptError:
        print
        'test.py -d <year-month-day>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'test.py -d <year-month-day> '
            sys.exit()
        elif opt in ("-d", "--idate"):
            date = arg

    print('Extraction rescue_time : ', date)
    extract(date,API)
