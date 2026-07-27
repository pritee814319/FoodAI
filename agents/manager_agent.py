import requests
from bs4 import BeautifulSoup
import json


def recipe_parser_agent(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
