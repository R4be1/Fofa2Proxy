import sys
import base64
import datetime
import requests
import concurrent.futures


yesterday = datetime.datetime.now()-datetime.timedelta(days=7)
yesterday = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"

email=''
api_key=''

def FofaAPICall(query, email, api_key):
    fields = 'host,ip,port,protocol,country_name,title,icp,country'
    qbase64 = base64.b64encode(query.encode()).decode()
    api = f'https://fofa.info/api/v1/search/all?email={email}&key={api_key}&qbase64={qbase64}&size=10000&fields={fields}'

    response = requests.get(api)
    if response.json().get('error'):
        print(response.json().get('errmsg'))
        return list()

    try:
        results = response.json().get("results",list())
        #print(results)
        print("\033[38;2;24;254;27m[ {} ]\033[0m Fofa API Search {} Results.".format(query, len(results)))

    except Exception as error :
        print(error)
        return list()

    hosts = list()
    file_name = "{}.csv".format(yesterday.replace(" ","_"))

    with open(file_name,"a") as results_file:
        results_file.write(fields+"\n")

        for result in results:
            hosts.append(
                    result[0].strip()
                    )
            results_file.write(
                    ",".join(result)+'\n'
                    )
    return hosts

def ProxyTest(socks5proxy):
    proxies = {
        'http': socks5proxy,
        'https': socks5proxy
    }
    try:
        response = requests.get(url='https://www.github.com', proxies=proxies, timeout=3)
        print(socks5proxy)
        return socks5proxy
    except:
        return None

results = FofaAPICall(
        query=f'protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && country!="CN" && after="{yesterday}"',
        email=email,
        api_key=api_key
        )
proxies = [ "socks5://"+host for host in results ]
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(ProxyTest, proxies)

with open('proxies.txt','a') as proxies_file:
    for result in results:
        if result:
            proxies_file.write(result+"\n")
