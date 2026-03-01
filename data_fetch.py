# data_fetch.py

import requests
import base64
from config import EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_BASE_URL


class EbayDataFetcher:
    def __init__(self):
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """
        Retrieves OAuth token from eBay.
        """
        from config import EBAY_IDENTITY_URL
        url = EBAY_IDENTITY_URL

        credentials = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}",
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        return response.json()["access_token"]

    def _make_request(self, endpoint, params=None):
        """
        General request handler.
        """
        url = f"{EBAY_BASE_URL}{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()

    def search_active_listings(
        self,
        keyword,
        brand=None,
        waist=None,
        inseam=None,
        condition=None,
        limit=50
    ):
        """
        Fetch active listings with optional filters.
        """

        endpoint = "/buy/browse/v1/item_summary/search"

        filters = []

        if brand:
            filters.append(f"brand:{brand}")

        if waist:
            filters.append(f"aspect_filter=Waist:{waist}")

        if inseam:
            filters.append(f"aspect_filter=Inseam:{inseam}")

        if condition:
            filters.append(f"conditionIds:{condition}")

        params = {
            "q": keyword,
            "limit": limit,
        }

        if filters:
            params["filter"] = ",".join(filters)

        data = self._make_request(endpoint, params=params)

        return self._extract_price_data(data)

    def _extract_price_data(self, raw_data):
        """
        Extracts structured price + metadata from raw response.
        """

        items = raw_data.get("itemSummaries", [])
        results = []

        for item in items:
            price_info = item.get("price", {})
            results.append({
                "title": item.get("title"),
                "price": float(price_info.get("value", 0)),
                "currency": price_info.get("currency"),
                "condition": item.get("condition"),
                "item_id": item.get("itemId"),
                "url": item.get("itemWebUrl"),
            })

        return results