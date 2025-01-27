import requests
import json

class URLExtractor:
    def __init__(self, base_url, query):
        self.base_url = base_url
        self.query = query
        self.urls = []

    def fetch_data(self):
        try:
            response = requests.get(self.base_url, params={"q": self.query, "format": "json"})
            response.raise_for_status()  # Raise an exception if the request fails
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
        return None

    def extract_urls(self):
        data = self.fetch_data()
        if data:
            try:
                for result in data["results"]:
                    url = result["url"]
                    self.urls.append(url)
            except KeyError as e:
                print(f"KeyError: {e}")

    def get_urls(self):
        return self.urls

# Example usage
base_url = "http://localhost:32768/search"
query = "Indian IT companies hiring scenario in 2025"

extractor = URLExtractor(base_url, query)
extractor.extract_urls()
urls = extractor.get_urls()
print("Extracted URLs:", urls)
print("No. of URLs:", len(urls))