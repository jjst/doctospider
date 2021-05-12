# -*- coding: utf-8 -*-
import re

import os
import requests
from bs4 import BeautifulSoup
import re
from twilio.rest import Client
from itertools import count

DOCTOLIB_SEARCH_URL = os.environ['DOCTOLIB_SEARCH_URL']

try:
    DOCTOLIB_JSON_FETCH_URL_EXTRA_ARGS = os.environ['DOCTOLIB_JSON_FETCH_URL_EXTRA_ARGS']
except KeyError:
    DOCTOLIB_JSON_FETCH_URL_EXTRA_ARGS = "force_max_limit=2" # Chronodoses
try:
    SPECIALITY_ID = os.environ["DOCTOLIB_SPECIALITY_ID"] # personnes +75 ans
except KeyError:
    print("DOCTOLIB_SPECIALITY_ID not defined, defaulting to 'personnes de + de 75 ans'")
    SPECIALITY_ID = "5494" # personnes + 75 ans
    # SPECIALITY_ID = "5912" # medecins personnels de sante

# Find these values at https://twilio.com/user/account
# To set up environmental variables, see http://twil.io/secure
twilio_from = "+19196299849"
try:
    twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
    twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_target_number = os.environ['TWILIO_TARGET_NUMBER']
    twilio_client = Client(twilio_account_sid, twilio_auth_token)
except KeyError:
    print("Environment variables for Twilio not found. I won't be able to send texts!")

def fetch_appointments():
    for page in count(1):
        centers = find_vaccination_centers(page)
        if not centers:
            break
        for center in centers:
            find_availabilities(center)

def find_vaccination_centers(page=1):
    response = requests.get(DOCTOLIB_SEARCH_URL, params={"page": page})
    print(f"Using search url {response.url}")
    soup = BeautifulSoup(response.text)
    results = soup.select(".dl-search-result")
    print(f"Found {len(results)} centers")
    return results

def find_availabilities(result):
    css_id = result.attrs['id']
    center_id = re.search('search-result-(\d+)', css_id).group(1)
    response = requests.get(f"https://www.doctolib.fr/search_results/{center_id}.json?speciality_id={SPECIALITY_ID}&{DOCTOLIB_JSON_FETCH_URL_EXTRA_ARGS}")
    json = response.json()
    place_name = json['search_result']['name_with_title']
    availabilities = json['total']
    print(f"Found {availabilities} available spots for location: {place_name}")
    if availabilities or 'next_slot' in json:
        print(f"I found a spot at '{place_name}'! Sending notification...")
        message_body = f"Bonjour, il y a un RDV disponible au centre de vaccination: '{place_name}' sur doctolib.fr"
        twilio_client.api.account.messages.create(
            to=twilio_target_number,
            from_=twilio_from,
            body=message_body
        )
        print("Successfully sent notification.")
        print(json)


if __name__ == "__main__":
    fetch_appointments()
