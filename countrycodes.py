from bs4 import BeautifulSoup
import urllib.request
import webbrowser
from pprint import pprint


def get_name_and_codes():
    html = urllib.request.urlopen('http://www.nationsonline.org/oneworld/country_code_list.htm').read()
    soup = BeautifulSoup(html, 'html.parser')
    country_dict = dict()
    for country in soup.find_all('tr', class_='border1'):
        country_name = country.find_all('td')[1].get_text()
        country_abbr = country.find_all('td')[2].get_text()
        country_dict[country_name] = country_abbr
    return country_dict

def get_pogo_countries():
    with open('pogo_countries_2017-01.txt', 'r') as f:
        countries = f.read().split("\n")
    return countries

def get_pogo_abbr(country_dict, countries):
    abbr_list = list()
    for c in countries:
        abbr= country_dict.get(c, c)
        abbr_list.append(abbr)
    return abbr_list

def sanitize(abbr_list):
    clean_list = list()
    for abbr in abbr_list:
        if len(abbr) == 2:
            clean_list.append(abbr)
    return clean_list

def create_link(abbr_list):
    base_URL = 'https://www.amcharts.com/visited_countries/#'
    clean_list = sanitize(abbr_list)
    missing = [c for c in abbr_list if c not in clean_list]
    extension = ",".join(clean_list)
    URL = base_URL + extension
    print("The following countries could not be converted automatically")
    print("Please check up and add manually:")
    pprint(missing)
    return URL

def open_page(URL):
    webbrowser.open(URL, new=2)

if __name__ == "__main__":
    country_dict = get_name_and_codes()
    countries = get_pogo_countries()
    abbr_list = get_pogo_abbr(country_dict, countries)
    URL = create_link(abbr_list)
    open_page(URL)

# relevant links:
# https://www.cnet.com/how-to/pokemon-go-where-its-available-now-and-coming-soon/
# full list with current state of early 2017 (mentioned above)
# https://www.amcharts.com/visited_countries/#AL,AT,BE,BA,BG,HR,CY,CZ,DK,EE,FI,DE,GR,HU,IS,IE,LV,LT,LU,MK,MT,NL,NO,PL,RO,RS,SK,SI,SE,CH,BZ,CA,CR,SV,GL,GT,HN,MX,NI,PA,US,AR,BO,BR,CL,CO,EC,FK,GF,GY,PY,PE,SR,UY,VE,BJ,BW,BF,CV,TD,CI,EG,GA,GM,GH,GN,GW,KE,LR,MG,MW,MR,MU,MA,MZ,NA,NE,RW,ST,SC,SL,ZA,SZ,TZ,TG,UG,ZM,BH,BD,BT,BN,KH,HK,IN,ID,IL,JO,KZ,KW,KG,LA,LB,MO,MY,MN,NP,OM,PK,PH,QA,SG,KR,LK,TW,TJ,TH,TM,AE,UZ,VN,AU,FM,FJ,NZ,PW,PG,SB
# TODO: this list is not correct, need to obtain a complete list
