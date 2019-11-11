#
import re
import datetime
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from extractors import (
    extract_currency,
    extract_price,
    extract_date,
    extract_period,
    extract_date,
    extract_vals,
    get_table_rows_todict,
)

from utils import save_data

base_url = "https://meqasa.com"
url = "https://meqasa.com/properties-for-rent-in-ghana"
result = requests.get(url)
src = result.content

soup = BeautifulSoup(src, "lxml")

containers = soup.findAll("div", {"class": "mqs-featured-prop-inner-wrap"})


#
def extract_from_house_link(house_url):
    result = requests.get(house_url)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    container = soup.find("section", {"class": "span8"})

    table_info = get_table_rows_todict(container)
    areas = extract_vals(table_info, "Area")
    garages = extract_vals(table_info, "Garage")
    address = extract_vals(table_info, "Address")

    descriptions = container.p.text.strip()

    date_ctr = soup.find("p", {"class": "listed-by-text"}).text.strip()
    posted_time = extract_date(date_ctr)

    return (areas, garages, address, descriptions, posted_time)


def house_info(houses_list):
    house_names = []
    house_beds = []
    house_showers = []
    house_garages = []
    house_areas = []
    house_descriptions = []
    house_prices = []
    house_currencys = []
    house_rent_periods = []
    house_urls = []
    house_address = []
    house_posted_times = []

    for idx, link in enumerate(houses_list):
        if idx == 20:
            break

        prop_features_li = link.find("ul", {"class": "prop-features"})
        lx1 = prop_features_li.find_all("li")

        page_link = base_url + link.find("a").attrs["href"]

        areas, garages, addresses, descriptions, posted_times = extract_from_house_link(
            page_link
        )

        beds = link.find("ul", {"class": "prop-features"}).li.text
        showers = lx1[1].text

        price_snip = link.find("p", {"class": "h3"}).text.strip()
        prices = extract_price(price_snip)
        currency = extract_currency(price_snip)
        periods = extract_period(price_snip)

        house_names.append(link.h2.a["href"].split("/")[1])
        house_beds.append(beds)
        house_showers.append(showers)

        house_garages.append(garages)
        house_areas.append(areas)
        house_descriptions.append(descriptions)
        house_prices.append(prices)
        house_currencys.append(currency)
        house_rent_periods.append(periods)

        house_urls.append(base_url + link.find("a").attrs["href"])
        house_address.append(addresses)
        house_posted_times.append(posted_times)

    df_houses = pd.DataFrame(
        {
            "Property": house_names,
            "Beds": house_beds,
            "Showers": house_showers,
            "Garages": house_garages,
            "Area": house_areas,
            "Description": house_descriptions,
            "Price": house_prices,
            "Currency": house_currencys,
            "Rent Period": house_rent_periods,
            "Url": house_urls,
            "Address": house_address,
            "Time Posted": house_posted_times,
        }
    )

    return df_houses


#
# df_house = house_info(containers)
# save_data(df_house)


if __name__ == "__main__":
    df_house = house_info(containers)
    save_data(df_house)
