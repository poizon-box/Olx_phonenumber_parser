from bs4 import BeautifulSoup
import requests
import json
from random import choice
import sys

link=sys.argv[1]

desktop_agents = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

curagent = choice(desktop_agents)

def olxGetPage(link):
    '''Simply choose random user-agent and request site'''

    s = requests.Session()
    s.headers.update({'User-Agent': curagent})
    init = s.get(link)

    if init.status_code == 301: return False

    soup = BeautifulSoup(init.text, 'html.parser')
    s.close()
    return soup, init.cookies

def olxGetPhoneToken(soup):
    phonetokenbs = soup.findAll(id='body-container')
    phonetoken = [x.text.split('\'') for x in phonetokenbs]
    try:
        token = phonetoken[0][1]
    except IndexError:
        print('Parsing failed.')
        token = '0'
    return token

def olxGetRawJson(link,cookies, token):
    idbs = link.split('-')[-1].split('.')[0]

    sesjatel = requests.Session()
    sesjatel.headers.update({'Referer': link, "User-Agent": curagent})
    numeryraw = sesjatel.get('https://www.olx.pl/ajax/misc/contact/phone/' + idbs[2:] + '/?pt=' + token,
                             cookies=cookies)
    sesjatel.close()

    return numeryraw

def parseJsonToNumber(numeryraw):
    try:
        numerydict = json.loads(numeryraw.content)


        if numerydict['value'].startswith('<span'):
            phonesoup = BeautifulSoup(numerydict['value'], 'html.parser')
            abc = phonesoup.findAll(class_='block')

            numery = [''.join(x.text.split(' ')) for x in abc]

            numery = '&'.join(numery)

        else:
            numery = numerydict['value']

    except:
        print('No numbers found!')
        numery = '0'
        exit(0)

    return numery


def olxGetDescription(soup):
    '''This script parses'''

    opisbs = soup.findAll(id='textContent')
    textopis = [x.text for x in opisbs]

    return textopis[-1] or 'Brak opisu'



if __name__=='__main__':
    soup, cookies = olxGetPage(link)
    token=olxGetPhoneToken(soup)
    description=olxGetDescription(soup)
    raw_numbers=olxGetRawJson(link,cookies,token)
    out_numbers=parseJsonToNumber(raw_numbers)
    print(out_numbers, description)