from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import time


def c(x): 
    if x:
        return x.text.replace('\r', '').replace('\t', '').replace('\n', ' ').strip()
    return ''

def parse_pages(pages):
    "Return parsed pages"
    results = []

    for page in range(pages):
        print(f'Getting page {page+1} from looperghana')
        results.append(requests.get(f"https://listings.loopghana.com/pageNumber_{page}").text)

    soups = []
    for r in results:
        soup = BeautifulSoup(r, 'lxml')
        soups.append(soup)
    
    return soups    


def extract_listings(soups):
    "Extract listings from list ofbeautiful soup objects"
    
    data = []

    for soup in soups:
        listings = soup.find_all('ul', {'class': 'listings-list'})[1].find_all('li')

        for prop in listings:
            d = {
                # 'id': prop.find('a').attrs['data-id'],
                # 'description':  
                # 'categorys':
                'beds': c(prop.find('span', {'class': 'bedrooms'})),
                'baths': c(prop.find('span', {'class': 'bathrooms'})),                
                'price': c(prop.find('span', {'class': 'price'})),
                'url': prop.find('a').attrs['href'],
                'area': c(prop.find('span', {'class': 'size'})), 
                'broker': c(prop.find('span', {'class': 'agt'})),
                'listing_title': c(prop.find('span', {'class': 'name'})),
                # 'amenities'
            }
            data.append(d)

    return data


def clean(df):
    df['currency'] = df.price.apply(lambda x: re.match(r'[A-Z\$]+', x.replace(',', '')).group())
    df['price'] = df.price.apply(lambda x: re.findall(r'[0-9]+', x.replace(',', ''))[0])
    df['area'] = df['area'].str.replace('m2', '')
    df['beds'] = df['beds'].str.replace('Bed', '')
    df['baths'] = df['baths'].str.replace('Bath', '')
    df['source'] = 'loopghana'
    
    return df

def write(df):
    "Write data out to csv"

    df.to_csv(f'looper_{pd.datetime.now()}.csv', index=False)
    print('Data written!')


def scrape_looper(pages=1, add_gps=False):
    soups = parse_pages(pages)
    data = extract_listings(soups)
    df = pd.DataFrame(data)
    df = clean(df)
    
    # if enrich:
    #     df = enrich(df)
    
    return df


if __name__ == '__main__':
    df = scrape_looper()
    write(df)


"""
def get_coords(url):
    
    try:
        results = requests.get(url)
        soup = BeautifulSoup(results.text, 'lxml')
        js = soup.find_all('script', {'type': "text/javascript"})[0]

        coords = re.findall(r"(ws_l[a-z]+ = '-?[0-9].[0-9]+')", js.text)

        if coords:
            coords = dict(map(lambda x: x.split(' = '), coords))
            lat = coords.get('ws_lat', None)
            lon = coords.get('ws_lon', None)

        return lat, lon
    except:
        return None, None


def enrich(df):
    df['lat'] = None
    df['lon'] = None
    df[['lat', 'lon']] = df.url.apply(lambda x: get_coords(x)).apply(pd.Series)

    df['lat'] = df['lat'].apply(lambda x: x[1:-1] if x else None).astype(float)
    df['lon'] = df['lon'].apply(lambda x: x[1:-1] if x else None).astype(float)
    
#     df = df[['id', 'location', 'currency', 'price', 'area', 'bedrooms', 'bathrooms', 'url', 'lat', 'lon']]
    
    return df
"""
