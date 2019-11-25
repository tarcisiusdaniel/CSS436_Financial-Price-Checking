import re
import codecs
import json
import requests

def update_table():
    homepage =  codecs.open("templates/index.html",'rb+',encoding='utf-8').read()
    pattern = re.compile(r'"symbol": "\w+:\w+"')
    test = re.sub(pattern,'"symbol": '+'"'+idx+":"+ticker+'"',homepage)#re.findall(pattern,homepage)
    f = codecs.open("templates/index.html",'w+',encoding='utf-8')
    print(test)
    f.write(test)

def get_index(ticker):
    #json.dumps(getQuotes('AAPL'), indent=2)
    info = requests.get('https://sandbox.iexapis.com/stable/stock/{}/company?token=Tpk_a71985faa6ab4c84b8e2cfdb7b021731'.format(ticker)).json()
    ex_name = info['exchange']
    print(ex_name)
    if(sorted(ex_name) == sorted("NASDAQ")):
        print("its nas")
    elif(sorted(ex_name) == sorted("New York Stock Exchange")):
        print("its nyse")    

def main():
    idx = "NASDAQ"
    ticker = "M"
    
    get_index(ticker)
    #print('running')
    #update_table()

if __name__ == "__main__":
    main()