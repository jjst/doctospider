# -*- coding: utf-8 -*-
import re

import os
import requests
from bs4 import BeautifulSoup
import re
from twilio.rest import Client

DOCTOLIB_SEARCH_URL = "https://www.doctolib.fr/vaccination-covid-19/rosheim?ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005"


# Find these values at https://twilio.com/user/account
# To set up environmental variables, see http://twil.io/secure
try:
    twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
    twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_target_number = os.environ['TWILIO_TARGET_NUMBER']
    twilio_client = Client(account_sid, auth_token)
except KeyError:
    print("Environment variables for Twilio not found. I won't be able to send texts!")


def fetch_appointments():
    response = requests.get(DOCTOLIB_SEARCH_URL)
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
            message_body = "Bonjour, il y a un RDV disponible au centre de vaccination {place_name} sur doctolib.fr"
            twilio_client.api.account.messages.create(
                to=twilio_target_number,
                from_=twilio_from,
                body=message_body
            )



if __name__ == "__main__":
    fetch_appointments()
