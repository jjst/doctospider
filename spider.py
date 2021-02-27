# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.doctolib.fr/vaccination-covid-19/rosheim?ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005"


def fetch_appointments():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text)
    results = soup.select(".dl-search-result")
    for result in results:
        css_id = result.attrs['id']
        center_id = re.search('search-result-(\d+)', css_id).group(1)
        response = requests.get(f"https://www.doctolib.fr/search_results/{center_id}.json?speciality_id=5494")
        json = response.json()
        place_name = json['search_result']['name_with_title']
        availabilities = json['availabilities']
        avail_count = len(availabilities)
        print(f"Found {avail_count} available spots for location: {place_name}")
        if avail_count:
            print("I found a spot at {place_name}! Sending notification.")



if __name__ == "__main__":
    fetch_appointments()
