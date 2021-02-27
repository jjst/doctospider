# -*- coding: utf-8 -*-
import re

import requests

URL = "https://www.doctolib.fr/vaccination-covid-19/rosheim?ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005"

def fetch_appointments():
    response = requests.get(URL)
    print(response.text)


if __name__ == "__main__":
    fetch_appointments()
