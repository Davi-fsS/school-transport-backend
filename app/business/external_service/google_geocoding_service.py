from dotenv import load_dotenv
import os
import requests

class GoogleGeocodingService():
    secret_key: str

    def __init__(self):
        load_dotenv()
        self.secret_key = os.getenv("GOOGLE_SECRET_KEY")

    def get_geocode_by_address(self, address: str):
        params = {
            'key': self.secret_key,
            'address': address.replace(' ', '+')
        }

        base_url = "https://maps.googleapis.com/maps/api/geocode/json?"

        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            result = data['results'][0]
            location = result['geometry']['location']
            return location
        else:
            return
